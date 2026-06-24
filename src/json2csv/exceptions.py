"""Project-specific exceptions."""


class Json2CsvError(Exception):
    """Base exception for the package."""


class InputValidationError(Json2CsvError):
    """Raised when the input data or options are invalid."""


class ConversionRuntimeError(Json2CsvError):
    """Raised when a conversion cannot be completed."""
