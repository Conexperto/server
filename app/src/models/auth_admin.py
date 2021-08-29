from firebase_admin import auth
from flask import abort

from .admin import Admin
from .user_record import UserRecord
from src.firebase import admin_sdk


class AuthAdmin:
    def authentication(self, id_token):
        decoded_token = UserRecord.verify_id_token(
            id_token, check_revoked=True, app=admin_sdk
        )
        user_record = UserRecord.get_user(decoded_token["uid"], app=admin_sdk)

        if user_record.disabled:
            raise abort(
                401, description="AccountDisabled", response="auth/account-disabled"
            )

        claims = user_record.custom_claims

        if not "admin" in claims:
            raise abort(401, description="Unauthorized", response="auth/unauthorized")

        admin = Admin.query.filter_by(uid=user_record.uid).first()

        return {"uid": user_record.uid, "a": user_record, "b": admin}
