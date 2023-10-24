"""The build task builds the codebase."""
import logging
import typing

from bob.api import Command
from bob.common import determine_output_folder, generate_container_command
from bob.typehints import CommandListT, EnvMapT, OptionsMapT


def depends_on() -> typing.List[Command]:
    """Generate a list of task names this task depends on.

    Returns:
        A list of commands.
    """
    return [Command.Configure]


def parse_env(env: EnvMapT, options: OptionsMapT) -> EnvMapT:
    """Update the envorinment map.

    Args:
        env: a map with relevant locations in the codebase.
        options: set of options to take into account.

    Returns:
        An updated env map.
    """
    return env


def parse_options(options: OptionsMapT) -> OptionsMapT:
    """Update the options map.

    Args:
        options: set of options to take into account.

    Returns:
        An updated options map.
    """
    return options


def generate_commands(options: OptionsMapT, env: EnvMapT) -> CommandListT:
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
    return ["cmake", "--build", f"build/{output_folder}"]
