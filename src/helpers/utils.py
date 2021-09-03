""" src.helpers.utils """
from uuid import uuid4

__all__ = ["inc", "dec", "generate_hash", "parse_order"]


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


def parse_order(order):
    if str(order).isnumeric():
        __order = int(order)
        if __order == 1:
            return "asc"
        if __order == -1:
            return "desc"
    return order or None
