"""The builder, Bob the builder.

Usage:
    bob.py configure
    bob.py build [<target>] [(debug|release)]
    bob.py -h | --help
    bob.py --version

Possible commands:
    build: build the project for the a target.

Options:
    -h --help        Show this screen.
    --version        Show version.
"""
import logging
import os
import subprocess
import typing

import docopt

from .api import BuildConfig, BuildTarget, Command
from .bob import bob


Args = typing.TypeVar("Args", None, bool, str)


def main() -> int:
    """CLI entry-point."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s: %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
    )

    arguments = docopt.docopt(__doc__, version="Bob 0.1")
    print(arguments)
    command = _determine_command(arguments)
    options = _determine_options(arguments)

    try:
        bob(command, options)
    except subprocess.CalledProcessError as e:
        print(e)
        return os.EX_SOFTWARE
    return os.EX_OK


def _determine_command(arguments: typing.Mapping[str, Args]) -> Command:
    """Returns a Command based on the given arguments."""
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
    elif arguments["debug"]:
        return BuildConfig.Debug

    logging.info("No build config selected, defaulting to release build config")
    return BuildConfig.Release


def _determine_build_target(arguments: typing.Mapping[str, Args]) -> BuildTarget:
    """Returns a BuildTarget based on the given arguments."""
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
