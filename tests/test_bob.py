"""Test the basic flow for each command."""

import subprocess

import pytest_mock

import bob
from bob.api import BuildConfig, BuildTarget


def test_bob_configure(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the configure command produces a configure command call."""
    # 1. Prepare
    mocker.patch("subprocess.run")

    cmd = bob.Command.Configure
    options = {
        "build": {
            "config": BuildConfig.Debug,
            "target": BuildTarget.Native,
        },
        "use-container": False,
    }

    # 2. Execute
    bob.bob(cmd, options)

    # 3. Verify
    subprocess.run.assert_called_once_with(
        ["cmake", "-B", "build/native-debug", "-S", ".", "-DCMAKE_BUILD_TYPE=Debug"],
        check=True,
    )


def test_bob_build(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the build command produces a configure and build command call.

    Todo:
    * Improve by enforcing call order. However, I do not want to assert every in between call.
    """
    # 1. Prepare
    mocker.patch("subprocess.run")

    cmd = bob.Command.Build
    options = {
        "build": {
            "config": BuildConfig.Release,
            "target": BuildTarget.Native,
        },
        "use-container": False,
    }

    # 2. Execute
    bob.bob(cmd, options)

    # 3. Verify
    subprocess.run.assert_any_call(
        [
            "cmake",
            "-B",
            "build/native-release",
            "-S",
            ".",
            "-DCMAKE_BUILD_TYPE=Release",
        ],
        check=True,
    )
    subprocess.run.assert_any_call(
        ["cmake", "--build", "build/native-release"], check=True
    )
