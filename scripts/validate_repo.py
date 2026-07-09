#!/usr/bin/env python3
"""Run deterministic maintenance checks for this skill repo."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - depends on local Python environment
    print("ERROR: PyYAML is required to validate YAML files", file=sys.stderr)
    raise SystemExit(1)


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "SKILL.md"
README_PATH = ROOT / "README.md"
CHANGELOG_PATH = ROOT / "CHANGELOG.md"
OPENAI_YAML_PATH = ROOT / "agents" / "openai.yaml"
LICENSE_PATH = ROOT / "LICENSE"
GITHUB_WORKFLOW_PATH = ROOT / ".github" / "workflows" / "validate.yml"
FORWARD_CASES_VALIDATOR = ROOT / "scripts" / "validate_forward_cases.py"
EXPECTED_PATTERN_COUNT = 33
EXPECTED_UPSTREAM_VERSION = "2.8.2"
MAX_SKILL_LINES = 500
MIN_PATTERN_BODY_CHARS = 100
ALLOWED_SKILL_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata"}
REQUIRED_SKILL_HEADINGS = [
    "## 任務原則",
    "## Voice matching",
    "### 事實與 SEO 保護",
    "### 不要硬改的內容",
    "## False positives：不要誤殺真人文字",
    "## 真人寫作訊號：看到要保留",
    "## 處理流程",
    "## 輸出格式",
    "## 完整範例",
    "## 來源",
]
EXPECTED_LICENSE_NOTICES = [
    "Copyright (c) 2025 Siqi Chen",
    "Copyright (c) 2026 歸藏",
    "Copyright (c) 2026 SlivenRed",
    "Copyright (c) 2026 humanizer-zh-TW-Pro contributors",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing required file: {path.relative_to(ROOT)}")


def load_skill_frontmatter() -> dict:
    text = read_text(SKILL_PATH)
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail("SKILL.md must start with YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        fail("SKILL.md frontmatter must be a YAML object")
    return data


def extract_skill_patterns() -> list[tuple[int, str]]:
    text = read_text(SKILL_PATH)
    matches = re.findall(r"^### ([0-9]+)\. (.+)$", text, re.M)
    return [(int(number), name.strip()) for number, name in matches]


def extract_skill_pattern_sections() -> list[tuple[int, str, str]]:
    text = read_text(SKILL_PATH)
    headings = list(re.finditer(r"^### ([0-9]+)\. ([^\n]+)$", text, re.M))
    final_boundary = text.find("\n## False positives：不要誤殺真人文字")
    if final_boundary < 0:
        fail("SKILL.md must contain the false-positive section after the pattern list")

    sections = []
    for index, heading in enumerate(headings):
        body_end = headings[index + 1].start() if index + 1 < len(headings) else final_boundary
        body = text[heading.end() : body_end].strip()
        sections.append((int(heading.group(1)), heading.group(2).strip(), body))
    return sections


def extract_readme_patterns() -> list[tuple[int, str]]:
    text = read_text(README_PATH)
    matches = re.findall(r"^\|\s*([0-9]+)\s*\|\s*(.*?)\s*\|$", text, re.M)
    return [(int(number), name.strip()) for number, name in matches]


def latest_readme_version() -> str:
    text = read_text(README_PATH)
    match = re.search(r"## 版本紀錄\n\n### ([^\n]+)", text)
    if not match:
        fail("README.md must contain a latest version under ## 版本紀錄")
    return match.group(1).strip()


def latest_changelog_version() -> str:
    text = read_text(CHANGELOG_PATH)
    match = re.search(r"^## \[([^\]]+)\](?: - .+)?$", text, re.M)
    if not match:
        fail("CHANGELOG.md must contain a release heading such as ## [1.0.0-pro.5] - YYYY-MM-DD")
    return match.group(1).strip()


def validate_skill_frontmatter(frontmatter: dict) -> str:
    unexpected_keys = set(frontmatter) - ALLOWED_SKILL_FRONTMATTER_KEYS
    if unexpected_keys:
        fail(f"SKILL.md frontmatter has unexpected keys: {sorted(unexpected_keys)}")
    if frontmatter.get("name") != "humanizer-zh-tw-pro":
        fail("SKILL.md frontmatter name must be humanizer-zh-tw-pro")
    name = frontmatter["name"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        fail("SKILL.md frontmatter name must be valid hyphen-case with at most 64 characters")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip():
        fail("SKILL.md frontmatter description must be non-empty")
    if len(description.strip()) > 1024 or "<" in description or ">" in description:
        fail("SKILL.md description must follow the official length and character limits")
    if frontmatter.get("license") != "MIT":
        fail("SKILL.md frontmatter license must be MIT")
    allowed_tools = frontmatter.get("allowed-tools")
    if not isinstance(allowed_tools, list) or not all(isinstance(tool, str) for tool in allowed_tools):
        fail("SKILL.md allowed-tools must be a list of strings")
    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        fail("SKILL.md frontmatter metadata must be an object")
    version = metadata.get("version")
    if not isinstance(version, str) or not version.strip():
        fail("SKILL.md metadata.version must be non-empty")
    return version


def validate_skill_size() -> None:
    lines = len(read_text(SKILL_PATH).splitlines())
    if lines > MAX_SKILL_LINES:
        fail(f"SKILL.md has {lines} lines; split references before exceeding {MAX_SKILL_LINES}")


def validate_upstream_attribution(frontmatter: dict) -> None:
    metadata = frontmatter.get("metadata", {})
    needle = f"blader/humanizer v{EXPECTED_UPSTREAM_VERSION}"
    if needle not in str(metadata.get("source", "")):
        fail(f"SKILL.md metadata.source must mention {needle}")
    readme_pattern = rf"blader/humanizer.*?v{re.escape(EXPECTED_UPSTREAM_VERSION)}"
    if not re.search(readme_pattern, read_text(README_PATH)):
        fail(f"README.md must mention {needle}")


def validate_patterns() -> None:
    skill_patterns = extract_skill_patterns()
    skill_sections = extract_skill_pattern_sections()
    readme_patterns = extract_readme_patterns()
    expected_numbers = list(range(1, EXPECTED_PATTERN_COUNT + 1))

    if [number for number, _ in skill_patterns] != expected_numbers:
        fail("SKILL.md pattern headings must be numbered 1 through 33")
    if [number for number, _ in readme_patterns] != expected_numbers:
        fail("README.md pattern table must be numbered 1 through 33")
    if skill_patterns != readme_patterns:
        fail("README.md pattern table must match SKILL.md pattern names exactly")

    for number, _, body in skill_sections:
        if len(body) < MIN_PATTERN_BODY_CHARS:
            fail(f"SKILL.md pattern {number} body is unexpectedly short")
        if "**警訊" not in body and "**高風險詞" not in body:
            fail(f"SKILL.md pattern {number} must describe its warning signs")
        if number != 23 and ("**前：**" not in body or "**後：**" not in body):
            fail(f"SKILL.md pattern {number} must keep its before/after example")

    skill_text = read_text(SKILL_PATH)
    for heading in REQUIRED_SKILL_HEADINGS:
        if heading not in skill_text:
            fail(f"SKILL.md is missing core heading: {heading}")


def validate_openai_yaml() -> None:
    data = yaml.safe_load(read_text(OPENAI_YAML_PATH))
    if not isinstance(data, dict):
        fail("agents/openai.yaml must be a YAML object")
    interface = data.get("interface")
    if not isinstance(interface, dict):
        fail("agents/openai.yaml must contain interface")
    default_prompt = interface.get("default_prompt")
    if not isinstance(default_prompt, str) or "$humanizer-zh-tw-pro" not in default_prompt:
        fail("agents/openai.yaml interface.default_prompt must mention $humanizer-zh-tw-pro")
    short_description = interface.get("short_description")
    if not isinstance(short_description, str) or not 25 <= len(short_description) <= 64:
        fail("agents/openai.yaml interface.short_description must be 25-64 characters")


def validate_license() -> None:
    text = read_text(LICENSE_PATH)
    for notice in EXPECTED_LICENSE_NOTICES:
        if notice not in text:
            fail(f"LICENSE is missing notice: {notice}")


def validate_github_workflow() -> None:
    data = yaml.safe_load(read_text(GITHUB_WORKFLOW_PATH))
    if not isinstance(data, dict):
        fail(".github/workflows/validate.yml must be a YAML object")
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not isinstance(jobs.get("validate"), dict):
        fail(".github/workflows/validate.yml must define the validate job")
    steps = jobs["validate"].get("steps")
    if not isinstance(steps, list) or not all(isinstance(step, dict) for step in steps):
        fail(".github/workflows/validate.yml validate job must contain structured steps")

    uses = {step.get("uses") for step in steps}
    runs = {str(step.get("run", "")).strip() for step in steps}
    for action in ("actions/checkout@v4", "actions/setup-python@v5"):
        if action not in uses:
            fail(f".github/workflows/validate.yml must use {action}")
    if "python scripts/validate_repo.py" not in runs:
        fail(".github/workflows/validate.yml must execute python scripts/validate_repo.py")


def validate_forward_cases() -> None:
    result = subprocess.run(
        [sys.executable, str(FORWARD_CASES_VALIDATOR)],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        fail("forward-test corpus validation failed")


def main() -> None:
    frontmatter = load_skill_frontmatter()
    skill_version = validate_skill_frontmatter(frontmatter)
    if latest_readme_version() != skill_version:
        fail("README.md latest version must match SKILL.md metadata.version")
    if latest_changelog_version() != skill_version:
        fail("CHANGELOG.md latest release must match SKILL.md metadata.version")

    validate_skill_size()
    validate_upstream_attribution(frontmatter)
    validate_patterns()
    validate_openai_yaml()
    validate_license()
    validate_github_workflow()
    validate_forward_cases()

    print("Repo validation valid: SKILL/README/CHANGELOG/upstream/agent metadata/corpus/CI are consistent")


if __name__ == "__main__":
    main()
