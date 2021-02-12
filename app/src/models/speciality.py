from src.mixins import BaseMixin
from sqlalchemy import String, Integer, ARRAY, Boolean
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from src.db import db



class Speciality(BaseMixin, db.Model):
    __tablename__ = 'speciality'

    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)        
    disabled        = Column(Boolean, default=False)
