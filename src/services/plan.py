""" src.services.plan """
from flask import abort
from src.db import db
from src.models import Plan


class PlanService:
    """
    PlanService contains all CRUD operations
    """

    def get(self, _id):
        """
        Get plan by id

        Args:
            _id (int): Plan id

        Returns: (Plan) Plan
        """
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description="NotFound", response="not_found")

        return plan

    def list(self, page, per_pages=10):
        """
        Get list plan

        Args:
            page (int): Pagination position
            per_pages (int): Limit result by page

        Returns: list Plan
        """
        plans = Plan.query.paginate(page, per_pages or 10, error_out=False)

        return plans

    def create(self, body):
        """
        Create plan

        Args:
            body (dict):
                duration (int): Duration
                price (int): Price
                coint (str): Coin
                expert_id (int): Expert id

        Returns: Plan
        """
        try:
            plan = Plan(
                duration=body["duration"],
                price=body["price"],
                coin=body["coin"],
                expert_id=body["expert_id"],
            )
            plan.add()
            plan.save()

            return plan
        except KeyError as ex:
            return abort(404, description="BadRequest", response=str(ex))

    def create_many(self, expert_id, body):
        """
        Create many plans

        Args: list
            body (dict):
                duration (int): Duration
                price (int): Price
                coint (str): Coin
                expert_id (int): Expert id

        Returns: Plan
        """
        mappings_create = []
        pipe = []

        if not isinstance(body, list):
            pipe.append(body)
        else:
            pipe = body

        for p in pipe:
            plan = Plan(
                duration=p["duration"],
                price=p["price"],
                coin=p["coin"],
                expert_id=expert_id,
            )
            mappings_create.append(plan)

        db.session.bulk_insert_mappings(Plan, mappings_create)

    def update(self, _id, body):
        """
        Update Plan

        Args:
            _id (int): Plan id
            body (dict):
                duration (int): Duration
                price (int): Price
                coint (str): Coin
                expert_id (int): Expert id

        Returns: Plan
        """
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description="NotFound", response="not_found")

        plan.serialize(body)
        plan.save()

        return plan

    def update_field(self, _id, body):
        """
        Update Plan

        Args:
            _id (int): Plan id
            body (dict):
                duration (int): Duration
                price (int): Price
                coint (str): Coin
                expert_id (int): Expert id

        Returns: Plan
        """
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description="NotFound", response="not_found")

        plan.serialize(body)
        plan.save()

        return plan

    def disabled(self, _id):
        """
        Disabled Plan

        Args:
            _id (int): Plan uid

        Returns: Plan
        """
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description="NotFound", response="not_found")

        plan.serialize({"disabled": not plan.disabled})
        plan.save()

        return plan

    def delete(self, _id):
        """
        Delete Plan

        Args:
            _id (int): Plan uid

        Returns: dict
            _id (str): Plan id
        """
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description="NotFound", response="not_found")

        plan.delete()

        return {"id": plan.id}

    def update_or_create_and_delete_many(self, expert_id, body):
        """
        Update or create and delete many plan

        Args:
            body (dict):
                duration (int): Duration
                price (int): Price
                coint (str): Coin
                expert_id (int): Expert id
        """
        mappings_create = []
        mappings_update = []
        mappings_delete = []
        pipe = []

        if not isinstance(body, list):
            pipe.append(body)
        else:
            pipe = body

        for p in pipe:
            if hasattr(p, "id"):
                if hasattr(p, "delete"):
                    mappings_delete.append({"id": p["id"]})
                    continue

                update = {"id": p["id"], "expert_id": expert_id}

                if hasattr(p, "duration"):
                    update.update({"duration": p["duration"]})
                if hasattr(p, "price"):
                    update.update({"price": p["price"]})
                if hasattr(p, "coin"):
                    update.update({"coin": p["coin"]})
                if hasattr(p, "disabled"):
                    update.update({"disabled": p["disabled"]})

                mappings_update.append(update)
                continue

            create = {
                "duration": p["duration"],
                "price": p["price"],
                "expert_id": expert_id,
            }

            if hasattr(p, "coin"):
                create.update({"coin": p["coin"]})
            if hasattr(p, "disabled"):
                create.update({"disabled": p["disabled"]})

            mappings_create.append(create)

        db.session.bulk_update_mappings(Plan, mappings_update)
        db.session.bulk_insert_mappings(Plan, mappings_create)
