"""
    Model: Session
"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from src.db import db
from src.mixins import BaseMixin


class AssociationUser(BaseMixin, db.Model):
    """
    The AssociationUser model,
    is association between session and session model.
    """

    __tablename__ = "association_session_to_user"

    left_id = Column(Integer, ForeignKey("session.id"), primary_key=True)
    right_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    disabled = Column(Boolean, default=False)


class Session(BaseMixin, db.Model):
    """
    The Session model contains all the database fields.
    """

    __tablename__ = "session"

    id = Column(Integer, primary_key=True)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    disabled = Column(Boolean, default=False)
    expert_id = Column(Integer, ForeignKey("user.id"))
