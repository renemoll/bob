"""Tests specifically for the configure command."""
import pathlib

import bob
from bob.api import generate_targets
from bob.common import parse_options
from bob.tasks.configure import depends_on, generate_commands, parse_env


def test_dependency() -> None:
    """Verify commands's dependecies."""
    result = depends_on()

    assert result == []


def test_configure_default_options(tmp_path: pathlib.Path) -> None:
    """Verify the default options generate a valid configure command.

    Todo:
    - Actually default the options?
    """
    # 1. Prepare
    targets = generate_targets(["native"])
    options = {
        "build": {"config": bob.BuildConfig.Release, "target": targets.Native},
    }
    options = parse_options(options)
    env = {"root_path": tmp_path}
    env = parse_env(env, options)

    # 2. Execute
    result = generate_commands(options, env)

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


def test_configure_with_container_linux_clang(tmp_path: pathlib.Path) -> None:
    """Verify Linux build triggers the use of a Linux container."""
    # 1. Prepare
    targets = generate_targets(["native", "linux"])
    options = {
        "build": {"config": bob.BuildConfig.Release, "target": targets.Linux},
        "toolchains": {"linux": {"container": "renemoll/builder_clang"}},
        "targets": {"linux": {"toolchain": "linux"}},
    }
    options = parse_options(options)
    env = {"root_path": tmp_path}
    env = parse_env(env, options)

    # 2. Execute
    result = generate_commands(options, env)

    # 3. Verify
    assert len(result) == 1
    assert result[0] == [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{env['root_path']}:/work/",
        "renemoll/builder_clang",
        "cmake",
        "-B",
        "build/linux-release",
        "-S",
        ".",
        "-DCMAKE_BUILD_TYPE=Release",
        # "-G",
        # "Ninja",
    ]
