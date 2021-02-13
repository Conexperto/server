from flask import abort
from src.models import Expert, \
                        Speciality, \
                        Method, \
                        Plan, \
                        AssociationMethod, \
                        AssociationSpeciality



class ExpertService:

    def get(self, _id):
        expert = Expert.query.get(_id)

        if not expert:
            abort(404, description='NotFound', response='not_found')

        return expert

    def list(self, page, per_pages=10):
        experts = Expert.query.paginate(page, per_pages or 10, error_out=False)

        return experts

    def create(self, body):
        try:
            expert = Expert(headline=body['headline'],
                            about_expert=body['about_expert'],
                            link_video=body['link_video'],
                            user_id=body['user_id'])

            if hasattr(body, 'specialities'):
                specialities = Speciality.query.filter(Speciality.id.in_(body['specialities'])).all()
                for speciality in specialities:
                    ass_speciality = AssociationSpeciality()
                    ass_speciality.speciality.append(speciality)
                    expert.speciality.append(ass_speciality)
            if hasattr(body, 'methods'):
                ids = [ method for method in body['method'] ]
                methods = Method.query.filter(Method.id.in_(ids)).all()
                for method in methods:
                    _, link = next(item for item in body['methods'] if item['method'] == method.id)
                    ass_method = AssociationMethod(link=link)
                    ass_method.method.append(method)
                expert.method.append(ass_method)
            if hasattr(body, 'plans'):
                for duration, price, coin in body['plans']:
                    expert.plan.append(
                            Plan(duration=duration, 
                                    price=price, 
                                    coin=coin))

            expert.add()
            expert.save()

            return expert
        except KeyError as ex:
            abort(400, description='BadRequest', response=str(ex))
    
    def update(self, _id, body):
        expert = Expert.query.get(_id)

        if not expert:
            abort(404, description='NotFound', response='not_found')

        expert.serialize(body)
        expert.save()


        return expert

    def update_field(self, _id, body):
        expert = Expert.query.get(_id)

        if not expert:
            abort(404, description='NotFound', response='not_found')

        expert.serialize(body)
        expert.save()

        return expert

    def disabled(self, _id):
        expert = Expert.query.get(_id)

        if not expert:
            abort(4004, description='NotFound', response='not_found')

        expert.serialize({ 'disabled': not expert.disabled })
        expert.save()

        return expert

    def delete(self, _id):
        expert = Expert.query.get(_id)

        if not expert:
            abort(404, description='NotFound', response='not_found')

        expert.delete()

        return {
            'id': expert.id
        }
