"""Tests for the schema utils."""

from pathlib import Path

import pytest

from argo_metadata_validator.schema_utils import (
    DEFAULT_SCHEMA_VERSION,
    _get_registry,
    _get_schema_dir,
    _get_schema_file,
    _retrieve_from_filesystem,
    infer_schema_from_data,
)


def test_get_schema_dir_default_version(mocker):
    """Test _get_schema_dir using the default version."""
    mocker.patch("argo_metadata_validator.schema_utils.argo_metadata_validator.__file__", "")

    r = _get_schema_dir()

    assert r.as_posix() == f"schema/{DEFAULT_SCHEMA_VERSION}"


def test_get_schema_dir(mocker):
    """Test _get_schema_dir with a provided version number."""
    mocker.patch("argo_metadata_validator.schema_utils.argo_metadata_validator.__file__", "")

    r = _get_schema_dir("9.9.9")

    assert r.as_posix() == "schema/9.9.9"


def test_get_schema_file(mocker):
    """Test _get_schema_file with a valid type."""
    mocker.patch("argo_metadata_validator.schema_utils._get_schema_dir", return_value=Path("schema_dir"))

    result = _get_schema_file("sensor")

    assert result.as_posix() == "schema_dir/argo.sensor.schema.json"


def test_get_schema_file_bad_type():
    """Test _get_schema_file with an invalid type."""
    with pytest.raises(ValueError) as exc_info:
        _get_schema_file("not-sensor")

    assert str(exc_info.value).startswith("Unrecognised schema type not-sensor.")


def test_retrieve_from_filesystem(mocker):
    """Test that _retrieve_from_filesystem calls the right methods and returns correct content."""
    mocker.patch("argo_metadata_validator.schema_utils._get_schema_dir", return_value=Path("schema_dir"))
    mock_load = mocker.patch("argo_metadata_validator.schema_utils.load_json", return_value={})
    mock_resource_from_contents = mocker.patch("argo_metadata_validator.schema_utils.Resource.from_contents")

    result = _retrieve_from_filesystem("./argo.sensor.schema.json")

    mock_load.assert_called_once_with(Path("schema_dir/argo.sensor.schema.json"))
    mock_resource_from_contents.assert_called_once_with({})
    assert result == mock_resource_from_contents.return_value


def test_get_registry(mocker):
    """Simple test that _get_registry calls the right method."""
    mock_registry = mocker.patch("argo_metadata_validator.schema_utils.Registry")

    result = _get_registry()

    mock_registry.assert_called_once()
    assert result == mock_registry.return_value


@pytest.mark.parametrize(
    "input_data,expected_output",
    [
        [{"sensor_info": 1}, "sensor"],
        [{"platform_info": 1}, "platform"],
        [{"float_info": 1}, "float"],
        [{"sensor_info": 1, "platform_info": 2, "float_info": 3}, "sensor"],
    ]
)
def test_infer_schema_from_data(input_data, expected_output):
    """Tests infer_schema_from_data with various inputs."""
    assert infer_schema_from_data(input_data) == expected_output

def test_infer_schema_from_data_no_match():
    """Tests infer_schema_from_data where the input doesn't match - exception is thrown."""
    with pytest.raises(ValueError) as exc_info:
        infer_schema_from_data({})

    assert str(exc_info.value) == "Unable to determine matching schema type from data"
