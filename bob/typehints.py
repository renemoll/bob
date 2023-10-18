"""Provide type hints for commonly used types."""
import typing

from .api import BuildConfig, BuildTarget

OptionsT = typing.TypeVar("OptionsT", BuildConfig, BuildTarget)
OptionsMapT = typing.Mapping[str, typing.Mapping[str, OptionsT]]
