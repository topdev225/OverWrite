from safrs import DB as db, SAFRSBase
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, SearchMixin, TimestampMixin, UpdateMixin
from src.models.order_event import OrderEvent


class Order(SearchMixin, SAFRSMixin, db.Model, RoleMixin, TimestampMixin, UpdateMixin):
    __tablename__ = "orders"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, default="processing")
    checkout_fields = db.Column(db.JSON)

    # relationships
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
    order_items = db.relationship("OrderItem", cascade="delete")
    order_events = db.relationship("OrderEvent", cascade="delete", backref="order")
    order_notes = db.relationship("OrderNote", cascade="delete", backref="order")

    @property
    def total(self):
        total_sum = 0

        for item in self.order_items:
            total_sum += item.campaign_product_variant.price * item.quantity

        return round(total_sum, 2)

    @hybrid_property
    def fullname(self):
        if self.checkout_fields.get("First Name") and self.checkout_fields.get("Last Name"):
            return (
                f'{self.checkout_fields.get("First Name")} {self.checkout_fields.get("Last Name")}'
            )

    @validates("status")
    def validate_status(self, key, value):
        # only create an event if the status has changed and the model already exists
        if self.id and self.status != value:
            event = OrderEvent(order_id=self.id, note=f'Status changed to "{value}"')
            db.session.add(event)

        return value

    def to_dict(self):
        """Serialize this class into a SAFRS-compatible dictionary.

        Notes
        -----
        This is where we expose additional fields that are either 1) not in the model or 2) not
        automatically put in the model by SAFRS because it does not work with custom properties.
        """
        result = SAFRSBase.to_dict(self)
        result.update({"total": self.total})

        return result
