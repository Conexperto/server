""" src.services.speciality """
from flask import abort
from sqlalchemy import asc
from sqlalchemy import desc

from src.db import db
from src.exceptions import HandlerException
from src.models import Admin
from src.models import Speciality


class SpecialityService:
    """
    SpecialityService
    """

    def search(self, search):
        """
        Make search query
        """
        if search is None:
            return self.__query

        self.__query = self.__query.filter(Speciality.name.like(f"%{search}%"))
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

        if not hasattr(Admin, __order_by):
            raise HandlerException(400, "Bad order_by, field not found")

        if __order == "asc":
            __subquery = asc(__order_by)
        if __order == "desc":
            __subquery = desc(__order_by)

        self.__query = self.__query.order_by(__subquery)
        return self.__query

    def get(self, _id):
        """
        Get speciality by id

        Args:
            _id (str): Speciality.id

        Returns: Speciality
        """
        speciality = Speciality.query.get(_id)

        if not speciality:
            raise HandlerException(404, "Not found speciality")

        return speciality

    def list(self, search, page, per_pages, order_by, order):
        """
        Get list specialities

        Args:
            search (str): Search
            page (int): Pagination position
            per_pages (int): Limit result by page
            order_by (str): Field by order
            order (str): desc or asc (1|-1)

        Returns: list specialities
        """
        self.__query = Speciality.query
        self.search(search)
        self.sort(order_by, order)
        paginate = self.__query.paginate(int(page), int(per_pages), error_out=False)

        return paginate

    def create(self, body):
        """
        Create Speciality

        Args:
            body (dict):
                name (str): Speciality.name
        Returns: Expert
        """
        try:
            speciality = Speciality(name=body["name"])

            speciality.add()
            speciality.save()

            return speciality
        except KeyError as ex:
            raise HandlerException(404, "Bad request: " + str(ex))

    def create_many(self, body):
        """
        Create many specialities

        Args:
            body (list<dict>):
                name (str): Speciality.name

        Returns: List<Speciality>
        """
        try:
            mappings_create = []
            pipe = body

            if not isinstance(pipe, list):
                pipe = [body]

            for p in pipe:
                speciality = Speciality(
                    duration=p["duration"], price=p["price"], coin=p["coin"]
                )
                mappings_create.append(speciality)

            db.session.bulk_insert_mappings(Speciality, mappings_create)

            return mappings_create

        except KeyError as ex:
            raise HandlerException(
                400, "Bad request, field {}".format(str(ex)), str(ex)
            )

    def update(self, _id, body):
        """
        Update Speciality

        Args:
            _id (int): Speciality.id
            body (dict):
                name (str): Speciality.name

        Returns: Speciality
        """
        speciality = Speciality.query.get(_id)

        if not speciality:
            raise HandlerException(404, "Not found speciality")

        speciality.serialize(body)
        speciality.save()

        return speciality

    def update_many(self, body):
        """
        Update many Specialities

        Args:
            body (list<dict>):
                id (int): Speciality.id
                name (str): Speciality.name

        Returns: List<Speciality>
        """
        mappings_update = []
        identifiers = [item["id"] for item in body]

        __query = Speciality.query
        _specialities = __query.filter(Speciality.id.in_(identifiers)).all()

        for _speciality in _specialities:
            index = next(
                [
                    index
                    for (index, item) in enumerate(body)
                    if item["id"] == _speciality.id
                ]
            )

            _speciality.serialize(body[index])
            mappings_update.append(_speciality)

        db.session.bulk_update_mappings(Speciality, mappings_update)
        return mappings_update

    def update_field(self, _id, body):
        """
        Update Speciality

        Args:
            _id (int): Speciality._id
            body (dict):
                name (str): Speciality.name

        Returns: Speciality
        """
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description="NotFound", response="not_found")

        speciality.serialize(body)
        speciality.save()

        return speciality

    def disabled(self, _id):
        """
        Disabled Speciality

        Args:
            _id (str):Speciality _id

        Returns: Speciality
        """
        speciality = Speciality.query.get(_id)

        if not speciality:
            raise HandlerException(404, "Not found speciality")

        speciality.serialize({"disabled": not speciality.disabled})
        speciality.save()

        return speciality

    def delete(self, _id):
        """
        Delete Speciality

        Args:
            _id (int): Speciality _id

        Returns (dict):
            id (int): Speciality id
        """
        speciality = Speciality.query.get(_id)

        if not speciality:
            raise HandlerException(404, "Not found speciality")

        speciality.delete()

        return {"id": speciality.id}
