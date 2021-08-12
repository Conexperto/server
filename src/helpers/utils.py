""" src.helpers.utils """
from uuid import uuid4

__all__ = ["inc", "dec", "generate_hash"]


def inc(i):
    """
    Increment count
    """
    return i + 1


def dec(i):
    """
    Decrement count
    """
    return i - 1


def generate_hash():
    """
    Generate randon hash
    """
    return uuid4().hex
