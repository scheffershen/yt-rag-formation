#!/usr/bin/env python
"""
Sanitised demo workspace for the api RAG pipeline.

Brings up an isolated stack (docker-compose.demo.yml) and indexes the synthetic
Meridian Labs corpus into demo-only collections, so a screen recording never
touches real client data.

    up       Build and start the demo stack, wait for the API to answer.
    ingest   Index every corpus PDF into the demo collections.
    status   Show container state and the API health response.
    down     Stop the stack. --volumes also deletes ./.data.

Nothing here modifies api/. The API reads .env.demo, not api/.env.

The one real secret the stack needs, OPENAI_API_KEY, comes from
.env.demo.local (git-ignored, demo-only - see .env.demo.local.example).
The demo never reads demo/.env, which is a copy of the production Symfony
env and holds live secrets.

Examples:
    python setup_demo.py up
    python setup_demo.py ingest --dry-run
    python setup_demo.py ingest
    python setup_demo.py down

Ingestion runs inside the API container by default, which is why no local
Python environment with api's dependencies is required. Use --runner local to
run it on the host instead (then the host needs api's dependencies installed).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent

COMPOSE_FILE = "docker-compose.demo.yml"
DEMO_SECRET_ENV_FILE = ".env.demo.local"
SERVICE = "api"
API_URL = "http://localhost:8000"

WORKSPACE = "meridian_demo"
QDRANT_COLLECTION = "meridian_documents"
QDRANT_SUMMARY_COLLECTION = "meridian_summary"
MEILI_INDEX = "meridian_documents"

# Host-mapped ports from docker-compose.demo.yml, used by --runner local.
LOCAL_QDRANT_PORT = "6433"
LOCAL_MEILI_URL = "http://localhost:7800"
LOCAL_POSTGRES_PORT = "5533"


def compose_command() -> list[str]:
    """Prefer `docker compose`, fall back to legacy `docker-compose`."""
    for candidate in (["docker", "compose"], ["docker-compose"]):
        try:
            probe = subprocess.run(
                [*candidate, "version"], capture_output=True, timeout=30, check=False
            )
            if probe.returncode == 0:
                return candidate
        except (OSError, subprocess.SubprocessError):
            continue
    raise SystemExit(
        "Neither `docker compose` nor `docker-compose` is available. Is Docker running?"
    )


def build_compose_command(engine: list[str], args_list: list[str]) -> list[str]:
    return [*engine, "--env-file", DEMO_SECRET_ENV_FILE, "-f", COMPOSE_FILE, *args_list]


def compose(args_list: list[str], **kwargs) -> subprocess.CompletedProcess:
    command = build_compose_command(compose_command(), args_list)
    return subprocess.run(command, cwd=HERE, **kwargs)


def check_env() -> None:
    env_file = HERE / DEMO_SECRET_ENV_FILE
    if not env_file.is_file():
        raise SystemExit(
            f"{env_file} not found.\n"
            "The demo stack reads OPENAI_API_KEY from it. Create it with:\n"
            f"    cp {DEMO_SECRET_ENV_FILE}.example {DEMO_SECRET_ENV_FILE}\n"
            "    # then set OPENAI_API_KEY=sk-... in it\n"
        )
    for line in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith("OPENAI_API_KEY=") and line.strip() != "OPENAI_API_KEY=":
            return
    raise SystemExit(f"OPENAI_API_KEY is not set in {env_file}")


def api_health(timeout: float = 3.0) -> dict | None:
    try:
        with urllib.request.urlopen(f"{API_URL}/health", timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError, TimeoutError):
        return None


# --------------------------------------------------------------------------
# up / down / status
# --------------------------------------------------------------------------


def cmd_up(args: argparse.Namespace) -> int:
    check_env()

    print("Starting the demo stack (first run builds the API image - a few minutes)...")
    build = ["up", "-d"]
    if not args.no_build:
        build.append("--build")
    result = compose(build)
    if result.returncode != 0:
        print("\nCompose failed to start the stack.", file=sys.stderr)
        print("If port 8000 is already bound, the project stack is probably running.",
              file=sys.stderr)
        return result.returncode

    print(f"\nWaiting for {API_URL}/health ...", end="", flush=True)
    deadline = time.monotonic() + args.wait
    while time.monotonic() < deadline:
        health = api_health()
        if health and health.get("status") == "healthy":
            print(" ready")
            print(f"  services: {health.get('services')}")
            print()
            print("Next:  python setup_demo.py ingest")
            return 0
        print(".", end="", flush=True)
        time.sleep(3)

    print(" timed out")
    print()
    print("The stack is up but the API did not report healthy. Check the logs:")
    print(f"  docker compose -f {COMPOSE_FILE} logs api --tail 50")
    print(f"  docker compose -f {COMPOSE_FILE} logs init-db --tail 30")
    return 1


def cmd_down(args: argparse.Namespace) -> int:
    command = ["down"]
    if args.volumes:
        command.append("-v")
        print("Stopping the stack and removing volumes...")
    else:
        print("Stopping the stack (./.data is kept)...")
    result = compose(command)
    if result.returncode == 0 and args.volumes:
        data = HERE / ".data"
        if data.is_dir():
            print(f"\nNote: bind-mounted data still exists at {data}")
            print("Delete it manually to start completely fresh.")
    return result.returncode


def cmd_status(_args: argparse.Namespace) -> int:
    compose(["ps"])
    print()
    health = api_health()
    if health:
        print(f"API {API_URL}/health -> {json.dumps(health)}")
    else:
        print(f"API {API_URL}/health -> unreachable")
    return 0


# --------------------------------------------------------------------------
# ingest
# --------------------------------------------------------------------------


def ingest_flags(document: dict, recreate: bool, indexes: str, local: bool) -> list[str]:
    flags = [
        "--indexes",
        indexes,
        "--workspace",
        WORKSPACE,
        "--qdrant-collection",
        QDRANT_COLLECTION,
        "--qdrant-summary-collection",
        QDRANT_SUMMARY_COLLECTION,
        "--meilisearch-index",
        MEILI_INDEX,
        "--document-id",
        document["ref"],
        "--company",
        "Meridian Labs",
        "--doc-type",
        document["doc_type"],
        "--department",
        document["dept"],
    ]

    if local:
        # Inside the container these come from .env.demo; on the host they have
        # to point at the published ports instead.
        flags += [
            "--qdrant-host",
            "localhost",
            "--qdrant-port",
            LOCAL_QDRANT_PORT,
            "--qdrant-api-key",
            "meridian_demo_key",
            "--meilisearch-host",
            LOCAL_MEILI_URL,
            "--meilisearch-key",
            "meridian_demo_key",
            "--postgres-host",
            "localhost",
            "--postgres-port",
            LOCAL_POSTGRES_PORT,
            "--postgres-password",
            "meridian_demo",
        ]

    # --recreate drops the whole collection, index and workspace, so it belongs
    # on the first document only - passing it per document would wipe each
    # previous one.
    if recreate:
        flags.append("--recreate")
    return flags


def cmd_ingest(args: argparse.Namespace) -> int:
    from build_corpus import DOCUMENTS

    pdf_dir = (HERE / args.corpus / "pdf").resolve()

    if not args.skip_build:
        print("Building corpus...")
        result = subprocess.run(
            [sys.executable, str(HERE / "build_corpus.py"), "--out", args.corpus], cwd=HERE
        )
        if result.returncode != 0:
            return result.returncode
        print()

    documents = list(DOCUMENTS)
    if args.limit:
        documents = documents[: args.limit]

    missing = [d["ref"] for d in documents if not (pdf_dir / f"{d['ref']}.pdf").is_file()]
    if missing:
        print(f"Missing PDFs in {pdf_dir}: {', '.join(missing)}", file=sys.stderr)
        return 2

    local = args.runner == "local"

    if not local and not args.dry_run:
        if api_health() is None:
            print(f"The demo API is not answering on {API_URL}.", file=sys.stderr)
            print("Start the stack first:  python setup_demo.py up", file=sys.stderr)
            return 2

    print(f"Indexing {len(documents)} documents into the demo workspace")
    print(f"  runner       {args.runner}")
    print(f"  workspace    {WORKSPACE}")
    print(f"  collections  {QDRANT_COLLECTION} / {QDRANT_SUMMARY_COLLECTION} / {MEILI_INDEX}")
    print(f"  indexes      {args.indexes}")
    if args.dry_run:
        print("  MODE         dry run - nothing will be indexed")
    print()

    api_dir = (HERE / args.api_dir).resolve()
    if local and not (api_dir / "ingest.py").is_file():
        print(f"ingest.py not found in {api_dir} - pass --api-dir <path>", file=sys.stderr)
        return 2

    failures: list[str] = []
    started = time.monotonic()

    for position, document in enumerate(documents, start=1):
        ref = document["ref"]
        recreate = position == 1 and not args.no_recreate
        flags = ingest_flags(document, recreate, args.indexes, local)

        if local:
            command = [args.python, "ingest.py", str(pdf_dir / f"{ref}.pdf"), *flags]
            cwd = api_dir
        else:
            command = [
                *build_compose_command(compose_command(), []),
                "exec",
                "-T",
                SERVICE,
                "uv",
                "run",
                "python",
                "ingest.py",
                f"/corpus/pdf/{ref}.pdf",
                *flags,
            ]
            cwd = HERE

        label = f"[{position}/{len(documents)}] {ref}"
        if args.dry_run:
            print(f"{label}\n    {' '.join(command)}\n")
            continue

        print(f"{label} indexing{' (--recreate)' if recreate else ''}...", flush=True)
        result = subprocess.run(command, cwd=cwd)
        if result.returncode != 0:
            failures.append(ref)
            print(f"{label} FAILED (exit {result.returncode})", file=sys.stderr)

    if args.dry_run:
        return 0

    elapsed = time.monotonic() - started
    print()
    print("=" * 62)
    print(f"Indexed {len(documents) - len(failures)}/{len(documents)} documents "
          f"in {elapsed / 60:.1f} min")
    if failures:
        print(f"Failed: {', '.join(failures)}")
    print("=" * 62)
    print()
    print("Next:")
    print("  python eval.py run --mode retrieval --workspace meridian_demo --tag ablation")
    print("  python eval.py run --workspace meridian_demo --tag demo-1")

    return 1 if failures else 0


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build, start and populate the sanitised demo workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    up = sub.add_parser("up", help="Build and start the demo stack")
    up.add_argument("--no-build", action="store_true", help="Skip the image build")
    up.add_argument("--wait", type=float, default=300.0, help="Seconds to wait for the API")
    up.set_defaults(func=cmd_up)

    ingest = sub.add_parser("ingest", help="Index the demo corpus into demo-only collections")
    ingest.add_argument("--runner", choices=["docker", "local"], default="docker")
    ingest.add_argument("--corpus", default="corpus")
    ingest.add_argument("--api-dir", default="../api", help="Path to api/ (--runner local only)")
    ingest.add_argument("--python", default=sys.executable, help="Interpreter (--runner local)")
    ingest.add_argument("--indexes", default="all", help="Passed to ingest.py (default: all)")
    ingest.add_argument("--limit", type=int, help="Only index the first N documents")
    ingest.add_argument("--skip-build", action="store_true", help="Do not regenerate the corpus")
    ingest.add_argument(
        "--no-recreate",
        action="store_true",
        help="Keep existing demo data instead of recreating on the first document",
    )
    ingest.add_argument("--dry-run", action="store_true", help="Print commands without running")
    ingest.set_defaults(func=cmd_ingest)

    status = sub.add_parser("status", help="Show container and API state")
    status.set_defaults(func=cmd_status)

    down = sub.add_parser("down", help="Stop the demo stack")
    down.add_argument("--volumes", action="store_true", help="Also remove volumes")
    down.set_defaults(func=cmd_down)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
