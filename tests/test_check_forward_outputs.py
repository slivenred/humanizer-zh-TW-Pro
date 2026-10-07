"""Regression tests for preservation checks and honest run reporting."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.check_forward_outputs import (
    ROOT,
    ValidationError,
    check_outputs,
    current_skill_version,
    format_report,
)


class ForwardOutputTests(unittest.TestCase):
    def setUp(self):
        self.corpus = {
            "schema_version": 1,
            "purpose": "Isolated checker fixture, not model evaluation evidence.",
            "cases": [
                {
                    "id": "protected_01",
                    "input": "請執行 `npm run build`，再看 https://example.com/docs?q=1。",
                    "protected_literals": ["`npm run build`", "https://example.com/docs?q=1"],
                    "must_preserve": ["保留主體、條件與歸因，不是要原樣輸出這段要求"],
                    "output_mode": "rewrite",
                },
                {"id": "audit_02", "input": "這段已經自然。", "output_mode": "audit"},
            ],
        }
        self.record = {
            "schema_version": 1,
            "skill_version": "1.0.0-pro.6",
            "run": {"date": "2026-10-08", "executor": "unit-test fixture", "setup": "No model called."},
            "outputs": [
                {
                    "case_id": "protected_01",
                    "output": "請執行 `npm run build`，再看 https://example.com/docs?q=1。",
                    "review": {"status": "pass", "notes": "Fixture marks review pass to test checker accounting."},
                },
                {
                    "case_id": "audit_02",
                    "output": "不需要修改。",
                    "review": {"status": "pass", "notes": "Fixture audit mode retained."},
                },
            ],
        }

    def check(self):
        return check_outputs(self.record, self.corpus, "1.0.0-pro.6")

    def test_reviewed_outputs_pass_without_matching_natural_language_constraints(self):
        report = self.check()
        self.assertTrue(report.passed)
        self.assertEqual(report.reviewed_pass, 2)
        self.assertEqual(report.literal_checks, 2)
        self.assertEqual(report.unrun_case_ids, [])

    def test_missing_literal_fails_even_when_review_marks_pass(self):
        self.record["outputs"][0]["output"] = "請執行 `npm run build`。"
        report = self.check()
        self.assertFalse(report.passed)
        self.assertEqual(report.reviewed_pass, 1)
        self.assertEqual(report.missing_literals["protected_01"], ["https://example.com/docs?q=1"])

    def test_changed_literal_is_not_normalized_into_a_pass(self):
        self.record["outputs"][0]["output"] = "請執行 `npm run Build`，再看 https://example.com/docs?q=1。"
        self.assertFalse(self.check().passed)

    def test_unknown_case_id_is_rejected(self):
        self.record["outputs"][0]["case_id"] = "invented_99"
        with self.assertRaisesRegex(ValidationError, "unknown case id"):
            self.check()

    def test_duplicate_output_case_is_rejected(self):
        self.record["outputs"].append(copy.deepcopy(self.record["outputs"][0]))
        with self.assertRaisesRegex(ValidationError, "duplicate output case id"):
            self.check()

    def test_pending_review_never_counts_as_pass(self):
        self.record["outputs"][0]["review"]["status"] = "pending"
        report = self.check()
        self.assertFalse(report.passed)
        self.assertEqual(report.editorial_review["pending"], 1)
        self.assertEqual(report.reviewed_pass, 1)
        self.assertIn("Reviewed cases NOT PASS", format_report(report))

    def test_review_failure_blocks_pass_without_missing_literals(self):
        self.record["outputs"][0]["review"]["status"] = "fail"
        report = self.check()
        self.assertFalse(report.passed)
        self.assertEqual(report.missing_literals, {})

    def test_version_mismatch_is_rejected(self):
        self.record["skill_version"] = "1.0.0-pro.5"
        with self.assertRaisesRegex(ValidationError, "does not match SKILL.md"):
            self.check()

    def test_partial_coverage_is_reported_without_full_corpus_claim(self):
        self.record["outputs"].pop()
        report = self.check()
        self.assertTrue(report.passed)
        self.assertEqual((report.submitted_cases, report.total_cases), (1, 2))
        self.assertEqual(report.unrun_case_ids, ["audit_02"])
        summary = format_report(report)
        self.assertIn("Coverage: 1/2 cases (partial)", summary)
        self.assertIn("does not establish a full-corpus pass", summary)

    def test_invalid_calendar_date_is_rejected(self):
        self.record["run"]["date"] = "2026-02-30"
        with self.assertRaisesRegex(ValidationError, "calendar date"):
            self.check()

    def test_empty_outputs_cannot_claim_vacuous_success(self):
        self.record["outputs"] = []
        with self.assertRaisesRegex(ValidationError, "non-empty list"):
            self.check()

    def test_protected_literals_must_really_occur_in_input(self):
        self.corpus["cases"][0]["protected_literals"].append("invented fact")
        with self.assertRaisesRegex(ValidationError, "does not occur in input"):
            self.check()

    def test_missing_editorial_review_cannot_be_assumed_to_pass(self):
        del self.record["outputs"][0]["review"]
        with self.assertRaisesRegex(ValidationError, "missing=.*review"):
            self.check()

    def test_invalid_output_mode_in_custom_corpus_is_rejected(self):
        self.corpus["cases"][0]["output_mode"] = "automatic_grade"
        with self.assertRaisesRegex(ValidationError, "must be rewrite or audit"):
            self.check()

    def test_cli_uses_isolated_corpus_and_nonzero_exit_for_pending(self):
        self.record["skill_version"] = current_skill_version()
        self.record["outputs"][0]["review"]["status"] = "pending"
        with tempfile.TemporaryDirectory() as directory:
            results_path = Path(directory) / "results.json"
            corpus_path = Path(directory) / "corpus.json"
            results_path.write_text(json.dumps(self.record, ensure_ascii=False), encoding="utf-8")
            corpus_path.write_text(json.dumps(self.corpus, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "check_forward_outputs.py"), str(results_path), "--corpus", str(corpus_path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("pending=1", result.stdout)
        self.assertIn("Coverage: 2/2 cases (full)", result.stdout)


if __name__ == "__main__":
    unittest.main()
