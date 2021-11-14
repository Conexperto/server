""" src.services.association_speciality """
from src.db import db
from src.exceptions import HandlerException
from src.models import AssociationSpeciality


class AssociationUserToSpecialityService:
    """
    AssociationUserToMethodService contains all CRUD operations
    """

    def get_by_user(self, user_id):
        """
        Get association between User and Speciality

        Args:
            user_id (int): User.id

        Returns: AssociationSpeciality
        """
        association = AssociationSpeciality.query.filter_by(
            left_id=user_id
        ).all()

        if not association:
            raise HandlerException(404, "Not found association")

        return association

    def get_speciality(self, speciality_id):
        """
        Get association between User and Speciality

        Args:
            speciality_id (int): Speciality.id

        Returns: AssociationSpeciality
        """
        association = AssociationSpeciality.query.filter_by(
            right_id=speciality_id
        ).all()

        if not association:
            raise HandlerException(404, "Not found association")

        return association

    def create(self, user_id, speciality_id):
        """
        Create association between User and Speciality

        Args:
            user_id (int): User id
            speciality_id (int): Speciality id

        Returns: AssociationSpeciality
        """
        association = AssociationSpeciality(
            left_id=user_id, right_id=speciality_id
        )

        association.add()
        association.save()

        return association

    def create_many(self, user_id, specialities):
        """
        Create many association between User and Speciality

        Args:
            user_id (int): User.id
            specialities (list<int>): List Speciality.id

        Returns: List<AssociationSpeciality>
        """
        mappings_create = []
        pipe = []

        if not isinstance(specialities, list):
            pipe.append(specialities)
        else:
            pipe = specialities

        for p in pipe:
            ass_speciality = AssociationSpeciality(
                left_id=user_id, right_id=p["speciality"]
            )
            mappings_create.append(ass_speciality)

        db.session.bulk_save_objects(mappings_create, return_defaults=True)
        db.session.commit()

        return mappings_create

    def update(self, _id, user_id, speciality_id):
        """
        Update association between User and Speciality

        Args:
            user_id (int): User.id
            speciality_id (int): Speciality.id

        Returns: AssociationSpeciality
        """
        association = AssociationSpeciality.query.get(_id)

        if not association:
            raise HandlerException(404, "Not found association")

        association.left_id = user_id
        association.right_id = speciality_id

        association.save()

        return association

    def disabled(self, _id):
        """
        Disabled association between User and Speciality

        Args:
            _id (int): AssociationSpeciality.id

        Returns: void
        """
        association = AssociationSpeciality.query.get(_id)

        if not association:
            raise HandlerException(404, "Not found association")

        association.disabled = not association.disabled
        association.save()

    def delete(self, _id):
        """
        Delete association between User and Speciality

        Args:
            _id (int): AssociationSpeciality.id

        Returns: void
        """
        association = AssociationSpeciality.query.get(_id)

        if not association:
            raise HandlerException(404, "Not found association")

        association.delete()
