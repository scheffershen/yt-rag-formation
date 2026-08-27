from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import chunk_lab


class ChunkLabTest(unittest.TestCase):
    def test_build_windows_keeps_short_paragraphs_as_independent_windows(self) -> None:
        windows = chunk_lab.build_windows("# Heading\n\nFact 45\n\nNext step", 12, 0)

        self.assertEqual([window.text for window in windows], ["# Heading", "Fact 45", "Next step"])

    def test_score_windows_requires_fact_and_reference_in_the_same_window(self) -> None:
        windows = [
            chunk_lab.Window(index=1, text="PR-QA-MRD-009\nFact 45"),
            chunk_lab.Window(index=2, text="PR-QA-MRD-009"),
            chunk_lab.Window(index=3, text="Fact 45"),
        ]

        score = chunk_lab.score_windows(windows, "PR-QA-MRD-009", ["45"])

        self.assertEqual(score["evidence_identity_windows"], [1])
        self.assertEqual(score["evidence_identity_rate"], 1 / 3)

    def test_question_report_uses_the_demo_corpus_and_q24_ground_truth(self) -> None:
        project = Path(__file__).resolve().parent

        report = chunk_lab.build_question_report(project, "q24", 280, 40)

        self.assertEqual(report["question_id"], "q24")
        self.assertEqual(report["expected_sources"], ["PR-QA-MRD-009"])
        self.assertEqual(report["must_include"], ["45"])
        self.assertGreater(report["source_reports"][0]["window_count"], 0)

    def test_write_report_creates_json_and_markdown(self) -> None:
        report = {
            "question_id": "q-test",
            "question": "Test question",
            "metric": "source-window proxy",
            "limitation": "Test limitation",
            "window_chars": 280,
            "overlap_chars": 40,
            "source_reports": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "chunk-lab"

            json_path, markdown_path = chunk_lab.write_report(report, output)

            self.assertTrue(json_path.is_file())
            self.assertTrue(markdown_path.is_file())
            self.assertIn("source-window proxy", markdown_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
