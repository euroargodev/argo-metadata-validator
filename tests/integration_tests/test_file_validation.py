"""Test complete validation process for input files."""

import json
from pathlib import Path

import pytest

from argo_metadata_validator.models.results import ERROR, ValidationError
from argo_metadata_validator.validation import ArgoValidator

test_cases = [
    ["valid_sensor.json", []],
    ["valid_platform.json", []],
    ["valid_float.json", []],
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
    [
        "platform_invalid_vocabs.json",
        [
            ValidationError(
                message="Unknown NVS term: http://vocab.nerc.ac.uk/collection/R28/current/APF9/",
                path="PLATFORM.0.CONTROLLER_BOARD_TYPE_PRIMARY",
                level=ERROR,
            ),
            ValidationError(
                message="Unknown NVS term: http://vocab.nerc.ac.uk/collection/R28/current/USEA/",
                path="PLATFORM.0.CONTROLLER_BOARD_TYPE_SECONDARY",
                level=ERROR,
            ),
        ],
    ],
    [
        "sensor_deprecated_vocab.json",
        [
            ValidationError(
                message="Deprecated NVS term: http://vocab.nerc.ac.uk/collection/R03/current/NB_SAMPLE/",
                path="PARAMETERS.0.PARAMETER",
                level=ERROR,
            )
        ],
    ],
]


@pytest.mark.parametrize("file_path,expected_errors", test_cases)
def test_validating_files(file_path, expected_errors):
    """Test the overall validation with various files."""
    resolved_file_path = Path(__file__).parent.parent / "files" / file_path

    errors = ArgoValidator().validate([str(resolved_file_path)])

    assert errors == {file_path: expected_errors}


@pytest.mark.parametrize("file_path,expected_errors", test_cases)
def test_validating_json_dicts(file_path, expected_errors):
    """Test the overall validation with various files."""
    resolved_file_path: Path = Path(__file__).parent.parent / "files" / file_path
    data = json.loads(resolved_file_path.read_text())

    assert isinstance(data, dict)
    errors = ArgoValidator().validate([data])

    key = list(errors.keys())[0]
    assert errors[key] == expected_errors


def test_validating_non_existant_file():
    """Test correct exception raises when a non-existing file is passed in."""
    with pytest.raises(Exception) as exc_info:
        ArgoValidator().validate(["not_real.com"])

    assert str(exc_info.value) == "Provided JSON file could not be found: not_real.com"
