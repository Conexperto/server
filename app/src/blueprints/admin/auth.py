from flask import Blueprint, request, jsonify


router = Blueprint(name='AuthAdmin', import_name=__name__)


@router.route('/', methods=['GET'])
def index():
    return jsonify({});
