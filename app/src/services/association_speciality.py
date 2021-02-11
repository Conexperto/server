from flask import abort 
from src.models import AssociationSpeciality
from src.db import db



class AssociationExpertToSpecialityService:

    def get_expert(self, expert_id):
        # Search how make join
        association = AssociationSpeciality.query.filter_by(left_id=expert_id).all()

        if not association:
            abort(404, description='NotFound', response='not_found')

        return association

    def get_method(self, speciality_id):
        association = AssociationSpeciality.query.filter_by(right_id=speciality_id).all()
        
        if not association:
            abort(404, description='NotFound', response='not_found')

        return association

    def create(self, expert_id, speciality_id):
        association = AssociationSpeciality(left_id=expert_id, right_id=speciality_id)

        association.add()
        association.save()

        return association

    def create_many(self, expert_id, body):
        mappings_create = []
        pipe = []

        if type(body) is not list:
            pipe.append(body)
        else:
            pipe = body
        
        for p in pipe:
            ass_speciality = AssociationSpeciality(left_id=expert_id,
                                                        right_id=p['speciality'])
            mappings_create.append(ass_speciality)

        db.session.bulk_insert_mappings(AssociationSpeciality, mappings_create)

    def update(self, _id, expert_id, speciality_id):
        association = AssociationSpeciality.query.get(_id)

        if not association:
            abort(404, description='NotFound', response='not_found')

        return association

    def disabled(self, _id):
        association = AssociationSpeciality.query.get(_id)
        
        if not association: 
            abort(404, description='NotFound', response='not_found')

        association.disabled = not association.disabled
        association.save()

    def delete(self, _id):
        association = AssociationSpeciality.query.get(_id)

        if not association: 
            abort(404, description='NotFound', response='not_found')

        association.delete()

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

                update = { 'id': p['id'] }

                if hasattr(p, 'speciality'):
                    update.update({ 'right_id': p['speciality'] })

                mappings_update.append(update)
                continue

            mappings_create.append({ 
                            'left_id': expert_id, 
                            'right_id': p['speciality'] })

        db.session.bulk_update_mappings(AssociationSpeciality, mappings_update)
        db.session.bulk_insert_mappings(AssociationSpeciality, mappings_create)
        db.session.bulk_delete_mappings(AssociationSpeciality, mappings_delete)
