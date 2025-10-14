"""Tests for the vocab utils."""

import pytest
import requests_mock

from argo_metadata_validator.vocab_utils import (
    ALL_ARGO_VOCABS,
    NVS_HOST,
    VocabTerms,
    expand_vocab,
    get_all_terms_from_argo_vocabs,
    get_all_terms_from_vocab,
)


@pytest.mark.parametrize(
    "input_val,expected_result",
    [
        ["SDN:R03::test", "http://vocab.nerc.ac.uk/collection/R03/current/test/"],
        ["SDN:R99::test", "SDN:R99::test"],
    ],
)
def test_expand_vocab(input_val, expected_result):
    """Test expand_vocab with different inputs."""
    context = {
        "SDN:R03::": "http://vocab.nerc.ac.uk/collection/R03/current/",
        "SDN:R08::": "http://vocab.nerc.ac.uk/collection/R08/current/",
        "SDN:R09::": "http://vocab.nerc.ac.uk/collection/R09/current/",
    }

    result = expand_vocab(context, input_val)

    assert result == expected_result


def test_get_all_terms_from_argo_vocabs(mocker):
    """Test for get_all_terms_from_argo_vocabs calling mocked version of sub-method."""
    mock_get = mocker.patch(
        "argo_metadata_validator.vocab_utils.get_all_terms_from_vocab",
        return_value=VocabTerms(active=["1"], deprecated=[])
    )

    result = get_all_terms_from_argo_vocabs()

    # Check the per-vocab call happens the right number of times
    assert mock_get.call_count == len(ALL_ARGO_VOCABS)
    # Check that result is correctly a list of strings
    assert isinstance(result.active, list)
    assert all(isinstance(x, str) for x in result.active)


def test_get_all_terms_from_vocab():
    """Simple unit test for get_all_terms_from_vocab, mocking the HTTP call."""
    example_response = {
        "results": {
            "bindings": [
                {"uri": {"value": "http://vocab/hi"}, "isDeprecated": {"value": "false"}},
                {"uri": {"value": "http://vocab/bye"}, "isDeprecated": {"value": "true"}},
            ]
        }
    }

    with requests_mock.Mocker() as mock_req:
        mock_req.post(f"{NVS_HOST}/sparql/sparql", json=example_response)
        result = get_all_terms_from_vocab("R01")

    assert result.active == ["http://vocab/hi"]
    assert result.deprecated == ["http://vocab/bye"]
