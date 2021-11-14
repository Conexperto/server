""" src.seeds.method """
from faker import Faker

from src.db import db
from src.exceptions import HandlerException
from src.models import Method


faker = Faker()

payload = ["Skype", "Google Meet", "Zoom", "Discord", "Telegram", "Whatsapp"]


class MethodSeed:
    """
    MethodSeed
    """

    __seed__ = "method"

    def up(self):
        """up"""
        try:
            to_create = []
            for item in payload:
                method = Method(name=item)
                to_create.append(method)
            db.session.bulk_save_objects(to_create)
            db.session.commit()
        except HandlerException as ex:
            print(ex.message)
        except Exception as ex:
            print(ex, "error")

    def down(self):
        """down"""
        try:
            db.session.query(Method).filter(Method.name.in_(payload)).delete(
                synchronize_session=False
            )
        except HandlerException as ex:
            print(ex.message)
        except Exception as ex:
            print(ex, "error")
