""" src.helpers.utils """
import os
import re
from uuid import uuid4

__all__ = [
    "inc",
    "dec",
    "generate_hash",
    "parse_order",
    "computed_operator",
    "env_is_dev",
    "env_is_prod",
]


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


def env_is_dev():
    return os.getenv("FLASK_ENV") == "development"


def env_is_prod():
    return os.getenv("FLASK_ENV") == "production"


def computed_operator(column, v):
    """
    Computed operator, extracted from the query
    value to assign it to a column

    Args:
        column (sqlalchemy.Column): column to assign operator
        v (str): value with operator and value e.g `!=value`

    Returns operator binary
    """
    if re.match(r"^!", v):
        """__ne__"""
        val = re.sub(r"!", "", v)
        return column.__ne__(val)
    if re.match(r">(?!=)", v):
        """__gt__"""
        val = re.sub(r">(?!=)", "", v)
        return column.__gt__(val)
    if re.match(r"<(?!=)", v):
        """__lt__"""
        val = re.sub(r"<(?!=)", "", v)
        return column.__lt__(val)
    if re.match(r">=", v):
        """__ge__"""
        val = re.sub(r">=", "", v)
        return column.__ge__(val)
    if re.match(r"<=", v):
        """__le__"""
        val = re.sub(r"<=", "", v)
        return column.__le__(val)
    if re.match(r"(\w*),(\w*)", v):
        """between"""
        a, b = re.split(r",", v)
        return column.between(a, b)
    """ default __eq__ """
    return column.__eq__(v)
