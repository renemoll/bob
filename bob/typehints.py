"""Provide type hints for commonly used types."""
import pathlib
import typing


OptionsMapT = typing.MutableMapping[str, typing.Any]
EnvMapT = typing.MutableMapping[str, pathlib.Path]
CommandListT = typing.List[typing.List[str]]
