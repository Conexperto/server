from flask_script import Command, Option
import importlib
import inspect


modules = importlib.import_module("src.seeds")

class __SeedCommand(Command):

    option_list = (
        Option('--model', 
                dest='model', 
                default='test'),
    )

    def __init__(self):
        self.modules = {}
        for name, obj in inspect.getmembers(modules):
            if inspect.isclass(obj):
                self.modules[obj.__seed__] = obj
    
    def __run_model(self, model):
        __class = self.modules[model]
        __instance = __class()
        __instance.run()

    def __run_all(self):
        for key, obj in self.modules:
            self.__run_model(key)

    def __is_option(self, model):
        if 'all' == model:
            return self.__run_all()

    def __is_model(self, model):
        if self.__is_option(model):
            return

        if not model in self.modules:
            raise TypeError("%s not found in registered modules list" % model)
        
        self.__run_model(model)


    def run(self, model):
        self.__is_model(model)
        

SeedCommand = __SeedCommand()
        




