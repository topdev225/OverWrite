from src.plugins.celery import celery_app


@celery_app.task
def example():
    print("example")
