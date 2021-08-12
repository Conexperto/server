""" helpers.json_serializable """
from flask.json import JSONEncoder as __JSONEncoder
from sqlalchemy.ext.declarative import DeclarativeMeta
from src.mixins import Record


# pylint: disable=super-with-arguments
class JSONEncoder(__JSONEncoder):
    """JSONEncoder"""

    def default(self, o):
        """default"""
        if isinstance(o.__class__, DeclarativeMeta):
            return o.deserialize()
        if isinstance(o, Record):
            return o.deserialize()
        return super(JSONEncoder, self).default(o)


def JSONSerializable(app=None):
    """JSONSerializable"""
    if app is not None:
        app.json_encoder = JSONEncoder
