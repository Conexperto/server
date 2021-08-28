from collections import OrderedDict
from datetime import datetime


class Record:
    __repr_hide = ['app', 'tokens_valid_after_timestamp']
    __insert_hide = []
    
    @property
    def _repr_hide(self):
        return self.__repr_hide;

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
        for k, v in obj.items():
            if k in self.__repr_hide:
                continue
            if k in self.__insert_hide:
                continue
            if k in self.__dict__.keys():
                setattr(self, k, v)
        return self

    def deserialize(self, o=None):
        result = OrderedDict()
        for k in self.__dict__.keys():
            if k in self.__repr_hide:
                continue
            result[k] = getattr(self, k)
        return result

    def __repr__(self):
        vals = ', '.join("%s=%r" % (n, getattr(self,n)) for n in self.__dict__.keys() if n not in self.__repr_hide)
        return "<%s={%s}>" % (self.__class__.__name__, vals)
