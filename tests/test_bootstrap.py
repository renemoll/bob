"""Tests specifically for the bootstrap command."""
import os
import pathlib

import bob
from bob.tasks.bootstrap import depends_on, generate_commands


def test_dependency() -> None:
    """Verify bootstraps's dependecies."""
    result = depends_on()

    assert result == []


def test_bootstrap_default_options(tmp_path: pathlib.Path) -> None:
    """Verify the default option to bootstrap a project."""
    # 1. Prepare
    options = {}
    env = {"root_path": tmp_path}

    # 2. Execute
    result = generate_commands(options, env)

    # 3. Verify
    assert len(result) == 2
    assert result[0] == ["cmake", "-E", "make_directory", f"{env['root_path']}/cmake"]
    template_path = pathlib.Path(bob.__file__).parent / "templates"
    template = template_path / "FindBob.cmake"
    assert result[1] == [
        "cmake",
        "-E",
        "copy",
        str(template.resolve()),
        f"{env['root_path']}/cmake",
    ]


def test_bootstrap_external_git_repo(tmp_path: pathlib.Path) -> None:
    """Verify bootstrap will clone extrnal repositories."""
    # 1. Prepare
    options = {
        "dependencies": {
            "test": {
                "repository": "https://github.com/renemoll/bob-cmake.git",
                "tag": "master",
            },
        }
    }

    cwd = tmp_path / "work"
    cwd.mkdir()
    os.chdir(str(cwd))

    env = {"dependencies_path": cwd / "external", "root_path": cwd}

    # 2. Execute
    result = generate_commands(options, env)

    # 3. Verify
    assert len(result) == 3
    assert result[2] == [
        "git",
        "clone",
        "-b",
        "master",
        "https://github.com/renemoll/bob-cmake.git",
        str(cwd / "external" / "test"),
    ]
