""" src.services.auth """
from src.exceptions import HandlerException
from src.firebase import web_sdk
from src.models import User
from src.models import UserRecord


class AuthService:
    """
    Service Auth
    """

    def authentication(self, id_token):
        """
        Authentcation

        Args:
            id_token (str): id token session

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User
        """

        decoded_token = UserRecord.verify_id_token(
            id_token, check_revoked=True, app=web_sdk
        )

        user_record = UserRecord.get_user(decoded_token["uid"], app=web_sdk)

        if user_record.disabled:
            raise HandlerException(401, "Account disabled")

        claims = user_record.custom_claims

        if claims and "admin" in claims:
            raise HandlerException(404, "Not found user")

        user = User.query.filter_by(uid=user_record.uid).first()

        return {"uid": user_record.uid, "a": user_record, "b": user}

    def create(self, body):
        """
        Create user account

        Args:
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
            user_record = UserRecord.create_user(
                email=body["email"],
                password=body["password"],
                display_name=body["display_name"],
                app=web_sdk,
            )
            user_record.make_claims({"complete_register": False})

            user = User(
                uid=user_record.uid,
                email=body["email"],
                display_name=body["display_name"],
            )
            user.add()
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except KeyError as ex:
            raise HandlerException(
                400, "Bad request, field {}".format(str(ex)), str(ex)
            )

    def update(self, user, body):
        """
        Update user account

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

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User
        """
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            raise HandlerException(404, "Not found user")

        user_record.serialize(body)
        user_record.update_user()

        if "complete_register" in body:
            user_record.make_claims({"complete_register": body["complete_register"]})

        if "specialities" in body:
            if not isinstance(body["specialities"], list):
                raise HandlerException(400, "Bad request: specialities should be array")
            _user.update_specialities(body["specialities"])

        if "methods" in body:
            if not isinstance(body["methods"], list):
                raise HandlerException(400, "Bad request: methods should be array")
            _user.update_methods(body["methods"])

        if "plans" in body:
            if not isinstance(body["plans"], list):
                raise HandlerException(400, "Bad request: plans should be array")
            _user.update_plans(body["plans"])

        _user.serialize(body)
        _user.save()

        return {"uid": user_record.uid, "a": user_record, "b": _user}

    def update_field(self, user, body):
        """
        Update field user account

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

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User
        """
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            raise HandlerException(404, "Not found user")

        user_record.serialize(body)
        user_record.update_user()

        if "complete_register" in body:
            user_record.make_claims({"complete_register": body["complete_register"]})

        if "specialities" in body:
            if not isinstance(body["specialities"], list):
                raise HandlerException(400, "Bad request: specialities should be array")
            user.update_specialities(body["specialities"])

        if "methods" in body:
            if not isinstance(body["methods"], list):
                raise HandlerException(400, "Bad request: methods should be array")
            user.update_methods(body["methods"])

        if "plans" in body:
            if not isinstance(body["plans"], list):
                raise HandlerException(400, "Bad request: plans should be array")
            user.update_plans(body["plans"])

        _user.serialize(body)
        _user.save()

        return {"uid": user_record.uid, "a": user_record, "b": _user}

    def disabled(self, user):
        """
        Disabled user account

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
            a (UserRecord): UserRecord
            b (User): User
        """
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            raise HandlerException(404, "Not found user")

        user_record.serialize({"disabled": True})
        user_record.update_user()

        _user.serialize({"disabled": True})
        _user.save()

        return {"uid": user_record.uid, "a": user_record, "b": _user}

    def delete(self, user):
        """
        Delete account user

        Args:
            uid (str): User uid

        Returns: dict
            uid (str): User uid
        """
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            raise HandlerException(404, "Not found user")

        user_record.delete_user()
        _user.delete()

        return {"uid": user_record.uid}
