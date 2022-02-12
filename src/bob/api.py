"""Collection of types used in the API."""

import enum


class Command(enum.Enum):
    """Command represents an action to perform on the codebase."""

    # bootstrap
    Configure = 1
    Build = 2
    # Test = 3
    # 	Debug
    # 	Format
    # lint
    # analyzers

    def __str__(self: "Command") -> str:
        """String conversion."""
        return self.name


class BuildConfig(enum.Enum):
    """Build configuration during the build process."""

    Release = 1
    Debug = 2

    def __str__(self: "BuildConfig") -> str:
        """String conversion."""
        return self.name


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
