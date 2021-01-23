from random import randint
from faker import Faker
from src.models import Plan

faker = Faker()

class PlanSeed():
    __seed__ = 'plan'

    def __init__(self):
        self.__model = Plan(
                duration=randint(0, 60),
                price=randint(0, 20))

    def run(self):
        self.__model.add()
        self.__model.save()
