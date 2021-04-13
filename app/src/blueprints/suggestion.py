from flask import Blueprint, g, request, jsonify, abort 
from functools import wraps
from src.services import ExpertService, SpecialityService


router = Blueprint(name='Suggestion', import_name=__name__)

# GET: /api/v1/search/
