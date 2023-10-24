"""Module with functionality shared between various modules."""
import pathlib
import typing

from bob.api import BuildTarget


def determine_output_folder(options: typing.Mapping[str, str]) -> str:
    """Generate the output path based on project settings.

    Args:
        options: set of options to take into account.

    Returns:
        The output' folder name for the given options.
    """
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
        - use containers from TOML file
    """
    if target == BuildTarget.Linux:
        return [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{cwd}:/work/",
            "renemoll/builder_clang",
        ]
    # if target == BuildTarget.Stm32:
    #     return [
    #         "docker",
    #         "run",
    #         "--rm",
    #         "-v",
    #         f"{cwd}:/work/",
    #         "renemoll/builder_arm_gcc",
    #     ]

    return []
