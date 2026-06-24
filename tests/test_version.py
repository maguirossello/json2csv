"""Tests for the project metadata."""

import re

from json2csv.version import BUILD, VERSION, __version__


def test_version_metadata() -> None:
    """The package exposes well-formed version metadata (build-number agnostic)."""
    assert re.fullmatch(r"\d+\.\d+\.\d+", __version__)
    assert re.fullmatch(r"\d{3}", BUILD)
    assert VERSION == f"1.0 build {BUILD}"
