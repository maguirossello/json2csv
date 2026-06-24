"""Core conversion services."""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any, Final, cast

from json2csv.exceptions import ConversionRuntimeError, InputValidationError
from json2csv.models import ConversionOptions, ConversionRequest

DEFAULT_NEWLINE: Final[str] = ""


class JsonToCsvConverter:
    """Convert JSON content into CSV representations."""

    def convert_text(
        self,
        json_text: str,
        options: ConversionOptions | None = None,
    ) -> str:
        """Convert JSON text content into a CSV string."""
        selected_options = options or ConversionOptions()
        self._validate_options(selected_options)
        records = self._parse_records(json_text, selected_options)
        return self._serialize_csv(records, selected_options)

    def convert_file(self, request: ConversionRequest) -> Path:
        """Convert a JSON file into a CSV file and return the destination path."""
        self._validate_options(request.options)

        try:
            json_text = request.source.read_text(
                encoding=request.options.input_encoding,
            )
        except FileNotFoundError as error:
            msg = f"Source file not found: {request.source}"
            raise ConversionRuntimeError(msg) from error
        except OSError as error:
            msg = f"Unable to read source file: {request.source}"
            raise ConversionRuntimeError(msg) from error

        records = self._parse_records(json_text, request.options)
        payload = self._serialize_csv(records, request.options)

        try:
            request.destination.parent.mkdir(parents=True, exist_ok=True)
            request.destination.write_text(
                payload,
                encoding=request.options.output_encoding,
                newline=DEFAULT_NEWLINE,
            )
        except OSError as error:
            msg = f"Unable to write destination file: {request.destination}"
            raise ConversionRuntimeError(msg) from error

        return request.destination

    def _parse_records(
        self,
        json_text: str,
        options: ConversionOptions,
    ) -> list[dict[str, Any]]:
        """Parse JSON text into a list of record dictionaries."""
        if options.json_lines:
            return self._parse_json_lines(json_text)

        try:
            data: Any = json.loads(json_text)
        except json.JSONDecodeError as error:
            msg = "Unable to parse JSON text."
            raise ConversionRuntimeError(msg) from error

        if isinstance(data, dict):
            return [self._ensure_object(data)]
        if isinstance(data, list):
            items = cast("list[object]", data)
            return [self._ensure_object(item) for item in items]

        msg = "The JSON top level must be an object or an array of objects."
        raise InputValidationError(msg)

    def _parse_json_lines(self, json_text: str) -> list[dict[str, Any]]:
        """Parse JSON Lines text (one JSON object per line)."""
        records: list[dict[str, Any]] = []
        for number, raw_line in enumerate(json_text.splitlines(), start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                item: Any = json.loads(line)
            except json.JSONDecodeError as error:
                msg = f"Unable to parse JSON on line {number}."
                raise ConversionRuntimeError(msg) from error
            records.append(self._ensure_object(item))
        return records

    def _ensure_object(self, item: Any) -> dict[str, Any]:
        """Ensure a parsed JSON item is an object (mapping)."""
        if not isinstance(item, dict):
            msg = "Each JSON record must be an object."
            raise InputValidationError(msg)
        return cast("dict[str, Any]", item)

    def _serialize_csv(
        self,
        records: list[dict[str, Any]],
        options: ConversionOptions,
    ) -> str:
        """Serialize record dictionaries into CSV text."""
        fieldnames = self._collect_fieldnames(records, options)
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=fieldnames,
            delimiter=options.delimiter,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for record in records:
            writer.writerow(
                {key: self._stringify(record.get(key), options) for key in fieldnames}
            )
        return buffer.getvalue()

    def _collect_fieldnames(
        self,
        records: list[dict[str, Any]],
        options: ConversionOptions,
    ) -> list[str]:
        """Collect the ordered union of keys across all records."""
        ordered: list[str] = []
        for record in records:
            for key in record:
                if key not in ordered:
                    ordered.append(key)
        if options.sort_keys:
            ordered.sort()
        return ordered

    def _stringify(self, value: Any, options: ConversionOptions) -> str:
        """Convert a JSON value into its CSV cell representation."""
        if value is None:
            return ""
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, dict | list):
            return json.dumps(
                value,
                ensure_ascii=options.ensure_ascii,
                sort_keys=options.sort_keys,
            )
        return str(value)

    def _validate_options(self, options: ConversionOptions) -> None:
        """Validate user-selected options and map errors to domain exceptions."""
        try:
            options.validate()
        except ValueError as error:
            raise InputValidationError(str(error)) from error
