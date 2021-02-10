from sqlalchemy.ext.declarative import DeclarativeMeta
from flask.json import JSONEncoder
from src.mixins import Record


class JSONEncoder(JSONEncoder):
    
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            return o.deserialize()
        if isinstance(o, Record):
            return o.deserialize()
        return super(JSONEncoder, self).default(o)


def JSONSerializable(app=None, **kwargs):
    if app is not None:
        app.json_encoder = JSONEncoder
