"""Provide type hints for commonly used types."""
import typing

from .api import BuildTarget, BuildConfig

OptionsType = typing.TypeVar("OptionsType", BuildConfig, BuildTarget)
OptionsMapType = typing.Mapping[str, typing.Mapping[str, OptionsType]]
