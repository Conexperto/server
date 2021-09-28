"""
    Credentials of Firebase for Admin & Web
"""
import os

import firebase_admin


admin_sdk_cred = firebase_admin.credentials.Certificate(
    os.path.abspath(
        os.path.join(__package__, "./config/conexperto-admin-sdk.json")
    )
)
admin_sdk = firebase_admin.initialize_app(
    credential=admin_sdk_cred, name="admin"
)


web_sdk_cred = firebase_admin.credentials.Certificate(
    os.path.abspath(
        os.path.join(__package__, "./config/conexperto-web-sdk.json")
    )
)
web_sdk = firebase_admin.initialize_app(credential=web_sdk_cred, name="web")

if os.getenv("TESTING"):
    web_sdk = admin_sdk
