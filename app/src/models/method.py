from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Booelan, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Method(BaseMixin, Base):
    __tablename__ = 'method'

    id              = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)

