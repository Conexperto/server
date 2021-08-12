""" __init__ """
from src.seeds.admin import AdminSeed
from src.seeds.expert import ExpertSeed
from src.seeds.method import MethodSeed
from src.seeds.plan import PlanSeed
from src.seeds.speciality import SpecialitySeed
from src.seeds.test import TestSeed
from src.seeds.user import UserSeed


__all__ = [
    "AdminSeed",
    "ExpertSeed",
    "MethodSeed",
    "PlanSeed",
    "SpecialitySeed",
    "TestSeed",
    "UserSeed",
]
