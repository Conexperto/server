""" src.seeds.user """
from faker import Faker
from firebase_admin import auth
from flask import current_app

from src.db import db
from src.firebase import web_sdk
from src.models import User
from src.models import UserRecord


faker = Faker()


class UserSeed:
    """
    UserSeed
    """

    __seed__ = "user"

    def __init__(self):
        self.__models = []

        # Make user common
        user_record = UserRecord.create_user(
            email="user@conexperto.com",
            password="token_user",
            display_name="user",
            app=web_sdk,
        )
        self.__models.append(
            User(
                uid=user_record.uid,
                display_name=user_record.display_name,
                email=user_record.email,
                phone_number="+10000000000",
                photo_url=faker.image_url(),
                name="user",
                lastname="",
                disabled=False,
                headline=faker.text(max_nb_chars=50),
                about_me=faker.text(max_nb_chars=100),
                complete_register=True,
            )
        )

    def up(self):
        """up"""
        for model in self.__models:
            model.add()
            model.save()

        current_app.logger.info("Seed User")

    @classmethod
    def down(cls):
        """down"""
        users = []
        page = auth.list_users(app=web_sdk)
        while page:
            for user in page.users:
                users.append(user.uid)
            page = page.get_next_page()
        auth.delete_users(users, app=web_sdk)
        db.session.query(User).filter(User.uid.in_(users)).delete(
            synchronize_session=False
        )
        db.session.commit()
