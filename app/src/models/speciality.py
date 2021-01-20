from src.mixins import BaseMixin
from sqlalchemy import String, Integer, ARRAY
from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Speciality(BaseMixin, Base):
    __tablename__ = 'speciality'

    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)        
