""" src.seeds.user """
import logging

from faker import Faker
from firebase_admin import auth

from src.db import db
from src.exceptions import HandlerException
from src.firebase import web_sdk
from src.models import AssociationMethod
from src.models import AssociationSpeciality
from src.models import Method
from src.models import Plan
from src.models import Speciality
from src.models import User
from src.models import UserRecord


logger = logging.getLogger(__name__)
faker = Faker()


payload = {
    "email": "user@conexperto.com",
    "password": "token_user",
    "display_name": "user",
    "phone_number": "+10000000000",
    "photo_url": faker.image_url(),
    "name": "user",
    "lastname": "",
    "headline": faker.text(max_nb_chars=50),
    "about_me": faker.text(max_nb_chars=100),
    "complete_register": True,
    "timezone": "GMT",
    "link_video": "https://youtube.com/asdcvfgb",
    "location": "Argentina",
    "specialities": ["Reporter", "Lawyer"],
    "methods": [{"link": "https://skype.com/user", "method": "YouMeet"}],
    "plans": [{"duration": 60, "price": 15}],
}


class UserSeed:
    """
    UserSeed
    """

    __seed__ = "user"

    def up(self):
        """up"""
        try:
            user_record = UserRecord.create_user(
                email=payload["email"],
                password=payload["password"],
                display_name=payload["display_name"],
                phone_number=payload["phone_number"],
                app=web_sdk,
            )
            user_record.make_claims(
                {"complete_register": payload["complete_register"]}
            )

            user = User(
                uid=user_record.uid,
                display_name=payload["display_name"],
                email=payload["email"],
                phone_number=payload["phone_number"],
                photo_url=payload["photo_url"],
                name=payload["name"],
                lastname=payload["lastname"],
                headline=payload["headline"],
                about_me=payload["about_me"],
                complete_register=payload["complete_register"],
                timezone=payload["timezone"],
                link_video=payload["link_video"],
                location=payload["location"],
            )

            for item in payload["specialities"]:
                ass_speciality = AssociationSpeciality()
                ass_speciality.speciality = Speciality(name=item)
                user.specialities.append(ass_speciality)

            for item in payload["methods"]:
                ass_method = AssociationMethod(link=item["link"])
                ass_method.method = Method(name=item["method"])
                user.methods.append(ass_method)

            for item in payload["plans"]:
                plan = Plan(duration=item["duration"], price=item["price"])
                user.plans.append(plan)

            user.add()
            user.save()
        except HandlerException as ex:
            print(ex.message, "up")
        except Exception as ex:
            print(ex, "error")

    def down(self):
        """down"""

        try:
            user_record = auth.get_user_by_email(payload["email"], app=web_sdk)
            auth.delete_user(user_record.uid, app=web_sdk)

            user = User.query.filter_by(uid=user_record.uid).first()

            user.delete()

            identifiers_specialities = [
                item.speciality.id for item in user.specialities
            ]
            db.session.query(Speciality).filter(
                Speciality.id.in_(identifiers_specialities)
            ).delete()

            identifiers_methods = [item.method.id for item in user.methods]
            db.session.query(Method).filter(
                Method.id.in_(identifiers_methods)
            ).delete()

            db.commit()
        except HandlerException as ex:
            print(ex.message, "down")
        except Exception as ex:
            print(ex, "error")
