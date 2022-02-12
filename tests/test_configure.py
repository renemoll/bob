"""Tests specifically for the configure command."""
import pathlib

import bob
from bob.configure import bob_configure, depends_on


def test_dependency() -> None:
    """Verify commands's dependecies."""
    result = depends_on()

    assert result == []


def test_configure_default_options() -> None:
    """Verify the default options generate a valid configure command.

    Todo:
    - Actually default the options?
    """
    # 1. Prepare
    options = {
        "build": {"config": bob.BuildConfig.Release, "target": bob.BuildTarget.Native},
        "use-container": False,
    }
    cwd = ""

    # 2. Execute
    result = bob_configure(options, cwd)

    # 3. Verify
    assert len(result) == 1
    assert result[0] == [
        "cmake",
        "-B",
        "build/native-release",
        "-S",
        ".",
        "-DCMAKE_BUILD_TYPE=Release",
    ]


def test_configure_with_container_native() -> None:
    """Given a build request with a native target, `use-container` has no impact."""
    # 1. Prepare
    options = {
        "build": {"config": bob.BuildConfig.Release, "target": bob.BuildTarget.Native},
        "use-container": True,
    }
    cwd = pathlib.Path("/some/path/to/my/code")

    # 2. Execute
    result = bob_configure(options, cwd)

    # 3. Verify
    assert len(result) == 1
    assert result[0] == [
        "cmake",
        "-B",
        "build/native-release",
        "-S",
        ".",
        "-DCMAKE_BUILD_TYPE=Release",
    ]


def test_configure_with_container_linux_clang() -> None:
    """Verify `use-container` triggers the use of a Linux container."""
    # 1. Prepare
    options = {
        "build": {"config": bob.BuildConfig.Release, "target": bob.BuildTarget.Linux},
        "use-container": True,
    }
    cwd = pathlib.Path("/some/path/to/my/code")

    # 2. Execute
    result = bob_configure(options, cwd)

    # 3. Verify
    assert len(result) == 1
    assert result[0] == [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{cwd}:/work/",
        "renemoll/builder_clang",
        "cmake",
        "-B",
        "build/linux-release",
        "-S",
        ".",
        "-DCMAKE_BUILD_TYPE=Release",
        "-G",
        "Ninja",
    ]
