"""
    Model: User
"""
from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.db import db
from src.mixins import BaseMixin
from src.models import AssociationSpeciality
from src.models import Speciality


class User(BaseMixin, db.Model):
    """
    The User model contains all the database fields.
    """

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
    link_video = Column(String)
    location = Column(String)
    plans = relationship("Plan")
    specialities = relationship("AssociationSpeciality")
    methods = relationship("AssociationMethod")

    def append_speciality(self, identifier):
        """
        Associate Specialities to the user

        Args:
            identifiers (list): List of _id associated with the speciality

        Returns: void
        """
        __query = Speciality.query
        speciality = __query.filter(Speciality.id.in_(identifier)).all()
        ass_speciality = AssociationSpeciality()
        ass_speciality.speciality.append(speciality)
        self.specialities.append(ass_speciality)
