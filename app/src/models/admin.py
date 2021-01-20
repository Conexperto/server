from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Booelan, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Admin(BaseMixin, Base):
    __tablename__ = 'admin'

    id              = Column(Integer, primary_key=True)
    uid             = Column(String, unique=True, nullable=False)
    display_name    = Column(String, unique=True, nullable=False)
    email           = Column(String, unique=True, nullable=False)
    phone_number    = Column(String, unique=True)
    photo_url       = Column(String)
    name            = Column(String)
    lastname        = Column(String)
    disabled        = Column(Booelan, default=False)

