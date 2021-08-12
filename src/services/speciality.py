""" src.services.speciality """
from flask import abort

from src.models import Speciality


class SpecialityService:
    """
    SpecialityService
    """

    def get(self, _id):
        """
        Get speciality by uid

        Args:
            _id (str): Speciality id

        Returns: Speciality
        """
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description="NotFound", response="not_found")

        return speciality

    def list(self, page, per_pages=10):
        """
        Get list specialities

        Args:
            page (int): Pagination position
            per_pages (int): Limit result by page

        Returns: list specialities
        """
        specialities = Speciality.query.paginate(page, per_pages or 10, error_out=False)

        return specialities

    def create(self, body):
        """
        Create Speciality

        Args:
            body (dict):
                name (str): Speciality name
        Returns: Expert
        """
        try:
            speciality = Speciality(name=body["name"])

            speciality.add()
            speciality.save()

            return speciality
        except KeyError as ex:
            return abort(404, description="BadRequest", response=str(ex))

    def update(self, _id, body):
        """
        Update Speciality

        Args:
            _id (int): Speciality id
            body (dict):
                name (str): Speciality name

        Returns: Speciality
        """
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description="NotFound", response="not_found")

        speciality.serialize(body)
        speciality.save()

        return speciality

    def update_field(self, _id, body):
        """
        Update Speciality

        Args:
            _id (int): Speciality uid
            body (dict):
                name (str): Speciality name

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
            abort(404, description="NotFound", response="not_found")

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
            abort(404, description="NotFound", response="not_found")

        speciality.delete()

        return {"id": speciality.id}
