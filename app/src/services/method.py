from flask import abort 
from src.models import Method 



class MethodService:

    def get(self, _id):
        method = Method.query.get(_id)

        if not method:
            abort(404, description='NotFound', response='not_found')

        return method

    def list(self, page, per_pages=10):
        methods = Method.query.paginate(page, per_pages or 10, error_out=False)

        return methods

    def create(self, body):
        try:
            method = Speciality(name=body['name'])

            method.add()
            method.save()

            return method
        except KeyError as ex:
            abort(404, description='BadRequest', response=str(ex))

    def update(self, _id, body):
        method = Method.query.get(_id)

        if not method:
            abort(404, description='NotFound', response='not_found')

        method.serialize(body)
        method.save()

        return method

    def update_field(self, _id, body):
        method = Method.query.get(_id)

        if not method:
            abort(404, description='NotFound', response='not_found')

        method.serialize(body)
        method.save()

        return method;

    def disabled(self, _id):
        method = Method.query.get(_id)

        if not method:
            abort(404, description='NotFound', response='not_found')

        method.serialize({ 'disabled': not method.disabled })
        method.save()

        return method

    def delete(self, _id):
        method = Method.query.get(_id)

        if not method:
            abort(404, description='NotFound', response='not_found')

        method.delete()

        return {
            'id': method.id
        }
