""" __init__ """
from src.blueprints.admin.admin import router as admin
from src.blueprints.admin.auth_admin import router as auth_admin
from src.blueprints.admin.method import router as method
from src.blueprints.admin.plan import router as plan
from src.blueprints.admin.speciality import router as speciality
from src.blueprints.admin.user import router as user


__all__ = ["admin", "auth_admin", "expert", "method", "plan", "speciality", "user"]
