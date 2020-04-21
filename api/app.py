import os

from src.create_app import create_app
from src.plugins import celery_app  # noqa: F401

if not os.path.exists("static"):
    os.mkdir("static")
if not os.path.exists("static/resources"):
    os.mkdir("static/resources")


app = create_app()


if __name__ == "__main__":
    app.run()
