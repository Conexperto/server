from functools import wraps

from flask import abort
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request

from src.services import SpecialityService


router = Blueprint(name="Speciality", import_name=__name__)

# GET: /api/v1/speciality/<int:_id>
@router.route("/<int:_id>", methods=["GET"])
def index_speciality_one(_id):
    service = SpecialityService()
    speciality = service.get(_id)

    return jsonify({"success": True, "response": speciality})


# GET: /api/v1/speciality
@router.route("/", methods=["GET"])
def index_speciality():
    search = request.args.get("search")
    page = request.args.get("page") or 1
    per_page = request.args.get("limit") or 10
    order_by = request.args.get("orderBy")
    order = request.args.get("order")

    service = SpecialityService()
    paginate = service.list(search, page, per_page, order_by, order)

    return jsonify(
        {
            "success": True,
            "response": paginate.items,
            "total": paginate.total,
            "page": paginate.page,
            "limit": paginate.per_page,
            "next": paginate.next_num,
        }
    )
