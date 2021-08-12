"""
    Model: Test
"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from src.db import db
from src.helpers import generate_hash
from src.mixins import BaseMixin


class TestModel(BaseMixin, db.Model):
    """
    The TestModel is for testing only
    """

    __tablename__ = "test"

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, default=generate_hash())
    name = Column(String)
