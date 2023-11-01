"""Module focussing on the `configure` command.

Contains the task and helpers to configure a build.
"""
import contextlib
import logging
import pathlib
import typing

from bob.api import Command
from bob.common import determine_output_folder, generate_container_command
from bob.typehints import CommandListT, EnvMapT, OptionsMapT


def depends_on() -> typing.List[Command]:
    """Generate a list of task names this task depends on.

    Returns:
        A list of commands.
    """
    return [Command.Bootstrap]


def parse_env(env: EnvMapT, options: OptionsMapT) -> EnvMapT:
    """Update the envorinment map.

    Args:
        env: a map with relevant locations in the codebase.
        options: set of options to take into account.

    Returns:
        An updated env map.
    """
    name = determine_output_folder(options["build"])
    env["build_path"] = pathlib.Path("build") / name
    env["source_path"] = pathlib.Path(".")  # noqa: PTH201
    logging.debug("Determined output folder: %s", env["build_path"])
    return env


def parse_options(options: OptionsMapT) -> OptionsMapT:
    """Update the options map.

    Args:
        options: set of options to take into account.

    Returns:
        An updated options map.
    """
    target = options["build"]["target"].name.lower()
    result = []
    with contextlib.suppress(KeyError):
        addopts = options["targets"][target]["additional_options"]["configuration"]
        result += addopts.split(" ")

    with contextlib.suppress(KeyError):
        addopts = options["toolchains"][target]["additional_options"]["configuration"]
        result += addopts.split(" ")

    options["configure"] = {"additional_options": result}

    return options


def generate_commands(options: OptionsMapT, env: EnvMapT) -> CommandListT:
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
    steps = []
    steps += generate_container_command(options, env["root_path"])
    steps += _generate_build_system_command(
        options, env["build_path"], env["source_path"]
    )

    with contextlib.suppress(KeyError):
        steps += options["configure"]["additional_options"]

    return [steps]


def _generate_build_system_command(
    options: OptionsMapT, output_path: pathlib.Path, source_path: pathlib.Path
) -> typing.List[str]:
    return [
        "cmake",
        "-B",
        str(output_path),
        "-S",
        str(source_path),
        f"-DCMAKE_BUILD_TYPE={options['build']['config']}",
    ]
