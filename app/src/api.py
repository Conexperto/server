from os.path import abspath, join
from flask import Flask, render_template, g
from flask_cors import CORS

from src.helpers import JSONSerializable
from src.db import db 


# Initialize Application.
def create_api(env):
    api = Flask(__name__, 
                    root_path=abspath(join(__package__, '../')),
                    static_folder='/static')

    api.config.from_object(env)
    JSONSerializable(api)

    CORS(api)
    
    with api.app_context():
        db.init_app(api)
        #db.create_all()

    from src.blueprints import auth, auth_admin
    
    api.register_blueprint(auth_admin, url_prefix='/admin')
    api.register_blueprint(auth, url_prefix='/')
    
    
    @api.route('/')
    def index():
        return render_template('index.html')

    @api.route('/admin')
    def index_admin():
        return render_template('index-admin.html')
    
    @api.route('/instructions')
    def instructions():
        return render_template('instructions.html')

    # Handler Errors HTTP
    def error_handler(err, msg, detail=None):
        return jsonify(err=err, msg=msg, detail=detail)

    @api.errorhandler(500)
    def internal_server_error(e):
        return error_handler(500, 'Internal server error', str(e))

    @api.errorhandler(400)
    def bad_request(e):
        return error_handler(400, 'Bad request', str(e))

    @api.errorhandler(401)
    def unauthorized(e):
        return error_handler(401, 'Unauthorized', str(e))

    @api.errorhandler(404)
    def not_found(e):
        return error_handler(404, 'Not found endpoint', str(e))

    return api
