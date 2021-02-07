import json
import flask
import inspect
from collections import OrderedDict
from datetime import datetime

try:
    from flask_sqlalchemy.model import Model
    from src.mixins import Record
except ImportError as e:
    print(str(e))

class JSONEncoder(json.JSONEncoder):
    
    def default(self, o):
        if isinstance(o, Model):
            return dict(o.deserialize())
       
        if isinstance(o, Record):
            return dict(o.deserialize())

        return flask.json.JSONEncoder.default(self, o)

def JSONSerializable(app=None, **kwargs):
    if app is not None:
        app.json_encoder = JSONEncoder
