"""Tests for util methods related to CLI entry point."""

import json
import re
from unittest.mock import call

import click
import pytest

from argo_metadata_validator.cli import output_to_json_string, output_to_terminal
from argo_metadata_validator.models.results import WARNING, ValidationError


@pytest.fixture
def sample_errors():
    """Example error response from validation call."""
    return {
        "file_1": [
            ValidationError(message="error 1", path="sensors"),
            ValidationError(message="error 2", path="parameters"),
            ValidationError(message="warning 1", path="vendorinfo", level=WARNING),
        ],
        "file_2": [],
    }


def test_output_to_terminal(mocker, sample_errors):
    """Test output_to_terminal method."""
    mock_echo = mocker.patch("argo_metadata_validator.cli.click.echo")

    output_to_terminal(sample_errors)

    assert mock_echo.call_count == 8
    assert mock_echo.mock_calls[0] == call(click.style("file_1 has 2 errors", fg="red"))
    assert mock_echo.mock_calls[1] == call(click.style("file_1 has 1 warnings", fg="yellow"))
    assert mock_echo.mock_calls[2] == call("-----")
    assert mock_echo.mock_calls[3] == call(click.style("error 1 at path sensors", fg="red"))
    assert mock_echo.mock_calls[4] == call(click.style("error 2 at path parameters", fg="red"))
    assert mock_echo.mock_calls[5] == call(click.style("warning 1 at path vendorinfo", fg="yellow"))
    assert mock_echo.mock_calls[6] == call(click.style("file_2 has no errors", fg="green"))
    assert mock_echo.mock_calls[7] == call("-----")


def test_output_json_string(sample_errors):
    """Test output_to_json_string method."""
    result = output_to_json_string(sample_errors)

    expected = json.dumps(
        {
            "file_1": {
                "is_valid": False,
                "errors": [
                    {"message": "error 1", "path": "sensors"},
                    {"message": "error 2", "path": "parameters"},
                ],
                "warnings": [{"message": "warning 1", "path": "vendorinfo"}],
            },
            "file_2": {
                "is_valid": True,
                "errors": [],
                "warnings": [],
            },
        }
    )

    # Remove whitespace to compare just JSON string content
    whitespace_regex = re.compile(r"\s+")
    assert whitespace_regex.sub("", result) == whitespace_regex.sub("", expected)
