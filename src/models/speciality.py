"""
    Model: Speciality
"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from src.db import db
from src.mixins import BaseMixin


class Speciality(BaseMixin, db.Model):
    """
    The speciality model contains all the database fields.
    """

    __tablename__ = "speciality"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
