"""
    Credentials of Firebase for Admin & Web
"""
from os.path import abspath
from os.path import join

import firebase_admin


admin_cred = firebase_admin.credentials.Certificate(
    abspath(join(__package__, "../conexperto-admin-firebase-adminsdk.json"))
)
admin_sdk = firebase_admin.initialize_app(credential=admin_cred)


web_cred = firebase_admin.credentials.Certificate(
    abspath(join(__package__, "../conexperto-web-firebase-adminsdk.json"))
)
web_sdk = firebase_admin.initialize_app(credential=web_cred, name="web")
