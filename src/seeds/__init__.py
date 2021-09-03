""" __init__ """
from src.seeds.admin import AdminSeed
from src.seeds.method import MethodSeed
from src.seeds.plan import PlanSeed
from src.seeds.speciality import SpecialitySeed
from src.seeds.user import UserSeed


__all__ = [
    "AdminSeed",
    "MethodSeed",
    "PlanSeed",
    "SpecialitySeed",
    "UserSeed",
]
