""" src.services.expert """
from flask import abort

from src.models import AssociationMethod
from src.models import AssociationSpeciality
from src.models import Expert
from src.models import Method
from src.models import Plan
from src.models import Speciality


class ExpertService:
    """
    ExpertService contains all CRUD operations
    """

    def get(self, _id):
        """
        Get expert by uid

        Args:
            _id (str): Expert id

        Returns: Expert
        """
        expert = Expert.query.get(_id)

        if not expert:
            abort(404, description="NotFound", response="not_found")

        return expert

    def list(self, page, per_pages=10):
        """
        Get list expert

        Args:
            page (int): Pagination position
            per_pages (int): Limit result by page

        Returns: list experts
        """
        experts = Expert.query.paginate(page, per_pages or 10, error_out=False)

        return experts

    def create(self, body):
        """
        Create Expert

        Args:
            body (dict):
                headline (str): Headline
                about_expert (str): About Expert
                link_video (str): Link Video
                user_id (int): User id
                specialities (list[int]): Specialities id
                methods (list):
                    body (dict):
                        method (int): Method id
                        link (str): Link method
                plans (list):
                    body (dict):
                        duration (int): Duration
                        price (int): Price
                        coin (str): Coin
        Returns: Expert
        """
        try:
            expert = Expert(
                headline=body["headline"],
                about_expert=body["about_expert"],
                link_video=body["link_video"],
                user_id=body["user_id"],
            )

            if hasattr(body, "specialities"):
                self.__create_speciality(expert, body)
            if hasattr(body, "methods"):
                self.__create_method(expert, body)
            if hasattr(body, "plans"):
                self.__create_plan(expert, body)

            expert.add()
            expert.save()

            return expert
        except KeyError as ex:
            return abort(400, description="BadRequest", response=str(ex))

    def __create_speciality(self, expert, body):
        """
        Create specialities for expert
        """
        specialities = Speciality.query.filter(
            Speciality.id.in_(body["specialities"])
        ).all()
        for speciality in specialities:
            ass_speciality = AssociationSpeciality()
            ass_speciality.speciality.append(speciality)
            expert.speciality.append(ass_speciality)

    def __create_method(self, expert, body):
        """
        Create methods for expert
        """
        ids = list(body["method"])
        methods = Method.query.filter(Method.id.in_(ids)).all()
        for method in methods:
            _, link = next(
                item for item in body["methods"] if item["method"] == method.id
            )
            ass_method = AssociationMethod(link=link)
            ass_method.method.append(method)
        expert.method.append(ass_method)

    def __create_plan(self, expert, body):
        """
        Create plans for expert
        """
        for duration, price, coin in body["plans"]:
            expert.plan.append(Plan(duration=duration, price=price, coin=coin))

    def update(self, _id, body):
        """
        Update Expert

        Args:
            _id (int): Expert id
            body (dict):
                headline (str): Headline
                about_expert (str): About Expert
                link_video (str): Link Video
                user_id (int): User id
                specialities (list[int]): Specialities id
                methods (list):
                    body (dict):
                        method (int): Method id
                        link (str): Link method
                plans (list):
                    body (dict):
                        duration (int): Duration
                        price (int): Price
                        coin (str): Coin
        Returns: Expert
        """
        expert = Expert.query.get(_id)

        if not expert:
            abort(404, description="NotFound", response="not_found")

        expert.serialize(body)
        expert.save()

        return expert

    def update_field(self, _id, body):
        """
        Update Expert

        Args:
            _id (int): Expert uid
            body (dict):
                headline (str): Headline
                about_expert (str): About Expert
                link_video (str): Link Video

        Returns: Expert
        """
        expert = Expert.query.get(_id)

        if not expert:
            abort(404, description="NotFound", response="not_found")

        expert.serialize(body)
        expert.save()

        return expert

    def disabled(self, _id):
        """
        Disabled Expert

        Args:
            _id (str): Expert _id

        Returns: Expert
        """
        expert = Expert.query.get(_id)

        if not expert:
            abort(4004, description="NotFound", response="not_found")

        expert.serialize({"disabled": not expert.disabled})
        expert.save()

        return expert

    def delete(self, _id):
        """
        Delete Expert

        Args:
            _id (int): Expert _id

        Returns (dict):
            id (int): Expert id
        """
        expert = Expert.query.get(_id)

        if not expert:
            abort(404, description="NotFound", response="not_found")

        expert.delete()

        return {"id": expert.id}
