"""Test for validation methods."""

import pytest

from argo_metadata_validator.validation import ArgoValidator


def test_model_parsing_invalid_data(mocker):
    """Test the validator's parse method mocking the case where the data is invalid."""
    validator = ArgoValidator()
    mocker.patch.object(validator, "validate", return_value={"123.json": ["hi"]})

    with pytest.raises(Exception) as exc_info:
        validator.parse("123.json")

    assert str(exc_info.value) == "Data not valid, run the validation function for detailed errors."


def test_model_parsing_invalid_type(mocker):
    """Test correct error is thrown if parse method gets an unknown schema type."""
    validator = ArgoValidator()
    mocker.patch.object(validator, "validate", return_value={"123.json": []})
    mocker.patch.object(validator, "all_json_data", return_value={"123.json": []})
    mocker.patch("argo_metadata_validator.validation.infer_schema_from_data", return_value="unknown")

    with pytest.raises(Exception) as exc_info:
        validator.parse("123.json")

    assert str(exc_info.value) == "Data does not match a defined Python model."
