""" src.exceptions.handler_exception """
from flask import abort
from flask import current_app


class HandlerException(Exception):
    def __init__(self, status_code, description, exception=None):
        self.__status_code = status_code
        self.__description = description
        self.__exception = exception
        self.__logger = current_app.logger
        super().__init__()

    @property
    def status_code(self):
        return self.__status_code

    @property
    def description(self):
        return self.__description

    @property
    def exception(self):
        return self.__exception

    @property
    def message(self):
        return "{} - {} \n {}".format(
            self.__status_code, self.__description, self.__exception
        )

    def logger(self):
        if self.status_code == 500:
            self.__logger.error(self.message)

        self.__logger.warning(self.message)

    def abort(self):
        self.logger()
        abort(
            self.__status_code,
            self.__description,
        )
