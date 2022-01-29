========
Meet Bob
========

Bob is my collection of build tools. The goal is to provide a simple interface to build and test projects without having to remember or lookup various commands.

For now, this project limits itself to C/C++ projects.


Development
===========

1. Setup a virtual environment and activate it:

  ::

    python -m venv .env
    . .env/bin/activate

2. Install locally:

  ::

    pip install -e .[testing]

3. Test:

  ::

    tox .
