from dataclasses import dataclass
import json

from safrs import DB as db, SAFRSBase
from sqlalchemy.orm import validates

from src.exceptions import ValidationError
from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, SearchMixin, UpdateMixin


@dataclass
class Decoration:
    cost: float
    location: str
    logo_description: str


class CampaignProductVariant(SearchMixin, SAFRSMixin, db.Model, RoleMixin, UpdateMixin):
    """Represent the set of variants that are part of a live/complete campaign.

    Notes
    -----
    When a Campaign is in draft mode, it is linked with ProductVariant models that have dynamic
    links with the rest of the database. This makes everything editable and re-usable between
    campaigns. When a Campaign is made live, the contents of those related models are copied into
    this model. This creates a "frozen" version of the model at the moment the campaign went live.
    """

    __tablename__ = "campaign_product_variants"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    bin_id = db.Column(db.Integer, default=None)
    decorations = db.Column(db.JSON)
    margin = db.Column(db.Float)
    vendor_cost = db.Column(db.Float)

    # from Distributor
    ow_cost = db.Column(db.Float)

    # from ProductVariant
    description = db.Column(db.String)
    _sku = db.Column("sku", db.String)

    # from ProductAttributeValues
    attributes = db.Column(db.JSON)

    # from Vendor
    supplier_name = db.Column(db.String)
    supplier_email = db.Column(db.String)
    supplier_address = db.Column(db.String)

    decorator_name = db.Column(db.String)
    decorator_email = db.Column(db.String)
    decorator_address = db.Column(db.String)

    # from Product
    product_id = db.Column(db.Integer)
    product_name = db.Column(db.String)

    # from ProductType
    product_type_name = db.Column(db.String)

    # relationships
    product_variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"))
    product_variant = db.relationship("ProductVariant", foreign_keys=[product_variant_id])

    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    order_items = db.relationship("OrderItem", cascade="delete")

    @property
    def total(self):
        if not self.campaign:
            raise ValidationError(
                f"CampaignProductVariant {self.id} is not associated with a campaign"
            )

        if self.ow_cost:
            ow_cost = self.ow_cost
        elif not self.campaign.distributor:
            raise ValidationError(
                f"Campaign {self.campaign.id} is not associated with a distributor"
            )
        else:
            ow_cost = self.campaign.distributor.ow_cost

        total = self.vendor_cost + self.campaign.bfl_cost + ow_cost

        if self.decorations:
            total += sum([obj["cost"] for obj in self.decorations])

        return total

    @property
    def price(self):
        divider = 1 - (self.margin / 100)

        return round(self.total / divider, 2)

    @property
    def sku(self):
        if self._sku:
            return self._sku
        elif not self.product_variant:
            raise ValidationError(
                f"CampaignProductVariant {self.id} is not associated with a product variant"
            )

        sku = self.product_variant.sku.split("-")

        if self.decorations:
            for decoration in self.decorations:
                sku.append(decoration["location"].upper())

        return "-".join(sku)

    @sku.setter
    def sku(self, value):
        self._sku = value

    def to_dict(self):
        """Serialize this class into a SAFRS-compatible dictionary.

        Notes
        -----
        This is where we expose additional fields that are either 1) not in the model or 2) not
        automatically put in the model by SAFRS because it does not work with custom properties.
        """
        result = SAFRSBase.to_dict(self)
        result.update({"price": self.price, "sku": self.sku, "total": self.total})

        return result

    @validates("margin")
    def validate_margin(self, key, margin):
        if margin > 100:
            raise ValidationError("Margin cannot be more than 100")

        return margin

    @validates("decorations")
    def validate_decorations(self, key, value):
        if isinstance(value, str):
            value = json.loads(value)

        if not isinstance(value, list):
            raise ValidationError("Decorations must be a list")

        for item in value:
            if not isinstance(item, dict):
                raise ValidationError("Items in decorations list must be dictionaries")

            if set(item.keys()).difference({"cost", "location", "logo_description"}):
                raise ValidationError(f"Invalid keys in decoration: {item.keys()}")

        return value

    def populate_from_variant(self):
        """Copy various pieces of information into this model from its related ProductVariant

        Notes
        -----
        Call this when finalizing a campaign and moving it out of "draft" mode.
        """
        self.ow_cost = self.campaign.distributor.ow_cost
        self.description = self.product_variant.description
        self.sku = self.sku

        # copy attribute values into JSON
        attributes = []

        for attr_value in self.product_variant.attribute_values:
            attributes.append({"name": attr_value.product_attribute.name, "value": attr_value.name})

        self.attributes = attributes

        self.supplier_name = self.product_variant.supplier.name
        self.supplier_email = self.product_variant.supplier.email
        self.supplier_address = self.product_variant.supplier.address

        self.product_id = self.product_variant.product.id
        self.product_name = self.product_variant.product.name
        self.product_type_name = self.product_variant.product.product_type.name

    def populate_from_decorator(self, decorator_id):
        """Copy data from the Vendor table, representing the decorator of this variant."""
        from src.models import Vendor

        decorator = Vendor.query.get(decorator_id)

        if decorator is None:
            raise ValidationError(f"Vendor {decorator_id} does not exist")

        if not decorator.is_decorator:
            raise ValidationError(f"Vendor {decorator_id} is not a decorator")

        self.decorator_name = decorator.name
        self.decorator_email = decorator.email
        self.decorator_address = decorator.address
