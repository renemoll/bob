Usage
=====

Bob automates a number of tasks commonly encountered when building and testing
software, this is reflected in the design of Bob. Bob provides a shothand for
common tasks such as executing unit-test, code linters, sanitizers, etc.

Tasks:
 * bootstrap
 * configure
 * build
 * (test)
 * (install)
 * (lint)
 * (check)

Essentialy, each task generates a set of commands to perform their task. And
given that tasks can depend on each other, executing a single task will
ensure all depending tasks are executed.

You can customize the build environement using a single human readable
configuration file.

.. _installation:

Installation
------------

Bob is availble on *PyPi*:

.. code-block:: console

   (.venv) $ pip install bob-the-developer


.. _configuration:

Configuration
-------------

TODO: show how to define a target
TODO: show how to add compile options


.. _build:

Compiling a codebase
--------------------

By default, Bob will use the compile for your host environement using the first
compiler/toolchain it can find.

.. code-block:: console

   (.venv) $ bob compile

If you want to compile for a specific target, you can specify that as follows:

.. code-block:: console

   (.venv) $ bob compile (target)

You define targets in your projects configuration file.
