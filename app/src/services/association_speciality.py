from flask import abort

from src.db import db
from src.models import AssociationSpeciality


class AssociationExpertToSpecialityService:
    def get_expert(self, expert_id):
        # Search how make join
        association = AssociationSpeciality.query.filter_by(left_id=expert_id).all()

        if not association:
            abort(404, description="NotFound", response="not_found")

        return association

    def get_method(self, speciality_id):
        association = AssociationSpeciality.query.filter_by(
            right_id=speciality_id
        ).all()

        if not association:
            abort(404, description="NotFound", response="not_found")

        return association

    def create(self, expert_id, speciality_id):
        association = AssociationSpeciality(left_id=expert_id, right_id=speciality_id)

        association.add()
        association.save()

        return association

    def update(self, _id, expert_id, speciality_id):
        association = AssociationSpeciality.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        return association

    def disabled(self, _id):
        association = AssociationSpeciality.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.disabled = not association.disabled
        association.save()

    def delete(self, _id):
        association = AssociationSpeciality.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.delete()
