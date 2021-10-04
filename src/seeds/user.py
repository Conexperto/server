""" src.seeds.user """
import logging

from faker import Faker

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


payload = [
    {
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
    },
    {
        "email": "user_current@conexperto.com",
        "password": "token_user",
        "display_name": "user_current",
        "phone_number": "+10010010001",
        "photo_url": faker.image_url(),
        "name": "user_current",
        "lastname": "",
        "headline": faker.text(max_nb_chars=50),
        "about_me": faker.text(max_nb_chars=100),
        "complete_register": True,
        "timezone": "GMT",
        "link_video": "https://youtube.com/asdcvfgb",
        "location": "Argentina",
        "specialities": ["Art", "Engineer Mechanic"],
        "methods": [{"link": "https://skype.com/user", "method": "YouGroup"}],
        "plans": [{"duration": 60, "price": 15}],
    },
]


class UserSeed:
    """
    UserSeed
    """

    __seed__ = "user"

    def up(self):
        """up"""
        try:
            for item in payload:
                user_record = UserRecord.create_user(
                    email=item["email"],
                    password=item["password"],
                    display_name=item["display_name"],
                    phone_number=item["phone_number"],
                    auth=web_sdk.auth,
                )
                user_record.make_claims(
                    {"complete_register": item["complete_register"]}
                )

                user = User(
                    uid=user_record.uid,
                    display_name=item["display_name"],
                    email=item["email"],
                    phone_number=item["phone_number"],
                    photo_url=item["photo_url"],
                    name=item["name"],
                    lastname=item["lastname"],
                    headline=item["headline"],
                    about_me=item["about_me"],
                    complete_register=item["complete_register"],
                    timezone=item["timezone"],
                    link_video=item["link_video"],
                    location=item["location"],
                )

                for subitem in item["specialities"]:
                    ass_speciality = AssociationSpeciality()
                    ass_speciality.speciality = Speciality(name=subitem)
                    user.specialities.append(ass_speciality)

                for subitem in item["methods"]:
                    ass_method = AssociationMethod(link=subitem["link"])
                    ass_method.method = Method(name=subitem["method"])
                    user.methods.append(ass_method)

                for subitem in item["plans"]:
                    plan = Plan(
                        duration=subitem["duration"], price=subitem["price"]
                    )
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
            to_delete_users = []
            to_delete_specialities = []
            to_delete_methods = []
            emails = [item["email"] for item in payload]
            page = web_sdk.auth.list_users()
            while page:
                to_delete_users.extend(
                    [item.uid for item in page.users if item.email in emails]
                )
                page = page.get_next_page()
            web_sdk.auth.delete_users(to_delete_users)

            users = User.query.filter(User.uid.in_(to_delete_users)).all()
            for user in users:
                to_delete_specialities.extend(
                    [item.right_id for item in user.specialities]
                )
                to_delete_methods.extend(
                    [item.right_id for item in user.methods]
                )

            db.session.query(User).filter(
                User.uid.in_(to_delete_users)
            ).delete(synchronize_session=False)
            db.session.query(Speciality).filter(
                Speciality.id.in_(to_delete_specialities)
            ).delete(synchronize_session=False)
            db.session.query(Method).filter(
                Method.id.in_(to_delete_methods)
            ).delete(synchronize_session=False)
            db.session.commit()
        except HandlerException as ex:
            print(ex.message, "down")
        except Exception as ex:
            print(ex, "error")
