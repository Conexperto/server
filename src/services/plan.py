""" src.services.plan """
from sqlalchemy import asc
from sqlalchemy import desc

from src.db import db
from src.exceptions import HandlerException
from src.models import Plan


class PlanService:
    """
    PlanService contains all CRUD operations
    """

    def search(self, search):
        """
        Make search query
        """
        if search is None:
            return self.__query

        self.__query = self.__query.filter(Plan.name.like(f"%{search}"))
        return self.__query

    def sort(self, order_by, order):
        """
        Make sort query
        """
        __order = order or "asc"
        __order_by = order_by or "id"
        __subquery = None

        if __order not in ["desc", "asc"]:
            raise HandlerException(400, "Bad order, mest be desc or asc")

        if not hasattr(Plan, __order_by):
            raise HandlerException(400, "Bad order_by, field not found")

        if __order == "asc":
            __subquery = asc(__order_by)
        if __order == "desc":
            __subquery = desc(__order_by)

        self.__query = self.__query.order_by(__subquery)
        return self.__query

    def get(self, _id):
        """
        Get plan by id

        Args:
            _id (int): Plan id

        Returns: (Plan) Plan
        """
        plan = Plan.query.get(_id)

        if not plan:
            raise HandlerException(404, "Not found plan")

        return plan

    def list(self, search, page, per_pages, order_by, order):
        """
        Get list plan

        Args:
            search (str)L Search
            page (int): Pagination position
            per_pages (int): Limit result by page
            order_by (str): Field by order
            order (str|int): desc or asc (1|-1)

        Returns: list Plan
        """
        self.__query = Plan.query
        self.search(search)
        self.sort(order_by, order)
        paginate = self.__query.paginate(
            int(page), int(per_pages) or 10, error_out=False
        )

        return paginate

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
            raise HandlerException(
                400, "Bad request, field {}".format(str(ex)), str(ex)
            )

    def create_many(self, expert_id, body):
        """
        Create many plans

        Args: list
            body (dict):
                duration (int): Duration
                price (int): Price
                coint (str): Coin
                expert_id (int): Expert id

        Returns: List<Plan>
        """
        try:
            mappings_create = []
            pipe = body

            if not isinstance(pipe, list):
                pipe = [body]

            for p in pipe:
                plan = Plan(
                    duration=p["duration"],
                    price=p["price"],
                    coin=p["coin"],
                    expert_id=expert_id,
                )
                mappings_create.append(plan)

            db.session.bulk_insert_mappings(Plan, mappings_create)

            return mappings_create
        except KeyError as ex:
            raise HandlerException(
                400, "Bad request: field {}".format(str(ex)), str(ex)
            )

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
            raise HandlerException(404, "Not found plan")

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
            raise HandlerException(404, "Not found plan")

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
            raise HandlerException(404, "Not found plan")

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
            raise HandlerException(404, "Not found plan")

        plan.delete()

        return {"id": plan.id}
