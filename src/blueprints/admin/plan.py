""" src.blueprints.admin.plan """
from flask import Blueprint
from flask import jsonify
from flask import request

from src.exceptions import HandlerException
from src.helpers import parse_order
from src.middlewares import login_required
from src.services import PlanService


router = Blueprint(name="PlanAdmin", import_name=__name__)


@router.route("/<uid>", methods=["GET"])
@login_required(admin=True)
def index_plan_admin_one(uid):
    """
    GET: /api/v1/admin/plan/<uid>
    """
    try:
        service = PlanService()
        plan = service.get(uid)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/", methods=["GET"])
@login_required(admin=True)
def index_plan_admin():
    """
    GET: /api/v1/admin/plan
    """
    try:
        query = request.args.get("query")
        page = request.args.get("page") or 1
        per_pages = request.args.get("limit") or 10
        order_by = request.args.get("orderBy") or None
        order = parse_order(request.args.get("order"))

        service = PlanService()
        plans = service.list(query, page, per_pages, order_by, order)

        return jsonify({"success": True, "response": plans})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response:" + str(ex))


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
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["PUT"])
@login_required(admin=True)
def update_plan_admin(uid):
    """
    PUT: /api/v1/admin/plan/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = PlanService()
        plan = service.update(uid, body)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["PATCH"])
@login_required(admin=True)
def update_field_plan_admin(uid):
    """
    PATCH: /api/v1/admin/plan/<uid>
    """
    try:
        body = request.get_json()

        if not body:
            raise HandlerException(400, "Not found body")

        service = PlanService()
        plan = service.update_field(uid, body)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/disabled/<uid>", methods=["PATCH"])
@login_required(admin=True)
def disabled_plan_admin(uid):
    """
    PATCH /api/v1/admin/plan/disabled/<uid>
    """
    try:
        service = PlanService()
        plan = service.disabled(uid)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))


@router.route("/<uid>", methods=["DELETE"])
@login_required(admin=True)
def delete_plan_admin(uid):
    """
    DELETE: /api/v1/admin/plan/<uid>
    """
    try:
        service = PlanService()
        plan = service.delete(uid)

        return jsonify({"success": True, "response": plan})
    except HandlerException as ex:
        ex.abort()
    except Exception as ex:
        HandlerException(500, "Unexpected response: " + str(ex))
