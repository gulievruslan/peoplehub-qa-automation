"""Module contains custom types"""
from typing import Annotated, Generator, TypeVar

import pytest

T = TypeVar('T')

Fixture = Annotated[T, pytest.fixture]
FixtureYield = Generator[T, None, None]
