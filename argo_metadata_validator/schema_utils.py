"""Utilities related to the schema validation."""

from pathlib import Path

import jsonschema.validators
from jsonschema.protocols import Validator
from referencing import Registry, Resource

import argo_metadata_validator
from argo_metadata_validator.constants import (
    DEFAULT_SCHEMA_VERSION,
    FLOAT_SCHEMA,
    PLATFORM_SCHEMA,
    SCHEMA_TYPES,
    SENSOR_SCHEMA,
)
from argo_metadata_validator.exceptions import InvalidSchemaTypeError
from argo_metadata_validator.utils import load_json


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
        raise InvalidSchemaTypeError(schema_type)
    schema_dir = _get_schema_dir(version)
    return schema_dir / f"argo.{schema_type}.schema.json"


def _retrieve_from_filesystem(uri: str):
    schema_dir = _get_schema_dir()
    file = Path(uri).name
    path = schema_dir / file
    return Resource.from_contents(load_json(path))


def _get_registry():
    return Registry(retrieve=_retrieve_from_filesystem)


def infer_schema_from_data(data: dict) -> str:
    """Determines which schema type should be applied to the provided data."""
    if "float_info" in data:
        return FLOAT_SCHEMA
    if "platform_info" in data:
        return PLATFORM_SCHEMA
    if "sensor_info" in data:
        return SENSOR_SCHEMA
    raise ValueError("Unable to determine matching schema type from data")


def infer_version_from_data(data: dict) -> str:
    """Gets the format version by looking into the data file."""
    try:
        if "float_info" in data:
            return data["float_info"]["format_version"]
        if "platform_info" in data:
            return data["platform_info"]["format_version"]
        if "sensor_info" in data:
            return data["sensor_info"]["format_version"]
    except KeyError:
        return DEFAULT_SCHEMA_VERSION
    return DEFAULT_SCHEMA_VERSION


def get_json_validator(schema_type: str, version: str = DEFAULT_SCHEMA_VERSION) -> Validator:
    """Returns a jsonschema Validator for the given schema version.

    Args:
        schema_type (str): Which schema type, e.g. float, sensor.
        version (str, optional): Schema version, defaults to DEFAULT_SCHEMA_VERSION.

    Returns:
        Validator: validator with the appropriate schema loaded in.
    """
    schema_file = _get_schema_file(schema_type, version)
    schema = load_json(schema_file)
    registry = _get_registry()

    validator_cls = jsonschema.validators.validator_for(schema)
    validator: Validator = validator_cls(schema, registry=registry)
    return validator
