"""CLI entry point for argo-metadata-validator package."""

import click

from argo_metadata_validator.validation import ArgoValidator


@click.command()
@click.option("--files", prompt="List of input JSON files, comma separated")
def main(files: str):
    """Main entrypoint when running as CLI.

    Args:
        files (str): Comma separated list of file paths to be validated.
    """
    file_paths = files.split(",")
    errors = ArgoValidator().validate(file_paths)

    for file, file_errors in errors.items():
        if file_errors:
            click.echo(click.style(f"{file} has {len(file_errors)} errors", fg="red"))
        else:
            click.echo(click.style(f"{file} has no errors", fg="green"))


if __name__ == "__main__":
    main()
