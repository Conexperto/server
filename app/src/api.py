from os.path import abspath, join
from flask import Flask, render_template, g, jsonify
from flask_cors import CORS

from src.helpers import JSONSerializable
from src.db import db 


# Initialize Application.
def create_api(env):
    api = Flask(__name__, 
                    root_path=abspath(join(__package__, '../')),
                    static_folder='/static')

    api.config.from_object(env)
    api.url_map.strict_slashes = False
    JSONSerializable(api)

    CORS(api)
    
    with api.app_context():
        db.init_app(api)
        #db.create_all()

    from src.blueprints.admin import auth_admin, admin, \
                                        user_admin, \
                                        expert_admin, \
                                        method_admin, \
                                        plan_admin, \
                                        speciality_admin

    api.register_blueprint(auth_admin, url_prefix='/admin/auth')
    api.register_blueprint(admin, url_prefix='/admin')
    api.register_blueprint(user_admin, url_prefix='/admin/user')
    api.register_blueprint(expert_admin, url_prefix='/admin/expert')
    api.register_blueprint(method_admin, url_prefix='/admin/method')
    api.register_blueprint(plan_admin, url_prefix='/admin/plan')
    api.register_blueprint(speciality_admin, url_prefix='/admin/speciality')


    from src.blueprints import auth, \
                                user, \
                                expert, \
                                speciality, \
                                method
                                    
                                

    api.register_blueprint(auth, url_prefix='/auth')
    api.register_blueprint(user, url_prefix='/user')
    api.register_blueprint(expert, url_prefix='/expert')
    api.register_blueprint(speciality, url_prefix='/speciality')
    api.register_blueprint(method, url_prefix='/method')
    

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
        return jsonify({
            'success': False,
            'err': err,
            'msg': msg, 
            'detail': str(detail), 
            'code': detail.response
            }), err

    @api.errorhandler(500)
    def internal_server_error(e):
        return error_handler(500, 'Internal server error', e)

    @api.errorhandler(400)
    def bad_request(e):
        return error_handler(400, 'Bad request', e)

    @api.errorhandler(401)
    def unauthorized(e):
        return error_handler(401, 'Unauthorized', e)

    @api.errorhandler(404)
    def not_found(e):
        return error_handler(404, 'Not found endpoint', e)

    return api
