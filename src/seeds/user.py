""" src.seeds.user """
from faker import Faker
from firebase_admin import auth

from src.firebase import web_sdk
from src.models import AssociationMethod
from src.models import AssociationSpeciality
from src.models import Method
from src.models import Plan
from src.models import Speciality
from src.models import User
from src.models import UserRecord


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
    "specialities": [AssociationSpeciality(speciality=Speciality(name="Developer"))],
    "methods": [
        AssociationMethod(link="https://skype.com/user", method=Method(name="Skype"))
    ],
    "plans": [Plan(duration=60, price=15)],
}


class UserSeed:
    """
    UserSeed
    """

    __seed__ = "user"

    def up(self):
        """up"""
        user_record = UserRecord.create_user(
            email=payload["email"],
            password=payload["password"],
            display_name=payload["display_name"],
            phone_number=payload["phone_number"],
            app=web_sdk,
        )
        user_record.make_claims({"complete_register": payload["complete_register"]})

        payload["uid"] = user_record.uid
        user = User(
            uid=payload["uid"],
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
            specialities=payload["specialities"],
            methods=payload["methods"],
            plans=payload["plans"],
        )

        user.add()
        user.save()
        print(user.uid)

    def down(self):
        """down"""
        user_record = auth.get_user_by_email(payload["email"], app=web_sdk)
        auth.delete_user(user_record.uid, app=web_sdk)

        user = User.query.filter_by(uid=user_record.uid).first()
        print(user.uid)
        user.delete()
