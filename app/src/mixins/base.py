from collections import OrderedDict
from src.db import db 
from .audit import AuditMixin
from datetime import datetime


class BaseMixin(AuditMixin):
    _repr_hide = ['created_at', 'updated_at']
    
    def add(self):
        db.session.add(self)

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self, obj):
        for k, v in obj.items():
            if k in self.__table__.c.keys() and v:
                setattr(self, k, v)
        return self

    def deserialize(self, o=None):
        result = OrderedDict()
        for k in self.__table__.c.keys():
            if k in self._repr_hide:
                continue
            result[k] = getattr(self, k)

            if isinstance(result[k], dict):
                result[k] = self.deserialize(result[k])
            if isinstance(result[k], datetime):
                result[k] = result[k].timestamp()

        return result

    def __repr__(self):
        vals = ', '.join("%s=%r" % (n, getattr(self,n)) for n in self.__table__.c.keys() if n not in self._repr_hide)
        return "<%s={%s}>" % (self.__class__.__name__, vals)
