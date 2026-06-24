"""Create a zip archive of the project, ready to upload to GitHub."""

from __future__ import annotations

import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "json2csv_project.zip"
SKIP_DIRS = {
    ".git", ".venv", ".venv312", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".hypothesis", "docs/site", "build", "dist",
}


def main() -> int:
    """Package the project tree into a single zip archive."""
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT)
            if any(part in SKIP_DIRS for part in relative.parts):
                continue
            if relative.name == ARCHIVE.name:
                continue
            bundle.write(path, relative)
    print(f"Created {ARCHIVE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
