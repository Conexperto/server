"""
    Model: Method
"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.db import db
from src.mixins import BaseMixin


class AssociationMethod(BaseMixin, db.Model):
    """
    The AssociationMethod model,
    is association between method and expert models.
    """

    __tablename__ = "association_user_to_method"

    left_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    right_id = Column(Integer, ForeignKey("method.id"), unique=True, primary_key=True)
    link = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    method = relationship("Method")


class Method(BaseMixin, db.Model):
    """
    The Method model contains all the database fields.
    """

    __tablename__ = "method"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
