"""Models related to validation results."""

from pydantic import BaseModel

ERROR = 1
WARNING = 0


class ValidationError(BaseModel):
    """Model to hold validation errors."""

    message: str
    path: str | None = None
    level: int
