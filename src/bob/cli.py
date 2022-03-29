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
import subprocess
import typing

import docopt

from .api import BuildConfig, BuildTarget, Command
from .bob import bob
from .compat import EX_DATAERR, EX_OK, EX_SOFTWARE


Args = typing.TypeVar("Args", None, bool, str)


def main() -> int:
    """CLI entry-point."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s: %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    )

    arguments = docopt.docopt(__doc__, version="Bob 0.1")
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


def _determine_command(arguments: typing.Mapping[str, Args]) -> Command:
    """Returns a Command based on the given arguments."""
    if arguments["bootstrap"]:
        return Command.Bootstrap
    if arguments["configure"]:
        return Command.Configure
    # elif arguments["build"]:
    return Command.Build

    # raise ValueError("Unsupported command")


def _determine_options(
    arguments: typing.Mapping[str, Args]
) -> typing.Dict[str, typing.Any]:
    """Returns map with options based on the given arguments.

    Args:
        arguments (dict): a map with input arguments.

    Returns:
        A map representing the options for each step.

    Todo:
        - update return type annotation.
    """
    return {
        "build": {
            "config": _determine_build_config(arguments),
            "target": _determine_build_target(arguments),
        },
        "use-container": True,
    }


def _determine_build_config(arguments: typing.Mapping[str, Args]) -> BuildConfig:
    """Returns a BuildConfig based on the given arguments."""
    if arguments["release"]:
        return BuildConfig.Release
    if arguments["debug"]:
        return BuildConfig.Debug

    logging.info("No build config selected, defaulting to release build config")
    return BuildConfig.Release


def _determine_build_target(arguments: typing.Mapping[str, Args]) -> BuildTarget:
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

        raise ValueError(f"Invalid target specified: '{target}'")
    except AttributeError:
        logging.info("No build target selected, defaulting to native build config")
        return BuildTarget.Native

    # try:
    # 	target = args['<target>'].lower()
    # 	if target == 'stm32':
    # 		return BuildTarget.Stm32
    # 	elif target == 'linux':
    # 		return BuildTarget.Linux
    # 	return BuildTarget.Native
    # except:
    # 	logging.warning("No build target selected, defaulting to native")
