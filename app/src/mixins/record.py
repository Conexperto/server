from collections import OrderedDict
from datetime import datetime


class Record:
    _repr_hide = ['app', 'custom_claims', 'tokens_valid_after_timestamp']

    def serialize(self, obj):
        for k, v in obj.items():
            if k in self._repr_hide:
                continue
            if k in self.__dict__.keys() and v:
                setattr(self, k, v)
        return self

    def deserialize(self, o=None):
        result = OrderedDict()
        for k in self.__dict__.keys():
            if k in self._repr_hide:
                continue
            result[k] = getattr(self, k)

        return result

    def __repr__(self):
        vals = ', '.join("%s=%r" % (n, getattr(self,n)) for n in self.__dict__.keys() if n not in self._repr_hide)
        return "<%s={%s}>" % (self.__class__.__name__, vals)
