import unittest
from flask_testing import TestCase

from src.api import create_api, db
from config import Config

class AppTesting(TestCase):

    def create_app(self):
        return create_api(Config)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()
