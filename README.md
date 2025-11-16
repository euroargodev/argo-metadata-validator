# Argo Metadata Validator

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17207141.svg)](https://doi.org/10.5281/zenodo.17207141)

Validator for ARGO sensor metadata JSON.

Schema definitions are taken from https://github.com/euroargodev/sensor_metadata_json.

Package: https://pypi.org/project/argo-metadata-validator

## Usage

### Installation

Install the package from PyPi with
```
pip install argo-metadata-validator
```

### From the Terminal

Once installed, you can run the tool to validate files from the terminal (Bash, Powershell, etc.) as follows
```
argo-validate file_1.json,file_2.json
```

To output the results to a JSON file you can specify a path for this, e.g.
```
argo-validate input/file_1.json --output-file output/results.json
```

To see the available CLI options you can run `argo-validate --help`.

### From Python

As well as the command-line script version the validator can be used as a Python package, e.g. from Python scripts or Jupyter notebooks.

See [demos/argo_validator.ipynb](demos/argo_validator.ipynb) for an example of how to validate and parse input metadata from within Python scripts.


## Development

[Poetry](https://python-poetry.org/) is used to manage the building of this package and managing the package dependencies.

To run the script locally:
- `poetry install`
- `poetry run argo-validate`

For example, from the root of the repo
```
poetry run argo-validate tests/files/valid_sensor.json
```

To run lint/tests, first install dev dependencies ``poetry install --with dev``

- ``poetry run task lint`` - Check linting
- ``poetry run task format`` - Autofix lint errors (where possible)
- ``poetry run task test`` - Run unit tests


### Releasing a new version

This done by creating a new release in Github. Make sure the created tag follows SemVer conventions.
