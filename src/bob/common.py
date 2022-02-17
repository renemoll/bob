"""Module with functionality shared between various modules."""
import pathlib
import typing

from .api import BuildTarget
from .typehints import OptionsType


def determine_output_folder(options: typing.Mapping[str, OptionsType]) -> str:
    """Generate the output path based on project settings."""
    return f"{options['target']}-{options['config']}".lower()


def generate_container_command(
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
