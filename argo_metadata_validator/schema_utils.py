"""Utilities related to the schema validation."""

from pathlib import Path

import jsonschema.validators
from jsonschema.protocols import Validator
from referencing import Registry, Resource

import argo_metadata_validator
from argo_metadata_validator.utils import load_json

DEFAULT_SCHEMA_VERSION = "0.4.0"
SCHEMA_TYPES = [
    "float",
    "MRV",
    "platform",
    "RBR",
    "SBE",
    "sensor",
    "TRIOS",
    "vendors",
]


def _get_schema_dir(version: str = DEFAULT_SCHEMA_VERSION) -> Path:
    """Get path to the directory containing schema definitions.

    Args:
        version (str, optional): Schema version, defaults to DEFAULT_SCHEMA_VERSION.

    Returns:
        Path: Schema directory path.
    """
    return Path(argo_metadata_validator.__file__).parent / "schema" / version


def _get_schema_file(schema_type: str, version: str = DEFAULT_SCHEMA_VERSION) -> Path:
    """Gets the schema definition for a given type and version.

    Args:
        schema_type (str): Which schema type, e.g. float, sensor.
        version (str, optional): Schema version, defaults to DEFAULT_SCHEMA_VERSION.

    Raises:
        ValueError: Raised if an invalid schema_type is passed in.

    Returns:
        Path: path to the schema file.
    """
    if schema_type not in SCHEMA_TYPES:
        raise ValueError(f"Unrecognised schema type {schema_type}. Valid options: {', '.join(SCHEMA_TYPES)}")
    schema_dir = _get_schema_dir(version)
    return schema_dir / f"argo.{schema_type}.schema.json"


def _retrieve_from_filesystem(uri: str):
    schema_dir = _get_schema_dir()
    file = Path(uri).name
    path = schema_dir / file
    return Resource.from_contents(load_json(path))


def _get_registry():
    return Registry(retrieve=_retrieve_from_filesystem)


def get_json_validator(version: str = DEFAULT_SCHEMA_VERSION) -> Validator:
    """Returns a jsonschema Validator for the given schema version.

    Args:
        version (str, optional): Schema version, defaults to DEFAULT_SCHEMA_VERSION.

    Returns:
        Validator: validator with the appropriate schema loaded in.
    """
    schema_file = _get_schema_file("sensor")
    schema = load_json(schema_file)
    registry = _get_registry()

    validator_cls = jsonschema.validators.validator_for(schema)
    validator: Validator = validator_cls(schema, registry=registry)
    return validator
