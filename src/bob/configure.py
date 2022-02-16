"""Module focussing on the `configure` command.

Contains the task and helpers to configure a build.
"""
import logging
import pathlib
import typing

from .api import BuildTarget, Command
from .typehints import OptionsType, OptionsMapType


def depends_on() -> typing.List[Command]:
    """Returns a list of task names this task depends on."""
    return []


def bob_configure(
    options: OptionsMapType, cwd: pathlib.Path
) -> typing.List[typing.List[str]]:
    """Generate a set of commands to configure the build.

    Args:
        options: set of build options to take into account.
        cwd: the location of the codebase.

    Returns:
        A list of commands, each command is a list of strings which can be
        passed to `subprocess.run`.

    Todo:
        - rename cwd
    """
    output_folder = _determine_output_folder(options["build"])
    logging.debug("Determined output folder: %s", output_folder)

    def generate_build_env() -> typing.List[str]:
        steps = []

        if options["use-container"]:
            steps += _generate_container_command(options["build"]["target"], cwd)

        steps += _generate_build_system_command(options, output_folder)

        # if options['build']['target'] == BuildTarget.Stm32:
        # steps += build_stm32()

        return steps

    return [
        generate_build_env(),
    ]


def _determine_output_folder(options: typing.Mapping[str, OptionsType]) -> str:
    """Todo: share with bob_build."""
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
        - share with bob_build
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


def _generate_build_system_command(
    options: OptionsMapType, output_folder: str
) -> typing.List[str]:
    """Generate the build configuration command."""
    cmd = [
        "cmake",
        "-B",
        "build/{}".format(output_folder),
        "-S",
        ".",
        "-DCMAKE_BUILD_TYPE={}".format(str(options["build"]["config"])),
    ]

    # if options['build']['target'] in (BuildTarget.Linux, BuildTarget.Stm32):
    if options["build"]["target"] == BuildTarget.Linux:
        cmd += [
            "-G",
            "Ninja",
        ]

    return cmd


# def build_stm32():
# return ["-DCMAKE_TOOLCHAIN_FILE=cmake/toolchain-stm32f767.cmake"]
