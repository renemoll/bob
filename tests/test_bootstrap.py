"""Tests specifically for the bootstrap command."""
import os
import pathlib

import bob
from bob.tasks.bootstrap import depends_on, generate_commands, parse_options


def test_dependency() -> None:
    """Verify bootstraps's dependecies."""
    result = depends_on()

    assert result == []


def test_bootstrap_default_options(tmp_path: pathlib.Path) -> None:
    """Verify the default option to bootstrap a project."""
    # 1. Prepare
    options = {}
    options = parse_options(options)
    env = {"root_path": tmp_path}

    # 2. Execute
    result = generate_commands(options, env)

    # 3. Verify
    nof_commands = 2
    assert len(result) == nof_commands
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
    options = parse_options(options)

    cwd = tmp_path / "work"
    cwd.mkdir()
    os.chdir(str(cwd))

    env = {"dependencies_path": cwd / "external", "root_path": cwd}

    # 2. Execute
    result = generate_commands(options, env)

    # 3. Verify
    nof_commands = 4
    assert len(result) == nof_commands
    assert result[2] == [
        "git",
        "clone",
        "https://github.com/renemoll/bob-cmake.git",
        str(cwd / "external" / "test"),
    ]
    assert result[3] == [
        "cmake",
        "-E",
        "chdir",
        str(env["dependencies_path"] / "test"),
        "git",
        "checkout",
        "master",
    ]


def test_bootstrap_external_git_repo_already_present(tmp_path: pathlib.Path) -> None:
    """Verify bootstrap clone if the repo is already present."""
    # 1. Prepare
    options = {
        "dependencies": {
            "test": {
                "repository": "https://github.com/renemoll/bob-cmake.git",
                "tag": "master",
            },
        }
    }
    options = parse_options(options)

    cwd = tmp_path / "work"
    cwd.mkdir()
    os.chdir(str(cwd))
    repo_path = cwd / "external" / "test"
    repo_path.mkdir(parents=True)

    env = {"dependencies_path": cwd / "external", "root_path": cwd}

    # 2. Execute
    result = generate_commands(options, env)

    # 3. Verify
    nof_commands = 3
    assert len(result) == nof_commands
    assert result[2] == [
        "cmake",
        "-E",
        "chdir",
        str(env["dependencies_path"] / "test"),
        "git",
        "checkout",
        "master",
    ]


def test_bootstrap_no_dependencies_no_toolchains(tmp_path: pathlib.Path) -> None:
    """Verify bootstrap without any dependencies and toolchains."""
    # 1. Prepare
    options = {"dependencies": {}, "toolchains": {}}
    options = parse_options(options)

    cwd = tmp_path / "work"
    cwd.mkdir()
    os.chdir(str(cwd))

    env = {"dependencies_path": cwd / "external", "root_path": cwd}

    # 2. Execute
    result = generate_commands(options, env)

    # 3. Verify
    nof_commands = 2
    assert len(result) == nof_commands
