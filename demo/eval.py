#!/usr/bin/env python
"""
Scored evaluation harness for the api RAG pipeline.

Two subcommands:

  verify   Offline consistency check. Confirms every `expect_sources` document
           exists in the corpus and every `must_include` token really appears in
           it. No network, no API cost. Run this after any corpus change so the
           eval set cannot silently drift from the documents. 

  run      Scores the live system over the eval set.

             --mode retrieval   POST /api/v1/search only. No LLM cost.
                                Produces the per-index ablation table
                                (vector / fulltext / summary / graph).
             --mode answer      POST /api/v1/qa. Scores answer correctness with
                                a keyword check plus an LLM judge.
             --mode both        Default. Runs both against the same questions.

Examples:
    python eval.py verify
    python eval.py run --mode retrieval --workspace meridian_demo
    python eval.py run --workspace meridian_demo --tag demo-run-1
    python eval.py run --mode answer --limit 10 --concurrency 2

Reports are written to ./reports/<tag>.json and ./reports/<tag>.md
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import statistics
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import httpx
except ImportError:  # pragma: no cover
    print("httpx is required:  pip install httpx", file=sys.stderr)
    raise SystemExit(3)

try:
    import yaml
except ImportError:  # pragma: no cover
    print("PyYAML is required:  pip install pyyaml", file=sys.stderr)
    raise SystemExit(3)

try:
    from rich.console import Console
    from rich.table import Table

    _console: Any = Console()
except ImportError:  # pragma: no cover
    _console = None
    Table = None  # type: ignore[assignment]

HERE = Path(__file__).resolve().parent

# Metadata keys that may carry a document reference. Retrieval matching looks at
# these only - never at chunk body text - because the corpus contains
# cross-references between documents and body-text matching would inflate the
# hit rate.
META_REF_KEYS = (
    "source",
    "document_name",
    "name",
    "reference",
    "filename",
    "file_name",
    "title",
    "doc_id",
    "document_id",
)

REFUSAL_MARKERS = (
    "i do not know based on the indexed data",
    "i don't know based on the indexed data",
    "je ne sais pas",
    "ne contient pas",
    "ne contiennent pas",
    "n'est pas présent",
    "n'est pas mentionn",
    "pas d'information",
    "aucune information",
    "not in the context",
    "not available in the indexed",
    "no information",
)

JUDGE_SYSTEM = (
    "You grade answers produced by a document question-answering system. "
    "You are strict, terse, and you never reward fluent text that misses the "
    "requested fact. Reply with JSON only."
)

JUDGE_TEMPLATE = """\
Question:
{question}

Reference answer (ground truth):
{expected}

System answer:
{actual}

Grade the system answer against the reference answer.

verdict must be one of:
  "correct"   - states the key fact(s) of the reference answer, no contradiction
  "partial"   - directionally right but incomplete, vague, or missing a required figure
  "incorrect" - wrong, contradicts the reference, or fails to answer

Extra numbers or context beyond the reference are fine as long as nothing
contradicts it. Language may differ from the reference; judge the meaning.

Return JSON: {{"verdict": "...", "reason": "<max 20 words>"}}
"""

JUDGE_REFUSAL_TEMPLATE = """\
Question:
{question}

The indexed documents contain NO information that answers this question.
A good system declines, says it does not know, or says the information is not
in the indexed documents.

System answer:
{actual}

verdict must be one of:
  "correct"   - declines or states the information is not available
  "partial"   - hedges but still asserts a substantive answer
  "incorrect" - confidently answers anyway (a hallucination)

Return JSON: {{"verdict": "...", "reason": "<max 20 words>"}}
"""


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def norm(text: Any) -> str:
    """Lowercase, strip accents, drop everything that is not alphanumeric."""
    if not text:
        return ""
    decomposed = unicodedata.normalize("NFKD", str(text))
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "", stripped.lower())


def load_env(explicit: str | None) -> None:
    """Populate os.environ from a .env file without requiring python-dotenv."""
    candidates = (
        [Path(explicit)]
        if explicit
        else [HERE / ".env", HERE / ".env.demo", HERE.parent / "api" / ".env"]
    )
    for path in candidates:
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
        return


def echo(message: str = "") -> None:
    if _console is not None:
        _console.print(message)
    else:
        print(re.sub(r"\[/?[a-z0-9 #]+\]", "", message))


# --------------------------------------------------------------------------
# eval set
# --------------------------------------------------------------------------


@dataclass
class Question:
    id: str
    category: str
    lang: str
    question: str
    expect_sources: list[str] = field(default_factory=list)
    must_include: list[str] = field(default_factory=list)
    expect_answer: str = ""
    expect_refusal: bool = False

    @property
    def answerable(self) -> bool:
        return not self.expect_refusal


def load_eval_set(path: Path) -> tuple[dict[str, Any], list[Question]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    meta = data.get("meta") or {}
    questions = []
    for raw in data.get("questions") or []:
        questions.append(
            Question(
                id=str(raw["id"]),
                category=raw.get("category", "uncategorised"),
                lang=raw.get("lang", "fr"),
                question=str(raw["question"]).strip(),
                expect_sources=[str(s) for s in raw.get("expect_sources") or []],
                must_include=[str(s) for s in raw.get("must_include") or []],
                expect_answer=str(raw.get("expect_answer") or "").strip(),
                expect_refusal=bool(raw.get("expect_refusal", False)),
            )
        )
    return meta, questions


# --------------------------------------------------------------------------
# verify
# --------------------------------------------------------------------------


def cmd_verify(args: argparse.Namespace) -> int:
    set_path = Path(args.set)
    if not set_path.is_absolute():
        set_path = HERE / set_path
    meta, questions = load_eval_set(set_path)

    corpus_dir = Path(args.corpus or meta.get("corpus") or "corpus/md")
    if not corpus_dir.is_absolute():
        corpus_dir = HERE / corpus_dir

    problems: list[str] = []

    if not corpus_dir.is_dir():
        echo(f"[red]Corpus directory not found: {corpus_dir}[/red]")
        echo("Run:  python build_corpus.py")
        return 2

    corpus: dict[str, str] = {}
    for md in sorted(corpus_dir.glob("*.md")):
        corpus[md.stem] = norm(md.read_text(encoding="utf-8"))

    if not corpus:
        echo(f"[red]No .md files in {corpus_dir}[/red]")
        return 2

    seen_ids: set[str] = set()
    referenced: set[str] = set()

    for q in questions:
        if q.id in seen_ids:
            problems.append(f"{q.id}: duplicate question id")
        seen_ids.add(q.id)

        if q.expect_refusal:
            if q.expect_sources:
                problems.append(f"{q.id}: expect_refusal is set but expect_sources is not empty")
            if q.must_include:
                problems.append(f"{q.id}: expect_refusal is set but must_include is not empty")
            continue

        if not q.expect_sources:
            problems.append(f"{q.id}: answerable question with no expect_sources")
            continue

        missing = [ref for ref in q.expect_sources if ref not in corpus]
        for ref in missing:
            problems.append(f"{q.id}: expect_sources '{ref}' is not in the corpus")
        referenced.update(q.expect_sources)

        haystack = "".join(corpus[ref] for ref in q.expect_sources if ref in corpus)
        for token in q.must_include:
            if norm(token) not in haystack:
                problems.append(
                    f"{q.id}: must_include '{token}' does not appear in "
                    f"{', '.join(q.expect_sources)}"
                )

    orphans = sorted(set(corpus) - referenced)

    echo()
    echo(f"[bold]Eval set:[/bold] {set_path.name}  ({len(questions)} questions)")
    echo(f"[bold]Corpus:[/bold]   {corpus_dir}  ({len(corpus)} documents)")
    answerable = sum(1 for q in questions if q.answerable)
    echo(f"           {answerable} answerable / {len(questions) - answerable} unanswerable")

    if orphans:
        echo(f"[yellow]Documents never referenced by any question: {', '.join(orphans)}[/yellow]")

    if problems:
        echo()
        echo(f"[red]{len(problems)} problem(s):[/red]")
        for p in problems:
            echo(f"  [red]x[/red] {p}")
        return 1

    echo()
    echo("[green]OK[/green] - every expected source exists and every must_include token "
         "is present in its source document.")
    return 0


# --------------------------------------------------------------------------
# scoring
# --------------------------------------------------------------------------


def meta_refs(metadata: dict[str, Any] | None) -> str:
    if not metadata:
        return ""
    return norm(" ".join(str(metadata.get(k) or "") for k in META_REF_KEYS))


def docs_contain(docs: list[dict[str, Any]] | None, ref_n: str) -> bool:
    for doc in docs or []:
        if ref_n and ref_n in meta_refs(doc.get("metadata")):
            return True
    return False


def hits_contain(hits: list[dict[str, Any]] | None, ref_n: str) -> bool:
    for hit in hits or []:
        haystack = norm(" ".join(str(hit.get(k) or "") for k in META_REF_KEYS))
        if ref_n and ref_n in haystack:
            return True
    return False


def score_retrieval(payload: dict[str, Any], expected: list[str]) -> dict[str, Any]:
    """Per-index retrieval scoring for one question.

    A document counts as retrieved by an index when its reference appears in the
    metadata of that index's results. The graph column is approximate: LightRAG
    returns a flat context string, so a reference found there may come from a
    cross-reference inside another document rather than from the document
    itself. It is reported separately and never silently merged.
    """
    graph_context = norm(payload.get("graph_context") or "")
    per_index: dict[str, list[bool]] = {"vector": [], "summary": [], "fulltext": [], "graph": []}

    for ref in expected:
        ref_n = norm(ref)
        per_index["vector"].append(docs_contain(payload.get("vector_results"), ref_n))
        per_index["summary"].append(docs_contain(payload.get("summary_results"), ref_n))
        per_index["fulltext"].append(hits_contain(payload.get("fulltext_results"), ref_n))
        per_index["graph"].append(bool(ref_n) and ref_n in graph_context)

    def summarise(flags: list[bool]) -> dict[str, bool]:
        return {"all": bool(flags) and all(flags), "any": any(flags)}

    indexes = {name: summarise(flags) for name, flags in per_index.items()}

    # Cumulative ablation: what each index adds on top of the previous ones.
    order = ["vector", "fulltext", "summary", "graph"]
    cumulative: dict[str, dict[str, bool]] = {}
    running = [False] * len(expected)
    label = ""
    for name in order:
        running = [a or b for a, b in zip(running, per_index[name])]
        label = name if not label else f"{label}+{name}"
        cumulative[label] = summarise(running)

    return {
        "indexes": indexes,
        "cumulative": cumulative,
        "union": summarise(running),
        "counts": {
            "vector": len(payload.get("vector_results") or []),
            "summary": len(payload.get("summary_results") or []),
            "fulltext": len(payload.get("fulltext_results") or []),
            "graph_chars": len(payload.get("graph_context") or ""),
        },
    }


def score_sources(sources: list[dict[str, Any]], expected: list[str]) -> dict[str, Any]:
    found = []
    for ref in expected:
        ref_n = norm(ref)
        hit = any(ref_n in norm(s.get("filename") or "") for s in sources)
        found.append(hit)
    return {
        "all": bool(found) and all(found),
        "any": any(found),
        "missing": [ref for ref, hit in zip(expected, found) if not hit],
    }


def score_keywords(answer: str, tokens: list[str]) -> dict[str, Any]:
    if not tokens:
        return {"ratio": None, "missing": []}
    answer_n = norm(answer)
    missing = [t for t in tokens if norm(t) not in answer_n]
    return {"ratio": (len(tokens) - len(missing)) / len(tokens), "missing": missing}


def looks_like_refusal(answer: str) -> bool:
    lowered = answer.lower()
    return any(marker in lowered for marker in REFUSAL_MARKERS)


# --------------------------------------------------------------------------
# API calls
# --------------------------------------------------------------------------


async def post_json(
    client: httpx.AsyncClient, url: str, payload: dict[str, Any], retries: int
) -> dict[str, Any]:
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            response = await client.post(url, json=payload)
            if response.status_code >= 500:
                raise httpx.HTTPStatusError(
                    f"{response.status_code}", request=response.request, response=response
                )
            response.raise_for_status()
            return response.json()
        except Exception as exc:  # noqa: BLE001 - retried and surfaced below
            last = exc
            if attempt < retries:
                await asyncio.sleep(1.5 * (attempt + 1))
    raise RuntimeError(str(last))


async def judge_answer(
    client: httpx.AsyncClient, q: Question, answer: str, model: str, retries: int
) -> dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"verdict": "skipped", "reason": "OPENAI_API_KEY not set"}

    base = (os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    template = JUDGE_REFUSAL_TEMPLATE if q.expect_refusal else JUDGE_TEMPLATE
    prompt = template.format(
        question=q.question, expected=q.expect_answer, actual=answer or "(empty)"
    )

    payload = {
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": prompt},
        ],
    }

    try:
        data = await post_json(client, f"{base}/chat/completions", payload, retries)
    except Exception as exc:  # noqa: BLE001
        return {"verdict": "error", "reason": str(exc)[:120]}

    try:
        content = data["choices"][0]["message"]["content"]
        parsed = json.loads(content)
        verdict = str(parsed.get("verdict", "")).lower().strip()
        if verdict not in {"correct", "partial", "incorrect"}:
            return {"verdict": "error", "reason": f"bad verdict: {verdict[:40]}"}
        return {"verdict": verdict, "reason": str(parsed.get("reason", ""))[:160]}
    except Exception as exc:  # noqa: BLE001
        return {"verdict": "error", "reason": f"unparseable judge reply: {exc}"[:120]}


async def evaluate_one(
    q: Question,
    args: argparse.Namespace,
    api_client: httpx.AsyncClient,
    judge_client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": q.id,
        "category": q.category,
        "lang": q.lang,
        "question": q.question,
        "expect_sources": q.expect_sources,
        "expect_refusal": q.expect_refusal,
    }

    async with semaphore:
        if args.mode in ("retrieval", "both"):
            started = asyncio.get_event_loop().time()
            try:
                payload = await post_json(
                    api_client,
                    "/api/v1/search",
                    {
                        "query": q.question,
                        "workspace": args.workspace,
                        "topk": args.topk,
                        "graph_topk": args.graph_topk,
                        "similarity_threshold": args.similarity_threshold,
                        "summary_threshold": args.summary_threshold,
                    },
                    args.retries,
                )
                result["retrieval"] = score_retrieval(payload, q.expect_sources)
                result["retrieval"]["latency_s"] = round(
                    asyncio.get_event_loop().time() - started, 3
                )
            except Exception as exc:  # noqa: BLE001
                result["retrieval"] = {"error": str(exc)[:200]}

        if args.mode in ("answer", "both"):
            started = asyncio.get_event_loop().time()
            try:
                body: dict[str, Any] = {
                    "question": q.question,
                    "workspace": args.workspace,
                    "topk": args.topk,
                    "graph_topk": args.graph_topk,
                    "similarity_threshold": args.similarity_threshold,
                    "summary_threshold": args.summary_threshold,
                    "show_sources": True,
                }
                if args.model:
                    body["model"] = args.model
                payload = await post_json(api_client, "/api/v1/qa", body, args.retries)
                answer = payload.get("answer") or ""
                latency = round(asyncio.get_event_loop().time() - started, 3)

                judged = await judge_answer(judge_client, q, answer, args.judge_model, args.retries)
                result["answer"] = {
                    "text": answer,
                    "latency_s": latency,
                    "sources": [s.get("filename") for s in payload.get("sources") or []],
                    "source_hit": score_sources(payload.get("sources") or [], q.expect_sources),
                    "keywords": score_keywords(answer, q.must_include),
                    "refusal_detected": looks_like_refusal(answer),
                    "judge": judged,
                    "stats": payload.get("stats") or {},
                }
            except Exception as exc:  # noqa: BLE001
                result["answer"] = {"error": str(exc)[:200]}

    return result


# --------------------------------------------------------------------------
# aggregation + reporting
# --------------------------------------------------------------------------


def pct(numerator: int, denominator: int) -> float:
    return round(100.0 * numerator / denominator, 1) if denominator else 0.0


def aggregate(results: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    answerable = [r for r in results if not r["expect_refusal"]]
    unanswerable = [r for r in results if r["expect_refusal"]]
    summary: dict[str, Any] = {
        "questions": len(results),
        "answerable": len(answerable),
        "unanswerable": len(unanswerable),
    }

    if mode in ("retrieval", "both"):
        scored = [r for r in answerable if "retrieval" in r and "error" not in r["retrieval"]]
        errors = [r for r in answerable if "retrieval" in r and "error" in r["retrieval"]]
        per_index: dict[str, int] = {}
        cumulative: dict[str, int] = {}
        for r in scored:
            for name, flags in r["retrieval"]["indexes"].items():
                per_index[name] = per_index.get(name, 0) + int(flags["all"])
            for name, flags in r["retrieval"]["cumulative"].items():
                cumulative[name] = cumulative.get(name, 0) + int(flags["all"])
        latencies = [
            r["retrieval"]["latency_s"] for r in scored if "latency_s" in r["retrieval"]
        ]
        summary["retrieval"] = {
            "scored": len(scored),
            "errors": len(errors),
            "per_index_pct": {k: pct(v, len(scored)) for k, v in per_index.items()},
            "cumulative_pct": {k: pct(v, len(scored)) for k, v in cumulative.items()},
            "union_pct": pct(
                sum(int(r["retrieval"]["union"]["all"]) for r in scored), len(scored)
            ),
            "latency_p50_s": round(statistics.median(latencies), 2) if latencies else None,
        }

    if mode in ("answer", "both"):
        scored = [r for r in results if "answer" in r and "error" not in r["answer"]]
        errors = [r for r in results if "answer" in r and "error" in r["answer"]]
        verdicts = {"correct": 0, "partial": 0, "incorrect": 0, "error": 0, "skipped": 0}
        for r in scored:
            verdicts[r["answer"]["judge"]["verdict"]] = (
                verdicts.get(r["answer"]["judge"]["verdict"], 0) + 1
            )
        graded = verdicts["correct"] + verdicts["partial"] + verdicts["incorrect"]

        ans_scored = [r for r in scored if not r["expect_refusal"]]
        unans_scored = [r for r in scored if r["expect_refusal"]]

        keyword_ratios = [
            r["answer"]["keywords"]["ratio"]
            for r in ans_scored
            if r["answer"]["keywords"]["ratio"] is not None
        ]
        latencies = [r["answer"]["latency_s"] for r in scored]
        latencies.sort()

        summary["answer"] = {
            "scored": len(scored),
            "errors": len(errors),
            "verdicts": verdicts,
            "strict_accuracy_pct": pct(verdicts["correct"], graded),
            "lenient_accuracy_pct": pct(verdicts["correct"] + verdicts["partial"], graded),
            "source_hit_pct": pct(
                sum(int(r["answer"]["source_hit"]["all"]) for r in ans_scored), len(ans_scored)
            ),
            "keyword_pct": round(100 * statistics.mean(keyword_ratios), 1)
            if keyword_ratios
            else None,
            "refusal_accuracy_pct": pct(
                sum(1 for r in unans_scored if r["answer"]["judge"]["verdict"] == "correct"),
                len(unans_scored),
            ),
            "hallucination_pct": pct(
                sum(1 for r in unans_scored if r["answer"]["judge"]["verdict"] == "incorrect"),
                len(unans_scored),
            ),
            "latency_p50_s": round(statistics.median(latencies), 2) if latencies else None,
            "latency_p95_s": round(latencies[int(len(latencies) * 0.95) - 1], 2)
            if len(latencies) >= 2
            else None,
        }

        by_category: dict[str, dict[str, int]] = {}
        for r in scored:
            bucket = by_category.setdefault(r["category"], {"n": 0, "correct": 0})
            bucket["n"] += 1
            bucket["correct"] += int(r["answer"]["judge"]["verdict"] == "correct")
        summary["answer"]["by_category"] = {
            k: {"n": v["n"], "correct": v["correct"], "pct": pct(v["correct"], v["n"])}
            for k, v in sorted(by_category.items())
        }

    return summary


def render_console(summary: dict[str, Any], results: list[dict[str, Any]], mode: str) -> None:
    echo()
    if mode in ("retrieval", "both") and "retrieval" in summary:
        r = summary["retrieval"]
        echo("[bold]Retrieval - all expected sources found (answerable questions)[/bold]")
        rows = [
            ("vector only", r["cumulative_pct"].get("vector")),
            ("+ fulltext", r["cumulative_pct"].get("vector+fulltext")),
            ("+ summary", r["cumulative_pct"].get("vector+fulltext+summary")),
            ("+ graph (approx)", r["cumulative_pct"].get("vector+fulltext+summary+graph")),
        ]
        if _console is not None and Table is not None:
            table = Table(show_header=True, header_style="bold")
            table.add_column("Indexes enabled")
            table.add_column("Hit rate", justify="right")
            table.add_column("Standalone", justify="right")
            standalone = ["vector", "fulltext", "summary", "graph"]
            for (label, value), name in zip(rows, standalone):
                table.add_row(
                    label,
                    f"{value}%" if value is not None else "-",
                    f"{r['per_index_pct'].get(name, 0)}%",
                )
            _console.print(table)
        else:
            for label, value in rows:
                print(f"  {label:<22} {value}%")
        p50 = f"{r['latency_p50_s']}s" if r["latency_p50_s"] is not None else "-"
        echo(f"  scored: {r['scored']}  errors: {r['errors']}  p50 latency: {p50}")
        if r["errors"]:
            echo(f"  [yellow]{r['errors']} question(s) failed to reach the API[/yellow]")
        echo()

    if mode in ("answer", "both") and "answer" in summary:
        a = summary["answer"]
        echo("[bold]Answer quality[/bold]")
        echo(f"  strict accuracy   {a['strict_accuracy_pct']}%   (judge verdict = correct)")
        echo(f"  lenient accuracy  {a['lenient_accuracy_pct']}%   (correct + partial)")
        echo(f"  source hit rate   {a['source_hit_pct']}%   (all expected docs cited)")
        if a["keyword_pct"] is not None:
            echo(f"  keyword coverage  {a['keyword_pct']}%")
        echo(f"  refusal accuracy  {a['refusal_accuracy_pct']}%   (on {summary['unanswerable']} unanswerable)")
        echo(f"  hallucination     {a['hallucination_pct']}%   (answered anyway)")
        p50 = f"{a['latency_p50_s']}s" if a["latency_p50_s"] is not None else "-"
        p95 = f"{a['latency_p95_s']}s" if a["latency_p95_s"] is not None else "-"
        echo(f"  latency           p50 {p50} / p95 {p95}")
        echo(f"  verdicts          {a['verdicts']}")
        if a["errors"]:
            echo(f"  [yellow]errors            {a['errors']}[/yellow]")
        echo()

        if _console is not None and Table is not None:
            table = Table(show_header=True, header_style="bold", title="By category")
            table.add_column("Category")
            table.add_column("n", justify="right")
            table.add_column("Correct", justify="right")
            table.add_column("%", justify="right")
            for name, v in a["by_category"].items():
                table.add_row(name, str(v["n"]), str(v["correct"]), f"{v['pct']}%")
            _console.print(table)
        else:
            for name, v in a["by_category"].items():
                print(f"  {name:<18} {v['correct']}/{v['n']}  {v['pct']}%")

        failures = [
            r
            for r in results
            if "answer" in r
            and "error" not in r["answer"]
            and r["answer"]["judge"]["verdict"] in ("partial", "incorrect")
        ]
        if failures:
            echo()
            echo(f"[bold]Failures ({len(failures)})[/bold]")
            for r in failures:
                verdict = r["answer"]["judge"]["verdict"]
                colour = "red" if verdict == "incorrect" else "yellow"
                echo(f"  [{colour}]{verdict:<9}[/{colour}] {r['id']}  {r['question'][:70]}")
                echo(f"             reason: {r['answer']['judge']['reason']}")
                if r["answer"]["source_hit"].get("missing"):
                    echo(f"             not retrieved: {', '.join(r['answer']['source_hit']['missing'])}")


def render_markdown(
    summary: dict[str, Any], results: list[dict[str, Any]], args: argparse.Namespace
) -> str:
    lines = [
        f"# RAG evaluation - {args.tag}",
        "",
        f"- run at: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"- api: `{args.api}`",
        f"- workspace: `{args.workspace}`",
        f"- eval set: `{Path(args.set).name}` ({summary['questions']} questions, "
        f"{summary['unanswerable']} unanswerable)",
        f"- topk: {args.topk}, graph_topk: {args.graph_topk}, "
        f"similarity_threshold: {args.similarity_threshold}",
        f"- judge: `{args.judge_model}`",
        "",
    ]

    if "retrieval" in summary:
        r = summary["retrieval"]
        lines += [
            "## Retrieval ablation",
            "",
            "Share of answerable questions where **every** expected source document was "
            "retrieved. Matching is on result metadata only, never on chunk body text.",
            "",
            "| Indexes enabled | Hit rate | Index alone |",
            "|---|---|---|",
        ]
        pairs = [
            ("vector only", "vector", "vector"),
            ("+ fulltext", "vector+fulltext", "fulltext"),
            ("+ summary", "vector+fulltext+summary", "summary"),
            ("+ graph (approx)", "vector+fulltext+summary+graph", "graph"),
        ]
        for label, cum_key, solo_key in pairs:
            lines.append(
                f"| {label} | {r['cumulative_pct'].get(cum_key, '-')}% | "
                f"{r['per_index_pct'].get(solo_key, '-')}% |"
            )
        lines += [
            "",
            "> The graph column is approximate: LightRAG returns a flat context string, so a "
            "reference found there may originate from a cross-reference inside another "
            "document rather than from the document itself.",
            "",
        ]

    if "answer" in summary:
        a = summary["answer"]
        lines += [
            "## Answer quality",
            "",
            "| Metric | Value |",
            "|---|---|",
            f"| Strict accuracy (judge = correct) | **{a['strict_accuracy_pct']}%** |",
            f"| Lenient accuracy (correct + partial) | {a['lenient_accuracy_pct']}% |",
            f"| Source hit rate (all expected docs cited) | {a['source_hit_pct']}% |",
            f"| Keyword coverage | {a['keyword_pct'] if a['keyword_pct'] is not None else '-'}% |",
            f"| Refusal accuracy on unanswerable | {a['refusal_accuracy_pct']}% |",
            f"| Hallucination rate on unanswerable | {a['hallucination_pct']}% |",
            f"| Latency p50 / p95 | {a['latency_p50_s']}s / {a['latency_p95_s']}s |",
            "",
            "### By category",
            "",
            "| Category | n | Correct | % |",
            "|---|---|---|---|",
        ]
        for name, v in a["by_category"].items():
            lines.append(f"| {name} | {v['n']} | {v['correct']} | {v['pct']}% |")
        lines.append("")

        failures = [
            r
            for r in results
            if "answer" in r
            and "error" not in r["answer"]
            and r["answer"]["judge"]["verdict"] in ("partial", "incorrect")
        ]
        lines += [f"### Failures ({len(failures)})", ""]
        if not failures:
            lines.append("None.")
        for r in failures:
            lines += [
                f"**{r['id']} - {r['answer']['judge']['verdict']}** - {r['question']}",
                "",
                f"- judge: {r['answer']['judge']['reason']}",
                f"- expected sources: {', '.join(r['expect_sources']) or '(none)'}",
                f"- not retrieved: {', '.join(r['answer']['source_hit'].get('missing') or []) or '-'}",
                f"- answer: {r['answer']['text'][:400].strip()}",
                "",
            ]
        lines.append("")

    return "\n".join(lines)


# --------------------------------------------------------------------------
# run
# --------------------------------------------------------------------------


async def run_async(args: argparse.Namespace) -> int:
    set_path = Path(args.set)
    if not set_path.is_absolute():
        set_path = HERE / set_path
    _meta, questions = load_eval_set(set_path)

    if args.category:
        wanted = {c.strip() for c in args.category.split(",")}
        questions = [q for q in questions if q.category in wanted]
    if args.limit:
        questions = questions[: args.limit]

    if not questions:
        echo("[red]No questions selected.[/red]")
        return 2

    if args.mode in ("answer", "both") and not os.getenv("OPENAI_API_KEY"):
        echo("[yellow]OPENAI_API_KEY is not set - the LLM judge will be skipped.[/yellow]")

    echo(
        f"Running [bold]{len(questions)}[/bold] questions against [bold]{args.api}[/bold] "
        f"(mode={args.mode}, workspace={args.workspace}, concurrency={args.concurrency})"
    )

    semaphore = asyncio.Semaphore(args.concurrency)
    timeout = httpx.Timeout(args.timeout)

    async with httpx.AsyncClient(base_url=args.api, timeout=timeout) as api_client:
        judge_headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', '')}"}
        async with httpx.AsyncClient(timeout=httpx.Timeout(90.0), headers=judge_headers) as judge:
            tasks = [evaluate_one(q, args, api_client, judge, semaphore) for q in questions]
            results = []
            for index, coro in enumerate(asyncio.as_completed(tasks), start=1):
                results.append(await coro)
                if not args.quiet:
                    print(f"\r  {index}/{len(questions)} done", end="", file=sys.stderr)
    if not args.quiet:
        print("", file=sys.stderr)

    order = {q.id: i for i, q in enumerate(questions)}
    results.sort(key=lambda r: order.get(r["id"], 0))

    summary = aggregate(results, args.mode)
    render_console(summary, results, args.mode)

    reports = HERE / "reports"
    reports.mkdir(exist_ok=True)
    payload = {
        "tag": args.tag,
        "run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config": {
            "api": args.api,
            "workspace": args.workspace,
            "mode": args.mode,
            "topk": args.topk,
            "graph_topk": args.graph_topk,
            "similarity_threshold": args.similarity_threshold,
            "summary_threshold": args.summary_threshold,
            "model": args.model,
            "judge_model": args.judge_model,
            "eval_set": set_path.name,
        },
        "summary": summary,
        "results": results,
    }
    (reports / f"{args.tag}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (reports / f"{args.tag}.md").write_text(
        render_markdown(summary, results, args), encoding="utf-8"
    )
    echo()
    echo(f"Reports written to [bold]reports/{args.tag}.json[/bold] and "
         f"[bold]reports/{args.tag}.md[/bold]")

    if args.fail_under is not None:
        headline = (
            summary.get("answer", {}).get("strict_accuracy_pct")
            if args.mode in ("answer", "both")
            else summary.get("retrieval", {}).get("union_pct")
        )
        if headline is not None and headline < args.fail_under:
            echo(f"[red]FAIL[/red] headline {headline}% is below --fail-under {args.fail_under}%")
            return 1
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    return asyncio.run(run_async(args))


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scored evaluation harness for the api RAG pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--env-file", help="Path to a .env file (default: ./.env, ../api/.env)")
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify", help="Offline check of eval set against the corpus")
    verify.add_argument("--set", default="eval_set.yaml")
    verify.add_argument("--corpus", help="Corpus markdown directory (default: from eval set meta)")
    verify.set_defaults(func=cmd_verify)

    run = sub.add_parser("run", help="Score the live system")
    run.add_argument("--api", default=os.getenv("EVAL_API", "http://localhost:8000"))
    run.add_argument("--set", default="eval_set.yaml")
    run.add_argument("--workspace", default=os.getenv("EVAL_WORKSPACE", "meridian_demo"))
    run.add_argument("--mode", choices=["retrieval", "answer", "both"], default="both")
    run.add_argument("--topk", type=int, default=5)
    run.add_argument("--graph-topk", type=int, default=20)
    run.add_argument("--similarity-threshold", type=float, default=0.2)
    run.add_argument("--summary-threshold", type=float, default=0.2)
    run.add_argument("--model", help="Override the answering model (gpt-4o-mini, gpt-4.1-mini)")
    run.add_argument("--judge-model", default=os.getenv("EVAL_JUDGE_MODEL", "gpt-4o-mini"))
    run.add_argument("--concurrency", type=int, default=3)
    run.add_argument("--timeout", type=float, default=180.0)
    run.add_argument("--retries", type=int, default=1)
    run.add_argument("--limit", type=int, help="Only run the first N questions")
    run.add_argument("--category", help="Comma-separated categories to include")
    run.add_argument("--tag", default=datetime.now().strftime("run-%Y%m%d-%H%M%S"))
    run.add_argument("--fail-under", type=float, help="Exit 1 if the headline metric is lower")
    run.add_argument("--quiet", action="store_true")
    run.set_defaults(func=cmd_run)

    args = parser.parse_args()
    load_env(args.env_file)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
