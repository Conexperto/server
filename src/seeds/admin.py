""" src.seeds.admin """
from faker import Faker
from firebase_admin import auth

from src.db import db
from src.firebase import admin_sdk
from src.models import Admin
from src.models import Privileges
from src.models import UserRecord


faker = Faker()


payload = [
    {
        "email": "user@adminconexperto.com",
        "password": "token_user",
        "display_name": "user",
        "phone_number": "+11000000000",
        "photo_url": faker.image_url(),
        "name": "user",
        "lastname": "",
        "privileges": Privileges.User.value,
    },
    {
        "email": "admin@adminconexperto.com",
        "password": "token_admin",
        "display_name": "admin",
        "phone_number": "+11100000000",
        "photo_url": faker.image_url(),
        "name": "admin",
        "lastname": "",
        "privileges": Privileges.Admin.value,
    },
    {
        "email": "root@adminconexperto.com",
        "password": "token_root",
        "display_name": "root",
        "phone_number": "+11110000000",
        "photo_url": faker.image_url(),
        "name": "root",
        "lastname": "",
        "privileges": Privileges.Root.value,
    },
    {
        "email": "superroot@adminconexperto.com",
        "password": "token_superroot",
        "display_name": "superroot",
        "phone_number": "+11111000000",
        "photo_url": faker.image_url(),
        "name": "superroot",
        "lastname": "",
        "privileges": Privileges.SuperRoot.value,
    },
]


class AdminSeed:
    """
    AdminSeed
    """

    __seed__ = "admin"

    def up(self):
        """up"""
        try:
            to_create = []
            for item in payload:
                user_record = UserRecord.create_user(
                    email=item["email"],
                    password=item["password"],
                    display_name=item["display_name"],
                    phone_number=item["phone_number"],
                    app=admin_sdk,
                )
                user_record.make_claims(
                    {"admin": True, "access_level": item["privileges"]}
                )
                user = Admin(
                    uid=user_record.uid,
                    display_name=item["display_name"],
                    email=item["email"],
                    phone_number=item["phone_number"],
                    photo_url=item["photo_url"],
                    name=item["name"],
                    lastname=item["lastname"],
                    privileges=item["privileges"],
                )
                to_create.append(user)
            db.session.bulk_save_objects(to_create)
            db.session.commit()

            print("Ok")
            exit(0)
        except Exception as ex:
            print(ex)
            exit(1)

    def down(self):
        """down"""
        try:
            emails = [item["email"] for item in payload]
            users = []
            page = auth.list_users(app=admin_sdk)
            while page:
                users.extend([item.uid for item in page.users if item.email in emails])
                page = page.get_next_page()
            auth.delete_users(users, app=admin_sdk)
            db.session.query(Admin).filter(Admin.uid.in_(users)).delete(
                synchronize_session=False
            )
            db.session.commit()
            print("Ok")
            exit(0)
        except Exception as ex:
            print(ex)
            exit(1)
