"""Data structures used by the converter."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ConversionOptions:
    """Immutable options for JSON-to-CSV conversion."""

    delimiter: str = ","
    sort_keys: bool = False
    json_lines: bool = False
    ensure_ascii: bool = False
    input_encoding: str = "utf-8"
    output_encoding: str = "utf-8"

    def validate(self) -> None:
        """Validate the conversion options."""
        if len(self.delimiter) != 1:
            msg = "The delimiter must be a single character."
            raise ValueError(msg)


@dataclass(slots=True, frozen=True)
class ConversionRequest:
    """Represent a file-based conversion request."""

    source: Path
    destination: Path
    options: ConversionOptions
