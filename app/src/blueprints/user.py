from flask import Blueprint, request, jsonify
from src.models import User

router = Blueprint(name='User', import_name=__name__)

@router.route('/', methods=['GET'])
def index():
    return jsonify(hello='Hey Bro!!')
