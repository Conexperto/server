""" tests.conftest """
import logging

import pytest

from .confauth import AuthActions
from src.api import create_api
from src.db import db


logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def api():
    """
    Initialize API
    """
    api = create_api()

    with api.app_context():
        db.init_app(api)
        db.create_all()

    yield api

    AuthActions.drop_all()
    with api.app_context():
        db.drop_all()


@pytest.fixture(scope="module")
def client(api):
    """
    Initialize client api
    """
    return api.test_client()


@pytest.fixture(scope="module")
def runner(api):
    """
    Initialize cli runner api
    """
    return api.test_cli_runner()


@pytest.fixture(scope="module")
def auth(runner):
    """
    Fixture for AuthActions
    """
    runner.invoke(args=["seed", "admin", "up"])
    runner.invoke(args=["seed", "user", "up"])
    return AuthActions()


@pytest.fixture
def login(auth):
    """
    Fixture for login common user
    """
    auth.login("user@conexperto.com", "token_user")


@pytest.fixture
def login_user(auth):
    """
    Fixture for login user with user privileges
    """
    auth.login("user@adminconexperto.com", "token_user")


@pytest.fixture
def login_admin(auth):
    """
    Fixture for login user with admin privileges
    """
    auth.login("admin@adminconexperto.com", "token_admin")


@pytest.fixture
def login_root(auth):
    """
    Fixture for login user with root privileges
    """
    auth.login("root@adminconexperto.com", "token_root")


@pytest.fixture
def login_superroot(auth):
    """
    Fixture for login user with superroot privileges
    """
    auth.login("superroot@adminconexperto.com", "token_superroot")


@pytest.fixture(scope="module")
def seed_speciality(runner):
    """
    Fixture seed speciality
    """
    runner.invoke(args=["seed", "speciality", "up"])


@pytest.fixture(scope="module")
def seed_method(runner):
    """
    Fixture seed method
    """
    runner.invoke(args=["seed", "method", "up"])
