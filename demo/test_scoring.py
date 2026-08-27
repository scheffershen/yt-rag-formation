#!/usr/bin/env python
"""
Self-test for the scoring logic in eval.py.

The point of this file is trust: if score_retrieval() or score_sources() is
wrong, eval.py still prints a confident headline percentage - just the wrong
one. Run this before quoting any number publicly.

    python test_scoring.py

Payloads below mirror the real shapes returned by the API:
  /api/v1/search -> vector_results / summary_results = [{text, score, metadata}]
                    fulltext_results = raw Meilisearch hits
                    graph_context    = flat string
  /api/v1/qa     -> sources = [{filename, text, type}]

用于验证 `eval.py` 中评分逻辑的自测脚本。

该脚本旨在确保结果可信：如果 `score_retrieval()` 或 `score_sources()` 存在逻辑错误，`eval.py` 仍会输出一个看似确信无疑的百分比数值——只不过该数值是错误的。因此，在公开引用任何数据之前，请务必先运行此脚本：

python test_scoring.py

下方的测试数据（payloads）模拟了 API 实际返回的数据结构：
/api/v1/search -> vector_results / summary_results = [{text, score, metadata}]
                  fulltext_results = 原始 Meilisearch 命中结果 (raw hits)
                  graph_context    = 扁平字符串 (flat string)
/api/v1/qa     -> sources = [{filename, text, type}]
"""

from __future__ import annotations

import sys

from eval import norm, score_keywords, score_retrieval, score_sources

FAILURES: list[str] = []


def check(label: str, actual, expected) -> None:
    if actual != expected:
        FAILURES.append(f"{label}\n    expected: {expected!r}\n    actual:   {actual!r}")


def doc(source: str, text: str = "chunk text") -> dict:
    return {"text": text, "score": 0.81, "metadata": {"source": source, "document_name": source}}


# -- normalisation ---------------------------------------------------------
check("norm strips accents and punctuation", norm("PR-QA-MRD-009.pdf"), "prqamrd009pdf")
check("norm is accent insensitive", norm("procédure"), norm("procedure"))
check("norm handles None", norm(None), "")

# -- retrieval: single expected source found only by fulltext --------------
payload = {
    "vector_results": [doc("PR-QA-MRD-001.pdf")],
    "summary_results": [],
    "fulltext_results": [{"source": "PR-QA-MRD-009.pdf", "content": "..."}],
    "graph_context": "",
}
scored = score_retrieval(payload, ["PR-QA-MRD-009"])
check("vector misses", scored["indexes"]["vector"]["all"], False)
check("fulltext hits", scored["indexes"]["fulltext"]["all"], True)
check("union hits", scored["union"]["all"], True)
check("cumulative vector alone misses", scored["cumulative"]["vector"]["all"], False)
check("cumulative vector+fulltext hits", scored["cumulative"]["vector+fulltext"]["all"], True)

# -- retrieval: body-text mentions must NOT count as a hit -----------------
# PR-QA-MRD-001 cross-references PR-QA-MRD-009 in its body. Matching chunk text
# would wrongly credit the vector index with retrieving PR-QA-MRD-009.
payload = {
    "vector_results": [doc("PR-QA-MRD-001.pdf", "... constitue une NC au sens de PR-QA-MRD-009.")],
    "summary_results": [],
    "fulltext_results": [],
    "graph_context": "",
}
scored = score_retrieval(payload, ["PR-QA-MRD-009"])
check("cross-reference in body text is not a hit", scored["indexes"]["vector"]["all"], False)
check("union stays false", scored["union"]["all"], False)

# -- retrieval: multi-source question needs ALL sources --------------------
payload = {
    "vector_results": [doc("PR-QA-MRD-001.pdf")],
    "summary_results": [doc("PR-EXM-MRD-003.pdf")],
    "fulltext_results": [],
    "graph_context": "",
}
scored = score_retrieval(payload, ["PR-QA-MRD-001", "PR-EXM-MRD-003"])
check("vector alone has only one of two", scored["indexes"]["vector"]["all"], False)
check("vector alone registers partial", scored["indexes"]["vector"]["any"], True)
check("union has both", scored["union"]["all"], True)
check(
    "summary is what completes the pair",
    scored["cumulative"]["vector+fulltext+summary"]["all"],
    True,
)
check("vector+fulltext still incomplete", scored["cumulative"]["vector+fulltext"]["all"], False)

# -- retrieval: graph context is a flat string -----------------------------
payload = {
    "vector_results": [],
    "summary_results": [],
    "fulltext_results": [],
    "graph_context": "Entity: Camille Renard\nSource: TEAM-ITS-MRD-001.pdf\n...",
}
scored = score_retrieval(payload, ["TEAM-ITS-MRD-001"])
check("graph hit found in context string", scored["indexes"]["graph"]["all"], True)
check("graph appears in cumulative tail", scored["cumulative"]["vector+fulltext+summary+graph"]["all"], True)

# -- retrieval: nothing expected, nothing found ----------------------------
scored = score_retrieval(
    {"vector_results": [], "summary_results": [], "fulltext_results": [], "graph_context": ""}, []
)
check("empty expectation is not a free hit", scored["union"]["all"], False)

# -- answer sources --------------------------------------------------------
sources = [
    {"filename": "PR-QA-MRD-009.pdf", "text": "...", "type": "vector/summary"},
    {"filename": "AN-QA-MRD-000.pdf", "text": "...", "type": "fulltext"},
]
check("cited source found", score_sources(sources, ["PR-QA-MRD-009"])["all"], True)
check("uncited source missing", score_sources(sources, ["PR-MI-MRD-001"])["all"], False)
check(
    "missing list names the gap",
    score_sources(sources, ["PR-QA-MRD-009", "PR-MI-MRD-001"])["missing"],
    ["PR-MI-MRD-001"],
)

# -- keywords --------------------------------------------------------------
check(
    "keyword found despite accents and case",
    score_keywords("Le délai est de 45 JOURS calendaires.", ["45 jours"])["ratio"],
    1.0,
)
check(
    "partial keyword coverage",
    score_keywords("Bitdefender est deploye.", ["Bitdefender", "4 heures"])["ratio"],
    0.5,
)
check("no keywords means no score", score_keywords("anything", [])["ratio"], None)


if FAILURES:
    print(f"{len(FAILURES)} FAILED\n")
    for failure in FAILURES:
        print(f"  x {failure}")
    sys.exit(1)

print("scoring self-test: all checks passed")
