import json
import random

import mimesis
from safrs import DB as db

from src import models


class CampaignProductVariantSeeder:
    @staticmethod
    def seed():
        text = mimesis.Text()

        # generate some random decorations
        decorations = []

        for _ in range(15):
            decorations.append(
                {
                    "cost": random.randint(1, 20),
                    "location": random.choice(["top", "bottom", "left", "right"]),
                    "logo_description": text.words(3),
                }
            )

        campaigns = models.Campaign.query

        for campaign in campaigns:
            products = models.Product.query.filter_by(distributor_id=campaign.distributor_id)

            for product in products:
                decorator_ids = [obj.id for obj in product.product_type.vendors if obj.is_decorator]

                for variant in product.product_variants:
                    campaign_product_variant = models.CampaignProductVariant(
                        product_variant_id=variant.id,
                        campaign_id=campaign.id,
                        decorations=json.dumps(random.sample(decorations, random.randint(1, 4))),
                        margin=random.uniform(5, 15),
                        vendor_cost=random.uniform(5, 25),
                    )
                    db.session.add(campaign_product_variant)
                    db.session.commit()

                    campaign_product_variant.populate_from_variant()
                    campaign_product_variant.populate_from_decorator(random.choice(decorator_ids))

        db.session.commit()
