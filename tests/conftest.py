""" tests.conftest """
import logging
import os

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
    api.config["TESTING"] = True
    api.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    api.config["JSON_SORT_KEYS"] = False

    with api.app_context():
        db.init_app(api)
        db.create_all()

    yield api

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
    yield AuthActions()
    runner.invoke(args=["seed", "admin", "down"])
    runner.invoke(args=["seed", "user", "down"])


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
