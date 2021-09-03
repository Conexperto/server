"""
    Model: Admin
"""
from enum import Enum

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from src.db import db
from src.mixins import BaseMixin


class Privileges(Enum):
    """
    Enum Privileges
    """

    SuperRoot = 0
    Root = 1
    Admin = 2
    User = 3

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    def __str__(self):
        return str(self.value)


class Admin(BaseMixin, db.Model):
    """
    The Admin model contains all the database fields.
    """

    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True)
    photo_url = Column(String)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    privileges = Column(Integer, default=Privileges.User.value)

    def is_super_root(self):
        """Returns a boolean if the user has superroot privileges."""
        return self.privileges == Privileges.SuperRoot.value

    def is_root(self):
        """Returns a boolean if the user has root privileges."""
        return self.privileges == Privileges.Root.value

    def is_admin(self):
        """Returns a boolean if the user has admin privileges."""
        return self.privileges == Privileges.Admin.value

    def is_user(self):
        """Returns a boolean if the user has user privileges."""
        return self.privileges == Privileges.User.value

    def has_access(self, access, strict=False):
        """
        Returns a boolean if the user has access

            Parameters:
                access (int): The integer access level from Privileges Enum
                strict (bool): Specify access desc to user

            Returns:
                access (bool)
        """
        if self.is_super_root():  # superroot have all access
            return True

        return self.privileges < access if strict else self.privileges <= access
