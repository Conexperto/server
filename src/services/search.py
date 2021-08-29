from flask import abort
from sqlalchemy import asc
from sqlalchemy import desc
from sqlalchemy import or_
from sqlalchemy.orm import load_only

from src.db import db
from src.models import AssociationSpeciality
from src.models import Expert
from src.models import Speciality
from src.models import User


class SearchService:
    def sort(self, order_by, order):
        __order_by = ""
        __query = None

        if not order in ["desc", "asc"]:
            return

        if not hasattr(User, order_by):
            return

        if order == "asc":
            __query = asc(order_by)
        if order == "desc":
            __query = desc(order_by)

        self.query = self.query.order_by(__query)
        return self.query

    def projection(self):
        result = []

        for item in self.items:
            result.append(
                {
                    "email": item[0],
                    "display_name": item[1],
                    "name": item[2],
                    "lastname": item[3],
                    "headline": item[4],
                    "timezone": item[5],
                    "expert_headline": item[6],
                    "speciality": item[7],
                }
            )
        return result

    def filter(self, fragment=None):
        if fragment is None:
            return

        keywords = fragment.split()
        searchstring = "%%".join(keywords)
        searchstring = "%%%s%%" % (searchstring)

        self.query = self.query.filter(
            or_(
                User.display_name.ilike(searchstring),
                User.email.ilike(searchstring),
                User.name.ilike(searchstring),
                User.lastname.ilike(searchstring),
                User.headline.ilike(searchstring),
                User.timezone.ilike(searchstring),
                Expert.headline.ilike(searchstring),
                Speciality.name.ilike(searchstring),
            )
        )
        return self.query

    def filterBySpeciality(self, fragment=None):
        if fragment is None:
            return

        self.query = self.query.filter(Speciality.name == fragment)
        return self.query

    def suggestions(self, fragment=None):
        self.query = (
            db.session.query(
                User.email,
                User.display_name,
                User.name,
                User.lastname,
                User.headline,
                User.timezone,
                Expert.headline,
                Speciality.name,
            )
            .join(Expert)
            .join(AssociationSpeciality)
            .join(Speciality)
        )

        self.filter(fragment)
        self.items = self.query.all()

        return self.projection()

    def list(
        self,
        fragment=None,
        speciality=None,
        page=1,
        per_page=10,
        order_by="created_at",
        order="desc",
    ):
        self.query = (
            User.query.join(Expert).join(AssociationSpeciality).join(Speciality)
        )

        if speciality != None:
            self.filterBySpeciality(speciality)

        self.filter(fragment)
        self.sort(order_by, order)
        return self.query.paginate(int(page), int(per_page) or 10, error_out=False)

    def speciality(self, page=1, per_page=10, order_by="created_at", order="desc"):
        self.query = db.session.query(Speciality.id, Speciality.name).filter(
            Speciality.disabled.is_(False)
        )

        self.sort(order_by, order)
        paginate = self.query.paginate(int(page), int(per_page or 100), error_out=False)

        def projection(items):
            result = []

            for item in items:
                result.append(
                    {
                        "id": item[0],
                        "name": item[1],
                    }
                )
            return result

        paginate.items = projection(paginate.items)
        return paginate
