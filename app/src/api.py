from os.path import abspath, join
from flask import Flask, render_template, g
from flask_cors import CORS

from src.helpers import JSONSerializable
from src.db import db 


# Initialize Application.
def create_api(env):
    api = Flask(__name__, root_path=abspath(join(__package__, '../')))

    api.config.from_object(env)
    JSONSerializable(api)

    CORS(api, resources=r'*', origins=r'*', methods=r'*', allow_headers=r'*', expose_headers=r'*')

    from src.blueprints import user
    from src.blueprints import deal

    api.register_blueprint(user, url_prefix="/user")
    api.register_blueprint(deal, url_prefix="/deal")

    with api.app_context():
        db.init_app(api)
        #db.create_all()

    return api
