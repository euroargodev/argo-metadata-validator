"""Utilities related to NVS/vocabularies."""

import requests

NVS_HOST = "http://vocab.nerc.ac.uk"

ALL_ARGO_VOCABS = [
    "L22",
    "R03",
    "R08",
    "R09",
    "R10",
    "R22",
    "R23",
    "R24",
    "R25",
    "R26",
    "R27",
    "R28",
]


def expand_vocab(context: dict, value: str):
    """Use context from the JSON to expand vocab terms to full URIs."""
    val = value
    for k in context:
        if k in val:
            val = val.replace(k, context[k])
            if val[-1] != "/":
                val += "/"
    return val


def get_all_terms_from_argo_vocabs() -> list[str]:
    """Fetches all active terms from all of the ARGO vocabularies.

    Returns:
        list[str]: List of terms as URIs.
    """
    term_list = []
    for vocab in ALL_ARGO_VOCABS:
        term_list += get_all_terms_from_vocab(vocab)
    return term_list


def get_all_terms_from_vocab(vocab: str):
    """SPARQL query to fetch all active terms from a given vocab.

    Args:
        vocab (str): Name of the vocab, e.g. R01.
    """
    query_url = f"{NVS_HOST}/sparql/sparql"
    sparql_query = f"""
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    SELECT DISTINCT (?c as ?uri)
    WHERE {{
        <{NVS_HOST}/collection/{vocab}/current/> skos:member ?c .
        ?c owl:deprecated ?isDeprecated .
        FILTER (?isDeprecated = "false")
    }}
    """

    resp = requests.post(
        query_url, data=sparql_query, headers={"Content-Type": "application/sparql-query"}, timeout=120
    )
    resp.raise_for_status()
    results = [x["uri"]["value"] for x in resp.json()["results"]["bindings"]]
    return results
