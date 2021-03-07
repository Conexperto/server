from src.db import db 
from .audit import AuditMixin
from datetime import datetime
from sqlalchemy.ext.declarative import DeclarativeMeta


class BaseMixin(AuditMixin):
    __repr_hide = ['updated_at']
    __insert_hide = []
    
    @property
    def _repr_hide(self):
        return self.__repr_hide;
    
    @_repr_hide.setter
    def _repr_hide(self, k):
        self.__repr_hide.append(k)
    
    @property
    def _insert_hide(self):
        return self.__insert_hide
    
    @_insert_hide.setter
    def _insert_hide(self, k):
        self.__insert_hide.append(k)

    def add(self):
        db.session.add(self)

    def save(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def serialize(self, obj):
        for k, v in obj.items():
            if k in self.__repr_hide:
                continue
            if k in self.__insert_hide:
                continue
            if k in self.__table__.c.keys():
                setattr(self, k, v)
        return self

    def deserialize(self, backref=None):
        res = dict()

        for attr, col in self.__mapper__.c.items():
            if attr in self.__repr_hide:
                continue
            res[col.key] = getattr(self, attr)
       
        for attr, relation in self.__mapper__.relationships.items():
            if attr == str(backref):
                continue
            key = relation.key
            value = getattr(self, attr)
            if value is None:
                res[key] = None
            elif isinstance(value.__class__, DeclarativeMeta):
                res[key] = value.deserialize(backref=self.__table__)
            else:
                res[key] = [i.deserialize(backref=self.__table__) 
                                            for i in value]
        return res

    def __iter__(self):
        return self.deserialize().iteritems()

    def __repr__(self):
        vals = ', '.join("%s=%r" % (n, getattr(self,n)) for n in self.__table__.c.keys() if n not in self.__repr_hide)
        return "<%s={%s}>" % (self.__class__.__name__, vals)
