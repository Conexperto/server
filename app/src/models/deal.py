from src.mixins import BaseMixin
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.db import db
from src.helpers import generate_hash


class Deal(BaseMixin, db.Model):
    __tablename__ = 'deal'

    id                      = Column(Integer, primary_key=True)
    uid                     = Column(String(64), unique=True, default=generate_hash())

    
