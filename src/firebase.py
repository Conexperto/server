"""
    Initialize firebase_admin for admin & web
"""
import os

from firebase_admin import auth
from firebase_admin import credentials
from firebase_admin import initialize_app


class sdk:
    def __init__(self, sdk, auth):
        self.sdk = sdk
        self.auth = auth


def initialize_admin():
    if os.getenv("FLASK_ENV") == "development":
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = os.getenv(
            "FIREBASE_AUTH_EMULATOR_ADMIN_HOST"
        )
    sdk_cred = credentials.Certificate(
        os.path.abspath(
            os.path.join(__package__, "./config/conexperto-admin-sdk.json")
        )
    )
    sdk_app = initialize_app(credential=sdk_cred, name="admin")
    client = auth._get_client(sdk_app)
    return sdk(sdk_app, client)


def initialize_web():
    if os.getenv("FLASK_ENV") == "development":
        os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = os.getenv(
            "FIREBASE_AUTH_EMULATOR_WEB_HOST"
        )
    sdk_cred = credentials.Certificate(
        os.path.abspath(
            os.path.join(__package__, "./config/conexperto-web-sdk.json")
        )
    )
    sdk_app = initialize_app(credential=sdk_cred, name="web")
    client = auth._get_client(sdk_app)
    return sdk(sdk_app, client)


admin_sdk = initialize_admin()
web_sdk = initialize_web()
