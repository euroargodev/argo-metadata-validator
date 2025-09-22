"""CLI entry point for argo-metadata-validator package."""

import json

import click

from argo_metadata_validator.models.results import ValidationError
from argo_metadata_validator.validation import ArgoValidator


def output_to_terminal(errors: dict[str, list[ValidationError]]):
    """Convert validation errors to terminal output."""
    for file, file_errors in errors.items():
        if file_errors:
            click.echo(click.style(f"{file} has {len(file_errors)} errors", fg="red"))
        else:
            click.echo(click.style(f"{file} has no errors", fg="green"))
        click.echo("-----")
        for err in file_errors:
            click.echo(click.style(f"{err.message} at path {err.path}", fg="red"))


def output_to_json_string(errors: dict[str, list[ValidationError]]) -> str:
    """Convert validation errors to a JSON-string output."""
    serialised = {}
    for file, file_errors in errors.items():
        serialised[file] = {"is_valid": len(file_errors) == 0, "errors": [x.model_dump() for x in file_errors]}
    return json.dumps(serialised, indent=2)


@click.command()
@click.argument("files")
@click.option("--quiet", "-q", "quiet_mode", is_flag=True, help="Suppresses terminal output")
@click.option("--output-file", "-f", help="Path to output JSON file of results")
def main(files: str, quiet_mode: bool = False, output_file: str = ""):
    """Main entrypoint when running as CLI.

    FILES is a comma-separated list of the JSON files to validate.
    """
    file_paths = files.split(",")
    errors = ArgoValidator().validate(file_paths)

    if not quiet_mode:
        output_to_terminal(errors)
    if output_file:
        with open(output_file, "w") as file:
            file.write(output_to_json_string(errors))
