"""Validation functionality for ARGO metadata."""

import re
from pathlib import Path
from typing import Any

from jsonschema.exceptions import ValidationError as JsonValidationError

from argo_metadata_validator.models.results import ValidationError
from argo_metadata_validator.schema_utils import get_json_validator, infer_schema_from_data
from argo_metadata_validator.utils import load_json
from argo_metadata_validator.vocab_utils import expand_vocab, get_all_terms_from_argo_vocabs


def _parse_json_error(error: JsonValidationError) -> ValidationError:
    return ValidationError(message=error.message, path=".".join([str(x) for x in error.path]))


class ArgoValidator:
    """Validator class for ARGO metadata."""

    all_json_data: dict[str, Any] = {}  # Keyed by the original filename
    validation_errors: dict[str, list[ValidationError]] = {}  # Keyed by the original filename
    valid_argo_vocab_terms: list[str] = []

    def __init__(self):
        """Initialise by pre-loading the ARGO vocab terms."""
        self.valid_argo_vocab_terms = get_all_terms_from_argo_vocabs()

    def load_json_data(self, json_files: list[str]):
        """Take a list of JSON files and load content into memory.

        Args:
            json_files (list[str]): List of file paths.
        """
        json_file_paths = [Path(x) for x in json_files]

        self.all_json_data = {}
        for file in json_file_paths:
            if not file.exists():
                raise Exception(f"Provided JSON file could not be found: {file}")

            # Load the JSON into memory
            self.all_json_data[file.name] = load_json(file)

    def validate(self, json_files: list[str]) -> dict[str, list[ValidationError]]:
        """Takes a list of JSON files and validates each.

        Args:
            json_files (list[str]): List of file paths.

        Returns:
            dict[str, list[str]]: Errors, keyed by the input filename.
        """
        self.load_json_data(json_files)

        self.validation_errors = {}
        for file, json_data in self.all_json_data.items():
            self.validation_errors[file] = self.validate_json(json_data)

            if not self.validation_errors[file]:
                self.validation_errors[file] += self.validate_vocabs(json_data)
        return self.validation_errors

    def validate_json(self, json_data: Any) -> list[ValidationError]:
        """Apply JSON schema validation to given JSON data.

        Args:
            json_data (Any): JSON content to check.

        Returns:
            list[str]: List of errors.
        """
        schema_type = infer_schema_from_data(json_data)
        json_validator = get_json_validator(schema_type)

        errors = []

        if not json_validator.is_valid(json_data):
            errors = [_parse_json_error(err) for err in json_validator.iter_errors(json_data)]
        return errors

    def validate_vocabs(self, json_data: Any) -> list[ValidationError]:
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
                    if val not in self.valid_argo_vocab_terms:
                        errors.append(ValidationError(message=f"Unknown NSV term: {val}", path=f"{field}.{idx}.{x}"))
        return errors
