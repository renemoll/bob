"""Module for executing on the `bootstrap` command.

Contains the task and helpers to prepare the codebase for building.
"""
import logging
import pathlib
import typing

from .api import Command
from .typehints import OptionsMapT


def depends_on() -> typing.List[Command]:
    """Returns a list of task names this task depends on."""
    return []


def bob_bootstrap(
    options: OptionsMapT, cwd: pathlib.Path
) -> typing.List[typing.List[str]]:
    # pylint: disable=unused-argument
    """Generate a set of commands to prepare the codebase for building.

    Args:
        options: set of build options to take into account.
        cwd: the location of the codebase.

    Returns:
        A list of commands, each command is a list of strings which can be
        passed to `subprocess.run`.

    Todo:
        - rename cwd
        - which options are used?
        - split target and compiler (should be a matrix [target vs compiler])
    """
    output_folder = cwd / "cmake"
    logging.debug("Determined output folder: %s", output_folder)
    base_file = pathlib.Path(__file__).parent.resolve() / "templates" / "FindBob.cmake"

    return [
        ["cmake", "-E", "make_directory", str(output_folder)],
        ["cmake", "-E", "copy", str(base_file), str(output_folder)],
    ]
