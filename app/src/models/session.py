from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, ARRAY, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db import db



class AssociationUser(BaseMixin, db.Model):
    __tablename__ = 'association_session_to_user'

    left_id          = Column(Integer, ForeignKey('session.id'), primary_key=True)
    right_id         = Column(Integer, ForeignKey('user.id'), primary_key=True)
    disabled         = Column(Boolean, default=False)


class Session(BaseMixin, db.Model):
    __tablename__ = 'session'

    id              = Column(Integer, primary_key=True)
    date_start      = Column(DateTime, nullable=False)
    date_end        = Column(DateTime, nullable=False)
    duration        = Column(Integer, nullable=False)
    disabled        = Column(Boolean, default=False)
    expert_id       = Column(Integer, ForeignKey('user.id'))

