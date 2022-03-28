"""Module for executing on the `bootstrap` command.

Contains the task and helpers to prepare the codebase for building.
"""
import logging
import pathlib
import typing

from .api import Command
from .typehints import OptionsMapType


def depends_on() -> typing.List[Command]:
    """Returns a list of task names this task depends on."""
    return []


def bob_bootstrap(
    options: OptionsMapType, cwd: pathlib.Path
) -> typing.List[typing.List[str]]:
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

    output_folder.mkdir(parents=True, exist_ok=False)

    output_file = output_folder / "FindBob.cmake"
    output_file.write_text("""
include(FetchContent)

FetchContent_Declare(
  bob-cmake
  GIT_REPOSITORY https://github.com/renemoll/bob-cmake.git
  GIT_TAG        origin/main
  GIT_SHALLOW    true
)

FetchContent_MakeAvailable(bob-cmake)
""")
