""" src.blueprints.admin.plan """
from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.middlewares import login_required
from src.services import PlanService


router = Blueprint(name="PlanAdmin", import_name=__name__)


@router.route("/<int:_id>", methods=["GET"])
@login_required(admin=True)
def index_plan_admin_one(_id):
    """
    GET: /api/v1/admin/plan/<int:_id>
    """
    try:
        service = PlanService()
        plan = service.get(_id)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/", methods=["GET"])
@login_required(admin=True)
def index_plan_admin():
    """
    GET: /api/v1/admin/plan
    """
    try:
        search = request.args.get("search")
        page = request.args.get("page") or 1
        per_pages = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = PlanService()
        plans = service.list(search, page, per_pages, order_by, order)

        return jsonify({"success": True, "response": plans})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response:" + str(ex), str(ex)).abort()


@router.route("/", methods=["POST"])
@login_required(admin=True)
def register_plan_admin():
    """
    POST: /api/v1/admin/plan
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = PlanService()
        plan = service.create(body)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/<int:_id>", methods=["PUT"])
@login_required(admin=True)
def update_plan_admin(_id):
    """
    PUT: /api/v1/admin/plan/<_id>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = PlanService()
        plan = service.update(_id, body)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/", methods=["PUT"])
@login_required(admin=True)
def update_many_plan_admin():
    """
    PUT: /api/v1/admin/plan
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = PlanService()
        plan = service.update_many(body)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/<int:_id>", methods=["PATCH"])
@login_required(admin=True)
def update_field_plan_admin(_id):
    """
    PATCH: /api/v1/admin/plan/<int:_id>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = PlanService()
        plan = service.update_field(_id, body)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/disabled/<int:_id>", methods=["PATCH"])
@login_required(admin=True)
def disabled_plan_admin(_id):
    """
    PATCH /api/v1/admin/plan/disabled/<int:_id>
    """
    try:
        service = PlanService()
        plan = service.disabled(_id)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()


@router.route("/<int:_id>", methods=["DELETE"])
@login_required(admin=True)
def delete_plan_admin(_id):
    """
    DELETE: /api/v1/admin/plan/<int:_id>
    """
    try:
        service = PlanService()
        plan = service.delete(_id)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex), str(ex)).abort()
