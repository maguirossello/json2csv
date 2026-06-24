"""Tests for the project metadata."""

from json2csv.version import BUILD, VERSION, __version__


def test_version_metadata() -> None:
    """The package exposes well-formed version metadata."""
    assert __version__ == "1.0.0"
    assert BUILD == "000"
    assert VERSION == "1.0 build 000"
