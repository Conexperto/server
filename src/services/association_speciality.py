""" src.services.association_speciality """
from flask import abort
from src.db import db
from src.models import AssociationSpeciality


class AssociationExpertToSpecialityService:
    """
    AssociationExpertToMethodService contains all CRUD operations
    """

    def get_expert(self, expert_id):
        """
        Get Expert

        Args:
            expert_id (int): Expert id

        Returns: (Speciality&Expert)
        """
        association = AssociationSpeciality.query.filter_by(
            left_id=expert_id
        ).all()

        if not association:
            abort(404, description="NotFound", response="not_found")

        return association

    def get_speciality(self, speciality_id):
        """
        Get Speciality

        Args:
            speciality_id (int): Speciality id

        Returns: (Speciality&Expert)
        """
        association = AssociationSpeciality.query.filter_by(
            right_id=speciality_id
        ).all()

        if not association:
            abort(404, description="NotFound", response="not_found")

        return association

    def create(self, expert_id, speciality_id):
        """
        Create association speciality expert

        Args:
            expert_id (int): Expert id
            speciality_id (int): Speciality id

        Returns: (Speciality&Expert)
        """
        association = AssociationSpeciality(
            left_id=expert_id, right_id=speciality_id
        )

        association.add()
        association.save()

        return association

    def create_many(self, expert_id, body):
        """
        Create many association speciality expert

        Args:
            expert_id (int): Expert id
            body (dict):
                speciality (int): Speciality id
        """
        mappings_create = []
        pipe = []

        if not isinstance(body, list):
            pipe.append(body)
        else:
            pipe = body

        for p in pipe:
            ass_speciality = AssociationSpeciality(
                left_id=expert_id, right_id=p["speciality"]
            )
            mappings_create.append(ass_speciality)

        db.session.bulk_insert_mappings(AssociationSpeciality, mappings_create)

    def update(self, _id, expert_id, speciality_id):
        """
        Update association speciality expert

        Args:
            expert_id (int): Expert id
            speciality_id (int): Speciality id

        Returns: (Speciality&Expert)
        """
        association = AssociationSpeciality.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.left_id = expert_id
        association.right_id = speciality_id

        association.save()

        return association

    def disabled(self, _id):
        """
        Disabled association speciality expert

        Args:
            _id (int): AssociationSpeciality id
        """
        association = AssociationSpeciality.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.disabled = not association.disabled
        association.save()

    def delete(self, _id):
        """
        Delete association speciality experto

        Args:
            _id (int): AssociationSpeciality id
        """
        association = AssociationSpeciality.query.get(_id)

        if not association:
            abort(404, description="NotFound", response="not_found")

        association.delete()

    def update_or_create_and_delete_many(self, expert_id, body):
        """
        Update or create and delete many AssociationSpeciality

        Args:
            expert_id (int): Expert id
            body (dict):
                speciality (int): Speciality id
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

                if hasattr(p, "speciality"):
                    update.update({"right_id": p["speciality"]})

                mappings_update.append(update)
                continue

            mappings_create.append(
                {"left_id": expert_id, "right_id": p["speciality"]}
            )

        db.session.bulk_update_mappings(AssociationSpeciality, mappings_update)
        db.session.bulk_insert_mappings(AssociationSpeciality, mappings_create)
