from safrs import SAFRSAPI


def create_api(app):
    with app.app_context():
        api = SAFRSAPI(app)

        from src import models

        for model_name in models.__all__:
            api.expose_object(getattr(models, model_name))

        # expect API objects to be accessed via HTTPS when in production
        if app.config.get("ENV").lower() == "production":
            api._swagger_object["schemes"] = ["https"]

        api._swagger_object["securityDefinitions"] = {
            "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
        }
