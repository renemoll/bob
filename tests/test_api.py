from bob.api import BuildConfig, BuildTarget, Command


def test_command_to_string():
    assert str(Command.Build) == "Build"


def test_buildconfig_to_string():
    assert str(BuildConfig.Release) == "Release"


def test_buildtarget_to_string():
    assert str(BuildTarget.Native) == "Native"
