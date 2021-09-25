""" src.helpers.utils """
import re
from uuid import uuid4

__all__ = ["inc", "dec", "generate_hash", "parse_order", "computed_operator"]


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


def computed_operator(column, v):
    """
    Computed operator, extracted from the query
    value to assign it to a column

    Args:
        column (sqlalchemy.Column): column to assign operator
        v (str): value with operator and value e.g `!=value`

    Returns operator binary
    """
    if re.match(r"!=", v):
        """__ne__"""
        return column.__ne__(v)
    if re.match(r">(?!=)", v):
        """__gt__"""
        return column.__gt__(v)
    if re.match(r"<(?!=)", v):
        """__lt__"""
        return column.__lt__(v)
    if re.match(r">=", v):
        """__ge__"""
        return column.__ge__(v)
    if re.match(r"<=", v):
        """__le__"""
        return column.__le__(v)
    if re.match(r"(\w*),(\w*)", v):
        """between"""
        a, b = re.split(r",", v)
        return column.between(a, b)
    """ default __eq__ """
    return column.__eq__(v)
