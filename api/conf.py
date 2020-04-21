from addict import Dict
from copy import deepcopy
import os
import logging


configs = Dict()

configs.update(
    Dict(
        development=Dict(
            SECRET="asdfsghfjg",
            VERSION="0.2.7",
            DEBUG=True,
            PROFILE=False,
            SQLTAP=False,
            PROFILE_DEPTH=100,
            SQLTAP_PATH="./static/sqltap.html",
            SQLTAP_EXCLUDE=["/static/sqltap.html"],
            LOG_PATH="./static/log.txt",
            LOG_LEVEL=logging.DEBUG,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_PORT=465,
            MAIL_USE_TLS=False,
            MAIL_USE_SSL=True,
            MAIL_USERNAME="donotreply@myorderwrite.com",
            MAIL_PASSWORD="orderwrite",
            MAIL_DEFAULT_SENDER="OrderWrite <donotreply@myorderwrite.com>",
            SQLALCHEMY_DATABASE_URI=(
                os.environ.get(
                    "DATABASE_URL", "postgresql://orderwrite:orderwrite_secret@postgres/orderwrite"
                )
            ),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            PREFERRED_URL_SCHEME="http",
            SEEDERS=[
                "RoleSeeder",
                "DistributorSeeder",
                "ProductTypeSeeder",
                "ProductAttributeSeeder",
                "AccountSeeder",
                "VendorSeeder",
                "CampaignSeeder",
                "LocationSeeder",
                "ProductSeeder",
                "ProductVariantSeeder",
                "CampaignProductVariantSeeder",
                "OrderSeeder",
                "OrderItemSeeder",
                "OrderEventSeeder",
                "OrderNoteSeeder",
            ],
        )
    )
)

configs.development_server = deepcopy(configs.development)
configs.development_server.update(Dict(PROFILE=False, SQLTAP=False, PREFERRED_URL_SCHEME="https"))

configs.stage = deepcopy(configs.development_server)
configs.stage.update(Dict(SEEDERS=["RoleSeeder"]))

configs.production = deepcopy(configs.stage)
configs.production.update(
    Dict(SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL"), PREFERRED_URL_SCHEME="https")
)

conf = configs[os.environ.get("FLASK_ENV") or "development"]
