import os

from flask import Flask
from safrs import DB as db
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.contrib.profiler import ProfilerMiddleware
from werkzeug.contrib.fixers import ProxyFix

from conf import conf
from src import plugins, commands


def create_app():
    sentry_sdk.init(
        environment=os.environ.get("FLASK_ENV"),
        dsn="https://472cbb6eba964cbdb99e3ecf3697a2a8@sentry.io/2501098",
        integrations=[FlaskIntegration()],
    )

    app = Flask(
        __name__, template_folder=f"{os.getcwd()}/templates", static_folder=f"{os.getcwd()}/static"
    )

    app.config.update(conf)
    app.secret_key = conf.SECRET

    if conf.PROFILE:
        app.wsgi_app = ProfilerMiddleware(
            app.wsgi_app, sort_by=("tottime",), restrictions=[conf.PROFILE_DEPTH or 30]
        )

    plugins.init(app, db)
    commands.init(app)

    class ProxySchemeFix(object):
        def __init__(self, app):
            self.app = app

        def __call__(self, environ, start_response):
            scheme = environ.get("HTTP_X_FORWARDED_PROTO")

            if scheme:
                environ["wsgi.url_scheme"] = scheme

            return self.app(environ, start_response)

    app.wsgi_app = ProxySchemeFix(app.wsgi_app)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
