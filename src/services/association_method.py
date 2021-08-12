""" src.services.association_method """
from flask import abort

from src.db import db
from src.models import AssociationMethod


class AssociationExpertToMethodService:
    """
    AssociationExpertToMethodService contains all CRUD operations
    """

    def get_expert(self, expert_id):
        """
        Get Expert

        Args:
            expert_id (int): Expert id

        Returns: (Method&Expert)
        """
        association = AssociationMethod.query.filter_by(left_id=expert_id).all()

        if not association:
            abort(404, description="NotFound", response="not_found")

        return association

    def get_method(self, method_id):
        """
        Get Method

        Args:
            method_id (int): Method id

        Returns: (Method&Expert)
        """
        association = AssociationMethod.query.filter_by(right_id=method_id).all()

        if not association:
            abort(404, description="NotFound", response="not_found")

        return association

    def create(self, expert_id, method_id, link):
        """
        Create association method expert

        Args:
            expert_id (int): Expert id
            method_id (int): Method id
            link (str): Link method

        Returns: (Method&Expert)
        """
        association = AssociationMethod(
            left_id=expert_id, right_id=method_id, link=link
        )

        association.add()
        association.save()

        return association

    def create_many(self, expert_id, body):
        """
        Create many association method expert

        Args:
            expert_id (int): Expert id
            body (dict):
                method (int): Method id
                link (str): Link method
        """
        mappings_create = []
        pipe = []

        if not isinstance(body, list):
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
        """
        Update association method expert

        Args:
            expert_id (int): Expert id
            method_id (int): Method id
            link (str): Link method

        Returns: (Method&Expert)
        """
        association = AssociationMethod.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.left_id = expert_id
        association.right_id = method_id
        association.link = link

        association.save()

        return association

    def disabled(self, _id):
        """
        Disabled association method expert

        Args:
            _id (int): AssociationMethod id
        """
        association = AssociationMethod.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.disabled = not association.disabled
        association.save()

    def delete(self, _id):
        """
        Delete association method experto

        Args:
            _id (int): AssociationMethod id
        """
        association = AssociationMethod.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.delete()

    def update_or_create_and_delete_many(self, expert_id, body):
        """
        Update or create and delete many AssociationMethod

        Args:
            expert_id (int): Expert id
            body (dict):
                method (int): Method id
                link (str): Link method
        """
        mappings_create = []
        mappings_update = []
        mappings_delete = []
        pipe = []

        if not isinstance(body, list):
            pipe.append(body)
        else:
            pipe = body

        for p in pipe:
            if hasattr(p, "id"):
                if hasattr(p, "delete"):
                    mappings_delete.append({"id": p["id"]})
                    continue

                update = {"id": p["id"]}

                if hasattr(p, "method"):
                    update.update({"right_id": p["method"]})
                if hasattr(p, "link"):
                    update.update({"link": p["link"]})

                mappings_update.append(update)
                continue

            mappings_create.append(
                {
                    "left_id": expert_id,
                    "right_id": p["method"],
                    "link": p["link"],
                }
            )

        db.session.bulk_update_mappings(AssociationMethod, mappings_update)
        db.session.bulk_insert_mappings(AssociationMethod, mappings_create)
