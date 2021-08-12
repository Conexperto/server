"""
    Model: Method
"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from src.db import db
from src.mixins import BaseMixin


class Method(BaseMixin, db.Model):
    """
    The Method model contains all the database fields.
    """

    __tablename__ = "method"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
