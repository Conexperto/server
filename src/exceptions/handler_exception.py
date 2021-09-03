""" src.exceptions.handler_exception """
from flask import abort


class HandlerException(Exception):
    def __init__(self, status_code, description):
        self.__status_code = status_code
        self.__description = description
        super().__init__()

    @property
    def status_code(self):
        return self.__status_code

    @property
    def description(self):
        return self.__description

    @property
    def message(self):
        return "{} - {}".format(
            self.__status_code,
            self.__description,
        )

    def abort(self):
        abort(
            self.__status_code,
            self.__description,
        )
