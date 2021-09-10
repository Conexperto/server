""" src.services.method """
from sqlalchemy import asc
from sqlalchemy import desc

from src.db import db
from src.exceptions import HandlerException
from src.models import Method


class MethodService:
    """
    MethodService contains all CRUD operations
    """

    def search(self, search):
        """
        Make search query
        """
        if search is None:
            return self.__query

        self.__query = self.__query.filter(Method.name.like(f"%{search}"))
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

        if not hasattr(Method, __order_by):
            raise HandlerException(400, "Bad order_by, field not found")

        if __order == "asc":
            __subquery = asc(__order_by)
        if __order == "desc":
            __subquery = desc(__order_by)

        self.__query = self.__query.order_by(__subquery)
        return self.__query

    def get(self, _id):
        """
        Get method by uid

        Args:
            _id (str): Method id

        Returns: Method
        """
        method = Method.query.get(_id)

        if not method:
            raise HandlerException(404, "Not found method")

        return method

    def list(self, search, page, per_pages, order_by, order):
        """
        Get list method

        Args:
            search (str)L Search
            page (int): Pagination position
            per_pages (int): Limit result by page
            order_by (str): Field by order
            order (str|int): desc or asc (1|-1)

        Returns: list Method
        """
        self.__query = Method.query
        self.search(search)
        self.sort(order_by, order)
        paginate = self.__query.paginate(
            int(page), int(per_pages) or 10, error_out=False
        )

        return paginate

    def create(self, body):
        """
        Create Method

        Args:
            body (dict):
                method (str): Method name

        Returns: Method
        """
        try:
            method = Method(name=body["name"])

            method.add()
            method.save()

            return method
        except KeyError as ex:
            raise HandlerException(
                400, "Bad request, field {}".format(str(ex)), str(ex)
            )

    def create_many(self, body):
        """
        Create many methods

        Args:
            body (list<dict>):
                name(str): Method.name

        Returns: List<Method>
        """
        try:
            mappings_create = []
            pipe = body

            if not isinstance(pipe, list):
                pipe = [body]

            for p in pipe:
                method = Method(name=p["name"])
                mappings_create.append(method)

            db.session.bulk_insert_mappings(Method, mappings_create)

            return mappings_create

        except KeyError as ex:
            raise HandlerException(
                400, "Bad request, field {}".format(str(ex)), str(ex)
            )

    def update(self, _id, body):
        """
        Update Method

        Args:
            _id (int): Method id
            body (dict):
                method (str): Method name

        Returns: Method
        """
        method = Method.query.get(_id)

        if not method:
            raise HandlerException(404, "Not found method")

        method.serialize(body)
        method.save()

        return method

    def update_many(self, body):
        """
        Update many Methods

        Args:
            body (list<dict>):
                id (int): Speciality.id
                name (str): Speciality.name

        Returns: List<Method>
        """
        mappings_update = []
        identifiers = [item["id"] for item in body]

        __query = Method.query
        _methods = __query.filter(Method.id.in_(identifiers)).all()

        for _method in _methods:
            index = next(
                [index for (index, item) in enumerate(body) if item["id"] == _method.id]
            )

            _method.serialize(body[index])
            mappings_update.append(_method)

        db.session.bulk_update_mappings(Method, mappings_update)

        return mappings_update

    def update_field(self, _id, body):
        """
        Update Method

        Args:
            _id (int): Method uid
            body (dict):
                method (str): Method name

        Returns: Method
        """
        method = Method.query.get(_id)

        if not method:
            raise HandlerException(404, "Not found method")

        method.serialize(body)
        method.save()

        return method

    def disabled(self, _id):
        """
        Disabled Method

        Args:
            _id (str): Method _id

        Returns: Method
        """
        method = Method.query.get(_id)

        if not method:
            raise HandlerException(404, "Not found method")

        method.serialize({"disabled": not method.disabled})
        method.save()

        return method

    def delete(self, _id):
        """
        Delete Method

        Args:
            _id (int): Method_id

        Returns (dict):
            id (int): Method id
        """
        method = Method.query.get(_id)

        if not method:
            raise HandlerException(404, "Not found method")

        method.delete()

        return {"id": method.id}
