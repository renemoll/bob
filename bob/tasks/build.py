"""The build task builds the codebase."""
import logging
import typing

from ..api import Command
from ..common import determine_output_folder, generate_container_command
from ..typehints import OptionsMapT


def depends_on() -> typing.List[Command]:
    """Returns a list of task names this task depends on."""
    return [Command.Configure]


def parse_env(env, options):
    return env


def parse_options(options):
    return options


def generate_commands(options, env):
    """Generate a set of commands to build the codebase.

    Args:
        options: set of options to take into account.
        env: a map with relevant locations in the codebase.

    Returns:
        A list of commands, each command is a list of strings which can be
        passed to `subprocess.run`.

    Todo:
        - split target and compiler (should be a matrix [target vs compiler])
    """
    output_folder = determine_output_folder(options["build"])
    logging.debug("Determined output folder: %s", output_folder)

    steps = []
    if options["use-container"]:
        steps += generate_container_command(
            options["build"]["target"], env["root_path"]
        )

    steps += _generate_build_project_command(output_folder)

    return [steps]


def _generate_build_project_command(output_folder: str) -> typing.List[str]:
    """Generate the build command."""
    return ["cmake", "--build", f"build/{output_folder}"]
