""" __init__ """
from src.models.admin import Admin
from src.models.admin import Privileges
from src.models.method import AssociationMethod
from src.models.method import Method
from src.models.plan import Plan
from src.models.speciality import AssociationSpeciality
from src.models.speciality import Speciality
from src.models.user import User
from src.models.user_record import UserRecord

__all__ = [
    "Admin",
    "Privileges",
    "AssociationMethod",
    "AssociationSpeciality",
    "Method",
    "Plan",
    "Speciality",
    "User",
    "UserRecord",
]
