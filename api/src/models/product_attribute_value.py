from safrs import DB as db

from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, TimestampMixin, UpdateMixin


class ProductAttributeValue(SAFRSMixin, db.Model, RoleMixin, TimestampMixin, UpdateMixin):
    __tablename__ = "product_attributes_values"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    position = db.Column(db.Integer, default=0)

    # relationships
    product_attribute_id = db.Column(db.Integer, db.ForeignKey("product_attributes.id"))
