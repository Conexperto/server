from flask import abort
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import or_

from src.models import Speciality


class SpecialityService:
    def search(self, search):
        if search is None:
            return self.__query

        self.__query = self.__query.filter(Speciality.name.like(f"%{search}%"))
        return self.__query

    def sort(self, order_by, order):
        __order_by = ""
        __query = None

        if not order in ["desc", "asc"]:
            return

        if not hasattr(Speciality, order_by):
            return

        if order == "asc":
            __query = asc(order_by)
        if order == "desc":
            __query = desc(order_by)

        self.__query = self.__query.order_by(__query)
        return self.__query

    def get(self, _id):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description="NotFound", response="not_found")

        return speciality

    def list(
        self, search=None, page=1, per_page=10, order_by="created_at", order="desc"
    ):
        self.__query = Speciality.query

        self.search(search)
        self.sort(order_by, order)
        paginate = self.__query.paginate(int(page), int(per_page), error_out=False)
        return paginate

    def create(self, body):
        try:
            speciality = Speciality(name=body["name"])

            speciality.add()
            speciality.save()

            return speciality
        except KeyError as ex:
            abort(404, description="BadRequest", response=str(ex))

    def update(self, _id, body):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description="NotFound", response="not_found")

        speciality.serialize(body)
        speciality.save()

        return speciality

    def update_field(self, _id, body):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description="NotFound", response="not_found")

        speciality.serialize(body)
        speciality.save()

        return speciality

    def disabled(self, _id):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description="NotFound", response="not_found")

        speciality.serialize({"disabled": not speciality.disabled})
        speciality.save()

        return speciality

    def delete(self, _id):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description="NotFound", response="not_found")

        speciality.delete()

        return {"id": speciality.id}
