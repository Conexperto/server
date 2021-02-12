from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Boolean, ARRAY
from sqlalchemy.orm import relationship
from src.db import db



class Method(BaseMixin, db.Model):
    __tablename__ = 'method'

    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    disabled        = Column(Boolean, default=False)

