"""Collection of types used in the API."""

import enum


class Command(enum.Enum):
    """Command represents an action to perform on the codebase."""

    Bootstrap = 1
    Configure = 2
    Build = 3
    # Test = 3
    # 	Debug
    # 	Format
    # lint
    # analyzers

    def __str__(self: "Command") -> str:
        """Convert a Command to string.

        Returns:
            A string representation of a specific Command.
        """
        return self.name


class BuildConfig(enum.Enum):
    """Build configuration during the build process."""

    Release = 1
    Debug = 2

    def __str__(self: "BuildConfig") -> str:
        """Convert a BuildConfig to string.

        Returns:
            A string representation of a specific BuildConfig.
        """
        return self.name


class BuildTarget(enum.Enum):
    """Valid targets for the codebase.

    Todo:
     - generate based on toolchain/config
    """

    Native = 1
    Linux = 2
    Stm32 = 3

    def __str__(self: "BuildTarget") -> str:
        """Convert a BuildTarget to string.

        Returns:
            A string representation of a specific BuildTarget.
        """
        return self.name
