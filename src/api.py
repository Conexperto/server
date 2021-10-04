""" src.api """
import os
import re

from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from src.blueprints import auth
from src.blueprints import method
from src.blueprints import speciality
from src.blueprints import user
from src.blueprints.admin import admin
from src.blueprints.admin import auth_admin
from src.blueprints.admin import method as method_admin
from src.blueprints.admin import plan as plan_admin
from src.blueprints.admin import speciality as speciality_admin
from src.blueprints.admin import user as user_admin
from src.db import db
from src.helpers import JSONSerializable
from src.seed import seed


def create_api():
    """Initialize Application"""
    api = Flask(__name__)

    database_url = os.getenv("DATABASE_URL")
    if re.match("postgres://", database_url):
        database_url = database_url.replace("postgres", "postgresql", 1)
    api.config["SQLALCHEMY_DATABASE_URI"] = database_url
    api.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    api.config["JSON_SORT_KEYS"] = False

    Migrate(api, db)

    api.cli.add_command(seed)

    api.url_map.strict_slashes = False
    JSONSerializable(api)

    CORS(api)

    with api.app_context():
        db.init_app(api)

    api.register_blueprint(auth_admin, url_prefix="/admin/auth")
    api.register_blueprint(admin, url_prefix="/admins")
    api.register_blueprint(user_admin, url_prefix="/admin/users")
    api.register_blueprint(method_admin, url_prefix="/admin/methods")
    api.register_blueprint(plan_admin, url_prefix="/admin/plans")
    api.register_blueprint(speciality_admin, url_prefix="/admin/specialities")

    api.register_blueprint(auth, url_prefix="/auth")
    api.register_blueprint(user, url_prefix="/users")
    api.register_blueprint(speciality, url_prefix="/specialities")
    api.register_blueprint(method, url_prefix="/methods")

    # Handler Errors HTTP
    def error_handler(err, msg, detail=None):
        return (
            jsonify(
                {
                    "success": False,
                    "err": err,
                    "msg": msg,
                    "detail": str(detail.description),
                }
            ),
            err,
        )

    @api.errorhandler(500)
    def internal_server_error(e):
        return error_handler(500, "Internal server error", e)

    @api.errorhandler(400)
    def bad_request(e):
        return error_handler(400, "Bad request", e)

    @api.errorhandler(401)
    def unauthorized(e):
        return error_handler(401, "Unauthorized", e)

    @api.errorhandler(404)
    def not_found(e):
        return error_handler(404, "Not found endpoint", e)

    return api
