"""The builder, Bob the builder.

Usage:
    bob.py bootstrap
    bob.py configure [<target>] [(debug|release)]
    bob.py build [<target>] [(debug|release)]
    bob.py -h | --help
    bob.py --version

Possible commands:
    build:     build the project for the a target.
    configure: prepare the project for the first build, automatically executed with build.

Options:
    -h --help        Show this screen.
    --version        Show version.
"""
import logging
import pathlib
import subprocess
import sys
import typing

import docopt
import toml

from bob.api import BuildConfig, BuildTarget, Command
from bob.bob import bob
from bob.compat import EX_DATAERR, EX_OK, EX_SOFTWARE


ArgsT = typing.TypeVar("ArgsT", None, bool, str)


def main() -> int:
    """CLI entry-point.

    Returns:
        A result code to be returned to the OS.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s: %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    )

    arguments = docopt.docopt(__doc__, version="Bob 2023.10.0")
    try:
        command = _determine_command(arguments)
        options = _determine_options(arguments)
    except ValueError as ex:
        print(ex)
        return EX_DATAERR

    try:
        bob(command, options)
    except subprocess.CalledProcessError as ex:
        print(ex)
        return EX_SOFTWARE

    return EX_OK


def _determine_command(arguments: typing.Mapping[str, ArgsT]) -> Command:
    if arguments["bootstrap"]:
        return Command.Bootstrap
    if arguments["configure"]:
        return Command.Configure
    # elif arguments["build"]:
    return Command.Build

    # raise ValueError("Unsupported command")


def _determine_options(
    arguments: typing.Mapping[str, ArgsT]
) -> typing.MutableMapping[str, typing.Any]:
    """Returns map with options based on the given arguments.

    Args:
        arguments (dict): a map with input arguments.

    Returns:
        A map representing the options for each step.

    Raises:
        ValueError: upon errors parsing a `bob.toml` file.

    Todo:
        - update return type annotation.
    """
    options = {}

    cwd = pathlib.Path.cwd()
    toml_file = cwd / "bob.toml"

    try:
        file_options = toml.load(toml_file)
        logging.debug("Loading settings: %s", toml_file)
        options.update(file_options)
    except FileNotFoundError:
        pass
    except Exception as ex:
        print(f"Error parsing `{toml_file}`")
        print(f"{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}")  # type: ignore
        raise ValueError from ex

    user_options = {
        "build": {
            "config": _determine_build_config(arguments),
            "target": _determine_build_target(arguments),
        },
        "use-container": True,
    }
    options.update(user_options)
    return options


def _determine_build_config(arguments: typing.Mapping[str, ArgsT]) -> BuildConfig:
    if arguments["release"]:
        return BuildConfig.Release
    if arguments["debug"]:
        return BuildConfig.Debug

    logging.info("No build config selected, defaulting to release build config")
    return BuildConfig.Release


def _determine_build_target(arguments: typing.Mapping[str, ArgsT]) -> BuildTarget:
    """Parse the arguments to determine the BuildTarget.

    Args:
        arguments: input arguments map.

    Raises:
        ValueError: when the input cannot be parsed properly.

    Returns:
        A BuildTarget based on the given arguments.
    """
    try:
        target = arguments["<target>"].lower()  # type: ignore
        if target == "linux":
            return BuildTarget.Linux
        # if target == "stm32":
        # return BuildTarget.Stm32

        raise ValueError(f"Invalid target specified: '{target}'")
    except AttributeError:
        logging.info("No build target selected, defaulting to native build target")
        return BuildTarget.Native
