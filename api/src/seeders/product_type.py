from safrs import DB as db

from src import models


class ProductTypeSeeder:
    @staticmethod
    def seed():
        distributors = models.Distributor.query.all()

        for name in {"Wearables", "Mugs", "Posters", "Pencils"}:
            product_type = models.ProductType(name=name, distributors=distributors)
            db.session.add(product_type)

        db.session.commit()
