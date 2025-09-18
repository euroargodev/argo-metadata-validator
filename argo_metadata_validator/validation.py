"""Validation functionality for ARGO metadata."""

from pathlib import Path
from typing import Any

from argo_metadata_validator.schema_utils import get_json_validator
from argo_metadata_validator.utils import load_json
from argo_metadata_validator.vocab_utils import expand_vocab, get_all_terms_from_argo_vocabs


class ArgoValidator:
    """Validator class for ARGO metadata."""

    all_json_data: dict[str, Any] = {}  # Keyed by the original filename
    validation_errors: dict[str, list[str]] = {}  # Keyed by the original filename
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
                raise Exception("Provided JSON file could not be found: %s", str(file))

            # Load the JSON into memory
            self.all_json_data[str(file)] = load_json(file)

    def validate(self, json_files: list[str]) -> dict[str, list[str]]:
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

    def validate_json(self, json_data: Any) -> list[str]:
        """Apply JSON schema validation to given JSON data.

        Args:
            json_data (Any): JSON content to check.

        Returns:
            list[str]: List of errors.
        """
        json_validator = get_json_validator()

        errors = []

        if not json_validator.is_valid(json_data):
            errors = [err.message for err in json_validator.iter_errors(json_data)]
        return errors

    def validate_vocabs(self, json_data: Any) -> list[str]:
        """Check validity of used vocab terms in JSON data.

        Args:
            json_data (Any): Input data to check.

        Returns:
            list[str]: List of errors.
        """
        validation_errors: list[str] = []
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

    def validate_vocab_terms(self, json_data: Any, field: str, sub_fields: list[str]) -> list[str]:
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

        for item in items:
            for x in sub_fields:
                val = expand_vocab(context, item[x])
                if val not in self.valid_argo_vocab_terms:
                    errors.append(f"Unknown NSV term: {val}")
        return errors
