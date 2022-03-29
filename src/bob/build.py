"""Module focussing on the `build` command.

Contains the task and helpers to build a codebase.
"""
import logging
import pathlib
import typing

from .api import Command
from .common import determine_output_folder, generate_container_command
from .typehints import OptionsMapT


def depends_on() -> typing.List[Command]:
    """Returns a list of task names this task depends on."""
    return [Command.Configure]


def bob_build(options: OptionsMapT, cwd: pathlib.Path) -> typing.List[typing.List[str]]:
    """Generate a set of commands to build the codebase.

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
    output_folder = determine_output_folder(options["build"])
    logging.debug("Determined output folder: %s", output_folder)

    def build_project() -> typing.List[str]:
        steps = []

        if options["use-container"]:
            steps += generate_container_command(options["build"]["target"], cwd)

        steps += _generate_build_project_command(output_folder)

        return steps

    return [
        build_project(),
    ]


def _generate_build_project_command(output_folder: str) -> typing.List[str]:
    """Generate the build command."""
    return ["cmake", "--build", f"build/{output_folder}"]
