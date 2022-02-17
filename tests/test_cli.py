"""Test the CLI entry point."""
import os
import subprocess

import docopt
import pytest_mock

from bob.cli import main


def test_cli_configure(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a configure."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "build": False,
        "configure": True,
        "debug": False,
        "release": False,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
    subprocess.run.assert_called_once_with(
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


def test_cli_build_default(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a build."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "build": True,
        "configure": False,
        "debug": False,
        "release": False,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
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


def test_cli_build_release(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a build."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "build": True,
        "configure": False,
        "debug": False,
        "release": True,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
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


def test_cli_build_error(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI captures subprocess exceptions."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "build": True,
        "configure": False,
        "debug": True,
        "release": False,
    }

    subprocess.run.side_effect = subprocess.CalledProcessError(
        returncode=1, cmd="exception_cmd"
    )

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == os.EX_SOFTWARE
    subprocess.run.assert_called_once_with(
        ["cmake", "-B", "build/native-debug", "-S", ".", "-DCMAKE_BUILD_TYPE=Debug"],
        check=True,
    )
