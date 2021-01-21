from src.mixins import BaseMixin
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, ARRAY 
from sqlalchemy.orm import relationship
from src.db import db



class AssociationSpeciality(BaseMixin, db.Model):
    __tablename__ = 'association_expert_to_speciality'
    
    left_id          = Column(Integer, ForeignKey('expert.id'), primary_key=True)
    right_id         = Column(Integer, ForeignKey('speciality.id'), primary_key=True)


class AssociationMethod(BaseMixin, db.Model):
    __tablename__ = 'association_expert_to_method'

    left_id         = Column(Integer, ForeignKey('expert.id'), primary_key=True)
    right_id        = Column(Integer, ForeignKey('method.id'), primary_key=True)
    link            = Column(String, nullable=False)


class Expert(BaseMixin, db.Model):
    __tablename__ = 'expert'

    id              = Column(Integer, primary_key=True)
    headline        = Column(String)
    about_expert    = Column(String)
    rating_average  = Column(Integer, default=0)
    rating_stars    = Column(ARRAY(Integer), default=[0,0,0,0,0])
    rating_votes    = Column(Integer, default=0)
    link_video      = Column(String)
    session_done    = Column(Integer, default=0)
    user_id         = Column(Integer, ForeignKey('user.id'))
    user            = relationship("User", uselist=False, back_populates="expert")
    teach           = relationship("AssociationSpeciality")
    methods         = relationship("AssociationMethod")
    plans           = relationship("Plan")




