argo-metadata-validator
=======================

Validator for ARGO sensor metadata JSON

TODO: running/install instructions

**Development**

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


Releasing a new version
-----------------------

Versions of the package are denoted by tags in git.
To create a new tag, you can use the GitLab UI by following these steps:

#. Go the repository tags page
#. Click **New tag**
#. Enter the tag name. There are four options for the format for this tag:

   #. Alpha release (development release): ``vX.Y.ZaW``, for example ``v1.0.2a3``
   #. Beta release (development release): ``vX.Y.ZbW``, for example ``v2.3.0b1``.
   #. Release candidate (test release): ``vX.Y.ZrcW``, for example ``v1.10.9rc2``.
   #. Full release (production release): ``vX.Y.Z``, for example ``v3.0.11``.

#. Select the branch to create the tag from, this will normally be ``main``
#. Enter a message for the tag, this is required for the CI/CD pipeline to function correctly
#. Click **Create tag**
#. This will trigger a CI/CD pipeline
