""" src.services.method """
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy.orm import class_mapper

from src.db import db
from src.exceptions import HandlerException
from src.helpers import computed_operator
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

        searchstring = "{}".format(search)
        self.__query = self.__query.filter(
            Method.name.like(f"%{searchstring}")
        )
        return self.__query

    def filter_by(self, filter_by):
        """filter by column of model"""
        filters = []
        for k, v in filter_by.items():
            mapper = class_mapper(Method)
            if not hasattr(mapper.columns, k):
                continue
            filters.append(
                computed_operator(mapper.columns[k], "{}".format(v))
            )
        self.__query = self.__query.filter(*filters)
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

    def list(self, search, filter_by, page, per_pages, order_by, order):
        """
        Get list method

        Args:
            search (str): Search
            filter_by: Filter by column of model
            page (int): Pagination position
            per_pages (int): Limit result by page
            order_by (str): Field by order
            order (str|int): desc or asc (1|-1)

        Returns: list Method
        """
        self.__query = Method.query
        self.search(search)
        self.filter_by(filter_by)
        self.sort(order_by, order)
        paginate = self.__query.paginate(
            int(page), int(per_pages), error_out=False
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

            db.session.bulk_save_objects(mappings_create, return_defaults=True)
            db.session.commit()

            identifiers = [item.id for item in mappings_create]

            methods_created = Method.query.filter(
                Method.id.in_(identifiers)
            ).all()
            return methods_created

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
        methods = __query.filter(Method.id.in_(identifiers)).all()

        for method in methods:
            index = next(
                index
                for (index, item) in enumerate(body)
                if item["id"] == method.id
            )

            method.serialize(body[index])
            mappings_update.append(method)

        db.session.bulk_save_objects(mappings_update)
        db.session.commit()

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

    def disabled_many(self, body):
        """
        Disabled method many

        Args:
            body (list<int ): identifiers

        Returns: Method
        """
        __query = Method.query
        methods = __query.filter(Method.id.in_(body)).all()

        for method in methods:
            method.serialize({"disabled": not method.disabled})

        db.session.bulk_save_objects(methods)
        db.session.commit()

        return methods

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

    def delete_many(self, body):
        """
        Delete method many

        Args:
            body (list<int>): identifiers

        Returns: identifiers
        """
        db.session.query(Method).filter(Method.id.in_(body)).delete(
            synchronize_session=False
        )
        db.session.commit()

        return body
