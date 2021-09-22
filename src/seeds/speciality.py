""" src.seeds.speciality """
from faker import Faker

from src.db import db
from src.exceptions import HandlerException
from src.models import Speciality


faker = Faker()

payload = [
    "Product Design",
    "Management & Strategy",
    "Investing",
    "Development / Programming",
    "Technology",
    "Health",
    "Sales",
    "Money Management",
    "Tech",
]


class SpecialitySeed:
    """
    SpecialitySeed
    """

    __seed__ = "speciality"

    def up(self):
        """up"""
        try:
            to_create = []
            for item in payload:
                speciality = Speciality(name=item)
                to_create.append(speciality)
            db.session.bulk_save_objects(to_create)
            db.session.commit()
        except HandlerException as ex:
            print(ex.message)
        except Exception as ex:
            print(ex, "error")

    def down(self):
        """down"""
        try:
            db.session.query(Speciality).filter(Speciality.name.in_(payload)).delete(
                synchronize_session=False
            )
            db.session.commit()
        except HandlerException as ex:
            print(ex.message)
        except Exception as ex:
            print(ex, "error")
