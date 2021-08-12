"""
    Model: Expert
"""
from sqlalchemy import ARRAY
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.db import db
from src.mixins import BaseMixin


class AssociationSpeciality(BaseMixin, db.Model):
    """
    The AssociationSpeciality model,
    is association between speciality and expert models.
    """

    __tablename__ = "association_expert_to_speciality"

    left_id = Column(Integer, ForeignKey("expert.id"), primary_key=True)
    right_id = Column(Integer, ForeignKey("speciality.id"), primary_key=True)
    disabled = Column(Boolean, default=False)
    speciality = relationship("Speciality")


class AssociationMethod(BaseMixin, db.Model):
    """
    The AssociationMethod model,
    is association between method and expert models.
    """

    __tablename__ = "association_expert_to_method"

    left_id = Column(Integer, ForeignKey("expert.id"), primary_key=True)
    right_id = Column(Integer, ForeignKey("method.id"), primary_key=True)
    link = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    method = relationship("Method")


class Expert(BaseMixin, db.Model):
    """
    The Expert model contains all the database fields.
    """

    __tablename__ = "expert"

    id = Column(Integer, primary_key=True)
    headline = Column(String)
    about_expert = Column(String)
    rating_average = Column(Integer, default=0)
    rating_stars = Column(ARRAY(Integer), default=[0, 0, 0, 0, 0])
    rating_votes = Column(Integer, default=0)
    link_video = Column(String)
    disabled = Column(Boolean, default=False)
    session_done = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", uselist=False, back_populates="expert")
    speciality = relationship("AssociationSpeciality")
    method = relationship("AssociationMethod")
    plan = relationship("Plan")
