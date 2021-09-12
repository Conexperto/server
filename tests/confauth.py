""" tests.confauth """
import logging
import os

import requests


logger = logging.getLogger(__name__)
URI = "http://emulator:9099/identitytoolkit.googleapis.com/v1/accounts:{}?key={}"


class AuthActions(object):
    def __init__(self):
        self._key = os.getenv("FIREBASE_API_KEY")
        self._user = None
        self._token = None
        self._refresh_token = None

    def login(self, email, password):
        uri = URI.format("signInWithPassword", self._key)
        payload = {"email": email, "password": password, "returnSecureToken": True}
        rv = requests.post(uri, json=payload)
        assert rv.status_code == 200, "Faild authentication"
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
