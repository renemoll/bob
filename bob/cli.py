"""The builder, Bob the builder.

Usage:
    bob.py bootstrap [<target>]
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
import contextlib
import logging
import pathlib
import subprocess
import typing

import docopt
import toml

from bob import __version__
from bob.api import BuildConfig, Command, generate_targets
from bob.bob import bob
from bob.compat import EX_DATAERR, EX_OK, EX_SOFTWARE
from bob.typehints import BuildTargetT, OptionsMapT

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

    arguments = docopt.docopt(__doc__, version=__version__)
    try:
        command = _determine_command(arguments)
        options = _determine_options(arguments)
    except ValueError:
        logging.exception("Exception caught parsing command line input")
        return EX_DATAERR

    try:
        bob(command, options)
    except subprocess.CalledProcessError:
        logging.exception("Exception caught executing commands")
        return EX_SOFTWARE

    return EX_OK


def _determine_command(arguments: typing.Mapping[str, ArgsT]) -> Command:
    if arguments["bootstrap"]:
        return Command.Bootstrap
    if arguments["configure"]:
        return Command.Configure
    return Command.Build


def _determine_options(arguments: typing.Mapping[str, ArgsT]) -> OptionsMapT:
    """Returns map with options based on the given arguments.

    Args:
        arguments (dict): a map with input arguments.

    Returns:
        A map representing the options for each step.

    Raises:
        ValueError: upon errors parsing a `bob.toml` file.

    Todo:
        - settings such as toolchains and targets should be filtered such that only
          the active/relevant settings remain.
        - toolchain may have container and archive?
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
        logging.exception("Exception caught parsing %s", toml_file)
        raise ValueError from ex

    targets = ["native"]
    with contextlib.suppress(KeyError):
        targets += list(options["targets"].keys())
    options["targets"] = generate_targets(targets)

    user_options = {
        "build": {
            "config": _determine_build_config(arguments),
            "target": _determine_build_target(arguments, options),
        }
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


def _determine_build_target(
    arguments: typing.Mapping[str, ArgsT], options: OptionsMapT
) -> BuildTargetT:
    try:
        target = arguments["<target>"].lower().capitalize()  # type: ignore [attr-defined]
        for x in options["targets"]:
            if x.name == target:
                return x

        raise ValueError(f"Invalid target specified: {target}")
    except AttributeError:
        logging.info("No build target selected, defaulting to native build target")
        return options["targets"].Native
