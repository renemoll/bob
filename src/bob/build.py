"""Module focussing on the `build` command.

Contains the task and helpers to build a codebase.
"""
import logging
import pathlib
import typing

from .api import BuildTarget, Command
from .typehints import OptionsType, OptionsMapType


def depends_on() -> typing.List[Command]:
    """Returns a list of task names this task depends on."""
    return [Command.Configure]


def bob_build(
    options: OptionsMapType, cwd: pathlib.Path
) -> typing.List[typing.List[str]]:
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
    output_folder = _determine_output_folder(options["build"])
    logging.debug("Determined output folder: %s", output_folder)

    def build_project() -> typing.List[str]:
        steps = []

        if options["use-container"]:
            steps += _generate_container_command(options["build"]["target"], cwd)

        steps += _generate_build_project_command(output_folder)

        return steps

    return [
        build_project(),
    ]


def _determine_output_folder(options: typing.Mapping[str, OptionsType]) -> str:
    return f"{options['target']}-{options['config']}".lower()


def _generate_container_command(
    target: BuildTarget, cwd: pathlib.Path
) -> typing.List[str]:
    """Generate a Docker command to prepend the build command.

    Args:
        target: the target to compile for.
        cwd: the path to the codebase.

    Returns:
        List representing a single command, ready to be passed to subprocess.run.

    Todo:
        - targets may have more compilers
    """
    # 	elif target == BuildTarget.Stm32:
    # 		return ["docker",
    # 			"run",
    # 			"--rm",
    # 			"-v", "{}:/work/".format(cwd),
    # 			"renemoll/builder_arm_gcc"]
    if target == BuildTarget.Linux:
        return [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{cwd}:/work/",
            "renemoll/builder_clang",
        ]

    return []


def _generate_build_project_command(output_folder: str) -> typing.List[str]:
    """Generate the build command."""
    return ["cmake", "--build", f"build/{output_folder}"]
