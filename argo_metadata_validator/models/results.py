"""Models related to validation results."""

from pydantic import BaseModel


class ValidationError(BaseModel):
    """Model to hold validation errors."""

    message: str
    path: str | None = None
