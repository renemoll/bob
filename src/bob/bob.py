
import logging
import pathlib
import subprocess
import sys
import time


from .build import bob_build
from .debug import bob_debug
from .format import bob_format
from .test import bob_test


class ExecutionTimer:
	def __init__(self):
		self._start = None
		self.duration = None

	def __enter__(self):
		self._start = time.perf_counter()
		return self

	def __exit__(self, exc_type, exc_value, exc_traceback):
		stop = time.perf_counter()
		self.duration = stop - self._start
		return False


def bob(command, options):
	logging.info("Command: %s, options: %s", command, options)

	cwd = pathlib.Path(__file__).parent.resolve()
	logging.debug("Determined working directory: %s", cwd)

	tasks = []
	if command == Command.Build:
		tasks += bob_build(options, cwd)
	if command == Command.Debug:
		tasks += bob_debug(options, cwd)
	if command == Command.Test:
		tasks += bob_test(options)
	if command == Command.Format:
		tasks += bob_format(options, cwd)

	logging.debug("Processing %d tasks", len(tasks))
	for task in tasks:
		logging.debug(" ".join(task))
		with ExecutionTimer() as timer:
			result = subprocess.run(task)
		logging.debug("Result: %s in %f seconds", result, timer.duration)
		result.check_returncode()
