from random import randint
from faker import Faker
from src.models import User, \
                        Expert, \
                        Speciality, \
                        AssociationMethod, \
                        AssociationSpeciality, \
                        Method, \
                        Plan

faker = Faker()

class ExpertSeed():
    __seed__ = 'expert'

    def __init__(self):
        user = User.query.filter_by(email='conexpertotesting@gmail.com').first()

        self.__model = Expert(
                headline=faker.text(60),
                about_expert=faker.text(150),
                link_video=faker.image_url(),
                user_id=user.id)
        
        relation_a = AssociationSpeciality()
        relation_a.speciality = Speciality(name=faker.job())
        self.__model.teachs.append(relation_a) 


        relation_b = AssociationMethod(link=faker.image_url())
        relation_b.method = Method(name=faker.domain_word())
        self.__model.methods.append(relation_b)
        
        relation_c = Plan(
                duration=randint(0, 60),
                price=randint(0, 20))
        self.__model.plans.append(relation_c)

    def run(self):
        self.__model.add()
        self.__model.save()
