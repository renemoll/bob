"""Collection of types used in the API."""

import enum
import typing


class Command(enum.Enum):
    """Command represents an action to perform on the codebase."""

    Bootstrap = 1
    Configure = 2
    Build = 3
    # Test
    # Debug
    # Format
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


def generate_targets(targets: typing.Sequence[str]) -> enum.Enum:
    names = [x.capitalize() for x in targets]
    return enum.Enum("BuildTarget", names)
