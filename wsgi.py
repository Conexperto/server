""" wsgi """
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from src.api import create_api


def create_wsgi():
    """Create wsgi app"""
    wsgi = Flask(__name__)

    # Set api v1.
    wsgi.wsgi_app = DispatcherMiddleware(
        wsgi.wsgi_app, {"/api/v1": create_api().wsgi_app}
    )

    return wsgi
