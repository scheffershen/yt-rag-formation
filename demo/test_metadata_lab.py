from __future__ import annotations

import unittest
from pathlib import Path

import metadata_lab


class MetadataLabTest(unittest.TestCase):
    def test_inventory_aggregates_ingestion_metadata(self) -> None:
        inventory = metadata_lab.build_inventory([
            {"ref": "PR-1", "dept": "QA", "doc_type": "Procedure"},
            {"ref": "PR-2", "dept": "IT", "doc_type": "Procedure"},
        ])
        self.assertEqual(inventory["document_count"], 2)
        self.assertEqual(inventory["departments"], ["IT", "QA"])
        self.assertEqual(inventory["document_types"], ["Procedure"])
        self.assertEqual(inventory["enforcement_status"], "metadata available")

    def test_demo_report_uses_the_synthetic_corpus(self) -> None:
        report = metadata_lab.build_demo_report(Path(__file__).resolve().parent)
        self.assertEqual(report["company"], "Meridian Labs")
        self.assertEqual(report["document_count"], 25)
        self.assertIn("Assurance Qualite", report["departments"])


if __name__ == "__main__":
    unittest.main()
