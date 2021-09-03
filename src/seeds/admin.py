""" src.seeds.admin """
from faker import Faker
from firebase_admin import auth

from src.db import db
from src.firebase import admin_sdk
from src.models import Admin
from src.models import Privileges
from src.models import UserRecord


faker = Faker()


class AdminSeed:
    """
    AdminSeed
    """

    __seed__ = "admin"

    def __init__(self):
        self.__models = []

        # Make admin user
        user_record = UserRecord.create_user(
            email="user@adminconexperto.com",
            password="token_user",
            display_name="user",
            app=admin_sdk,
        )
        user_record.make_claims({"admin": True, "access_level": 3})
        self.__models.append(
            Admin(
                uid=user_record.uid,
                display_name=user_record.display_name,
                email=user_record.email,
                phone_number="+10000000000",
                photo_url=faker.image_url(),
                name="user",
                lastname="",
                disabled=False,
                privileges=Privileges.User.value,
            )
        )
        # Make admin admin
        user_record = UserRecord.create_user(
            email="admin@adminconexperto.com",
            password="token_admin",
            display_name="admin",
            app=admin_sdk,
        )
        user_record.make_claims({"admin": True, "access_level": 2})
        self.__models.append(
            Admin(
                uid=user_record.uid,
                display_name=user_record.display_name,
                email=user_record.email,
                phone_number="+11000000000",
                photo_url=faker.image_url(),
                name="admin",
                lastname="",
                disabled=False,
                privileges=Privileges.Admin.value,
            )
        )
        # Make admin root
        user_record = UserRecord.create_user(
            email="root@adminconexperto.com",
            password="token_root",
            display_name="root",
            app=admin_sdk,
        )
        user_record.make_claims({"admin": True, "access_level": 1})
        self.__models.append(
            Admin(
                uid=user_record.uid,
                display_name=user_record.display_name,
                email=user_record.email,
                phone_number="+12000000000",
                photo_url=faker.image_url(),
                name="root",
                lastname="",
                disabled=False,
                privileges=Privileges.Root.value,
            )
        )
        # Make admin superroot
        user_record = UserRecord.create_user(
            email="superroot@adminconexperto.com",
            password="token_superroot",
            display_name="superroot",
            app=admin_sdk,
        )
        user_record.make_claims({"admin": True, "access_level": 0})
        self.__models.append(
            Admin(
                uid=user_record.uid,
                display_name=user_record.display_name,
                email=user_record.email,
                phone_number="+13000000000",
                photo_url=faker.image_url(),
                name="superroot",
                lastname="",
                disabled=False,
                privileges=Privileges.SuperRoot.value,
            )
        )

    def up(self):
        """up"""
        for model in self.__models:
            model.add()
            model.save()

    @classmethod
    def down(cls):
        """down"""
        users = []
        page = auth.list_users(app=admin_sdk)
        while page:
            for user in page.users:
                users.append(user.uid)
            page = page.get_next_page()
        auth.delete_users(users, app=admin_sdk)
        db.session.query(Admin).filter(Admin.uid.in_(users)).delete(
            synchronize_session=False
        )
        db.session.commit()
