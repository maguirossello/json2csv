"""Tests for the core conversion service."""

from __future__ import annotations

import csv
import io
import json
import string
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st
from hypothesis.strategies import DrawFn

from json2csv.core import JsonToCsvConverter
from json2csv.exceptions import ConversionRuntimeError, InputValidationError
from json2csv.models import ConversionOptions, ConversionRequest

SAFE_TEXT = string.ascii_letters + string.digits


def test_convert_text_returns_csv() -> None:
    """It converts a JSON array into CSV with a header row."""
    converter = JsonToCsvConverter()

    result = converter.convert_text(
        '[{"name": "Ada", "age": "32"}, {"name": "Grace", "age": "45"}]'
    )

    assert list(csv.DictReader(io.StringIO(result))) == [
        {"name": "Ada", "age": "32"},
        {"name": "Grace", "age": "45"},
    ]


def test_convert_text_single_object() -> None:
    """A top-level JSON object is treated as a single record."""
    converter = JsonToCsvConverter()

    result = converter.convert_text('{"name": "Ada", "age": "32"}')

    assert list(csv.DictReader(io.StringIO(result))) == [{"name": "Ada", "age": "32"}]


def test_convert_text_supports_json_lines() -> None:
    """It can read JSON Lines input."""
    converter = JsonToCsvConverter()
    options = ConversionOptions(json_lines=True)

    result = converter.convert_text(
        '{"name": "Ada", "age": "32"}\n{"name": "Grace", "age": "45"}\n', options
    )

    assert list(csv.DictReader(io.StringIO(result))) == [
        {"name": "Ada", "age": "32"},
        {"name": "Grace", "age": "45"},
    ]


def test_convert_text_unions_and_sorts_columns() -> None:
    """Missing keys are filled and columns can be sorted."""
    converter = JsonToCsvConverter()
    options = ConversionOptions(sort_keys=True)

    result = converter.convert_text('[{"b": "1"}, {"a": "2", "b": "3"}]', options)

    reader = csv.reader(io.StringIO(result))
    rows = list(reader)
    assert rows[0] == ["a", "b"]
    assert rows[1] == ["", "1"]
    assert rows[2] == ["2", "3"]


def test_convert_text_serializes_nested_and_special_values() -> None:
    """Nested structures, booleans and nulls are serialized to cells."""
    converter = JsonToCsvConverter()

    result = converter.convert_text('[{"a": {"x": 1}, "b": true, "c": null, "d": 7}]')

    row = next(csv.DictReader(io.StringIO(result)))
    assert row["a"] == '{"x": 1}'
    assert row["b"] == "true"
    assert row["c"] == ""
    assert row["d"] == "7"


def test_convert_text_rejects_invalid_delimiter() -> None:
    """It maps invalid options to a domain exception."""
    converter = JsonToCsvConverter()

    with pytest.raises(InputValidationError):
        converter.convert_text('[{"a": "1"}]', ConversionOptions(delimiter="::"))


def test_convert_text_rejects_malformed_json() -> None:
    """Malformed JSON raises a runtime conversion error."""
    converter = JsonToCsvConverter()

    with pytest.raises(ConversionRuntimeError):
        converter.convert_text("this is not json")


def test_convert_text_rejects_non_object_records() -> None:
    """A JSON array of non-objects is rejected."""
    converter = JsonToCsvConverter()

    with pytest.raises(InputValidationError):
        converter.convert_text("[1, 2, 3]")


def test_convert_text_rejects_scalar_top_level() -> None:
    """A scalar JSON top level is rejected."""
    converter = JsonToCsvConverter()

    with pytest.raises(InputValidationError):
        converter.convert_text("42")


def test_json_lines_rejects_malformed_line() -> None:
    """A malformed JSON Lines row raises a runtime error."""
    converter = JsonToCsvConverter()

    with pytest.raises(ConversionRuntimeError):
        converter.convert_text(
            '{"a": "1"}\nnot-json\n', ConversionOptions(json_lines=True)
        )


def test_convert_file_writes_output(tmp_path: Path) -> None:
    """It writes the converted CSV to the destination file."""
    source = tmp_path / "input.json"
    destination = tmp_path / "nested" / "output.csv"
    source.write_text('[{"name": "Ada", "age": "32"}]', encoding="utf-8")
    converter = JsonToCsvConverter()

    result = converter.convert_file(
        ConversionRequest(
            source=source, destination=destination, options=ConversionOptions()
        )
    )

    assert result == destination
    assert list(csv.DictReader(destination.open(encoding="utf-8"))) == [
        {"name": "Ada", "age": "32"}
    ]


def test_convert_file_raises_when_source_is_missing(tmp_path: Path) -> None:
    """It raises a domain exception if the source file is missing."""
    converter = JsonToCsvConverter()

    with pytest.raises(ConversionRuntimeError):
        converter.convert_file(
            ConversionRequest(
                source=tmp_path / "missing.json",
                destination=tmp_path / "output.csv",
                options=ConversionOptions(),
            )
        )


@st.composite
def json_records(draw: DrawFn) -> tuple[list[str], list[dict[str, str]]]:
    """Generate JSON-compatible records with shared headers."""
    headers = draw(
        st.lists(
            st.text(alphabet=SAFE_TEXT, min_size=1, max_size=5),
            min_size=1,
            max_size=4,
            unique=True,
        )
    )
    value_strategy = st.text(alphabet=SAFE_TEXT, min_size=0, max_size=8)
    rows = draw(
        st.lists(
            st.fixed_dictionaries({header: value_strategy for header in headers}),
            min_size=1,
            max_size=5,
        )
    )
    return headers, rows


@given(json_records())
def test_convert_text_roundtrips(
    data: tuple[list[str], list[dict[str, str]]],
) -> None:
    """JSON records survive a round trip through CSV (property-based)."""
    _, rows = data
    converter = JsonToCsvConverter()

    csv_text = converter.convert_text(json.dumps(rows))

    assert list(csv.DictReader(io.StringIO(csv_text))) == rows
