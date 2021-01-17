from src.mixins import BaseMixin
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.db import db
from src.helpers import generate_hash


class TestModel(BaseMixin, db.Model):
    __tablename__ = 'test'

    id              = Column(Integer, primary_key=True)
    uid             = Column(String, unique=True, default=generate_hash())
    name            = Column(String)
