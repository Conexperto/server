"""
    Model: Speciality
"""
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
    is association between speciality and user model.
    """

    __tablename__ = "association_user_to_speciality"

    left_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    right_id = Column(
        Integer, ForeignKey("speciality.id"), unique=True, primary_key=True
    )
    disabled = Column(Boolean, default=False)
    speciality = relationship("Speciality")


class Speciality(BaseMixin, db.Model):
    """
    The speciality model contains all the database fields.
    """

    __tablename__ = "speciality"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
