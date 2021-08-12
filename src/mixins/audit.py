""" src.mixins.audit """
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func


class AuditMixin:
    """AuditMixin"""

    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), default=func.now(), onupdate=func.now())
