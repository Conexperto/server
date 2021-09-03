""" src.mixins.record """
from collections import OrderedDict


class Record:
    """Record"""

    __repr_hide = ["app", "tokens_valid_after_timestamp", "password"]
    __insert_hide = []

    @property
    def _repr_hide(self):
        return self.__repr_hide

    @_repr_hide.setter
    def _repr_hide(self, k):
        self.__repr_hide.append(k)

    @property
    def _insert_hide(self):
        return self.__insert_hide

    @_insert_hide.setter
    def _insert_hide(self, k):
        self.__insert_hide.append(k)

    def serialize(self, obj):
        """serialize"""
        for k, v in obj.items():
            if k in self.__repr_hide:
                continue
            if k in self.__insert_hide:
                continue
            if k in self.__dict__.keys():
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
