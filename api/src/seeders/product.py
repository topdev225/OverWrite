import random

import mimesis
from safrs import DB as db

from src import models


class ProductSeeder:
    @staticmethod
    def seed():
        text = mimesis.Text()

        product_types = models.ProductType.query.all()

        for product_type in product_types:
            for distributor in product_type.distributors:
                for _ in range(2):
                    product = models.Product(
                        name=f"{text.swear_word()} {product_type.name.rstrip('s')}",
                        item_number=str(random.randint(0, 10000)),
                        product_type=product_type,
                        distributor=distributor,
                    )
                    db.session.add(product)

        db.session.commit()
