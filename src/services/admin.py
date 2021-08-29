""" src.services.admin """
from flask import abort
from flask import current_app

from src.firebase import admin_sdk
from src.models import Admin
from src.models import Privileges
from src.models import UserRecord


class AdminService:
    """
    AdminService contains all CRUD operations
    """

    def search(self, search):
        """
        Make search query
        """
        if search is None:
            return self.__query

        self.__query = self.__query.filter(
            or_(
                Admin.display_name.like(f"%{search}%"),
                Admin.email.like(f"%{search}%"),
                Admin.name.like(f"%{search}%"),
                Admin.lastname.like(f"%{search}%"),
            )
        )
        return self.__query

    def sort(self, order_by, order):
        """
        Make sort query
        """
        __order_by = ""
        __query = None

        if not order in ["desc", "asc"]:
            raise abort(400, description="Bad order, must be desc or asc")

        if not hasattr(Admin, order_by):
            raise abort(400, description="Bad order_by, field not found")

        if order == "asc":
            __query = asc(order_by)
        if order == "desc":
            __query = desc(order_by)

        self.__query = self.__query.order_by(__query)
        return self.__query

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

    def list(
        self, search=None, page=1, per_pages=10, order_by="created_at", order="desc"
    ):
        """
        Get list user admin

        Args:
            search (str): Search
            page (int): Pagination position
            per_pages (int): Limit result by page
            order_by (str): Field by order
            order (str): desc or asc

        Returns: list
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin

        """
        self.__query = Admin.query

        self.search(search)
        self.sort(order_by, order)
        paginate = self.__query.paginate(
            int(page), int(per_page) or 10, error_out=False
        )

        return paginate

    def create(self, body, user_auth):
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
            user_auth (dict): Logged user

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        try:
            if not user_auth["b"].has_access(body["privileges"]):
                raise abort(
                    401,
                    description="Unauthorized",
                    response="Logged user doesn't have sufficient permissions to create a user with equal or higher privileges",
                )

            user_record = UserRecord.create_user(
                email=body["email"],
                password=body["password"],
                display_name=body["display_name"],
                app=admin_sdk,
            )
            user_record.make_claims(
                {
                    "admin": True,
                    "access_level": body["privileges"]
                    if "privileges" in body
                    else Privileges.User.value,
                }
            )

            user = Admin(
                uid=user_record.uid,
                email=user_record.email,
                display_name=user_record.display_name,
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

    def update(self, uid, body, user_auth):
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
            user_auth (dict): Logged user

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        try:
            if "privileges" in body:
                if not user_auth["b"].has_acess(body["privileges"]):
                    raise abort(
                        401,
                        description="Unauthorized",
                        response="Logged user doesn't have sufficient permissions to create a user with equal or higher privileges",
                    )

            user_record = UserRecord.get_user(uid, app=admin_sdk)
            user = Admin.query.filter_by(uid=user_record.uid).first()

            if not user_record or not user:
                abort(404, description="NotFound", response="not_found")

            user_record.serialize(body)
            user_record.update_user()

            if "privileges" in body:
                user_record.make_claims(
                    {"admin": True, "access_level": body["privileges"]}
                )

            user.serialize(body)
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except Exception as ex:
            return abort(400, description="BadRequest", response=str(ex))

    def update_field(self, uid, body, user_auth):
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
            user_auth (dict): Logged user

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """
        try:
            if "privileges" in body:
                if not user_auth["b"].has_acess(body["privileges"]):
                    raise abort(
                        401,
                        description="Unauthorized",
                        response="Logged user doesn't have sufficient permissions to create a user with equal or higher privileges",
                    )

            user_record = UserRecord.get_user(uid, app=admin_sdk)
            user = Admin.query.filter_by(uid=user_record.uid).first()

            if not user_record or not user:
                abort(404, description="NotFound", response="not_found")

            user_record.serialize(body)
            user_record.update_user()

            if "privileges" in body:
                user_record.make_claims(
                    {"admin": True, "access_level": body["privileges"]}
                )

            user.serialize(body)
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except Exception as ex:
            return abort(400, description="BadRequest", response=str(ex))

    def disabled(self, uid, user_auth):
        """
        Disabled admin user

        Args:
            uid (str): User uid
            user_auth (dict): Logged user

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (Admin): Admin
        """

        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description="NotFound", response="not_found")

        if not user_auth["b"].has_acess(user.privileges):
            return abort(
                401,
                description="Unauthorized",
                response="Logged user doesn't have sufficient permissions to create a user with equal or higher privileges",
            )

        user_record.serialize({"disabled": not user_record.disabled})
        user_record.update_user()

        user.serialize({"disabled": not user_record.disabled})
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def delete(self, uid, user_auth):
        """
        Delete admin user

        Args:
            uid (str): User uid
            user_auth (dict): Logged user

        Returns: dict
            uid (str): User uid
        """
        if not user_auth["b"].has_acess(body["privileges"]):
            return abort(
                401,
                description="Unauthorized",
                response="Logged user doesn't have sufficient permissions to create a user with equal or higher privileges",
            )

        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            return abort(404, description="NotFound", response="not_found")

        user_record.delete_user()
        user.delete()

        return {"uid": user_record.uid}
