"""Test complete validation process for input files when validated against a user-supplied schema."""

from pathlib import Path

import pytest

from argo_metadata_validator.models.results import ERROR, ValidationError
from argo_metadata_validator.validation import ArgoValidator

test_cases = [
    ["valid_sensor.json", []],
    [
        "invalid_sensor.json",
        [
            ValidationError(
                message="'SENSORS' is a required property",
                path="",
                level=ERROR,
            ),
            ValidationError(
                message="Additional properties are not allowed ('SENSORZ' was unexpected)",
                path="",
                level=ERROR,
            ),
        ],
    ],
]


@pytest.mark.parametrize("file_path,expected_errors", test_cases)
def test_validating_files_with_user_defined_schema(file_path, expected_errors):
    """Test that validation works as expected with a user-defined schema."""
    resolved_file_path = Path(__file__).parent.parent / "files" / "user_defined" / file_path
    resolved_schema_path = Path(__file__).parent.parent / "files" / "user_defined" / "schema" / "sensor.schema.json"

    errors = ArgoValidator().validate([str(resolved_file_path)], resolved_schema_path)

    assert errors == {file_path: expected_errors}
