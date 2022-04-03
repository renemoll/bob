"""Tests specifically for the bootstrap command."""
import os
import pathlib

import git
import pytest_mock

import bob
from bob.bootstrap import bob_bootstrap, depends_on


def test_dependency() -> None:
    """Verify bootstraps's dependecies."""
    result = depends_on()

    assert result == []


def test_bootstrap_default_options(tmp_path: pathlib.Path) -> None:
    """Verify the default option to bootstrap a project."""
    # 1. Prepare
    options = {}
    cwd = tmp_path

    # 2. Execute
    result = bob_bootstrap(options, cwd)

    # 3. Verify
    assert len(result) == 2
    assert result[0] == ["cmake", "-E", "make_directory", f"{cwd}/cmake"]
    template_path = pathlib.Path(bob.__file__).parent / "templates"
    template = template_path / "FindBob.cmake"
    assert result[1] == ["cmake", "-E", "copy", str(template.resolve()), f"{cwd}/cmake"]


def test_bootstrap_external_git_repo(
    mocker: pytest_mock.MockerFixture, tmp_path: pathlib.Path
) -> None:
    """Verify bootstrap will clone extrnal repositories."""
    # 1. Prepare
    mocker.patch("git.Repo.clone_from")

    options = {
        "external": {
            "destination_folder": "external",
            "stm32": {
                "repository": "https://github.com/renemoll/STM32CubeF7.git",
                "tag": "master",
            },
        }
    }

    cwd = tmp_path / "work"
    cwd.mkdir()
    os.chdir(str(cwd))

    # 2. Execute
    result = bob_bootstrap(options, cwd)

    # 3. Verify
    assert len(result) == 2
    git.Repo.clone_from.assert_called_once_with(
        "https://github.com/renemoll/STM32CubeF7.git",
        str(cwd / "external" / "stm32"),
        branch="master",
    )
