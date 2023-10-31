"""The bootstrap task prepares the codebase for building.

Bootstrapping ensures all dependencies and toolchains are avaialble. Actual building of
dependencies is out of scope due to the project to project variation.
"""
import collections.abc
import contextlib
import logging
import pathlib
import platform
import typing
import urllib.request
import shutil

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
        env["dependencies_path"] = env["root_path"] / "external"

    try:
        env["toolchains_path"] = pathlib.Path(options["toolchains"]["folder"])
    except KeyError:
        env["toolchains_path"] = env["root_path"] / "toolchains"

    return env


def parse_options(options: OptionsMapT) -> OptionsMapT:
    """Update the options map.

    Args:
        options: set of options to take into account.

    Returns:
        An updated options map.
    """
    deps = {}
    with contextlib.suppress(KeyError):
        for k, v in options["dependencies"].items():
            if isinstance(v, collections.abc.Mapping):
                deps[k] = v

    tools = {}
    with contextlib.suppress(KeyError):
        os = platform.system().lower()
        for k, v in options["toolchains"].items():
            with contextlib.suppress(TypeError, KeyError):
                tools[k] = v[os]

    options["bootstrap"] = {"dependencies": deps, "toolchains": tools}

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

    with contextlib.suppress(KeyError):
        result += _gather_dependencies(
            options["bootstrap"]["dependencies"],
            env["dependencies_path"],
        )

    with contextlib.suppress(KeyError):
        result += _gather_toolchain(
            options["bootstrap"]["toolchains"],
            env["toolchains_path"],
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
        rep_path = output_path / name

        if not rep_path.exists():
            result.append(["git", "clone", options["repository"], str(rep_path)])

        result.append(
            ["cmake", "-E", "chdir", str(rep_path), "git", "checkout", options["tag"]]
        )

    return result


def _get_package(url: str, output_path: pathlib.Path) -> pathlib.Path:
    path = output_path / pathlib.Path(url).name
    logging.info("Retrieving: %s", pathlib.Path(url).name)

    if not path.exists():
        logging.info("Downloading: %s", url)
        urllib.request.urlretrieve(url, path)
    else:
        logging.info("Archive found: %s", path)

    return path


def _extract_package(archive, output_path: pathlib.Path):
    logging.info("Extracting: %s to %s", archive, output_path)
    if not (output_path / archive.name).exists():
        shutil.unpack_archive(archive, output_path)


def _gather_toolchain(
    toolchains: typing.Mapping[str, str], output_path: pathlib.Path
) -> CommandListT:
    logging.debug("Ensure toolchain folder: %s", output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    archive_path = output_path / "download"
    archive_path.mkdir(parents=True, exist_ok=True)

    result = []
    for name, url in toolchains.items():
        logging.info("Found toolchain dependency: %s", name)
        archive = _get_package(url, archive_path)
        _extract_package(archive, output_path)

    return result
