"""Contains the entry point for the application.

The function `bob` is called by the CLI script and is the function to call
when integrating bob into custom scripting.
"""
import contextlib
import logging
import pathlib
import subprocess
import time
import types
import typing

# import sys


from .api import Command
from .build import bob_build, depends_on as build_depends
from .configure import bob_configure, depends_on as configure_depends

# from .debug import bob_debug
# from .format import bob_format
# from .test import bob_test


class ExecutionTimer(contextlib.AbstractContextManager):
    """High resolution timer to capture the execution time of a block.

    Attributes:
        duration (float): elapsed time in seconds.
        duration_ns (int): elapsed time in whole nanoseconds.
        duration_ms (float): elapsed time in miliseconds.
    """

    # def __init__(self: "ExecutionTimer") -> None:
    #     self._start = None
    #     self.duration = None
    #     self.duration_ms = None
    #     self.duration_ns = None

    def __enter__(self: "ExecutionTimer") -> "ExecutionTimer":
        """Start the timed context by recording the current time."""
        self._start = time.perf_counter_ns()
        return self

    def __exit__(
        self: "ExecutionTimer",
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        exc_traceback: typing.Optional[types.TracebackType],
    ) -> bool:
        """Stop the timed context and calculate the elapsed time."""
        stop = time.perf_counter_ns()
        self.duration_ns = stop - self._start
        self.duration_ms = self.duration_ns * 1e-6
        self.duration = self.duration_ns * 1e-9
        return False


def bob(command: Command, options: typing.Dict[str, str]) -> None:
    """Executes a `bob` command.

    Args:
        command: a command to execute
        options: a map of options to pass to the command
    """
    logging.info(f"Execting command: {command}")
    logging.debug(f"Options: {options}")

    cwd = pathlib.Path.cwd()
    logging.debug(f"Working directory: {cwd}")

    tasks = _determine_dependent_tasks(command)
    tasks += [command]
    logging.debug(f"Processing {len(tasks)} tasks ({tasks})")

    for task in tasks:
        if task == Command.Configure:
            cmd_list = bob_configure(options, cwd)
        # elif task == Command.Build:
        else:
            cmd_list = bob_build(options, cwd)

        for cmd in cmd_list:
            logging.debug(" ".join(cmd))
            with ExecutionTimer() as timer:
                result = subprocess.run(cmd)
            logging.debug(
                f"Result code: `{result.returncode}` in {timer.duration} seconds"
            )
            result.check_returncode()


#     if command == Command.Debug:
#         tasks += bob_debug(options, cwd)
#     if command == Command.Test:
#         tasks += bob_test(options)
#     if command == Command.Format:
#         tasks += bob_format(options, cwd)
#


def _determine_dependent_tasks(command: Command) -> typing.List[Command]:
    deps = _get_dependent_tasks(command)
    # i = len(deps)
    # for d in deps:
    # deps += _get_dependent_tasks(d)

    # if i == len(deps):
    return deps
    # return _determine_dependent_tasks(deps)


def _get_dependent_tasks(command: Command) -> typing.List[Command]:
    if command == Command.Build:
        return build_depends()

    return configure_depends()
