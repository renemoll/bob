"""Module with functionality shared between various modules."""
import contextlib
import pathlib
import typing

from bob.typehints import OptionsMapT


def determine_output_folder(options: OptionsMapT) -> str:
    """Generate the output path based on project settings.

    Args:
        options: set of options to take into account.

    Returns:
        The output' folder name for the given options.
    """
    return f"{options['target'].name}-{options['config']}".lower()


def parse_options(options: OptionsMapT) -> OptionsMapT:
    """Update the options map.

    Args:
        options: set of options to take into account.

    Returns:
        An updated options map.
    """
    with contextlib.suppress(KeyError):
        target = options["build"]["target"].name.lower()
        options["container"] = options["toolchains"][target]["container"]

    return options


def generate_container_command(
    options: OptionsMapT, cwd: pathlib.Path
) -> typing.List[str]:
    """Generate a Docker command to prepend the build command.

    Args:
        options: set of options to take into account.
        cwd: the path to the codebase.

    Returns:
        List representing a single command, ready to be passed to subprocess.run.
    """
    try:
        return [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{cwd}:/work/",
            options["container"],
        ]
    except KeyError:
        return []
