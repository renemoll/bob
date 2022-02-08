"""Module focussing on the `build` command.

Contains the task and helpers to build a codebase.
"""
import logging
import pathlib
import typing

from .api import BuildTarget


def depends_on() -> [str]:
    """Returns a list of task names this task depends on."""
    return ["configure"]


def bob_build(
    options: typing.Dict[str, str], cwd: pathlib.Path
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

    # 	def generate_build_env():
    # 		steps = []
    # 		if options['use-container']:
    # 			steps += container_command(options['build']['target'], cwd)
    #
    # 		steps += build_system_command(options, output_folder)
    #
    # 		if options['build']['target'] == BuildTarget.Stm32:
    # 			steps += build_stm32()
    #
    # 		return steps

    def build_project() -> typing.List[typing.List[str]]:
        steps = []

        if options["use-container"]:
            steps += container_command(options["build"]["target"], cwd)

        steps += build_project_command(output_folder)

        return steps

    return [
        # generate_build_env(),
        build_project()
    ]


def _determine_output_folder(options: typing.Dict[str, str]) -> str:
    return f"{options['target']}-{options['config']}".lower()


def container_command(target: BuildTarget, cwd: pathlib.Path) -> typing.List[str]:
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


# def build_system_command(options, output_folder):
# 	cmd = ["cmake",
# 		"-B", "build/{}".format(output_folder),
# 		"-S", ".",
# 		"-DCMAKE_BUILD_TYPE={}".format(str(options['build']['config']))
# 		# "–warn-uninitialized"
# 	]
#
# 	if options['build']['target'] in (BuildTarget.Linux, BuildTarget.Stm32):
# 		cmd += [
# 			"-G", "Ninja",
# 		]
#
# 	return cmd
#
#
# def build_stm32():
# 	return ["-DCMAKE_TOOLCHAIN_FILE=cmake/toolchain-stm32f767.cmake"]


def build_project_command(output_folder: str) -> str:
    """Generate the build command."""
    return ["cmake", "--build", "build/{}".format(output_folder)]
