from flask import Blueprint, request, jsonify
from src.models import Deal

router = Blueprint(name='Deal', import_name=__name__)

@router.route('/', methods=['GET'])
def index():
	pass
