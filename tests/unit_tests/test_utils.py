"""Tests for utils."""

from argo_metadata_validator.utils import load_json


def test_load_json(mocker):
    """Simple test of load_json with a mock object."""
    mock_path = mocker.Mock()
    mock_path.read_text.return_value = '{"hi": 123}'

    r = load_json(mock_path)

    assert r == {"hi": 123}
