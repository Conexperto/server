""" src.services.method """
from flask import abort
from src.models import Method


class MethodService:
    """
    MethodService contains all CRUD operations
    """

    def get(self, _id):
        """
        Get method by uid

        Args:
            _id (str): method id

        Returns: Method
        """
        method = Method.query.get(_id)

        if not method:
            abort(404, description="NotFound", response="not_found")

        return method

    def list(self, page, per_pages=10):
        """
        Get list method

        Args:
            page (int): Pagination position
            per_pages (int): Limit result by page

        Returns: list method
        """
        methods = Method.query.paginate(page, per_pages or 10, error_out=False)

        return methods

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
            return abort(404, description="BadRequest", response=str(ex))

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
            abort(404, description="NotFound", response="not_found")

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
            abort(404, description="NotFound", response="not_found")

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
            abort(404, description="NotFound", response="not_found")

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
            abort(404, description="NotFound", response="not_found")

        method.delete()

        return {"id": method.id}
