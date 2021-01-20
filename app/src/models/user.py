from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Booelan, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(BaseMixin, Base):
    __tablename__ = 'user'

    id              = Column(Integer, primary_key=True)
    uid             = Column(String, unique=True, nullable=False)
    display_name    = Column(String, unique=True, nullable=False)
    email           = Column(String, unique=True, nullable=False)
    phone_number    = Column(String, unique=True)
    photo_url       = Column(String)
    name            = Column(String)
    lastname        = Column(String)
    disabled        = Column(Booelan, default=False)
    rating_average  = Column(Integer, default=0)
    rating_stars    = Column(ARRAY(Integer), default=[0,0,0,0,0])
    rating_votes    = Column(Integer, default=0)
    headline        = Column(String)
    about_me        = Column(String)
    session_taken   = Column(Integer, default=0)
    expert          = relationship("Expert", uselist=False, back_populates="parent")

