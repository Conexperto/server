""" src.services.user """
from flask import abort
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.orm import class_mapper

from src.exceptions import HandlerException
from src.firebase import web_sdk
from src.helpers import computed_operator
from src.models import AssociationMethod
from src.models import AssociationSpeciality
from src.models import Method
from src.models import Speciality
from src.models import User
from src.models import UserRecord


class UserService:
    """
    UserServer contains all CRUD oprations
    """

    def search(self, search):
        """
        Make search query
        """
        if search is None:
            return self.__query

        searchstring = "{}".format(search)
        self.__query = (
            self.__query.join(AssociationSpeciality)
            .join(Speciality)
            .join(AssociationMethod)
            .join(Method)
            .filter(
                or_(
                    User.display_name.like(f"%{searchstring}%"),
                    User.email.like(f"%{searchstring}%"),
                    User.name.like(f"%{searchstring}%"),
                    User.lastname.like(f"%{searchstring}%"),
                    User.headline.like(f"%{searchstring}%"),
                    User.about_me.like(f"%{searchstring}%"),
                    User.location.like(f"%{searchstring}%"),
                    Speciality.name.like(f"%{searchstring}%"),
                    Method.name.like(f"%{searchstring}"),
                )
            )
        )
        return self.__query

    def filter_by(self, filter_by):
        filters = []
        for k, v in filter_by.items():
            mapper = class_mapper(User)
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
            raise HandlerException(400, "Bad order, mest be desc or asc")

        if not hasattr(User, __order_by):
            raise HandlerException(400, "Bad order_by, field not found")

        if __order == "asc":
            __subquery = asc(__order_by)
        if __order == "desc":
            __subquery = desc(__order_by)

        self.__query = self.__query.order_by(__subquery)
        return self.__query

    def get(self, uid):
        """
        Get user by uid

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User
        """
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise HandlerException(404, "Not found user")

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def list(self, search, filter_by, page, per_pages, order_by, order):
        """
        Get list user

        Args:
            search (str): Search
            filter_by: Filter by column in model
            page (int): Pagination position
            per_pages (int): Limit result by page
            order_by (str): Field by order
            order (str|int): desc or asc (1|-1)

        Returns: list
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User

        """
        self.__query = User.query
        self.search(search)
        self.filter_by(filter_by)
        self.sort(order_by, order)
        paginate = self.__query.paginate(
            int(page), int(per_pages), error_out=False
        )

        return paginate

    def create(self, body):
        """
        Create user and set custom claims if exits

        Args:
            body (dict):
                email (str): User email
                password (str): User password
                display_name (str): User display name
                phone_number (str): User phone number
                name (str): User name
                lastname (str): User lastname
                specialities (list[int]): Specialities id
                methods (list):
                    body (dict):
                        method (int): Method id
                        link (str): Link method
                plans (list):
                    body (dict):
                        duration (int): Duration
                        price (int): Price
                        coin (str): Coin

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
                app=web_sdk,
            )
            complete_register = body.get("complete_register") or False
            user_record.make_claims({"complete_register": complete_register})
            user = User(
                uid=user_record.uid,
                email=user_record.email,
                display_name=user_record.display_name,
                phone_number=body.get("phone_number"),
                name=body["name"],
                lastname=body["lastname"],
                headline=body.get("headline"),
                about_me=body.get("about_me"),
                complete_register=complete_register,
                link_video=body.get("link_video"),
                timezone=body.get("timezone"),
                location=body.get("location"),
            )

            if "specialities" in body:
                user.append_specialities(body["specialities"])
            if "methods" in body:
                user.append_methods(body["methods"])
            if "plans" in body:
                user.append_plans(body["plans"])

            user.add()
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except KeyError as ex:
            raise HandlerException(400, "Bad request: " + str(ex))

    def update(self, uid, body):
        """
        Update user and custom claims if exits

        Args:
            uid (str): User uid
            body (dict):
                email (str): User email
                password (str): User password
                display_name (str): User display name
                phone_number (str): User phone number
                name (str): User name
                lastname (str): User lastname
                specialities (list[int]): Specialities id
                methods (list):
                    body (dict):
                        method (int): Method id
                        link (str): Link method
                plans (list):
                    body (dict):
                        duration (int): Duration
                        price (int): Price
                        coin (str): Coin

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User
        """
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise abort(404, description="NotFound", response="not_found")

        user_record.serialize(body)
        user_record.update_user()

        if "complete_register" in body:
            user_record.make_claims(
                {"complete_register": body["complete_register"]}
            )

        if "specialities" in body:
            if not isinstance(body["specialities"], list):
                raise HandlerException(
                    400, "Bad request: specialities should be array"
                )
            user.update_specialities(body["specialities"])

        if "methods" in body:
            if not isinstance(body["methods"], list):
                raise HandlerException(
                    400, "Bad request: methods should be array"
                )
            user.update_methods(body["methods"])

        if "plans" in body:
            if not isinstance(body["plans"], list):
                raise HandlerException(
                    400, "Bad request: plans should be array"
                )
            user.update_plans(body["plans"])

        user.serialize(body)
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def update_field(self, uid, body):
        """
        Update user and custom claims if exits

        Args:
            uid (str): User uid
            body (dict):
                email (str): User email
                password (str): User password
                display_name (str): User display name
                phone_number (str): User phone number
                name (str): User name
                lastname (str): User lastname

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User
        """
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise HandlerException(404, "Not found user")

        user_record.serialize(body)
        user_record.update_user()

        if "complete_register" in body:
            user_record.make_claims(
                {"complete_register": body["complete_register"]}
            )

        if "specialities" in body:
            if not isinstance(body["specialities"], list):
                raise HandlerException(
                    400, "Bad request: specialities should be array"
                )
            user.update_specialities(body["specialities"])

        if "methods" in body:
            if not isinstance(body["methods"], list):
                raise HandlerException(
                    400, "Bad request: methods should be array"
                )
            user.update_methods(body["methods"])

        if "plans" in body:
            if not isinstance(body["plans"], list):
                raise HandlerException(
                    400, "Bad request: plans should be array"
                )
            user.update_plans(body["plans"])

        user.serialize(body)
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def disabled(self, uid):
        """
        Disabled user

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User
        """
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise HandlerException(404, "Not found user")

        user_record.serialize({"disabled": not user_record.disabled})
        user_record.update_user()

        user.serialize({"disabled": not user.disabled})
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def delete(self, uid):
        """
        Delete user

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
        """
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            raise HandlerException(404, "Not found user")

        user_record.delete_user()
        user.delete()

        return {"uid": user_record.uid}
