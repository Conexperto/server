from flask import abort

from src.db import db
from src.models import AssociationMethod


class AssociationExpertToMethodService:
    def get_expert(self, expert_id):
        # Search how make join
        association = AssociationMethod.query.filter_by(left_id=expert_id).all()

        if not association:
            abort(404, description="NotFound", response="not_found")

        return association

    def get_method(self, method_id):
        association = AssociationMethod.query.filter_by(right_id=method_id).all()

        if not association:
            abort(404, description="NotFound", response="not_found")

        return association

    def create(self, expert_id, method_id, link):
        association = AssociationMethod(
            left_id=expert_id, right_id=method_id, link=link
        )

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
            ass_method = AssociationMethod(
                left_id=expert_id, right_id=p["method"], link=p["link"]
            )
            mappings_create.append(ass_method)

        db.session.bulk_insert_mappings(AssociationMethod, mappings_create)

    def update(self, _id, expert_id, method_id, link):
        association = AssociationMethod.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.left_id = expert_id
        association.right_id = method_id
        association.link = link

        association.save()

        return association

    def disabled(self, _id):
        association = AssociationMethod.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.disabled = not association.disabled
        association.save()

    def delete(self, _id):
        association = AssociationMethod.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.delete()
