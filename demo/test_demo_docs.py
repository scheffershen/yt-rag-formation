#!/usr/bin/env python
"""Regression check that README.md states the real corpus/eval-set facts.

Prevents the documentation from silently drifting from build_corpus.py and
eval_set.yaml, the way it did when the corpus grew from 13 to 25 documents
and the eval set from 44 to 65 questions but the README kept the old numbers.

Run with: python test_demo_docs.py

进行回归检查，确保 README.md 中关于语料库（corpus）和评估集（eval-set）的描述与实际情况相符。

此举旨在防止文档内容与 `build_corpus.py` 及 `eval_set.yaml` 的实际配置发生脱节——此前就曾出现过语料库从 13 篇文档增至 25 篇、评估集从 44 个问题增至 65 个问题，而 README 却仍沿用旧数据的情况。

运行命令：`python test_demo_docs.py`
"""

from __future__ import annotations

import sys

from build_corpus import DOCUMENTS
from eval import HERE, load_eval_set

FAILURES: list[str] = []


def check(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        FAILURES.append(f"{label}\n    expected: {expected!r}\n    actual:   {actual!r}")


readme = (HERE / "README.md").read_text(encoding="utf-8")
meta, questions = load_eval_set(HERE / "eval_set.yaml")

check("README document count", f"{len(DOCUMENTS)} synthetic documents" in readme, True)
check("README question count", f"{len(questions)} questions" in readme, True)
check("README eval-set version", f"version `{meta['version']}`" in readme, True)
check("README does not still say 13 documents", "13 documents" in readme, False)
check("README does not still say 13 synthetic documents", "13 synthetic documents" in readme, False)
check("README does not still say 44 questions", "44 questions" in readme, False)

if FAILURES:
    print(f"{len(FAILURES)} FAILED\n")
    for failure in FAILURES:
        print(f"  x {failure}")
    sys.exit(1)

print("demo documentation checks: all checks passed")
