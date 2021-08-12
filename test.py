""" test """
import unittest

from config import Config
from flask_testing import TestCase

from src.api import create_api
from src.api import db


class AppTesting(TestCase):
    """AppTesting"""

    def create_app(self):
        """create_app"""
        return create_api(Config)

    def setUp(self):
        """setUp db"""
        db.create_all()

    def tearDown(self):
        """tearDown db"""
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
