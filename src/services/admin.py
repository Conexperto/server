""" src.services.admin """
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.orm import class_mapper

from src.exceptions import HandlerException
from src.firebase import admin_sdk
from src.helpers import computed_operator
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

        searchstring = "{}".format(search)
        self.__query = self.__query.filter(
            or_(
                Admin.display_name.like(f"%{searchstring}%"),
                Admin.email.like(f"%{searchstring}%"),
                Admin.name.like(f"%{searchstring}%"),
                Admin.lastname.like(f"%{searchstring}%"),
            )
        )
        return self.__query

    def filter_by(self, filter_by):
        filters = []
        for k, v in filter_by.items():
            mapper = class_mapper(Admin)
            if not hasattr(mapper.columns, k):
                continue
            filters.append(
                computed_operator(mapper.columns[k], "{}".format(v))
            )
        self.__query = self.__query.filter(*filters)
        return self.__query

    def sort(self, order_by, order):
        """
        Make sort query
        """
        __order = order or "asc"
        __order_by = order_by or "id"
        __subquery = None

        if __order not in ["desc", "asc"]:
            raise HandlerException(400, "Bad order, must be desc or asc")

        if not hasattr(Admin, __order_by):
            raise HandlerException(400, "Bad order_by, field not found")

        if __order == "asc":
            __subquery = asc(__order_by)
        if __order == "desc":
            __subquery = desc(__order_by)

        self.__query = self.__query.order_by(__subquery)
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
        user_record = UserRecord.get_user(uid, auth=admin_sdk.auth)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise HandlerException(404, "Not found user")

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def list(self, search, filter_by, page, per_pages, order_by, order):
        """
        Get list user admin

        Args:
            search (str): Search
            page (int): Pagination position
            per_pages (int): Limit result by page
            order_by (str): Field by order
            order (str): desc or asc (1|-1)

        Returns: list
            a (UserRecord): UserRecord
            b (Admin): Admin

        """
        self.__query = Admin.query
        self.search(search)
        self.filter_by(filter_by)
        self.sort(order_by, order)
        paginate = self.__query.paginate(
            int(page), int(per_pages) or 10, error_out=False
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
            if not user_auth["b"].has_access(body["privileges"], True):
                raise HandlerException(
                    401,
                    "Logged user doesn't have sufficient permissions \
                                  to create a user with equal or higher privileges",
                )

            user_record = UserRecord.create_user(
                email=body["email"],
                password=body["password"],
                display_name=body["display_name"],
                phone_number=body["phone_number"],
                photo_url=body.get("photo_url"),
                auth=admin_sdk.auth,
            )
            privileges = body.get("privileges") or Privileges.User.value
            user_record.make_claims(
                {"admin": True, "access_level": privileges}
            )
            user = Admin(
                uid=user_record.uid,
                email=user_record.email,
                display_name=user_record.display_name,
                phone_number=body["phone_number"],
                name=body["name"],
                lastname=body["lastname"],
                privileges=body["privileges"],
                photo_url=body.get("photo_url"),
            )
            user.add()
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except KeyError as ex:
            raise HandlerException(
                400, "Bad request, field {}".format(str(ex)), str(ex)
            )

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
        user_record = UserRecord.get_user(uid, auth=admin_sdk.auth)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise HandlerException(404, "Not found user")

        if user_auth["uid"] == uid:
            raise HandlerException(
                401, "Logged user can't modify own profile in this endpoint"
            )

        if not user_auth["b"].has_access(user.privileges, True):
            raise HandlerException(
                401,
                "Logged user doesn't have sufficient permissions \
                                        to create a user with equal or higher privileges",
            )

        user_record.serialize(body)
        user_record.update_user()

        if "privileges" in body:
            user_record.make_claims(
                {"admin": True, "access_level": body["privileges"]}
            )

        user.serialize(body)
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": user}

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
        user_record = UserRecord.get_user(uid, auth=admin_sdk.auth)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise HandlerException(404, "Not found user")

        if user_auth["uid"] == uid:
            raise HandlerException(
                401, "Logged user can't modify own profile in this endpoint"
            )

        if not user_auth["b"].has_access(user.privileges, True):
            raise HandlerException(
                401,
                "Logged user doesn't have sufficient permissions \
                                          to update a user with equal or higher privileges",
            )

        user_record.serialize(body)
        user_record.update_user()

        if "privileges" in body:
            user_record.make_claims(
                {"admin": True, "access_level": body["privileges"]}
            )

        user.serialize(body)
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": user}

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
        user_record = UserRecord.get_user(uid, auth=admin_sdk.auth)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise HandlerException(404, "Not found user")

        if user_auth["uid"] == uid:
            raise HandlerException(
                401, "Logged user can't modify own profile in this endpoint"
            )

        if not user_auth["b"].has_access(user.privileges, True):
            raise HandlerException(
                401,
                "Logged user doesn't have sufficient permissions \
                              to create a user with equal or higher privileges",
            )

        user_record.serialize({"disabled": not user_record.disabled})
        user_record.update_user()

        user.serialize({"disabled": not user.disabled})
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
        user_record = UserRecord.get_user(uid, auth=admin_sdk.auth)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise HandlerException(404, "Not found user")

        if user_auth["uid"] == uid:
            raise HandlerException(
                401, "Logged user can't modify own profile in this endpoint"
            )

        if not user_auth["b"].has_access(user.privileges, True):
            raise HandlerException(
                401,
                "Logged user doesn't have sufficient permissions \
                              to create a user with equal or higher privileges",
            )

        user_record.delete_user()
        user.delete()

        return {"uid": user_record.uid}
