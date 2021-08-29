from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.db import db
from src.mixins import BaseMixin


class User(BaseMixin, db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)
    photo_url = Column(String)
    name = Column(String)
    lastname = Column(String)
    disabled = Column(Boolean, default=False)
    rating_average = Column(Integer, default=0)
    rating_stars = Column(ARRAY(Integer), default=[0, 0, 0, 0, 0])
    rating_votes = Column(Integer, default=0)
    headline = Column(String(60))
    about_me = Column(String(150))
    session_taken = Column(Integer, default=0)
    complete_register = Column(Boolean, default=False)
    timezone = Column(String)
    expert = relationship(
        "Expert", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
