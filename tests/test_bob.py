import bob


def test_bob():

    cmd = bob.Command.Build
    options = {}

    result = bob.bob(cmd, options)

    assert result == None
