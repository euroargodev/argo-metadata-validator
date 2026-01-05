"""Utilities related to NVS/vocabularies."""

import re

import requests
from pydantic import BaseModel

NVS_HOST = "http://vocab.nerc.ac.uk"


class VocabTerms(BaseModel):
    """Model to hold fetched vocab terms from NVS."""

    collections: list[str]
    active: list[str]
    deprecated: list[str]


def expand_vocab(context: dict, value: str):
    """Use context from the JSON to expand vocab terms to full URIs."""
    val = value
    for k in context:
        if k in val:
            val = val.replace(k, context[k])
            if val[-1] != "/":
                val += "/"
    return val


def update_terms_from_context(terms: VocabTerms, context: dict):
    """Fetches terms for all vocabs found in the context object."""
    for k in context:
        re_search = re.search(r"SDN:(\w+)::", k)
        if re_search:
            vocab_name = re_search.groups()[0]
            if vocab_name not in terms.collections:
                vocab_terms = get_all_terms_from_vocab(vocab_name)
                terms.collections.append(vocab_name)
                terms.active += vocab_terms.active
                terms.deprecated += vocab_terms.deprecated


def get_all_terms_from_vocab(vocab: str) -> VocabTerms:
    """SPARQL query to fetch all active terms from a given vocab.

    Args:
        vocab (str): Name of the vocab, e.g. R01.
    """
    query_url = f"{NVS_HOST}/sparql/sparql"
    sparql_query = f"""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT (?c as ?uri) ?isDeprecated
    WHERE {{
        <{NVS_HOST}/collection/{vocab}/current/> skos:member ?c .
        ?c owl:deprecated ?isDeprecated
    }}
    """

    resp = requests.post(
        query_url, data=sparql_query, headers={"Content-Type": "application/sparql-query"}, timeout=120
    )
    resp.raise_for_status()
    results = VocabTerms(collections=[], active=[], deprecated=[])
    for x in resp.json()["results"]["bindings"]:
        if x["isDeprecated"]["value"] == "true":
            results.deprecated.append(x["uri"]["value"])
        else:
            results.active.append(x["uri"]["value"])
    return results
