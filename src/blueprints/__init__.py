""" __init__ """
from src.blueprints.auth import router as auth
from src.blueprints.method import router as method
from src.blueprints.speciality import router as speciality
from src.blueprints.user import router as user


__all__ = ["auth", "user", "speciality", "method"]
