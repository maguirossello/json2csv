"""Increment the project build number across tracked metadata files."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "src" / "json2csv" / "version.py"
README_FILE = ROOT / "README.md"
CHANGELOG_FILE = ROOT / "CHANGELOG.md"
BUILD_PATTERN = re.compile(r'BUILD = "(\d{3})"')
README_PATTERN = re.compile(r"`1\.0 build (\d{3})`")
CHANGELOG_PATTERN = re.compile(r"## 1\.0 build (\d{3}) - ")


def next_build(current: str) -> str:
    """Return the next zero-padded build string."""
    return f"{int(current) + 1:03d}"


def replace_once(content: str, pattern: re.Pattern[str], replacement: str) -> str:
    """Replace a single occurrence and fail if it is missing."""
    updated, count = pattern.subn(replacement, content, count=1)
    if count != 1:
        msg = f"Pattern not found for replacement: {pattern.pattern}"
        raise ValueError(msg)
    return updated


def main() -> int:
    """Increment build metadata and prepend a changelog entry."""
    version_content = VERSION_FILE.read_text(encoding="utf-8")
    match = BUILD_PATTERN.search(version_content)
    if match is None:
        raise ValueError("Could not locate build number in version.py")

    new_build = next_build(match.group(1))
    VERSION_FILE.write_text(
        replace_once(version_content, BUILD_PATTERN, f'BUILD = "{new_build}"'),
        encoding="utf-8",
    )

    readme_content = README_FILE.read_text(encoding="utf-8")
    README_FILE.write_text(
        replace_once(readme_content, README_PATTERN, f"`1.0 build {new_build}`"),
        encoding="utf-8",
    )

    changelog_content = CHANGELOG_FILE.read_text(encoding="utf-8")
    today = datetime.now(UTC).date().isoformat()
    entry = (
        f"## 1.0 build {new_build} - {today}\n\n"
        "- Actualizacion automatica de build tras push exitoso.\n\n"
    )
    CHANGELOG_FILE.write_text(entry + changelog_content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
