from flask import abort 
from src.models import Plan
from src.db import db



class PlanService:

    def get(self, _id):
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description='NotFound', response='not_found')

        return plan

    def list(self, page, per_pages=10):
        plans = Plan.query.paginate(page, per_pages or 10, error_out=False)

        return plans

    def create(self, body):
        try:
            plan = Plan(duration=body['duration'],
                            price=body['price'],
                            coin=body['coin'],
                            expert_id=body['expert_id'])
            plan.add()
            plan.save()

            return plan
        except KeyError as ex:
            abort(404, description='BadRequest', response=str(ex))

    def create_many(self, expert_id, body):
        mappings_create = []
        pipe = []

        if type(body) is not list:
            pipe.append(body)
        else:
            pipe = body
        
        for p in pipe:
            plan = Plan(duration=body['duration'],
                            price=body['price'],
                            coin=body['coin'],
                            expert_id=body['expert_id'])
            mappings_create.append(plan)

        db.session.bulk_insert_mappings(Plan, mappings_create)

    def update(self, _id, body):
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description='NotFound', response='not_found')

        plan.serialize(body)
        plan.save()

        return plan

    def update_field(self, _id, body):
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description='NotFound', response='not_found')

        plan.serialize(body)
        plan.save()

        return plan;

    def disabled(self, _id):
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description='NotFound', response='not_found')

        plan.serialize({ 'disabled': not method.plan })
        plan.save()

        return plan

    def delete(self, _id):
        plan = Plan.query.get(_id)

        if not plan:
            abort(404, description='NotFound', response='not_found')

        plan.delete()

        return {
            'id': plan.id
        }

    def update_or_create_and_delete_many(self, expert_id, body):
        mappings_create = []
        mappings_update = []
        mappings_delete = []
        pipe = []

        if type(body) is not list:
            pipe.append(body)
        else:
            pipe = body

        for p in pipe:
            if hasattr(p, 'id'):
                if hasattr(p, 'delete'):
                    mappings_delete.append({ 'id': p['id'] })
                    continue
                
                update = { 'id': p['id'], 'expert_id': expert_id }

                if hasattr(p, 'duration'):
                    update.update({ 'duration': p['duration'] })
                if hasattr(p, 'price'):
                    update.update({ 'price': p['price'] })
                if hasattr(p, 'coin'):
                    update.update({ 'coin': p['coin'] })
                if hasattr(p, 'disabled'):
                    update.update({ 'disabled': p['disabled'] })
                
                mappings_update.append(update)
                continue

            create = {
                'duration': p['duration'],
                'price': p['price'],
                'expert_id': expert_id
            }

            if hasattr(p, 'coin'):
                create.update({ 'coin': p['coin'] })
            if hasattr(p, 'disabled'):
                create.update({ 'disabled': p['disabled'] })

            mappings_create.append(create)

        db.session.bulk_update_mappings(Plan, mappings_update)
        db.session.bulk_insert_mappings(Plan, mappings_create)
        db.session.bulk_delete_mappings(Plan, mappings_delete)







