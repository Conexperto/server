from sqlalchemy import asc, desc, or_
from flask import abort
from src.models import UserRecord, \
                        User, \
                        Expert, \
                        Speciality, \
                        Method, \
                        Plan, \
                        AssociationMethod, \
                        AssociationSpeciality
from src.firebase import web_sdk
from src.db import db


class ExpertService:

    def search(self, search):
        if search is None:
            return self.__query

        self.__query = self.__query \
                    .filter(or_(
                        User.display_name.like(f"%{search}%"),
                        User.email.like(f"%{search}%"),
                        User.name.like(f"%{search}%"),
                        User.lastname.like(f"%{search}%")
                    ))
        return self.__query;

    def sort(self, order_by, order):
        __order_by = '';
        __query = None;

        if not order in ['desc', 'asc']:
            return

        if not hasattr(User, order_by):
            return

        if (order == 'asc'):
            __query = asc(order_by)
        if (order == 'desc'):
            __query = desc(order_by)

        self.__query = self.__query.order_by(__query)
        return self.__query 

    def get(self, uid):
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def list(self, 
                search=None, 
                page=1,
                per_page=10,
                order_by='created_at',
                order='desc'
    ):
        self.__query = User.query.filter(User.expert.has())

        self.search(search)
        self.sort(order_by, order)
        paginate = self.__query.paginate(
                                    int(page), 
                                    int(per_page) or 10,
                                    error_out=False)
        return paginate 

    def create(self, body):
        try:
            user = {
                'email': body['email'],
                'password': body['password'],
                'display_name': body['display_name'],
                'phone_number': body['phone_number']
            }
            user_record = UserRecord.create_user(user, app=web_sdk)
            user_record.make_claims({ 
                'complete_register': body['complete_register'] 
            })
            user = User(uid=user_record.uid,
                            email=body['email'],
                            display_name=body['display_name'],
                            phone_number=body['phone_number'],
                            name=body['name'],
                            lastname=body['lastname'],
                            headline=body['headline'],
                            about_me=body['about_me'],
                            complete_register=body['complete_register'])

            expert = Expert(headline=body['expert']['headline'],
                            about_expert=body['expert']['about_expert'],
                            link_video=body['expert']['link_video'],
                            user_id=user.id)

            if 'specialities' in body['expert']:
                body_specialities = body['expert']['specialities']
                __specialities = Speciality.query \
                                    .filter(Speciality.id.in_(body_specialities)) \
                                    .all()
                for count, __speciality in enumerate(__specialities):
                    if count > 3:
                        break;
                    __ass_speciality = AssociationSpeciality()
                    __ass_speciality.speciality = __speciality
                    expert.specialities.append(__ass_speciality)
            if 'methods' in body['expert']:
                body_methods = body['expert']['methods']
                __methods = Method.query \
                                .filter(Method.id.in_(body_methods)) \
                                .all()
                for count, __method in enumerate(__methods):
                    if count > 3:
                        break;
                    __ass_method = AssociationMethod()
                    __ass_method.method = __method
                    expert.methods.append(__ass_method)
            if 'plans' in body['expert']:
                body_plans = body['expert']['plans']
                for item in body_plans:
                    expert.plans.append(
                            Plan(duration=item['duration'], 
                                    price=item['price']))
            
            user.expert = expert
            user.add()
            user.save()

            return user
        except KeyError as ex:
            if user_record:
                user_record.delete_user();
            abort(400, description='BadRequest', response=str(ex))
    
    def update(self, uid, body):
        try:
            user_record = UserRecord.get_user(uid, app=web_sdk) 
            user = User.query.filter_by(uid=user_record.uid).first()

            if not user_record or not user:
                abort(404, description='NotFound', response='not_found')

            user_record.serialize(body)
            user_record.update_user()
            user_record.make_claims({ 'complete_register' : body['complete_register'] })

            if 'specialities' in body['expert']:
                body_specialities = body['expert']['specialities']
                __specialities = Speciality.query \
                                    .filter(Speciality.id.in_(body_specialities)) \
                                    .all()
                user.expert.specialities.clear()
                for count, __speciality in enumerate(__specialities):
                    if count > 3:
                        break;
                    __ass_speciality = AssociationSpeciality()
                    __ass_speciality.speciality = __speciality
                    user.expert.specialities.append(__ass_speciality)
            if 'methods' in body['expert']:
                body_methods = body['expert']['methods']
                __methods = Method.query \
                                .filter(Method.id.in_(body_methods)) \
                                .all()
                user.expert.methods.clear();
                for count, __method in enumerate(__methods):
                    if count > 3:
                        break;
                    __ass_method = AssociationMethod()
                    __ass_method.method = __method
                    user.expert.methods.append(__ass_method)
            if 'plans' in body['expert']:
                body_plans = body['expert']['plans']
                for item in body_plans:
                    if 'id' in item:
                        plan = Plan.query.get(item['id'])
                        plan.duration = item['duration']
                        plan.price = item['price']
                        continue
                    user.expert.plans.append(
                            Plan(duration=item['duration'], 
                                    price=item['price']))
            user.expert.serialize(body['expert'])
            user.serialize(body)
            user.save()

            return user 
        except KeyError as ex:
            abort(400, description='BadRequest', response=str(ex))

    def update_field(self, uid, body):
        try:
            user_record = UserRecord.get_user(uid, app=web_sdk) 
            user = User.query.filter_by(uid=user_record.uid).first()

            if not user_record or not user:
                abort(404, description='NotFound', response='not_found')

            user_record.serialize(body)
            user_record.update_user()
            user_record.make_claims({ 'complete_register' : body['complete_register'] })

            if 'specialities' in body['expert']:
                body_specialities = body['expert']['specialities']
                __specialities = Speciality.query \
                                    .filter(Speciality.id.in_(body_specialities)) \
                                    .all()
                user.expert.specialities.clear()
                for count, __speciality in enumerate(__specialities):
                    if count > 3:
                        break;
                    __ass_speciality = AssociationSpeciality()
                    __ass_speciality.speciality = __speciality
                    user.expert.specialities.append(__ass_speciality)
            if 'methods' in body['expert']:
                body_methods = body['expert']['methods']
                __methods = Method.query \
                                .filter(Method.id.in_(body_methods)) \
                                .all()
                user.expert.methods.clear();
                for count, __method in enumerate(__methods):
                    if count > 3:
                        break;
                    __ass_method = AssociationMethod()
                    __ass_method.method = __method
                    user.expert.methods.append(__ass_method)
            if 'plans' in body['expert']:
                body_plans = body['expert']['plans']
                for item in body_plans:
                    if 'id' in item:
                        plan = Plan.query.get(item['id'])
                        plan.duration = item['duration']
                        plan.price = item['price']
                        continue
                    expert.plans.append(
                            Plan(duration=item['duration'], 
                                    price=item['price']))
            user.expert.serialize(body['expert'])
            user.serialize(body)
            user.save()

            return user 
        except KeyError as ex:
            abort(400, description='BadRequest', response=str(ex))

    def disabled(self, uid):
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize({ 'disabled': not user_record.disabled })
        user_record.update_user()

        user.serialize({ 'disabled': not user.disabled })
        user.expert.serialize({ 'disabled': not user.expert.disabled })

        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def delete(self, _id):
        user = User.query.get(_id)

        if not expert:
            abort(404, description='NotFound', response='not_found')

        user.delete()

        return {
                'id': user.id
        }

