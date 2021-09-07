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
from src.models import AssociationMethod
from src.models import AssociationSpeciality
from src.models import Method
from src.models import Plan
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
    plans = relationship("Plan", cascade="all, delete", passive_deletes=True)
    specialities = relationship("AssociationSpeciality", cascade="all, delete")
    methods = relationship("AssociationMethod", cascade="all, delete")

    def append_specialities(self, identifiers):
        """
        Associate Specialities to the user

        Args:
            identifiers (list): List of Speciality.id

        Returns: void
        """
        __query = Speciality.query
        specialities = __query.filter(Speciality.id.in_(identifiers)).all()

        for speciality in specialities:
            if not any(item["right_id"] in identifiers for item in self.specialities):
                continue

            ass_speciality = AssociationSpeciality()
            ass_speciality.speciality.append(speciality)

            self.specialities.append(ass_speciality)

    def append_methods(self, methods):
        """
        Associate Methods to the user

        Args:
            methods (list<dict>):
                id (int): Method.id
                link (str): Method.link

        Returns: void
        """
        identifiers = [item["id"] for item in methods]

        __query = Method.query
        _methods = __query.filter(Method.id.in_(identifiers)).all()

        for _method in _methods:
            if not any(item["right_id"] in identifiers for item in self.methods):
                continue

            link = next(
                [item["link"] for item in methods if item["id"] == _method.id], None
            )
            if not link:
                continue

            _ass_method = AssociationMethod(link=link)
            _ass_method.method.append(_method)

            self.methods.append(_ass_method)

    def append_plans(self, plans):
        """
        Create plans and associates them to the user

        Args:
            plans (list<dict>):
                duration (int): duration
                price (int): price
                coin (str): coin default "USD"

        Returns: void
        """
        for item in plans:
            if not any(_item.id == item["id"] for _item in self.plans):
                continue

            plan = Plan(
                duration=item["duration"], price=item["price"], coin=item["coin"]
            )
            self.plans.append(plan)

    def update_specialities(self, ass_specialities):
        """
        Update specialities

        Args:
            specialities (list<dict>):
                id (int): AssociationSpeciality.id
                left_id (int): User.id
                right_id (int): Speciality.id

        Returns: void
        """
        to_update = []

        for item in ass_specialities:
            if not any(_item.id == item["id"] for _item in self.specialities):
                continue

            _ass_speciality = next(
                filter(lambda x: x.id == item["id"], self.specialities)
            )
            _ass_speciality.serialize(item)

            to_update.append(_ass_speciality)

        self.methods = to_update

    def update_methods(self, ass_methods):
        """
        Update methods

        Args:
            methods (list<dict>):
                id (int): AssociationMethod.id
                left_id (int): User.id
                right_id (int): Method.id

        Returns: void
        """
        to_update = []

        for item in ass_methods:
            if not any(_item.id == item["id"] for _item in self.methods):
                continue

            _ass_method = next(filter(lambda x: x.id == item["id"], self.methods))
            _ass_method.serialize(item)

            to_update.append(_ass_method)

        self.methods = to_update

    def update_plans(self, plans):
        """
        Update plans

        Args:
            plans (list<dict)):
                id (int): Plan.id
                duration (int): duration
                price (int): price
                coin (str): coin default "USD"

        Returns: void
        """
        to_update = []

        for item in plans:
            if not any(_item.id == item["id"] for _item in self.plans):
                continue

            _plan = next(filter(lambda x: x.id == item["id"], self.plans))
            _plan.serialize(item)

            to_update.append(_plan)

        self.plans = to_update
