"""Custom exceptions."""

from argo_metadata_validator.schema_utils import SCHEMA_TYPES


class InvalidSchemaTypeError(ValueError):
    """Exception thrown if a provided value doesn't match a known schema type."""

    def __init__(self, provided_type: str):
        """Construct a standard error message."""
        message = f"Unrecognised schema type {provided_type}. Valid options: {', '.join(SCHEMA_TYPES)}"
        super().__init__(message)
