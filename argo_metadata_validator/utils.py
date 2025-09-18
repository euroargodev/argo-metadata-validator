"""General utilities."""

import json
from pathlib import Path
from typing import Any


def load_json(file: Path) -> Any:
    """Load content from a JSON file.

    Args:
        file (Path): Path to the file.

    Returns:
        Any: Loaded JSON content.
    """
    return json.loads(file.read_text())
