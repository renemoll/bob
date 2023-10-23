"""Module focussing on the `configure` command.

Contains the task and helpers to configure a build.
"""
import logging
import typing

from ..api import BuildTarget, Command
from ..common import determine_output_folder, generate_container_command
from ..typehints import OptionsMapT


def depends_on() -> typing.List[Command]:
    """Returns a list of task names this task depends on."""
    return []


def parse_env(env, options):
    return env


def parse_options(options):
    return options


def generate_commands(options, env) -> typing.List[typing.List[str]]:
    """Generate a set of configure the build.

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

    steps += _generate_build_system_command(options, output_folder)

    # if options["build"]["target"] == BuildTarget.Stm32:
    #     steps += options["configure"]["stm32"]["options"]

    return [steps]


def _generate_build_system_command(
    options: OptionsMapT, output_folder: str
) -> typing.List[str]:
    """Generate the build configuration command."""
    cmd = [
        "cmake",
        "-B",
        f"build/{output_folder}",
        "-S",
        ".",
        f"-DCMAKE_BUILD_TYPE={options['build']['config']}",
    ]

    if options["build"]["target"] in (BuildTarget.Linux, BuildTarget.Stm32):
        cmd += [
            "-G",
            "Ninja",
        ]

    return cmd
