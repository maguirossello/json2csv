"""Tests for the command line interface."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from json2csv.cli import build_parser, main


def test_main_generates_csv_file(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI converts the source file and reports success."""
    source = tmp_path / "input.json"
    destination = tmp_path / "output.csv"
    source.write_text('[{"name": "Ada", "age": "32"}]', encoding="utf-8")

    result = main([str(source), "--output", str(destination)])

    assert result == 0
    assert list(csv.DictReader(destination.open(encoding="utf-8"))) == [
        {"name": "Ada", "age": "32"}
    ]
    assert "Generated" in capsys.readouterr().out


def test_main_returns_error_for_missing_source(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The CLI exits with a non-zero code for missing input files."""
    source = tmp_path / "missing.json"
    destination = tmp_path / "output.csv"

    result = main([str(source), "--output", str(destination)])

    assert result == 1
    assert "error" in capsys.readouterr().err.lower()


def test_build_parser_exposes_expected_options() -> None:
    """The parser accepts the documented flags."""
    parser = build_parser()
    args = parser.parse_args(
        ["in.json", "--output", "out.csv", "--sort-keys", "--json-lines"]
    )
    assert args.sort_keys is True
    assert args.json_lines is True
