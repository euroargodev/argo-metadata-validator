"""Tests for the vocab utils."""

import pytest
import requests_mock

from argo_metadata_validator.vocab_utils import (
    NVS_HOST,
    VocabTerms,
    expand_vocab,
    get_all_terms_from_vocab,
    update_terms_from_context,
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


def test_update_terms_from_context(mocker):
    """Test that update_terms_from_context correctly fetches terms for a vocab in the context."""
    vocab_terms = VocabTerms(collections=[], active=[], deprecated=[])
    mock_get_terms = mocker.patch(
        "argo_metadata_validator.vocab_utils.get_all_terms_from_vocab",
        return_value=VocabTerms(collections=[], active=[""], deprecated=[""]),
    )

    assert len(vocab_terms.active) == 0
    assert len(vocab_terms.deprecated) == 0

    update_terms_from_context(
        vocab_terms,
        {
            "SDN:A01::": "url",
        },
    )

    mock_get_terms.assert_called_once_with("A01")
    assert len(vocab_terms.active) == 1
    assert len(vocab_terms.deprecated) == 1


def test_update_terms_from_context_already_stored(mocker):
    """Test that update_terms_from_context doesn't recache terms for a vocab it has already."""
    vocab_terms = VocabTerms(collections=["A01"], active=[], deprecated=[])
    mock_get_terms = mocker.patch("argo_metadata_validator.vocab_utils.get_all_terms_from_vocab")

    update_terms_from_context(
        vocab_terms,
        {
            "SDN:A01::": "url",
        },
    )

    mock_get_terms.assert_not_called()


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
