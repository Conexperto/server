from flask import abort
from flask import Blueprint
from flask import g
from flask import jsonify
from flask import request

from src.services import ExpertService


router = Blueprint(name="Expert", import_name=__name__)

# GET: /api/v1/expert/<uid>
@router.route("/<uid>", methods=["GET"])
def index_expert_one(uid):
    service = ExpertService()
    expert = service.get(uid)

    return jsonify({"success": True, "response": expert})


# GET: /api/v1/expert
@router.route("/", methods=["GET"])
def index_expert():
    search = request.args.get("search")
    page = request.args.get("page") or 1
    per_page = request.args.get("limit") or 10
    order_by = request.args.get("orderBy")
    order = request.args.get("order")

    service = ExpertService()
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
