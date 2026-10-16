"""Module contains custom types"""
from collections.abc import Generator
from typing import Annotated, TypeVar

import pytest

T = TypeVar('T')

Fixture = Annotated[T, pytest.fixture]
FixtureYield = Generator[T, None, None]
