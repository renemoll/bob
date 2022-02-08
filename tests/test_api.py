
from bob.api import Command

def test_command_to_string():
    assert(str(Command.Build)) == "build"
