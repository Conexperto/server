""" src.services.method """
from sqlalchemy import asc
from sqlalchemy import desc

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
            raise HandlerException(400, "Unexpected response: " + str(ex))

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
