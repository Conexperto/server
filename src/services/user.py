""" src.services.user """
from flask import abort
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import or_

from src.exceptions import HandlerException
from src.firebase import web_sdk
from src.models import AssociationMethod
from src.models import AssociationSpeciality
from src.models import Method
from src.models import Plan
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

        self.__query = self.__query.filter(
            or_(
                User.display_name.like(f"%{search}%"),
                User.email.like(f"%{search}%"),
                User.name.like(f"%{search}%"),
                User.lastname.like(f"%{search}%"),
            )
        )
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

    def list(self, search, page, per_pages, order_by, order):
        """
        Get list user

        Args:
            page (int): Pagination position
            per_pages (int): Limit result by page

        Returns: list
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User

        """
        self.__query = User.query
        self.search(search)
        self.sort(order_by, order)
        paginate = self.__query.paginate(
            int(page), int(per_pages) or 10, error_out=False
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
            complete_register = (
                body["complete_register"] if "complete_register" in body else False
            )
            user_record.make_claims({"complete_register": complete_register})
            user = User(
                uid=user_record.uid,
                email=user_record.email,
                display_name=user_record.display_name,
                phone_number=body["phone_number"],
                name=body["name"],
                lastname=body["lastname"],
                headline=body["headline"],
                about_me=body["about_me"],
                complete_register=complete_register,
                link_video=body["link_video"],
                timezone=body["timezone"],
                location=body["location"],
            )

            if "specialities" in body:
                self.__create_speciality(user, body["specialities"])
            if "methods" in body:
                self.__create_method(user, body["methods"])
            if "plans" in body:
                self.__create_plan(user, body["plans"])

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
        try:
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

            user.serialize(body)
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except Exception as ex:
            raise HandlerException(400, "Bad request: " + str(ex))

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
        try:
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

            user.serialize(body)
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except Exception as ex:
            raise HandlerException(400, "Bad request: " + str(ex))

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

    def __create_ass_speciality(self, user, identifiers):
        """
        Associate Specialities to the User

        Args:
            user: User
            identifiers: List of _id associated with the speciality

        Returns: void
        """
        specialities = Speciality.query.filter(Speciality.id.in_(identifiers)).all()
        for speciality in specialities:
            ass_speciality = AssociationSpeciality()
            ass_speciality.speciality.append(speciality)
            user.specialities.append(ass_speciality)

    def __create_ass_method(self, user, methods):
        """
        Associate Methods to the User

        Args:
            user: User
            methods (list<dict>):
                method (str): identifier the method
                link (str): method link

        Returns: void
        """
        identifiers = [item["method"] for item in methods]
        _methods = Method.query.filter(Method.id.in_(identifiers)).all()
        for _method in _methods:
            link = next(
                [item["link"] for item in methods if item["method"] == _method.id], None
            )
            if not link:
                continue
            ass_method = AssociationMethod(link=link)
            ass_method.method.append(_method)
        user.methods.append(ass_method)

    def __create_plan(self, user, plans):
        """
        Creates plans and associates them to the User

        Args:
            user: User
            plans (list<dict>):
                duration (int): Duration
                price (int): Price
                coin (str): Coin

        Returns: void
        """
        for duration, price, coin in plans:
            user.plans.append(Plan(duration=duration, price=price, coin=coin))
