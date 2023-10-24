"""The bootstrap task prepares the codebase for building."""
import collections.abc
import logging
import pathlib
import typing

from bob.api import Command
from bob.typehints import CommandListT, EnvMapT, OptionsMapT


def depends_on() -> typing.List[Command]:
    """Generate a list of task names this task depends on.

    Returns:
        A list of commands.
    """
    return []


def parse_env(env: EnvMapT, options: OptionsMapT) -> EnvMapT:
    """Update the envorinment map.

    Args:
        env: a map with relevant locations in the codebase.
        options: set of options to take into account.

    Returns:
        An updated env map.
    """
    try:
        env["dependencies_path"] = pathlib.Path(options["dependencies"]["folder"])
    except KeyError:
        pass
    return env


def parse_options(options: OptionsMapT) -> OptionsMapT:
    """Update the options map.

    Args:
        options: set of options to take into account.

    Returns:
        An updated options map.
    """
    if "dependencies" in options:
        deps = {}
        for k, v in options["dependencies"].items():
            if isinstance(v, collections.abc.Mapping):
                deps[k] = v
        options["dependencies"] = deps
    return options


def generate_commands(options: OptionsMapT, env: EnvMapT) -> CommandListT:
    """Generate a set of commands to prepare the codebase.

    Args:
        options: set of options to take into account.
        env: a map with relevant locations in the codebase.

    Returns:
        A list of commands, each command is a list of strings which can be
        passed to `subprocess.run`.
    """
    result = []
    result += _setup_bob(env["root_path"])

    if "dependencies" in options:
        result += _gather_dependencies(
            options["dependencies"], env["dependencies_path"]
        )

    return result


def _setup_bob(root_path: pathlib.Path) -> CommandListT:
    output_folder = root_path / "cmake"
    logging.debug("Determined cmake folder: %s", output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    base_file = (
        pathlib.Path(__file__).parent.parent.resolve() / "templates" / "FindBob.cmake"
    )

    return [
        ["cmake", "-E", "make_directory", str(output_folder)],
        ["cmake", "-E", "copy", str(base_file), str(output_folder)],
    ]


def _gather_dependencies(
    deps: typing.Mapping[str, typing.Mapping[str, typing.Any]],
    output_path: pathlib.Path,
) -> CommandListT:
    logging.debug("Ensure external folder: %s", output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    result = []
    for name, options in deps.items():
        logging.info("Found external dependecy: %s", name)
        result.append(
            [
                "git",
                "clone",
                "-b",
                options["tag"],
                options["repository"],
                str(output_path / name),
            ]
        )

    return result
