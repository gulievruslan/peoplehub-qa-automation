"""Module contains custom types"""
from typing import TypedDict


class AuthData(TypedDict):
    """Authentication data type"""
    email: str
    password: str