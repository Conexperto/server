from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, ARRAY 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Plan(BaseMixin, Base):
    __tablename__ = 'plan'

    id              = Column(Integer, primary_key=True)
    duration        = Column(Integer, nullable=False)
    price           = Column(Integer, nullable=False)
    coin            = Column(String, default="USD")




