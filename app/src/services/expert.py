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

            if 'specialities' in body:
                body_specialities = body['specialities']
                __specialities = Speciality.query.filter(
                                                        Speciality.id.in_(body_specialities)
                                                    ) \
                                                    .all()
                for __speciality in __specialities:
                    __ass_speciality = AssociationSpeciality()
                    __ass_speciality.speciality.append(__speciality)
                    expert.specialities.append(__ass_speciality)
            if 'methods' in body:
                body_methods = body['methods']
                __methods = Method.query.filter(
                                                    Method.id.in_([method for _, method in body_methods])
                                            ) \
                                            .all()
                for __method in __methods:
                    _, link = next(item for item in body_methods if item['method'] == __method.id)
                    __ass_method = AssociationMethod(link=link)
                    __ass_method.method.append(__method)
                    expert.methods.append(ass_method)
            if 'plans' in body:
                body_plans = body['plans']
                for item in body_plans:
                    expert.plans.append(
                            Plan(duration=item['duration'], 
                                    price=item['price'], 
                                    coin=item['coin']))

            expert.add()
            expert.save()

            return expert
        except KeyError as ex:
            abort(400, description='BadRequest', response=str(ex))
    
    def update(self, _id, body):
        expert = Expert.query.get(_id)

        if not expert:
            abort(404, description='NotFound', response='not_found')
        
        if 'specialities' in body:
            self.__specialities(expert, body['specialities'])
        if 'methods' in body:
            self.__methods(expert, body['methods'])
        if 'plans' in body:
            self.__plans(expert, body)

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

    def __specialities(self, expert, body):
        specialities = expert.specialities

        for item in body:
            mode = item['mode']
            _id = item['id']
        
            if mode == 'delete':
                __filter = list(filter(lambda item: item[1]['id'] == _id), enumerate(specialities))
                pos, *_ = __filter[0]
                del expert.specialities[pos]
                continue
            speciality = Speciality.query.get(_id)
            ass = AssociationSpeciality()
            ass.speciality.append(speciality)
            expert.specialities.append(ass)

        return expert

    def __methods(self, expert, body):
        methods = expert.methods

        for item in body:
            mode = item['mode']
            _id = item['id']

            if mode == 'delete':
                __filter = list(filter(lambda item: item[1]['id'], enumerate(methods)))
                pos, *_ = __filter[0]
                del expert.methods[pos]
                continue

            if mode == 'update':
                __filter = list(filter(lambda item: item[1]['id'], enumerate(methods)))
                pos, *_ = __filter[0]
                method = expert.methods[0]
                method.link = item['link']
                continue

            method = Method.query.get(_id)
            ass = AssociationMethod()
            ass.methods.append(method)
            expert.methods.append(ass)

        return expert

    def __plans(self, expert, body):
        plans = expert.plans

        for item in body:
            mode = item['mode']
            _id = item['id']
