from flask_migrate import Migrate

# For correct models migrate
from src import models  # noqa: F401


migrate = Migrate()
