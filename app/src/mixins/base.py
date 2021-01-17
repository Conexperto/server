from src.db import db 
from .audit import AuditMixin


class BaseMixin(AuditMixin):
    _repr_hide = ['created_at', 'updated_at']

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        vals = ', '.join("%s=%r" % (n, getattr(self,n)) for n in self.__table__.c.keys() if n not in self._repr_hide)
        return "<%s={%s}>" % (self.__class__.__name__, vals)
