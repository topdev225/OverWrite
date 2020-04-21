import logging
from flask import request, Response
import traceback

from conf import conf


class Logger:
    def __init__(self, logger, app=None):
        self.logger = logger
        if app:
            raise NotImplementedError

    def init_app(self, app):
        app.after_request(self.after_request)
        app.errorhandler(Exception)(self.exceptions)
        app.route("/log/tail/<rows_count>")(self.tail)

    def after_request(self, response):
        self.logger.info(
            "%s %s %s %s %s",
            request.remote_addr,
            request.method,
            request.scheme,
            request.full_path,
            response.status,
        )
        return response

    def exceptions(self, e):
        tb = traceback.format_exc()
        self.logger.error(
            "%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s",
            request.remote_addr,
            request.method,
            request.scheme,
            request.full_path,
            tb,
        )
        return e

    @staticmethod
    def tail(rows_count):
        with open(conf.LOG_PATH) as f:
            rows = f.readlines()
            rows = rows[-(int(rows_count)) :]
        return Response("".join(rows), mimetype="text/plain")


logger = logging.getLogger("flask")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

fileHandler = logging.FileHandler(conf.LOG_PATH)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

logger.setLevel(conf.LOG_LEVEL)


logger_plugin = Logger(logger)
