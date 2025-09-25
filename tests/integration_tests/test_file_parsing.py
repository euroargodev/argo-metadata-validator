"""Integration tests for the file parsing function."""

from pathlib import Path

import pytest

from argo_metadata_validator.models.float import Float
from argo_metadata_validator.models.platform import Platform
from argo_metadata_validator.models.sensor import Sensor
from argo_metadata_validator.validation import ArgoValidator


@pytest.mark.parametrize(
    "file_path,output_class",
    [
        ["valid_sensor.json", Sensor],
        ["valid_platform.json", Platform],
        ["valid_float.json", Float],
    ],
)
def test_validating_files(file_path, output_class):
    """Test the overall validation with various files."""
    resolved_file_path = Path(__file__).parent.parent / "files" / file_path

    output = ArgoValidator().parse(str(resolved_file_path))

    assert isinstance(output, output_class)
