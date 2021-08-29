from random import randint

from faker import Faker

from src.models import AssociationMethod
from src.models import AssociationSpeciality
from src.models import Expert
from src.models import Method
from src.models import Plan
from src.models import Speciality
from src.models import User

faker = Faker()


class ExpertSeed:
    __seed__ = "expert"

    def __init__(self):
        user = User.query.filter_by(email="conexpertotesting@gmail.com").first()

        self.__model = Expert(
            headline=faker.text(60),
            about_expert=faker.text(150),
            link_video=faker.image_url(),
            user_id=user.id,
        )

        self.__speciality = Speciality(name=faker.job())
        self.__speciality.add()
        self.__speciality.save()

        self.__method = Method(name=faker.domain_word())
        self.__method.add()
        self.__method.save()

    def run(self):
        self.__model.add()
        self.__model.save()
        self.rel()

    def rel(self):
        plan = Plan(
            duration=randint(0, 60), price=randint(0, 20), expert_id=self.__model.id
        )
        plan.add()
        plan.save()
        relation_a = AssociationSpeciality(
            left_id=self.__model.id, right_id=self.__speciality.id
        )
        relation_b = AssociationMethod(
            left_id=self.__model.id, right_id=self.__method.id
        )
        relation_a.add()
        relation_a.save()
        relation_b.add()
        relation_b.save()
