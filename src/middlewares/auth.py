""" src.middlewares.auth """
from functools import wraps

from flask import g
from flask import request

from src.exceptions import HandlerException
from src.services import AuthAdminService
from src.services import AuthService


def get_token(headers):
    prefix = "Bearer "

    if "authorization" not in headers:
        raise HandlerException(400, "TokenId not found")

    token = headers["authorization"]

    if not token.startswith(prefix):
        raise HandlerException(400, "TokenId not found")

    if not token[len(prefix) :]:
        raise HandlerException(400, "TokenId not found")

    return token[len(prefix) :]


def login_required(admin=False):
    """
    Decorator login_required
    """

    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            try:
                id_token = get_token(request.headers)

                if not id_token:
                    raise HandlerException(400, "TokenId not found")

                if admin:
                    service = AuthAdminService()
                    g.admin = service.authentication(id_token)
                else:
                    service = AuthService()
                    g.user = service.authentication(id_token)
            except HandlerException as ex:
                ex.abort()
            except Exception as ex:
                HandlerException(500, "Unexpected response: ", str(ex)).abort()

            return func(*args, **kwargs)

        return wrap

    return decorator


def has_access(access_level, strict=False):
    """
    Decorator has_acess

    Args:
        - access_level (Privileges): Privileges enum
    """

    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            user = g.admin["b"]

            if not user.has_access(access_level.value, strict):
                HandlerException(401, "You not enough permissions to access").abort()

            return func(*args, **kwargs)

        return wrap

    return decorator
