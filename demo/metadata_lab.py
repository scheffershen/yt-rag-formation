from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def build_inventory(documents: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "document_count": len(documents),
        "company": "Meridian Labs",
        "departments": sorted({document["dept"] for document in documents}),
        "document_types": sorted({document["doc_type"] for document in documents}),
        "references": sorted(document["ref"] for document in documents),
        "metadata_fields": ["company", "department", "document type", "document reference"],
        "enforcement_status": "metadata available",
        "limitation": "This inventory does not implement or prove role-based authorization.",
    }


def build_demo_report(project: Path) -> dict[str, Any]:
    from build_corpus import DOCUMENTS

    return build_inventory(list(DOCUMENTS))


def markdown_report(report: dict[str, Any]) -> str:
    return "\n".join([
        "# Metadata lab — current demo inventory", "",
        f"- Documents: {report['document_count']}",
        f"- Company: {report['company']}",
        f"- Departments: {', '.join(report['departments'])}",
        f"- Document types: {', '.join(report['document_types'])}",
        f"- Status: {report['enforcement_status']}",
        f"- Limitation: {report['limitation']}", "",
    ])


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect metadata available to the Meridian demo ingestion.")
    parser.add_argument("--output-dir", type=Path, default=Path("reports"))
    args = parser.parse_args()
    project = Path(__file__).resolve().parent
    report = build_demo_report(project)
    output = project / args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    (output / "lesson-07-metadata-inventory.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / "lesson-07-metadata-inventory.md").write_text(markdown_report(report), encoding="utf-8")
    print("wrote lesson-07-metadata-inventory.json and lesson-07-metadata-inventory.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
