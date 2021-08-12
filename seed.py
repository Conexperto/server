"""
    SeedCommand
"""
import importlib
import inspect

from flask_script import Command
from flask_script import Option


modules = importlib.import_module("src.seeds")


class SeedCommand(Command):
    """
    SeedCommand Class
    """

    option_list = Option("--model", dest="model", default="test")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modules = {}
        for _, obj in inspect.getmembers(modules):
            if inspect.isclass(obj):
                self.modules[obj.__seed__] = obj

    def __run_model(self, model):
        __class = self.modules[model]
        __instance = __class()
        __instance.run()

    def __run_all(self):
        for key, _ in self.modules:
            self.__run_model(key)

    def __is_option(self, model):
        if not model == "all":
            return None

        return self.__run_all()

    def __is_model(self, model):
        if self.__is_option(model):
            return None

        if model not in self.modules:
            raise TypeError("%s not found in registered modules list" % model)

        return self.__run_model(model)

    # pylint: disable=arguments-differ
    def run(self, model):
        self.__is_model(model)
