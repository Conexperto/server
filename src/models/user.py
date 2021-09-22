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
    plans = relationship("Plan", passive_deletes=True)
    specialities = relationship(
        "AssociationSpeciality",
        cascade="all, delete, delete-orphan",
        passive_deletes=True,
    )
    methods = relationship(
        "AssociationMethod", cascade="all, delete, delete-orphan", passive_deletes=True
    )

    def __exists(self, _id, relationship, column):
        return any(getattr(item, column) == _id for item in getattr(self, relationship))

    def __get_by_id(self, _id, relationship, column):
        return next(
            filter(
                lambda item: getattr(item, column) == _id, getattr(self, relationship)
            )
        )

    def __extract(self, _id, body, column):
        return next(item.get(column) for item in body if item["id"] == _id)

    def append_specialities(self, identifiers):
        """
        Associate Specialities to the user

        Args:
            identifiers (list): List of Speciality.id

        Returns: void
        """
        __query = Speciality.query
        specialities = __query.filter(Speciality.id.in_(identifiers)).all()

        for item in specialities:
            if self.__exists(item.id, "specialities", "right_id"):
                continue
            ass_speciality = AssociationSpeciality()
            ass_speciality.speciality = item
            self.specialities.append(ass_speciality)

    def append_methods(self, body):
        """
        Associate Methods to the user

        Args:
            body (list<dict>):
                id (int): Method.id
                link (str): Method.link

        Returns: void
        """
        identifiers = [item["id"] for item in body]

        __query = Method.query
        methods = __query.filter(Method.id.in_(identifiers)).all()

        for item in methods:
            if self.__exists(item.id, "methods", "right_id"):
                continue

            link = self.__extract(item.id, body, "link")
            if not link:
                continue

            _ass_method = AssociationMethod(link=link)
            _ass_method.method = item
            self.methods.append(_ass_method)

    def append_plans(self, body):
        """
        Create plans and associates them to the user

        Args:
            body (list<dict>):
                duration (int): duration
                price (int): price
                coin (str): coin default "USD"

        Returns: void
        """
        for item in body:
            plan = Plan(duration=item["duration"], price=item["price"])
            self.plans.append(plan)

    def update_specialities(self, identifiers):
        """
        Update specialities

        Args:
            body: list identifiers specialities

        Returns: void
        """
        self.specialities = []
        __query = Speciality.query
        specialities = __query.filter(Speciality.id.in_(identifiers)).all()
        for speciality in specialities:
            ass_speciality = AssociationSpeciality()
            ass_speciality.speciality = speciality
            self.specialities.append(ass_speciality)

    def update_methods(self, body):
        """
        Update methods

        Args:
            body (list<dict>):
                id (int): AssociationMethod.id
                left_id (int): User.id
                right_id (int): Method.id

        Returns: void
        """
        to_update = []

        for item in body:
            if not self.__exists(item.get("id"), "methods", "right_id"):
                continue

            _ass_method = self.__get_by_id(item["id"], "methods", "right_id")
            _ass_method.serialize(item)

            to_update.append(_ass_method)

        self.methods = to_update
        self.append_methods(body)

    def update_plans(self, body):
        """
        Update plans

        Args:
            body (list<dict)):
                id (int): Plan.id
                duration (int): duration
                price (int): price
                coin (str): coin default "USD"

        Returns: void
        """
        to_update = []
        to_create = []

        for item in body:
            if not self.__exists(item.get("id"), "plans", "id"):
                to_create.append(item)
                continue

            _plan = self.__get_by_id(item["id"], "plans", "id")
            _plan.serialize(item)

            to_update.append(_plan)

        self.plans = to_update
        self.append_plans(to_create)
