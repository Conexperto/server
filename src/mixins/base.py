""" src.mixins.base """
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.orm import RelationshipProperty

from src.db import db
from src.exceptions import HandlerException
from src.mixins.audit import AuditMixin


class BaseMixin(AuditMixin):
    """BaseMixin"""

    __repr_hide = ["created_at", "updated_at"]
    __insert_hide = []

    @property
    def _repr_hide(self):
        return self.__repr_hide

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
        """add"""
        try:
            db.session.add(self)
        except IntegrityError as ex:
            db.session.rollback()
            raise HandlerException(400, "Bad request", str(ex))
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise HandlerException(500, "Unexpected response", str(ex))

    def save(self):
        """save"""
        try:
            db.session.commit()
            db.session.refresh(self)
        except IntegrityError as ex:
            db.session.rollback()
            raise HandlerException(400, "Bad request", str(ex))
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise HandlerException(500, "Unexpected response", str(ex))

    def delete(self):
        """delete"""
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as ex:
            db.session.rollback()
            raise HandlerException(500, "Unexpected response", str(ex))

    def serialize(self, obj):
        """serialize from json"""
        for k, v in obj.items():
            if k in self.__repr_hide:
                continue
            if k in self.__insert_hide:
                continue
            if k in self.__table__.c.keys():
                setattr(self, k, v)
        return self

    def deserialize(self, backref=None):
        """deserialize to json"""
        res = dict()

        for prop in class_mapper(self.__class__).iterate_properties:
            if prop.key in self.__repr_hide:
                continue
            if isinstance(prop, ColumnProperty):
                res[prop.key] = getattr(self, prop.key)

        for prop in class_mapper(self.__class__).iterate_properties:
            if prop.key in self.__repr_hide:
                continue
            if isinstance(prop, RelationshipProperty):
                if prop.key == str(backref):
                    continue
                key, value = prop.key, getattr(self, prop.key)
                if value is None:
                    res[key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[key] = value.deserialize(backref=self.__table__)
                else:
                    res[key] = [i.deserialize(backref=self.__table__) for i in value]
        return res

    def __iter__(self):
        return iter(self.deserialize().items())

    def __repr__(self):
        vals = ", ".join(
            "%s=%r" % (n, getattr(self, n))
            for n in self.__table__.c.keys()
            if n not in self._repr_hide
        )

        return "<%s={%s}>" % (self.__class__.__name__, vals)
