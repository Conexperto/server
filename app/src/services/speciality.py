from flask import abort 
from src.models import Speciality



class SpecialityService:

    def get(self, _id):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description='NotFound', response='not_found')

        return speciality

    def list(self, page, per_pages=10):
        specialities = Speciality.query.paginate(page, per_pages or 10, error_out=False)

        return specialities

    def create(self, body):
        try:
            speciality = Speciality(name=body['name'])

            speciality.add()
            speciality.save()

            return speciality
        except KeyError as ex:
            abort(404, description='BadRequest', response=str(ex))

    def update(self, _id, body):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description='NotFound', response='not_found')

        speciality.serialize(body)
        speciality.save()

        return speciality

    def update_field(self, _id, body):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description='NotFound', response='not_found')

        speciality.serialize(body)
        speciality.save()

        return speciality;

    def disabled(self, _id):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description='NotFound', response='not_found')

        speciality.serialize({ 'disabled': not speciality.disabled })
        speciality.save()

        return speciality

    def delete(self, _id):
        speciality = Speciality.query.get(_id)

        if not speciality:
            abort(404, description='NotFound', response='not_found')

        speciality.delete()

        return {
            'id': speciality.id
        }
