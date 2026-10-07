#!/usr/bin/env python3
"""Check recorded forward-test outputs without invoking a model or grading style."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
REVIEW_STATUSES = {"pass", "fail", "pending"}


class ValidationError(ValueError):
    """A recorded run or corpus cannot be checked reliably."""


@dataclass
class CheckReport:
    total_cases: int
    submitted_cases: int
    reviewed_pass: int
    editorial_review: dict[str, int]
    literal_checks: int
    missing_literals: dict[str, list[str]]
    unrun_case_ids: list[str]

    @property
    def passed(self) -> bool:
        return self.submitted_cases > 0 and self.reviewed_pass == self.submitted_cases


def require_object(value: object, label: str, keys: set[str]) -> dict:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    missing = keys - set(value)
    extra = set(value) - keys
    if missing or extra:
        raise ValidationError(f"{label} keys: missing={sorted(missing)}, unexpected={sorted(extra)}")
    return value


def require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be a non-empty string")
    return value


def index_corpus(corpus: object) -> dict[str, dict]:
    if not isinstance(corpus, dict) or type(corpus.get("schema_version")) is not int or corpus["schema_version"] != 1:
        raise ValidationError("corpus must be an object with schema_version 1")
    cases = corpus.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValidationError("corpus.cases must be a non-empty list")
    indexed = {}
    for number, case in enumerate(cases, 1):
        if not isinstance(case, dict):
            raise ValidationError(f"corpus case #{number} must be an object")
        case_id = require_string(case.get("id"), f"corpus case #{number}.id")
        if case_id in indexed:
            raise ValidationError(f"duplicate corpus case id: {case_id}")
        original = require_string(case.get("input"), f"{case_id}.input")
        literals = case.get("protected_literals", [])
        if not isinstance(literals, list):
            raise ValidationError(f"{case_id}.protected_literals must be a list")
        for literal in literals:
            require_string(literal, f"{case_id}.protected_literals item")
            if literal not in original:
                raise ValidationError(f"{case_id} protected literal does not occur in input: {literal!r}")
        if len(literals) != len(set(literals)):
            raise ValidationError(f"{case_id}.protected_literals must not contain duplicates")
        if "output_mode" in case:
            output_mode = require_string(case["output_mode"], f"{case_id}.output_mode")
            if output_mode not in {"rewrite", "audit"}:
                raise ValidationError(f"{case_id}.output_mode must be rewrite or audit")
        indexed[case_id] = case
    return indexed


def check_outputs(record: object, corpus: object, skill_version: str) -> CheckReport:
    cases = index_corpus(corpus)
    record = require_object(record, "record", {"schema_version", "skill_version", "run", "outputs"})
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise ValidationError("record.schema_version must be 1")
    require_string(record["skill_version"], "record.skill_version")
    if record["skill_version"] != skill_version:
        raise ValidationError(
            f"record.skill_version {record['skill_version']!r} does not match SKILL.md {skill_version!r}"
        )
    run = require_object(record["run"], "run", {"date", "executor", "setup"})
    run_date = require_string(run["date"], "run.date")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", run_date):
        raise ValidationError("run.date must be YYYY-MM-DD")
    try:
        date.fromisoformat(run_date)
    except ValueError as exc:
        raise ValidationError("run.date must be a valid calendar date") from exc
    require_string(run["executor"], "run.executor")
    require_string(run["setup"], "run.setup")
    outputs = record["outputs"]
    if not isinstance(outputs, list) or not outputs:
        raise ValidationError("outputs must be a non-empty list")

    seen = set()
    editorial_review = dict.fromkeys(sorted(REVIEW_STATUSES), 0)
    reviewed_pass = 0
    literal_checks = 0
    missing_literals = {}
    for number, output in enumerate(outputs, 1):
        output = require_object(output, f"output #{number}", {"case_id", "output", "review"})
        case_id = require_string(output["case_id"], f"output #{number}.case_id")
        if case_id not in cases:
            raise ValidationError(f"unknown case id: {case_id}")
        if case_id in seen:
            raise ValidationError(f"duplicate output case id: {case_id}")
        seen.add(case_id)
        body = require_string(output["output"], f"{case_id}.output")
        review = require_object(output["review"], f"{case_id}.review", {"status", "notes"})
        status = require_string(review["status"], f"{case_id}.review.status")
        if status not in REVIEW_STATUSES:
            raise ValidationError(f"{case_id}.review.status must be pass, fail, or pending")
        require_string(review["notes"], f"{case_id}.review.notes")
        editorial_review[status] += 1
        literals = cases[case_id].get("protected_literals", [])
        literal_checks += len(literals)
        missing = [literal for literal in literals if literal not in body]
        if missing:
            missing_literals[case_id] = missing
        if status == "pass" and not missing:
            reviewed_pass += 1

    return CheckReport(
        total_cases=len(cases),
        submitted_cases=len(seen),
        reviewed_pass=reviewed_pass,
        editorial_review=editorial_review,
        literal_checks=literal_checks,
        missing_literals=missing_literals,
        unrun_case_ids=[case_id for case_id in cases if case_id not in seen],
    )


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot read JSON {path}: {exc}") from exc


def current_skill_version() -> str:
    try:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ValidationError(f"cannot read SKILL.md: {exc}") from exc
    frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, re.S)
    version = re.search(r"^  version: ([^\n]+)$", frontmatter[1], re.M) if frontmatter else None
    if not version:
        raise ValidationError("cannot find SKILL.md metadata.version")
    return version[1].strip().strip("\"'")


def format_report(report: CheckReport) -> str:
    coverage = "full" if not report.unrun_case_ids else "partial"
    lines = [
        f"Coverage: {report.submitted_cases}/{report.total_cases} cases ({coverage})",
        "Editorial review: " + ", ".join(f"{status}={report.editorial_review[status]}" for status in ("pass", "fail", "pending")),
        f"Protected literal checks: {report.literal_checks}; cases with missing literals: {len(report.missing_literals)}",
    ]
    for case_id, missing in report.missing_literals.items():
        lines.append(f"FAIL {case_id}: missing protected literals {missing!r}")
    lines.append(
        f"Reviewed cases {'PASS' if report.passed else 'NOT PASS'}: "
        f"{report.reviewed_pass}/{report.submitted_cases} have review pass and intact protected literals"
    )
    if report.unrun_case_ids:
        lines.append("Unrun cases: " + ", ".join(report.unrun_case_ids))
        lines.append("Partial coverage does not establish a full-corpus pass.")
    lines.append("Style, meaning, and output mode rely on the recorded editorial review; they are not automatically verified.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path, help="JSON record of actual outputs and editorial reviews")
    parser.add_argument("--corpus", type=Path, default=ROOT / "tests" / "forward_cases.json")
    args = parser.parse_args()
    try:
        version = current_skill_version()
        record = read_json(args.results)
        report = check_outputs(record, read_json(args.corpus), version)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Skill version: {version}; run date: {record['run']['date']}; executor: {record['run']['executor']}")
    print(format_report(report))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
