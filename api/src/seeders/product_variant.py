import random

import mimesis
from safrs import DB as db

from src import models


class ProductVariantSeeder:
    @staticmethod
    def seed():
        text = mimesis.Text()

        products = models.Product.query.all()

        for product in products:
            for _ in range(random.randint(1, 3)):
                attributes = []

                for attribute in product.product_type.product_attributes:
                    attributes.append(random.choice(attribute.values))

                supplier = [obj for obj in product.product_type.vendors if obj.is_supplier is True][
                    0
                ]

                product_variant = models.ProductVariant(
                    description=text.title(),
                    attribute_values=attributes,
                    supplier=supplier,
                    product=product,
                )
                db.session.add(product_variant)

        db.session.commit()
