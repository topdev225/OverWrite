from safrs import DB as db, SAFRSBase
from sqlalchemy.orm import validates

from src.exceptions import ValidationError
from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, UpdateMixin


product_variant_attribute_values = db.Table(
    "product_variant_attribute_values",
    db.Model.metadata,
    db.Column("product_variant_id", db.Integer, db.ForeignKey("product_variants.id")),
    db.Column(
        "product_attribute_value_id", db.Integer, db.ForeignKey("product_attributes_values.id")
    ),
)


class ProductVariant(SAFRSMixin, db.Model, RoleMixin, UpdateMixin):
    __tablename__ = "product_variants"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

    # relationships
    attribute_values = db.relationship(
        "ProductAttributeValue", product_variant_attribute_values, backref="product_variants"
    )

    supplier_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=True)
    supplier = db.relationship("Vendor", foreign_keys=[supplier_id])

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product = db.relationship("Product", foreign_keys=[product_id])

    @property
    def sku(self):
        if not self.product:
            raise ValidationError(f"ProductVariant {self.id} is not associated with a product")

        sku = [str(self.product.item_number)]

        for attr in self.attribute_values:
            sku.append(attr.name)

        return "-".join(sku)

    def to_dict(self):
        """Serialize this class into a SAFRS-compatible dictionary.

        Notes
        -----
        This is where we expose additional fields that are either 1) not in the model or 2) not
        automatically put in the model by SAFRS because it does not work with custom properties.
        """
        result = SAFRSBase.to_dict(self)
        result.update({"sku": self.sku})

        return result

    @validates("attribute_values")
    def validate_attribute_values(self, key, value, product=None):
        """Validate the values of attributes associated with this variant.

        Notes
        -----
        A variant should have exactly one attribute value for every attribute specified in its
        corresponding product type. For example, a wearable product type has color and size
        attributes. Therefore, a variant of a wearable product must have a size (e.g., XXL) and a
        color (e.g., hot pink).
        """
        if product is None:
            product = self.product

        # skip validation if no product is associated with this model
        if product is None:
            return value

        if not isinstance(value, list):
            value = [value]

        # is this value for an attribute associated with this product type?
        expected_attributes = product.product_type.product_attributes

        for item in value:
            if item.product_attribute not in expected_attributes:
                raise ValidationError(
                    f"Variant of type '{product.product_type.name}' cannot have a "
                    f"'{item.product_attribute.name}' attribute"
                )

            # has a value for this attribute already been associated with this variant?
            for attr_value in self.attribute_values:
                if attr_value.id == item.id:
                    continue

                if item.product_attribute == attr_value.product_attribute:
                    raise ValidationError(
                        f"Must specify only one value for the "
                        f"'{item.product_attribute.name}' attribute"
                    )

        return value

    @validates("product_id", "product")
    def validate_product(self, key, product):
        if key == "product_id":
            from src.models.product import Product

            self.product = Product.query.get(product)

            return product

        self.validate_attribute_values(None, self.attribute_values, product=product)

        return product
