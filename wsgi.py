""" wsgi """
from config import Config
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from src.api import create_api
from src.db import db
from werkzeug.middleware.dispatcher import DispatcherMiddleware




def create_wsgi():
    """Create wsgi app"""
    env = Config
    wsgi = Flask(__name__)

    # Set environment variables to wsgi flask app.
    wsgi.config.from_object(env)

    # Set cors to wsgi flask app.
    CORS(wsgi)
    Migrate(wsgi, db)

    with wsgi.app_context():
        db.init_app(wsgi)
    
    # Handler Errors HTTP
    def error_handler(err, msg, detail=None):
        return jsonify(err=err, msg=msg, detail=detail)

    @wsgi.errorhandler(500)
    def internal_server_error(e):
        return error_handler(500, "Internal server error", str(e))

    @wsgi.errorhandler(400)
    def bad_request(e):
        return error_handler(400, "Bad request", str(e))

    @wsgi.errorhandler(404)
    def not_found(e):
        return error_handler(404, "Not found endpoint", str(e))

    # Set api v1.
    wsgi.wsgi_app = DispatcherMiddleware(
        wsgi.wsgi_app, {"/api/v1": create_api(env).wsgi_app}
    )

    return wsgi
