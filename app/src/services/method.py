from flask import abort
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import or_

from src.models import Method


class MethodService:
    def search(self, search):
        if search is None:
            return self.__query

        self.__query = self.__query.filter(Method.name.like(f"%{search}%"))
        return self.__query

    def sort(self, order_by, order):
        __order_by = ""
        __query = None

        if not order in ["desc", "asc"]:
            return

        if not hasattr(Method, order_by):
            return

        if order == "asc":
            __query = asc(order_by)
        if order == "desc":
            __query = desc(order_by)

        self.__query = self.__query.order_by(__query)
        return self.__query

    def get(self, _id):
        method = Method.query.get(_id)

        if not method:
            abort(404, description="NotFound", response="not_found")

        return method

    def list(
        self, search=None, page=1, per_page=10, order_by="created_at", order="desc"
    ):
        self.__query = Method.query

        self.search(search)
        self.sort(order_by, order)
        paginate = self.__query.paginate(int(page), int(per_page), error_out=False)
        return paginate

    def create(self, body):
        try:
            method = Method(name=body["name"])

            method.add()
            method.save()

            return method
        except KeyError as ex:
            abort(404, description="BadRequest", response=str(ex))

    def update(self, _id, body):
        method = Method.query.get(_id)

        if not method:
            abort(404, description="NotFound", response="not_found")

        method.serialize(body)
        method.save()

        return method

    def update_field(self, _id, body):
        method = Method.query.get(_id)

        if not method:
            abort(404, description="NotFound", response="not_found")

        method.serialize(body)
        method.save()

        return method

    def disabled(self, _id):
        method = Method.query.get(_id)

        if not method:
            abort(404, description="NotFound", response="not_found")

        method.serialize({"disabled": not method.disabled})
        method.save()

        return method

    def delete(self, _id):
        method = Method.query.get(_id)

        if not method:
            abort(404, description="NotFound", response="not_found")

        method.delete()

        return {"id": method.id}
