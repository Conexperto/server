from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Boolean, ARRAY
from sqlalchemy.orm import relationship
from firebase_admin import auth
from src.firebase import web_sdk
from src.db import db



class User(BaseMixin, db.Model):
    __tablename__ = 'user'

    id                  = Column(Integer, primary_key=True)
    uid                 = Column(String, unique=True, nullable=False)
    display_name        = Column(String, unique=True, nullable=False)
    email               = Column(String, unique=True, nullable=False)
    phone_number        = Column(String, unique=True)
    photo_url           = Column(String)
    name                = Column(String)
    lastname            = Column(String)
    disabled            = Column(Boolean, default=False)
    rating_average      = Column(Integer, default=0)
    rating_stars        = Column(ARRAY(Integer), default=[0,0,0,0,0])
    rating_votes        = Column(Integer, default=0)
    headline            = Column(String(60))
    about_me            = Column(String(150))
    session_taken       = Column(Integer, default=0)
    complete_register   = Column(Boolean, default=False) 
    timezone            = Column(Integer, default=0)
    expert              = relationship("Expert", uselist=False, back_populates="user")
    

    def create_user(self, password):
        user = auth.create_user(
            email=self.email,
            passwortd=password,
            display_name=self.display_name, app=web_sdk)

        self.uid = user.uid


    def update_user(self, password):
        auth.update_user(
                uid=self.uid,
                email=self.email,
                password=password,
                display_name=self.display_name,
                phone_number=self.phone_number,
                photo_url=self.photo_url,
                disabled=self.disabled, app=web_sdk)

    def delete_user(self):
        auth._delete_user(uid=self.uid, app=web_sdk)

    def make_claims(self):
        auth.set_custom_user_claims(
                self.uid,
                { 'complete_register': self.complete_register })
