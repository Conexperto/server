from flask_script import Command, Option 
import src.models

class Seed(Command):
    
    option_list = (
            Option('--model', '-m', dest='model'),
    )

    def run(self, model):
        pass
