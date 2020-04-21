from flask_cors import CORS

# FIXME: import order matters here because code is executed inside each of these modules. refactor
# to fix this, someday.
from src.plugins.auth import add_auth_endpoints
from src.plugins.logger import logger_plugin, logger  # noqa: F401
from src.plugins.sqla import sqla
from src.plugins.migrate import migrate
from src.plugins.sqltap import sqltap
from src.plugins.mail import mail
from src.plugins.celery import celery_app
from src.plugins.safrs import create_api


def init(app, db):
    CORS(app)
    logger_plugin.init_app(app)
    sqla.init_app(app)
    migrate.init_app(app, db=db)
    sqltap.init_app(app)
    mail.init_app(app)
    celery_app.init_app(app)
    create_api(app)
    add_auth_endpoints(app)
