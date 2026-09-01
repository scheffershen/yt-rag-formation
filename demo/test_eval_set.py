#!/usr/bin/env python
"""Regression checks for the versioned Meridian evaluation ground truth.

Run with: python test_eval_set.py

对 Meridian 版本化评估真值进行回归测试。

运行命令：python test_eval_set.py
"""

from __future__ import annotations

import sys

from eval import HERE, load_eval_set


def check(label: str, actual: object, expected: object, failures: list[str]) -> None:
    if actual != expected:
        failures.append(f"{label}\n    expected: {expected!r}\n    actual:   {actual!r}")


meta, questions = load_eval_set(HERE / "eval_set.yaml")
by_id = {question.id: question for question in questions}
failures: list[str] = []

check("eval set version", meta.get("version"), "1.1.0", failures)
check(
    "q29 reference answers the singular restoration-test question",
    by_id["q29"].expect_answer,
    "Un test de restauration trimestriel, decrit dans PR-EXM-MRD-003.",
    failures,
)
check(
    "q56 reference does not require an unasked date",
    by_id["q56"].expect_answer,
    "4 collaborateurs.",
    failures,
)

if failures:
    print(f"{len(failures)} FAILED\n")
    for failure in failures:
        print(f"  x {failure}")
    sys.exit(1)

print("eval-set regression checks: all checks passed")
