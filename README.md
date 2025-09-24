# Argo Metadata Validator

Validator for ARGO sensor metadata JSON

Package: https://pypi.org/project/argo-metadata-validator

## Usage

Install the package with `pip install argo-metadata-validator`.

You can validate files from the command line as follows
```
argo-validate file_1.json,file_2.json
```

To see the available CLI options you can run `argo-validate --help`.

TODO: Add Non-CLI usage example.


## Development

[Poetry](https://python-poetry.org/) is used to manage the building of this package and managing the package dependencies.

To run the script locally:
- `poetry install`
- `poetry run argo-validate`

For example, from the root of the repo
```
poetry run argo-validate tests/files/valid_sensor.json
```

To run lint/tests, first install dev dependencies ``poetry install -with dev``

- ``poetry run task lint`` - Check linting
- ``poetry run task format`` - Autofix lint errors (where possible)
- ``poetry run task test`` - Run unit tests


### Releasing a new version

This done by creating a new release in Github. Make sure the created tag follows SemVer conventions.
