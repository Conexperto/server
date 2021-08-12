""" src.services.admin """
from flask import abort

from src.firebase import admin_sdk
from src.models import Admin
from src.models import Privileges
from src.models import UserRecord


class AdminService:
    """
    AdminService contains all CRUD operations
    """

    def get(self, uid):
        """
        Get user admin by uid

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description="NotFound", response="not_found")

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def list(self, page=1, per_pages=10):
        """
        Get list user admin

        Args:
            page (int): Pagination position
            per_pages (int): Limit result by page

        Returns: list
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin

        """
        users = Admin.query.paginate(page, per_pages or 10, error_out=False)

        return users

    def create(self, body):
        """
        Create admin user and set custom claims if exits

        Args:
            body (dict):
                email (str): User email
                password (str): User password
                display_name (str): User display name
                phone_number (str): User phone number
                name (str): User name
                lastname (str): User lastname
                privileges (int): User privileges

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        try:
            user_record = UserRecord(body, app=admin_sdk)

            user_record.make_claims(
                {
                    "admin": True,
                    "access_level": body["privileges"]
                    if hasattr(body, "privileges")
                    else Privileges.User.value,
                }
            )

            user = Admin(
                uid=user_record.uid,
                email=body["email"],
                display_name=body["display_name"],
                phone_number=body["phone_number"],
                name=body["name"],
                lastname=body["lastname"],
                privileges=body["privileges"],
            )

            user.add()
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except KeyError as ex:
            return abort(400, description="BadRequest", response=str(ex))

    def update(self, uid, body):
        """
        Update admin user and custom claims if exits

        Args:
            uid (str): User uid
            body (dict):
                email (str): User email
                password (str): User password
                display_name (str): User display name
                phone_number (str): User phone number
                name (str): User name
                lastname (str): User lastname
                privileges (int): User privileges

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description="NotFound", response="not_found")

        user_record.serialize(body)
        user_record.update_user()

        if hasattr(body, "privileges"):
            user_record.make_claims({"admin": True, "access_level": body["privileges"]})

        user.serialize(body)
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def update_field(self, uid, body):
        """
        Update admin user and custom claims if exits

        Args:
            uid (str): User uid
            body (dict):
                email (str): User email
                password (str): User password
                display_name (str): User display name
                phone_number (str): User phone number
                name (str): User name
                lastname (str): User lastname
                privileges (int): User privileges

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description="NotFound", response="not_found")

        user_record.serialize(body)
        user_record.update_user()

        if hasattr(body, "privileges"):
            user_record.make_claims({"admin": True, "access_level": body["privileges"]})

        user.serialize(body)
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def disabled(self, uid):
        """
        Disabled admin user

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description="NotFound", response="not_found")

        user_record.serialize({"disabled": not user_record.disabled})
        user_record.update_user()

        user.serialize({"disabled": not user_record.disabled})
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def delete(self, uid):
        """
        Delete admin user

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
        """
        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description="NotFound", response="not_found")

        user_record.delete_user()
        user.delete()

        return {"uid": user_record.uid}
