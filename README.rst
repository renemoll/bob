========
Meet Bob
========

Bob is my collection of build tools. The goal is to provide a simple interface
to build and test projects without having to remember or lookup various commands.

For now, this project limits itself to C/C++ projects.

Development
===========

1. Setup a virtual environment and activate it:

  ::

    python -m venv .env_dev
    . .env_dev/bin/activate

2. Install locally:

  ::

    pip install -e .[develop]

3. Test:

  ::

    pytest


Run the complete test-suite
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Setup a virtual environment and activate it:

  ::

    python -m venv .env_tox
    . .env_tox/bin/activate

2. Install locally:

  ::

    pip install -e .[testing]

3. Test:

  ::

    tox .

Configured tools
~~~~~~~~~~~~~~~~

1. `black` for code formatting.
2. `flake8` for linting, static analysis (`flake8-bugbear`), docstyle checking (`flake8-docstrings`), additional format checks (`flake8-import-order`.)
3. `pylint` for linting.
4. `bandit` for static analysis.
5. `mypy`

Roadmap
=======

1. Python support
