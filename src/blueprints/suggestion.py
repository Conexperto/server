from functools import wraps

from flask import abort
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request

from src.services import ExpertService
from src.services import SpecialityService


router = Blueprint(name="Suggestion", import_name=__name__)

# GET: /api/v1/search/
