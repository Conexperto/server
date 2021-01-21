from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Boolean, ARRAY
from sqlalchemy.orm import relationship
from firebase_admin import auth
from src.firebase import admin_sdk
from enum import Enum
from src.db import db



class Privilegies(Enum):
    SuperRoot   = 0
    Root        = 1
    Admin       = 2
    User        = 3


class Admin(BaseMixin, db.Model):
    __tablename__ = 'admin'

    id              = Column(Integer, primary_key=True)
    uid             = Column(String, unique=True, nullable=False)
    display_name    = Column(String, unique=True, nullable=False)
    email           = Column(String, unique=True, nullable=False)
    phone_number    = Column(String, unique=True)
    photo_url       = Column(String)
    name            = Column(String)
    lastname        = Column(String)
    disabled        = Column(Boolean, default=False)
    privilegies     = Column(Integer, default=Privilegies.User)

    def create_user(self):
        user = auth.create_user(
            email=self.email,
            passwortd=self.password,
            display_name=self.display_name, app=admin_sdk)

        self.uid = user.uid

    def update_user(self):
        auth.update_user(
                uid=self.uid,
                email=self.email,
                password=self.password,
                display_name=self.display_name,
                phone_number=self.phone_number,
                photo_url=self.photo_url,
                disabled=self.disabled, app=admin_sdk)

    def disabled_user(self):
        auth.update_user(
                uid=self.uid, 
                disabled= not self.disabled, app=admin_sdk)

    def delete_user(self):
        auth.delete_user(uid=self.uid, app=admin_sdk)

    def make_claims(self):
        auth.set_custom_user_claims(
                self.uid,
                { 'admin': True, 'access_level': self.privilegies }, app=admin_sdk)

    def is_super_root(self):
        return self.privilegies is Privilegies.SuperRoot

    def is_root(self):
        return self.privilegies is Privilegies.Root

    def is_admin(self):
        return self.privilegies is Privilegies.Admin

    def is_user(self):
        return self.privilegies is Privilegies.User

    def hasAccess(self, access):
        return self.privilegies <= access
