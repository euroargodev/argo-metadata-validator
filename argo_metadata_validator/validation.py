"""Validation functionality for ARGO metadata."""

import re
from pathlib import Path
from typing import Any

from jsonschema.exceptions import ValidationError as JsonValidationError

from argo_metadata_validator.constants import FLOAT_SCHEMA, PLATFORM_SCHEMA, SENSOR_SCHEMA
from argo_metadata_validator.models.float import Float
from argo_metadata_validator.models.platform import Platform
from argo_metadata_validator.models.results import ValidationError
from argo_metadata_validator.models.sensor import Sensor
from argo_metadata_validator.schema_utils import get_json_validator, infer_schema_from_data, infer_version_from_data
from argo_metadata_validator.utils import load_json
from argo_metadata_validator.vocab_utils import VocabTerms, expand_vocab, get_all_terms_from_argo_vocabs


def _parse_json_error(error: JsonValidationError) -> ValidationError:
    return ValidationError(message=error.message, path=".".join([str(x) for x in error.path]))


class ArgoValidator:
    """Validator class for ARGO metadata."""

    all_json_data: dict[str, Any] = {}  # Keyed by the original filename
    validation_errors: dict[str, list[ValidationError]] = {}  # Keyed by the original filename
    argo_vocab_terms: VocabTerms

    def __init__(self):
        """Initialise by pre-loading the ARGO vocab terms."""
        self.argo_vocab_terms = get_all_terms_from_argo_vocabs()

    def load_json_data(self, json_obj: list[str | dict]):
        """Take a list of JSON files and load content into memory.

        Args:
            json_obj (list[str | dict]): List of file paths or JSON dictionaries
        """
        self.all_json_data = {}
        for item in json_obj:
            if isinstance(item, dict):
                # Load the JSON object into memory
                self.all_json_data.update({f"JSdict.{id(item)}": item})
            else:
                file = Path(item)
                if not file.exists():
                    raise Exception(f"Provided JSON file could not be found: {file}")

                # Load the JSON file into memory
                self.all_json_data[file.name] = load_json(Path(item))

    def validate(self, json_obj: list[str | dict]) -> dict[str, list[ValidationError]]:
        """Takes a list of JSON files or dictionaries and validates each.

        Args:
            json_obj (list[str|dict]): List of file paths or JSON dictionaries.

        Returns:
            dict[str, list[str]]: Errors, keyed by the input filename.
        """
        self.load_json_data(json_obj)

        self.validation_errors = {}
        for file, json_data in self.all_json_data.items():
            self.validation_errors[file] = self._validate_json(json_data)

            if not self.validation_errors[file]:
                self.validation_errors[file] += self._validate_vocabs(json_data)
        return self.validation_errors

    def parse(self, json_obj: str | dict) -> Sensor | Float | Platform:
        """Parses provided metadata into Pydantic models.

        Args:
            json_obj (str | dict): Path of an input JSON file or JSON data already in memory

        Returns:
            _type_: _description_
        """
        errors = self.validate([json_obj])
        if any(len(errors[e]) > 0 for e in errors):
            raise Exception("Data not valid, run the validation function for detailed errors.")

        key = f"JSdict.{id(json_obj)}" if isinstance(json_obj, dict) else Path(json_obj).name
        data = self.all_json_data[key]
        schema_type = infer_schema_from_data(data)
        if schema_type == SENSOR_SCHEMA:
            return Sensor(**data)
        if schema_type == FLOAT_SCHEMA:
            return Float(**data)
        if schema_type == PLATFORM_SCHEMA:
            return Platform(**data)
        raise Exception("Data does not match a defined Python model.")

    def _validate_json(self, json_data: Any) -> list[ValidationError]:
        """Apply JSON schema validation to given JSON data.

        Args:
            json_data (Any): JSON content to check.

        Returns:
            list[str]: List of errors.
        """
        schema_type = infer_schema_from_data(json_data)
        schema_version = infer_version_from_data(json_data)
        print(f"Validating against schema version {schema_version}")
        json_validator = get_json_validator(schema_type, version=schema_version)

        errors = []

        if not json_validator.is_valid(json_data):
            errors = [_parse_json_error(err) for err in json_validator.iter_errors(json_data)]
        return errors

    def _validate_vocabs(self, json_data: Any) -> list[ValidationError]:
        """Check validity of used vocab terms in JSON data.

        Args:
            json_data (Any): Input data to check.

        Returns:
            list[str]: List of errors.
        """
        validation_errors: list[ValidationError] = []
        if "SENSORS" in json_data:
            validation_errors += self.validate_vocab_terms(
                json_data, "SENSORS", ["SENSOR", "SENSOR_MAKER", "SENSOR_MODEL"]
            )
        if "PARAMETERS" in json_data:
            validation_errors += self.validate_vocab_terms(json_data, "PARAMETERS", ["PARAMETER", "PARAMETER_SENSOR"])
        if "PLATFORM" in json_data:
            validation_errors += self.validate_vocab_terms(
                json_data,
                "PLATFORM",
                [
                    "DATA_TYPE",
                    "POSITIONING_SYSTEM",
                    "TRANS_SYSTEM",
                    "PLATFORM_FAMILY",
                    "PLATFORM_TYPE",
                    "PLATFORM_MAKER",
                    "WMO_INST_TYPE",
                    "CONTROLLER_BOARD_TYPE_PRIMARY",
                    "CONTROLLER_BOARD_TYPE_SECONDARY",
                ],
            )
        return validation_errors

    def _is_term_found(self, uri: str, term_list: list[str]):
        if uri in term_list:
            return True
        if re.search(r"_\d+\/$", uri):
            # Check if this was a duplicate term (_N added to end)
            unduplicate_uri = re.sub(r"_\d+\/$", "/", uri)
            return unduplicate_uri in term_list
        else:
            # No _N at the end so can't be a duplicate term
            return False

    def _is_active_term(self, uri: str):
        return self._is_term_found(uri, self.argo_vocab_terms.active)

    def _is_deprecated_term(self, uri: str):
        return self._is_term_found(uri, self.argo_vocab_terms.deprecated)

    def validate_vocab_terms(self, json_data: Any, field: str, sub_fields: list[str]) -> list[ValidationError]:
        """Check that specific fields in the JSON match ARGO vocab terms.

        Args:
            json_data (Any): Input data to check.
            field (str): Top of level field in the JSON
            sub_fields (list[str]): Sub fields that are expected to contain vocab terms.

        Returns:
            list[str]: List of errors.
        """
        context = json_data["@context"]

        errors = []

        items = json_data[field]
        if type(items) is not list:
            items = [items]

        for idx, item in enumerate(items):
            for x in [field for field in sub_fields if field in item]:
                # Sometimes dealing with lists here. Making everything a list for simplicity
                values = item[x]
                if not isinstance(values, list):
                    values = [values]
                for val in values:
                    # Vocab terms can have optional text enclosed in square brackets
                    val = re.sub(r"\s+\[\w+\]", "", val)
                    val = expand_vocab(context, val)
                    if not self._is_active_term(val):
                        if self._is_deprecated_term(val):
                            error = ValidationError(message=f"Deprecated NSV term: {val}", path=f"{field}.{idx}.{x}")
                        else:
                            error = ValidationError(message=f"Unknown NSV term: {val}", path=f"{field}.{idx}.{x}")
                        errors.append(error)
        return errors
