from safrs import DB as db
from sqlalchemy.orm import validates

from src.exceptions import ValidationError
from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, UpdateMixin


class OrderItem(SAFRSMixin, db.Model, RoleMixin, UpdateMixin):
    __tablename__ = "order_items"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)

    # relationships
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    order = db.relationship("Order", foreign_keys=[order_id])

    campaign_product_variant_id = db.Column(
        db.Integer, db.ForeignKey("campaign_product_variants.id"), nullable=False
    )
    campaign_product_variant = db.relationship(
        "CampaignProductVariant", foreign_keys=[campaign_product_variant_id]
    )

    @validates("quantity")
    def validate_quantity(self, key, quantity, order=None, campaign_product_variant=None):
        """Validate the quantity of this line item in an order.

        Parameters
        ----------
        key : `str`
            The name of the attribute to validate, i.e. quantity.
        quantity : `int`
            The quantity of this item in the order.
        order : `models.Order`
            Specifying this will use the given Order to validate the quantity. If not given, will
            use the order relationship within this model, i.e. self.order.
        campaign_product_variant : `models.CampaignProductVariant`
            Specifying this will use the given ProductVariant to validate the quantity. If not
            given, will use the relationship in the model, i.e. self.campaign_product_variant.

        Returns
        -------
        `int`, the validated quantity
        """
        if order is None:
            order = self.order

        if campaign_product_variant is None:
            campaign_product_variant = self.campaign_product_variant

        # skip this validator if no quantity was specified (let SQL catch non-nullables)
        if quantity is None:
            return quantity

        # skip this validator if the necessary related models are not set
        if not order or not campaign_product_variant:
            return quantity

        # disallow changes if an order is not processing
        if order.status != "processing":
            raise ValidationError("Cannot update an order that is canceled or shipped")

        # skip the rest of this validator if neither limit is set
        if not (order.campaign.price_limit or order.campaign.items_count_limit):
            return quantity

        # raise if new quantity would put cart over the price limit or total item count limit
        basket_total = 0
        basket_count = 0

        for order_item in order.order_items:
            if order_item.campaign_product_variant_id == campaign_product_variant.id:
                continue

            basket_total += order_item.campaign_product_variant.price * order_item.quantity
            basket_count += order_item.quantity

        basket_total += campaign_product_variant.price * quantity
        basket_count += quantity

        if order.campaign.price_limit and basket_total > order.campaign.price_limit:
            raise ValidationError("Basket total price limit exceeded")

        if order.campaign.items_count_limit and basket_count > order.campaign.items_count_limit:
            raise ValidationError("Basket contains more items than allowed")

        return quantity

    # to validate quantity, two relationships are required: Order and CampaignProductVariant. if
    # either of those is not present in the model, quantity validation cannot occur. if either of
    # those model relationships changes, we need to re-validate the quantity, which we trigger here.
    @validates("order_id", "order")
    def validate_order(self, key, order):
        if key == "order_id":
            from src.models.order import Order

            self.order = Order.query.get(order)

            return order

        self.validate_quantity(None, self.quantity, order=order)

        return order

    @validates("campaign_product_variant_id", "campaign_product_variant")
    def validate_campaign_product_variant(self, key, campaign_product_variant):
        if key == "campaign_product_variant_id":
            from src.models.campaign_product_variant import CampaignProductVariant

            self.campaign_product_variant = CampaignProductVariant.query.get(
                campaign_product_variant
            )

            return campaign_product_variant

        # if we are changing this line item to another variant, ensure that it has the same
        # product_id as the previous item. we want to allow switching between variants within a
        # product--not changing products entirely!
        if self.campaign_product_variant is not None:
            if self.campaign_product_variant.product_id != campaign_product_variant.product_id:
                raise ValidationError(
                    "Can only change to variants of the same product. "
                    "Changing to a different product is currently unsupported."
                )

            if self.campaign_product_variant.campaign_id != campaign_product_variant.campaign_id:
                raise ValidationError(
                    "The variant you selected was not sold in the campaign associated "
                    "with this order"
                )

        self.validate_quantity(
            None, self.quantity, campaign_product_variant=campaign_product_variant
        )

        # skip the rest of this validator if order is not set
        if not self.order:
            return campaign_product_variant

        # disallow changes if an order is not processing
        if self.order.status != "processing":
            raise ValidationError("Cannot update an order that is canceled or shipped")

        return campaign_product_variant
