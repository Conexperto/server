"""
    Model: Plan
"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from src.db import db
from src.mixins import BaseMixin


class Plan(BaseMixin, db.Model):
    """
    The Plan model contains all the database fields.
    """

    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    duration = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    coin = Column(String, default="USD")
    disabled = Column(Boolean, default=False)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="cascade", onupdate="cascade")
    )
