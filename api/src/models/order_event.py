from safrs import DB as db

from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, TimestampMixin, UpdateMixin


class OrderEvent(SAFRSMixin, db.Model, RoleMixin, TimestampMixin, UpdateMixin):
    __tablename__ = "order_events"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String)

    # relationships
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
