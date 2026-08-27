from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


DEFAULT_QUESTIONS = ("q24", "q30", "q52")


@dataclass(frozen=True)
class Window:
    index: int
    text: str


def build_windows(text: str, window_chars: int, overlap_chars: int) -> list[Window]:
    """Create deterministic paragraph-aware source windows for a teaching experiment."""
    if window_chars <= 0:
        raise ValueError("window_chars must be positive")
    if overlap_chars < 0 or overlap_chars >= window_chars:
        raise ValueError("overlap_chars must be at least 0 and smaller than window_chars")

    paragraphs = [paragraph.strip() for paragraph in text.replace("\r\n", "\n").split("\n\n") if paragraph.strip()]
    windows: list[str] = []
    current = ""

    for paragraph in paragraphs:
        if len(paragraph) > window_chars:
            if current:
                windows.append(current)
                current = ""
            windows.extend(_slice_text(paragraph, window_chars, overlap_chars))
            continue

        candidate = paragraph if not current else f"{current}\n\n{paragraph}"
        if len(candidate) <= window_chars:
            current = candidate
            continue

        windows.append(current)
        overlap = current[-overlap_chars:] if overlap_chars else ""
        current = paragraph if not overlap else f"{overlap}\n\n{paragraph}"

    if current:
        windows.append(current)

    return [Window(index=index, text=window) for index, window in enumerate(windows, start=1)]


def _slice_text(text: str, window_chars: int, overlap_chars: int) -> list[str]:
    windows: list[str] = []
    start = 0
    while start < len(text):
        windows.append(text[start : start + window_chars])
        if start + window_chars >= len(text):
            break
        start += window_chars - overlap_chars
    return windows


def score_windows(windows: list[Window], reference: str, required_terms: list[str]) -> dict[str, Any]:
    """Measure only co-location of document identity and required fact terms."""
    reference_normalized = reference.casefold()
    terms = [term.casefold() for term in required_terms]
    matching = [
        window.index
        for window in windows
        if reference_normalized in window.text.casefold()
        and all(term in window.text.casefold() for term in terms)
    ]
    return {
        "evidence_identity_windows": matching,
        "evidence_identity_rate": len(matching) / len(windows) if windows else 0.0,
    }


def build_question_report(project: Path, question_id: str, window_chars: int, overlap_chars: int) -> dict[str, Any]:
    question = _find_question(project / "eval_set.yaml", question_id)
    source_reports = []
    for reference in question["expect_sources"]:
        source_path = project / "corpus" / "md" / f"{reference}.md"
        source_text = source_path.read_text(encoding="utf-8")
        windows = build_windows(source_text, window_chars, overlap_chars)
        score = score_windows(windows, reference, question["must_include"])
        source_reports.append(
            {
                "reference": reference,
                "source_path": str(source_path.relative_to(project)),
                "window_count": len(windows),
                "score": score,
                "windows": [
                    {**asdict(window), "contains_required_terms": all(term.casefold() in window.text.casefold() for term in question["must_include"])}
                    for window in windows
                ],
            }
        )

    return {
        "question_id": question["id"],
        "question": question["question"],
        "expected_sources": question["expect_sources"],
        "must_include": question["must_include"],
        "window_chars": window_chars,
        "overlap_chars": overlap_chars,
        "metric": "source-window proxy: windows containing both the source reference and every required fact term",
        "limitation": "This inspects synthetic Markdown source windows. It does not query, change, or reindex the live demo stack.",
        "source_reports": source_reports,
    }


def _find_question(eval_set_path: Path, question_id: str) -> dict[str, Any]:
    data = yaml.safe_load(eval_set_path.read_text(encoding="utf-8"))
    for question in data["questions"]:
        if question["id"] == question_id:
            return question
    raise ValueError(f"Unknown question: {question_id}")


def write_report(report: dict[str, Any], output: Path) -> tuple[Path, Path]:
    output.parent.mkdir(parents=True, exist_ok=True)
    json_path = output.with_suffix(".json")
    markdown_path = output.with_suffix(".md")
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(_markdown_report(report), encoding="utf-8")
    return json_path, markdown_path


def _markdown_report(report: dict[str, Any]) -> str:
    lines = [
        f"# Chunk lab — {report['question_id']}",
        "",
        f"**Question:** {report['question']}",
        "",
        f"**Metric:** {report['metric']}",
        "",
        f"**Limitation:** {report['limitation']}",
        "",
        f"Configuration: `{report['window_chars']}` characters per window, `{report['overlap_chars']}` overlap characters.",
        "",
    ]
    for source in report["source_reports"]:
        score = source["score"]
        lines.extend(
            [
                f"## {source['reference']}",
                "",
                f"- Windows: {source['window_count']}",
                f"- Evidence-and-identity windows: {score['evidence_identity_windows'] or 'none'}",
                f"- Evidence-and-identity rate: {score['evidence_identity_rate']:.1%}",
                "",
            ]
        )
        for window in source["windows"]:
            marker = "required fact present" if window["contains_required_terms"] else "required fact absent"
            lines.extend([f"### Window {window['index']} — {marker}", "", "```text", window["text"], "```", ""])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect deterministic source windows for Lesson 6.")
    parser.add_argument("--question", action="append", choices=DEFAULT_QUESTIONS, help="Question to inspect; repeatable. Defaults to q24, q30, and q52.")
    parser.add_argument("--window-chars", type=int, default=280, help="Maximum characters per source window.")
    parser.add_argument("--overlap-chars", type=int, default=40, help="Characters repeated at a window boundary.")
    parser.add_argument("--output-dir", type=Path, default=Path("reports"), help="Directory for JSON and Markdown reports.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(__file__).resolve().parent
    question_ids = args.question or DEFAULT_QUESTIONS
    for question_id in question_ids:
        report = build_question_report(project, question_id, args.window_chars, args.overlap_chars)
        json_path, markdown_path = write_report(report, project / args.output_dir / f"lesson-06-{question_id}-chunks")
        print(f"{question_id}: wrote {json_path.name} and {markdown_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
