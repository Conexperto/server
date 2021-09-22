""" src.services.association_method """
from src.db import db
from src.exceptions import HandlerException
from src.models import AssociationMethod


class AssociationUserToMethodService:
    """
    AssociationExpertToMethodService contains all CRUD operations
    """

    def get_by_user(self, user_id):
        """
        Get association between User and Method

        Args:
            user_id (int): User.id

        Returns: AssociationMethod
        """
        association = AssociationMethod.query.filter_by(left_id=user_id).all()

        if not association:
            raise HandlerException(404, "Not found association")

        return association

    def get_by_method(self, method_id):
        """
        Get association between User and Method

        Args:
            method_id (int): Method.id

        Returns: AssociationMethod
        """
        association = AssociationMethod.query.filter_by(right_id=method_id).all()

        if not association:
            raise HandlerException(404, "Not found association")

        return association

    def create(self, user_id, method_id, link):
        """
        Create association between User and Method

        Args:
            user_id (int): User.id
            method_id (int): Method.id
            link (str): Link method

        Returns: AssociationMethod
        """
        association = AssociationMethod(left_id=user_id, right_id=method_id, link=link)

        association.add()
        association.save()

        return association

    def create_many(self, user_id, methods):
        """
        Create many association between User and Method

        Args:
            user_id (int): User.id
            methods (list<dict>):
                method (int): Method.id
                link (str): Link method

        Returns: List<AssociationMethod>
        """
        mappings_create = []
        pipe = []

        if not isinstance(methods, list):
            pipe.append(methods)
        else:
            pipe = methods

        for p in pipe:
            ass_method = AssociationMethod(
                left_id=user_id, right_id=p["method"], link=p["link"]
            )
            mappings_create.append(ass_method)

        db.session.bulk_save_objects(mappings_create, return_defaults=True)
        db.session.commit()

        return mappings_create

    def update(self, _id, user_id, method_id, link):
        """
        Update association between User and Method

        Args:
            user_id (int): User.id
            method_id (int): Method.id
            link (str): Link method

        Returns: AssociationMethod
        """
        association = AssociationMethod.query.get(_id)

        if not association:
            raise HandlerException(404, "Not found association")

        association.left_id = user_id
        association.right_id = method_id
        association.link = link

        association.save()

        return association

    def disabled(self, _id):
        """
        Disabled association between User and Method

        Args:
            _id (int): AssociationMethod id
        """
        association = AssociationMethod.query.get(_id)

        if not association:
            raise HandlerException(404, "Not found association")

        association.disabled = not association.disabled
        association.save()

    def delete(self, _id):
        """
        Delete association method experto

        Args:
            _id (int): AssociationMethod id

        Returns: void
        """
        association = AssociationMethod.query.get(_id)

        if not association:
            raise HandlerException(404, "Not found association")

        association.delete()
