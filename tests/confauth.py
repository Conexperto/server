""" tests.confauth """
import logging
import os

import requests

from src.firebase import admin_sdk
from src.firebase import web_sdk


logger = logging.getLogger(__name__)
URI = "http://{}/identitytoolkit.googleapis.com/v1/accounts:{}?key=None"


class AuthActions(object):
    def __init__(self):
        self._host = {
            "admin": os.getenv("FIREBASE_AUTH_EMULATOR_ADMIN_HOST"),
            "web": os.getenv("FIREBASE_AUTH_EMULATOR_WEB_HOST"),
        }
        self._user = None
        self._token = None
        self._refresh_token = None

    def login(self, email, password, platform="web"):
        uri = URI.format(self._host[platform], "signInWithPassword")
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True,
        }
        rv = requests.post(uri, json=payload)
        assert rv.status_code == 200, "Faild authentication: " + rv.text
        self._user = rv.json()
        self._token = self._user["idToken"]
        self._refresh_token = self._user["refreshToken"]

    def delete(self):
        uri = URI.format("delete", self._key)

        payload = {"idToken": self._token}
        rv = requests.post(uri, json=payload)
        return rv

    @property
    def user(self):
        return self._user

    @property
    def token(self):
        return self._token

    @property
    def refresh_token(self):
        return self._refresh_token

    @classmethod
    def drop_all(self):
        identifiers = []
        page = admin_sdk.auth.list_users()
        while page:
            identifiers.extend([item.uid for item in page.users])
            page = page.get_next_page()
        admin_sdk.auth.delete_users(identifiers)

        identifiers = []
        page = web_sdk.auth.list_users()
        while page:
            identifiers.extend([item.uid for item in page.users])
            page = page.get_next_page()
        web_sdk.auth.delete_users(identifiers)
