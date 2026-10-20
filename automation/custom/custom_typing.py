"""Module contains custom types."""
from collections.abc import Generator
from typing import Annotated

import pytest

type Fixture[T] = Annotated[T, pytest.fixture]
type FixtureYield[T] = Generator[T, None, None]