from src.db import db 
from .audit import AuditMixin


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
        for key, val in obj.items():
            if key in self.__mapper__.c.keys():
                self[key] = val

    def deserialize(self):
        pass

    def __repr__(self):
        vals = ', '.join("%s=%r" % (n, getattr(self,n)) for n in self.__table__.c.keys() if n not in self._repr_hide)
        return "<%s={%s}>" % (self.__class__.__name__, vals)
