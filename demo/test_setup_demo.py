#!/usr/bin/env python
"""Regression checks for the demo-only secret boundary in setup_demo.py.

The demo stack must never depend on demo/.env at runtime. It must read OPENAI_API_KEY only from an explicit,
git-ignored, demo-only file passed to Compose via --env-file.

Run with: python test_setup_demo.py

针对 `setup_demo.py` 中“仅限演示环境”的密钥隔离机制进行回归检查。

演示环境的堆栈在运行时绝不能依赖 `demo/.env`。它必须仅从一个明确指定、被 Git 忽略且仅用于演示的文件中读取 `OPENAI_API_KEY`，该文件需通过 `--env-file` 参数传递给 Compose。

运行命令：`python test_setup_demo.py`
"""

from __future__ import annotations

import sys
from pathlib import Path

from setup_demo import COMPOSE_FILE, DEMO_SECRET_ENV_FILE, HERE, build_compose_command

FAILURES: list[str] = []


def check(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        FAILURES.append(f"{label}\n    expected: {expected!r}\n    actual:   {actual!r}")


check("demo secret filename", DEMO_SECRET_ENV_FILE, ".env.demo.local")
check(
    "compose receives only the demo secret file",
    build_compose_command(["docker", "compose"], ["config"]),
    ["docker", "compose", "--env-file", DEMO_SECRET_ENV_FILE, "-f", COMPOSE_FILE, "config"],
)

example_path = HERE / ".env.demo.local.example"
if not example_path.is_file():
    FAILURES.append(f"missing {example_path}")
else:
    example_text = example_path.read_text(encoding="utf-8")
    check("example has no key", example_text.strip(), "OPENAI_API_KEY=")

compose_yml = (HERE / COMPOSE_FILE).read_text(encoding="utf-8")
check("compose error message points at the demo-only secret file",
      f"set OPENAI_API_KEY in demo/{DEMO_SECRET_ENV_FILE}" in compose_yml, True)
check("compose error message no longer points at demo/.env",
      "set OPENAI_API_KEY in demo/.env}" in compose_yml, False)

gitignore = (HERE / ".gitignore").read_text(encoding="utf-8")
check("demo secret file is git-ignored", DEMO_SECRET_ENV_FILE in gitignore.splitlines(), True)

readme = (HERE / "README.md").read_text(encoding="utf-8")
check("README no longer instructs copying the production env", ".env` is a copy of the **Symfony" in readme, False)
check("README documents the demo-only secret file", DEMO_SECRET_ENV_FILE in readme, True)

if FAILURES:
    print(f"{len(FAILURES)} FAILED\n")
    for failure in FAILURES:
        print(f"  x {failure}")
    sys.exit(1)

print("setup demo checks: all checks passed")
