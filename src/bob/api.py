"""Collection of types used in the API."""

import enum

# import logging


class Command(enum.Enum):
    """Command represents an action to perform on the codebase."""

    Build = 1
    # 	Debug = 2
    # 	Format = 4
    Test = 3

    def __str__(self: "Command") -> str:
        """String conversion."""
        return self.name


#
# def determine_command(args):
#     if args["build"]:
#         return Command.Build
#     # elif args['debug']:
#     # return Command.Debug
#     elif args["test"]:
#         return Command.Test
#     # elif args['format']:
#     # return Command.Format
#
#     raise ValueError("Unsupported command")


class BuildConfig(enum.Enum):
    """Build configuration during the build process."""

    Release = 1
    Debug = 2

    def __str__(self: "BuildConfig") -> str:
        """String conversion."""
        return self.name


# def determine_build_config(args):
# 	if args['release']:
# 		return BuildConfig.Release
# 	elif args['debug']:
# 		return BuildConfig.Debug
#
# 	logging.warning("No build config selected, defaulting to release build config")
# 	return BuildConfig.Release


class BuildTarget(enum.Enum):
    """Valid targets for the codebase.

    Todo:
     - generate based on toolchain/config
    """

    Native = 1
    Linux = 2
    # 	Stm32 = 3

    def __str__(self: "BuildTarget") -> str:
        """String conversion."""
        return self.name


#
# def determine_build_target(args):
# 	try:
# 		target = args['<target>'].lower()
# 		if target == 'stm32':
# 			return BuildTarget.Stm32
# 		elif target == 'linux':
# 			return BuildTarget.Linux
# 		return BuildTarget.Native
# 	except:
# 		logging.warning("No build target selected, defaulting to native")
# 		return BuildTarget.Native
#
#
# def determine_options(args):
# 	return {
# 		'build' : {
# 			'config': determine_build_config(arguments),
# 			'target': determine_build_target(arguments),
# 		},
# 		'use-container': not args['--no-container']
# 	}
