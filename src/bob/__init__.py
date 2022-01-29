"""The builder, Bob the builder.

Usage:
	build.py build [<target>] [--no-container] [(debug|release)]
	build.py debug [<target>]
	build.py format
	build.py test
	build.py -h | --help
	build.py --version

Possible commands:
	build: build the project for the a target.
	debug: enter the debugger.
	format: apply the code format.
	test: (build and) execute the unit-tests.

Target: optional command to select the target to build for.
	Might be omited for automatic/native target selection, or
	any of the following values:
		- linux
		- stm32
		- native

Options:
	-h --help		Show this screen.
	--version		Show version.
	---no-container	Do not use the appropriate container to build the target.
"""
import logging

from .bob import bob
from .api import determine_command, determine_options

import docopt

__version__ = "0.1.0"

def main():
	logging.basicConfig(
		level=logging.DEBUG,
		format="%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s: %(message)s",
		datefmt='%Y.%m.%d %H:%M:%S'
	)

	arguments = docopt.docopt(__doc__, version='Bob 0.8')
	command = determine_command(arguments)
	options = determine_options(arguments)

	try:
		bob(command, options)
	except subprocess.CalledProcessError as e:
		print(e)
		sys.exit(1)
