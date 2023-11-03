"""Test the CLI entry point."""
import os
import pathlib
import shutil
import subprocess

import docopt
import pytest
import pytest_mock

from bob.cli import main


@pytest.fixture(scope="session")
def valid_config_path(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    """Fixture for a working folder with a valid configuration file."""
    work = tmp_path_factory.mktemp("work")
    os.chdir(str(work))

    toml_file = pathlib.Path(__file__).parent.resolve() / "config" / "bob.toml"
    shutil.copy(toml_file, work / "bob.toml")

    return work


def test_cli_bootstrap(
    mocker: pytest_mock.MockerFixture, tmp_path: pathlib.Path
) -> None:
    """Verify the CLI performs a plain bootstrap operation."""
    # 1. Prepare
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "bootstrap": True,
        "build": False,
        "configure": False,
        "debug": False,
        "release": False,
    }

    work = tmp_path / "work"
    work.mkdir()
    os.chdir(str(work))

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
    cmake = work / "cmake"
    assert cmake.is_dir()
    cmake_file = cmake / "FindBob.cmake"
    assert cmake_file.is_file()
    ref = pathlib.Path(__file__).parent.resolve() / "ref" / "bootstrap.cmake"
    assert cmake_file.read_text().strip() == ref.read_text().strip()


def test_cli_configure_default(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a configure."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "bootstrap": False,
        "build": False,
        "configure": True,
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


def test_cli_configure_release(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a configure."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "bootstrap": False,
        "build": False,
        "configure": True,
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


def test_cli_configure_debug(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a configure."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "bootstrap": False,
        "build": False,
        "configure": True,
        "debug": True,
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
            "build/native-debug",
            "-S",
            ".",
            "-DCMAKE_BUILD_TYPE=Debug",
        ],
        check=True,
    )


def test_cli_configure_linux_default(
    mocker: pytest_mock.MockerFixture, valid_config_path: pathlib.Path  # noqa: ARG001
) -> None:
    """Verify the CLI performs the correct argument conversion for a configure."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": "linux",
        "bootstrap": False,
        "build": False,
        "configure": True,
        "debug": False,
        "release": False,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
    cwd = pathlib.Path.cwd()
    subprocess.run.assert_any_call(
        [
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
            # "-G",
            # "Ninja",
        ],
        check=True,
    )


def test_cli_configure_linux_release(
    mocker: pytest_mock.MockerFixture, valid_config_path: pathlib.Path  # noqa: ARG001
) -> None:
    """Verify the CLI performs the correct argument conversion for a configure."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": "linux",
        "bootstrap": False,
        "build": False,
        "configure": True,
        "debug": False,
        "release": True,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
    cwd = pathlib.Path.cwd()
    subprocess.run.assert_any_call(
        [
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
        ],
        check=True,
    )


def test_cli_configure_linux_debug(
    mocker: pytest_mock.MockerFixture, valid_config_path: pathlib.Path  # noqa: ARG001
) -> None:
    """Verify the CLI performs the correct argument conversion for a configure."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": "linux",
        "bootstrap": False,
        "build": False,
        "configure": True,
        "debug": True,
        "release": False,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
    cwd = pathlib.Path.cwd()
    subprocess.run.assert_any_call(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{cwd}:/work/",
            "renemoll/builder_clang",
            "cmake",
            "-B",
            "build/linux-debug",
            "-S",
            ".",
            "-DCMAKE_BUILD_TYPE=Debug",
        ],
        check=True,
    )


def test_cli_configure_stm32_default(
    mocker: pytest_mock.MockerFixture, valid_config_path: pathlib.Path  # noqa: ARG001
) -> None:
    """Verify the CLI performs the correct argument conversion for a configure."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": "stm32",
        "bootstrap": False,
        "build": False,
        "configure": True,
        "debug": False,
        "release": False,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
    cwd = pathlib.Path.cwd()
    subprocess.run.assert_any_call(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{cwd}:/work/",
            "renemoll/builder_arm_gcc",
            "cmake",
            "-B",
            "build/stm32-release",
            "-S",
            ".",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DSTM32F4",
            "-G",
            "Ninja",
        ],
        check=True,
    )


def test_cli_configure_invalid_target(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a configure."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": "dummy",
        "bootstrap": False,
        "build": False,
        "configure": True,
        "debug": True,
        "release": False,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    invalid_arguments_code = 65
    assert result == invalid_arguments_code
    subprocess.run.assert_not_called()


def test_cli_build_default(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a build."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "bootstrap": False,
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
        "bootstrap": False,
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


def test_cli_build_debug(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a build."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "bootstrap": False,
        "build": True,
        "configure": False,
        "debug": True,
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
            "build/native-debug",
            "-S",
            ".",
            "-DCMAKE_BUILD_TYPE=Debug",
        ],
        check=True,
    )
    subprocess.run.assert_any_call(
        ["cmake", "--build", "build/native-debug"], check=True
    )


def test_cli_build_linux_default(mocker: pytest_mock.MockerFixture) -> None:
    """Verify the CLI performs the correct argument conversion for a build."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": "linux",
        "bootstrap": False,
        "build": True,
        "configure": False,
        "debug": False,
        "release": False,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
    cwd = pathlib.Path.cwd()
    subprocess.run.assert_any_call(
        [
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
            # "-G",
            # "Ninja",
        ],
        check=True,
    )
    subprocess.run.assert_any_call(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{cwd}:/work/",
            "renemoll/builder_clang",
            "cmake",
            "--build",
            "build/linux-release",
        ],
        check=True,
    )


def test_cli_build_linux_release(
    mocker: pytest_mock.MockerFixture, valid_config_path: pathlib.Path  # noqa: ARG001
) -> None:
    """Verify the CLI performs the correct argument conversion for a build."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": "linux",
        "bootstrap": False,
        "build": True,
        "configure": False,
        "debug": False,
        "release": True,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
    cwd = pathlib.Path.cwd()
    subprocess.run.assert_any_call(
        [
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
            # "-G",
            # "Ninja",
        ],
        check=True,
    )
    subprocess.run.assert_any_call(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{cwd}:/work/",
            "renemoll/builder_clang",
            "cmake",
            "--build",
            "build/linux-release",
        ],
        check=True,
    )


def test_cli_build_linux_debug(
    mocker: pytest_mock.MockerFixture, valid_config_path: pathlib.Path  # noqa: ARG001
) -> None:
    """Verify the CLI performs the correct argument conversion for a build."""
    # 1. Prepare
    mocker.patch("subprocess.run")
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": "linux",
        "bootstrap": False,
        "build": True,
        "configure": False,
        "debug": True,
        "release": False,
    }

    # 2. Execute
    result = main()

    # 3. Verify
    assert result == 0
    cwd = pathlib.Path.cwd()
    subprocess.run.assert_any_call(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{cwd}:/work/",
            "renemoll/builder_clang",
            "cmake",
            "-B",
            "build/linux-debug",
            "-S",
            ".",
            "-DCMAKE_BUILD_TYPE=Debug",
        ],
        check=True,
    )
    subprocess.run.assert_any_call(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{cwd}:/work/",
            "renemoll/builder_clang",
            "cmake",
            "--build",
            "build/linux-debug",
        ],
        check=True,
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
        "bootstrap": False,
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
    cwd = pathlib.Path.cwd()
    subprocess.run.assert_called_once_with(
        ["cmake", "-E", "make_directory", f"{cwd}/cmake"],
        check=True,
    )


def test_cli_read_toml_file(
    mocker: pytest_mock.MockerFixture, valid_config_path: pathlib.Path
) -> None:
    """Verify the CLI reads and utilizes an options TOML file."""
    # 1. Prepare
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "bootstrap": True,
        "build": False,
        "configure": False,
        "debug": False,
        "release": False,
    }

    # 2. Execute
    main()

    # 3. Verify
    assert (valid_config_path / "external").is_dir()


def test_cli_error_invalid_toml_file(
    mocker: pytest_mock.MockerFixture, tmp_path: pathlib.Path
) -> None:
    """Verify the CLI reads and utilizes an options TOML file."""
    # 1. Prepare
    mocker.patch("docopt.docopt")

    docopt.docopt.return_value = {
        "--help": False,
        "--version": False,
        "<target>": None,
        "bootstrap": True,
        "build": False,
        "configure": False,
        "debug": False,
        "release": False,
    }

    work = tmp_path / "work"
    work.mkdir()
    os.chdir(str(work))

    toml_file = pathlib.Path(__file__).parent.resolve() / "config" / "invalid.toml"
    shutil.copy(toml_file, work / "bob.toml")

    # 2. Execute
    main()

    # 3. Verify
    assert not (work / "external").is_dir()
