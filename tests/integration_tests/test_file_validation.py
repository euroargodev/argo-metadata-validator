"""Test complete validation process for input files."""

from pathlib import Path

import pytest

from argo_metadata_validator.models.results import ValidationError
from argo_metadata_validator.validation import ArgoValidator


@pytest.mark.parametrize(
    "file_path,expected_output",
    [
        ["valid_sensor.json", {"valid_sensor.json": []}],
        ["valid_platform.json", {"valid_platform.json": []}],
        ["valid_float.json", {"valid_float.json": []}],
        [
            "platform_invalid_vocabs.json",
            {
                "platform_invalid_vocabs.json": [
                    ValidationError(
                        message="Unknown NSV term: http://vocab.nerc.ac.uk/collection/R28/current/APF9/",
                        path="PLATFORM.0.CONTROLLER_BOARD_TYPE_PRIMARY",
                    ),
                    ValidationError(
                        message="Unknown NSV term: http://vocab.nerc.ac.uk/collection/R28/current/USEA/",
                        path="PLATFORM.0.CONTROLLER_BOARD_TYPE_SECONDARY",
                    ),
                ]
            },
        ],
    ],
)
def test_validating_files(file_path, expected_output):
    """Test the overall validation with various files."""
    resolved_file_path = Path(__file__).parent / "files" / file_path

    errors = ArgoValidator().validate([str(resolved_file_path)])

    assert errors == expected_output
