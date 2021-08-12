""" src.mixins.record """
from collections import OrderedDict


class Record:
    """Record"""

    _repr_hide = ["app", "custom_claims", "tokens_valid_after_timestamp"]

    def serialize(self, obj):
        """serialize"""
        for k, v in obj.items():
            if k in self._repr_hide:
                continue
            if k in self.__dict__.keys() and v:
                setattr(self, k, v)
        return self

    def deserialize(self):
        """deserialize"""
        result = OrderedDict()
        for k, _ in self.__dict__.items():
            if k in self._repr_hide:
                continue
            result[k] = getattr(self, k)

        return result

    def __repr__(self):
        vals = ", ".join(
            "%s=%r" % (n, getattr(self, n))
            for n, _ in self.__dict__.items()
            if n not in self._repr_hide
        )
        return "<%s={%s}>" % (self.__class__.__name__, vals)
