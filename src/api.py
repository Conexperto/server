""" src.api """
from os.path import abspath
from os.path import join

from flask import Flask
from flask import jsonify
from flask import render_template
from flask_cors import CORS
from src.blueprints import auth
from src.blueprints.admin import admin
from src.blueprints.admin import auth_admin
from src.blueprints.admin import expert
from src.blueprints.admin import method
from src.blueprints.admin import plan
from src.blueprints.admin import speciality
from src.blueprints.admin import user
from src.helpers import JSONSerializable


def create_api(env):
    """Initialize Application"""
    api = Flask(__name__)

    api.config.from_object(env)
    api.url_map.strict_slashes = False
    JSONSerializable(api)

    CORS(api)

    api.register_blueprint(auth_admin, url_prefix="/admin/auth")
    api.register_blueprint(admin, url_prefix="/admin")
    api.register_blueprint(user, url_prefix="/admin/user")
    api.register_blueprint(expert, url_prefix="/admin/expert")
    api.register_blueprint(method, url_prefix="/admin/method")
    api.register_blueprint(plan, url_prefix="/admin/plan")
    api.register_blueprint(speciality, url_prefix="/admin/speciality")

    api.register_blueprint(auth, url_prefix="/auth")

    # Handler Errors HTTP
    def error_handler(err, msg, detail=None):
        return (
            jsonify(
                {
                    "success": False,
                    "err": err,
                    "msg": msg,
                    "detail": str(detail),
                    "code": detail.response,
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
