import os 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import Config
from src.api import create_api, db
from src.seeds import TestSeed

#assert os.system('service postgresql status') == 0, 'Not postgresql daemon running.'

import src.models

api = create_api(Config)
migrate = Migrate(api, db)

manager = Manager(api)

# Command of flask migrate
manager.add_command('db', MigrateCommand)


# Comamnd of seed 
manager.add_command('seed', TestSeed())

if __name__ == "__main__":
    manager.run()




