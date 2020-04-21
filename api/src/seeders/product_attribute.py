import mimesis
from safrs import DB as db

from src import models


class ProductAttributeSeeder:
    @staticmethod
    def seed():
        # generate 10 random colors and sizes
        text = mimesis.Text()
        clothing = mimesis.Clothing()

        colors = list(set([text.color() for x in range(50)]))[:10]
        sizes = list(set([clothing.international_size() for x in range(50)]))[:10]

        # create a single color and size attribute to be shared by all product types
        color_attribute = models.ProductAttribute(name="Color")
        db.session.add(color_attribute)

        for color in colors:
            attribute_value = models.ProductAttributeValue(
                name=color, product_attribute_id=color_attribute.id,
            )
            db.session.add(attribute_value)

        size_attribute = models.ProductAttribute(name="Size")
        db.session.add(size_attribute)

        for size in sizes:
            attribute_value = models.ProductAttributeValue(
                name=size, product_attribute_id=size_attribute.id,
            )
            db.session.add(attribute_value)

        # link existing product types with these attributes (and values)
        product_types = models.ProductType.query.all()

        for product_type in product_types:
            product_type.product_attributes = [color_attribute, size_attribute]
            db.session.add(product_type)

        db.session.commit()
