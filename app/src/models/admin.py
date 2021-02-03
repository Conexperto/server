from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Boolean, ARRAY
from sqlalchemy.orm import relationship
from enum import Enum
from src.db import db



class Privilegies(Enum):
    SuperRoot   = 0
    Root        = 1
    Admin       = 2
    User        = 3    
    
    def __str__(self):
        return str(self.value)


class Admin(BaseMixin, db.Model):
    __tablename__ = 'admin'

    id              = Column(Integer, primary_key=True)
    uid             = Column(String, unique=True, nullable=False)
    display_name    = Column(String, unique=True, nullable=False)
    email           = Column(String, unique=True, nullable=False)
    phone_number    = Column(String, unique=True)
    photo_url       = Column(String)
    name            = Column(String, nullable=False)
    lastname        = Column(String, nullable=False)
    disabled        = Column(Boolean, default=False)
    privilegies     = Column(Integer, default=Privilegies.User.value)


    def is_super_root(self):
        return self.privilegies == Privilegies.SuperRoot

    def is_root(self):
        return self.privilegies == Privilegies.Root

    def is_admin(self):
        return self.privilegies == Privilegies.Admin

    def is_user(self):
        return self.privilegies == Privilegies.User

    def hasAccess(self, access):
        return self.privilegies <= access
