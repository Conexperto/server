''' src.middlewares.auth '''
from functools import wraps 
from flask import current_app

from flask import abort 
from flask import g
from flask import request

from src.services import AuthService, AuthAdminService


def get_token(headers):
    prefix = "Bearer "
    
    if "authorization" not in headers:
        raise abort(400, description="NotFoundToken", response="auth/not-found-token")

    token = headers["authorization"]

    if not token.startswith(prefix):
        raise abort(400, description="InvalidIdToken", response="auth/invalid-id-token")

    if not token[len(prefix) :]:
        raise abort(400, description="InvalidIdToken", response="auth/invalid-id-token")

    return token[len(prefix) :]

def login_required(admin=False): 
    """
    Decorator login_required
    """
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            id_token = get_token(request.headers)

            if not id_token:
                raise abort(400, description="NotFoundToken", response="auth/not-found-token")
            
            if admin:
                service = AuthAdminService()
                g.admin = service.authentication(id_token)
            else:
                service = AuthService()
                g.user = service.authentication(id_token)

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
                raise abort(
                    401,
                    description="Unauthorized",
                    response="You not enough permissions to access"
                )

            return func(*args, **kwargs)

        return wrap

    return decorator

