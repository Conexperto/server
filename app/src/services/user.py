from sqlalchemy import asc, desc, or_
from flask import abort
from src.models import UserRecord, User
from src.firebase import web_sdk



class UserService:

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

    def list(self, search=None, page=1, per_page=10, order_by='created_at', order='desc'):
        self.__query = User.query
        
        self.search(search)
        self.sort(order_by, order)
        paginate = self.__query.paginate(int(page), int(per_page) or 10, error_out=False)
        
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
            user_record.make_claims({ 'complete_register': body['complete_register'] if hasattr(body, 'complete_register') else False })
            
            user = User(uid=user_record.uid,
                            email=body['email'],
                            display_name=body['display_name'],
                            phone_number=body['phone_number'],
                            name=body['name'],
                            lastname=body['lastname'],
                            headline=body['headline'],
                            about_me=body['about_me'],
                            complete_register=body['complete_register'] if hasattr(body, 'complete_register') else False)

            user.add()
            user.save()

            return {
                'uid': user_record.uid,
                'a': user_record,
                'b': user
            }
        except KeyError as ex:
            abort(400, description='BadRequest', response=str(ex))

    def update(self, uid, body):
        user_record = UserRecord.get_user(uid, app=web_sdk) 
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize(body)
        user_record.update_user()
            
        if hasattr(body, 'complete_register'):
            user_record.make_claims({ 'complete_register' : body['complete_register'] })

        user.serialize(body)
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def update_field(self, uid, body):
        user_record = UserRecord.get_user(uid, app=web_sdk) 
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize(body)
        user_record.update_user()
        
        if hasattr(body, 'complete_register'):
            user_record.make_claims({ 'complete_register' :  body['complete_register'] })

        user.serialize(body)
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def disabled(self, uid):
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize({ 'disabled': not user_record.disabled })
        user_record.update_user()

        user.serialize({ 'disabled': not user_record.disabled })
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }


    def delete(self, uid):
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        user_record.delete_user()
        user.delete()

        return {
            'uid': user_record.uid
        }

    def delete_many(self, uid):
        pass
