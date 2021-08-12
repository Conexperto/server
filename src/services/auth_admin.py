"""
    Service Auth Admin
"""
from flask import abort

from src.firebase import admin_sdk
from src.models import Admin
from src.models import Privileges
from src.models import UserRecord


class AuthAdminService:
    """
    Service Auth Admin
    """

    def authentication(self, id_token):
        """
        Authentcation

        Args:
            id_token (str): id token session

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): Admin
        """
        decoded_token = UserRecord.verify_id_token(
            id_token, check_revoked=True, app=admin_sdk
        )
        user_record = UserRecord.get_user(decoded_token["uid"], app=admin_sdk)

        if user_record.disabled:
            raise abort(
                401,
                description="AccountDisabled",
                response="auth/account-disabled",
            )
        claims = user_record.custom_claims

        if hasattr(claims, "admin"):
            if not claims.admin:
                raise abort(
                    401,
                    description="Unauthorized",
                    response="auth/unauthorized",
                )
        admin = Admin.query.filter_by(uid=user_record.uid).first()
        return {"uid": user_record.uid, "a": user_record, "b": admin}

    def create(self, body):
        """
        Create admin user account

        Args:
            body (dict):
                email (str): User email
                password (str): User password
                display_name (str): User display name
                phone_number (str): User phone number
                name (str): User name
                lastname (str): User lastname
                Privileges (int): User Privileges

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User
        """
        try:
            user_record = UserRecord.create_user(
                email=body["email"],
                password=body["password"],
                display_name=body["display_name"],
                app=admin_sdk,
            )
            user_record.make_claims(
                {
                    "admin": True,
                    "access_level": body["Privileges"]
                    if hasattr(body, "Privileges")
                    else Privileges.User.value,
                }
            )

            user = Admin(
                uid=user_record.uid,
                display_name=body["display_name"],
                email=body["email"],
                phone_number=body["phone_number"],
                name=body["name"],
                lastname=body["lastname"],
                Privileges=body["Privileges"] or Privileges.User.value,
            )
            user.add()
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except KeyError as ex:
            return abort(400, description="BadRequest", response=str(ex))

    def update(self, user, body):
        """
        Update admin user account

        Args:
            user (str):
                uid (str): User uid
                a (UserRecord): UserRecord
                b (User): User
            body (dict):
                email (str): User email
                password (str): User password
                display_name (str): User display name
                phone_number (str): User phone number
                name (str): User name
                lastname (str): User lastname
                Privileges (int): User Privileges

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            abort(404, description="NotFound", response="not_found")

        user_record.serialize(body)
        user_record.update_user()

        if hasattr(body, "Privileges") and not body["Privileges"]:
            user_record.make_claims({"access_level": body["Privileges"]})

        _user.serialize(body)
        _user.save()

        return {"uid": user_record.uid, "a": user_record, "b": _user}

    def update_field(self, user, body):
        """
        Update field admin user account

        Args:
            user (str):
                uid (str): User uid
                a (UserRecord): UserRecord
                b (User): User
            body (dict):
                email (str): User email
                password (str): User password
                display_name (str): User display name
                phone_number (str): User phone number
                name (str): User name
                lastname (str): User lastname
                Privileges (int): User Privileges

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            abort(404, description="NotFound", response="not_found")

        user_record.serialize(body)
        user_record.update_user()

        if hasattr(body, "Privileges") and not body["Privileges"]:
            user_record.make_claims({"access_level": body["Privileges"]})

        _user.serialize(body)
        _user.save()

        return {"uid": user_record.uid, "a": user_record, "b": _user}

    def disabled(self, user):
        """
        Disabled admin user account

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            abort(404, description="NotFound", response="not_found")

        user_record.serialize({"disabled": not user_record.disabled})
        user_record.update_user()

        user.serialize({"disabled": not user_record.disabled})
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": _user}

    def delete(self, user):
        """
        Delete admin user account

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
        """
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            abort(404, description="NotFound", response="not_found")

        user_record.delete_user()
        _user.delete()

        return {"uid": user_record.uid}
