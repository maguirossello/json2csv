"""Command line interface for json2csv."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from json2csv.core import JsonToCsvConverter
from json2csv.exceptions import Json2CsvError
from json2csv.models import ConversionOptions, ConversionRequest
from json2csv.version import VERSION


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(description="Convert JSON files to CSV.")
    parser.add_argument("source", type=Path, help="Path to the source JSON file.")
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path to the destination CSV file.",
    )
    parser.add_argument(
        "--delimiter",
        default=",",
        help="Single-character CSV delimiter.",
    )
    parser.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort the CSV columns alphabetically.",
    )
    parser.add_argument(
        "--json-lines",
        action="store_true",
        help="Read one JSON object per line instead of a JSON array.",
    )
    parser.add_argument(
        "--ensure-ascii",
        action="store_true",
        help="Escape non-ASCII characters when serializing nested values.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    options = ConversionOptions(
        delimiter=args.delimiter,
        sort_keys=args.sort_keys,
        json_lines=args.json_lines,
        ensure_ascii=args.ensure_ascii,
    )

    try:
        request = ConversionRequest(
            source=args.source,
            destination=args.output,
            options=options,
        )
        converter = JsonToCsvConverter()
        output_path = converter.convert_file(request)
    except Json2CsvError as error:
        sys.stderr.write(f"json2csv: error: {error}\n")
        return 1

    sys.stdout.write(f"Generated {output_path}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
