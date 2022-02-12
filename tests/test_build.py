"""Tests specifically for the build command."""
import pathlib

import bob
from bob.build import bob_build, depends_on


def test_dependency() -> None:
    """Verify build's dependecies."""
    result = depends_on()

    assert result == [bob.Command.Configure]


def test_build_default_options() -> None:
    """Verify the default options generate a valid build command.

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
    result = bob_build(options, cwd)

    # 3. Verify
    assert len(result) == 1
    assert result[0] == ["cmake", "--build", "build/native-release"]


def test_build_with_container_native() -> None:
    """Verify `use-container` has no impact for a native target."""
    # 1. Prepare
    options = {
        "build": {"config": bob.BuildConfig.Release, "target": bob.BuildTarget.Native},
        "use-container": True,
    }
    cwd = pathlib.Path("/some/path/to/my/code")

    # 2. Execute
    result = bob_build(options, cwd)

    # 3. Verify
    assert len(result) == 1
    assert result[0] == ["cmake", "--build", "build/native-release"]


def test_build_with_container_linux_clang() -> None:
    """Verify `use-container` triggers the use of a Linux container."""
    # 1. Prepare
    options = {
        "build": {"config": bob.BuildConfig.Release, "target": bob.BuildTarget.Linux},
        "use-container": True,
    }
    cwd = pathlib.Path("/some/path/to/my/code")

    # 2. Execute
    result = bob_build(options, cwd)

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
        "--build",
        "build/linux-release",
    ]
