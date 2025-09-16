argo-metadata-validator
=======================

Validator for ARGO sensor metadata JSON

**Overview**

PROVIDE AN OVERVIEW OF THE PROJECT HERE
--------



**Documentation**

PROVIDE A LINK TO THE DOCUMENTATION HERE
-------------


**Development**

PROVIDE A LINK TO ANY DEVELOPMENT INFORMATION HERE
-----------


**Running Locally**

PROVIDE AN EXPLANATION ON RUNNING THE PROJECT LOCALLY HERE
-----------


**Package Installation**

Poetry is used to manage the building of this package (.whl & .tar.gz files), and Poetry can be used to install the package
dependencies for you. The dependencies are in the pyproject.toml file, to install them run:

- ``poetry install``

To update your installed dependencies, run:
- ``poetry update``

To install a new dependency and add it to the projects pyproject.toml file, run:
- ``poetry add package_name``

To view your projects dependencies, run:
- ``poetry show``

To view the specific dependencies for a particular package, run:
- ``poetry show package_name``

**Virtual Environments**

This project uses ``tox`` to manage virtual environments. This allows us to have the same environment configuration
for all users, as well as in our GitLab CI/CD pipelines.


To run a ``tox`` environment (for example the linting checks), you can use::

    (argo-metadata-validator-tox) $ tox -e lint

The ``(argo-metadata-validator-tox) $`` indicates that we're running with the conda environment activated.

The available tox environments and their uses are:

py310
    Run the tests from the ``tests`` directory.
``lint``
    Run the static analysis of the code to check for possible errors and style requirements.
``build``
    Build the Python package to check that it will be able to be uploaded.
``docs``
    Build the documentation from the ``docs/source`` directory and output the HTML to ``docs/build``.
``format``
    Format the Python code using ``black``.

Troubleshooting
+++++++++++++++

If you have made changes to the repository that don't seem to be updating in the tox environments,
you can recreate an environment using the ``-r`` option. For example::

    (argo-metadata-validator-tox) $ tox -r -e 310

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
