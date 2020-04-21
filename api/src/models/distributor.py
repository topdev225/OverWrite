from safrs import DB as db
from sqlalchemy.orm import validates

from src.exceptions import ValidationError
from src.models.decorators import login_required, role_policy
from src.models.mixins import (
    RoleMixin,
    SAFRSMixin,
    SoftDeleteMixin,
    SearchMixin,
    TimestampMixin,
    UpdateMixin,
)


class Distributor(
    SearchMixin, SAFRSMixin, db.Model, RoleMixin, SoftDeleteMixin, TimestampMixin, UpdateMixin
):
    __tablename__ = "distributors"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    # FIXME: going to have to figure out which of these columns stay
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=False)
    address = db.Column(db.String, unique=False)

    ow_cost = db.Column(db.Float, default=0.0)

    campaign_cost = db.Column(db.Float, default=0.0)
    transaction_cost = db.Column(db.Float, default=0.0)
    max_sales_count = db.Column(db.Integer)

    # relationships
    accounts = db.relationship("Account", cascade="delete")
    campaigns = db.relationship("Campaign", cascade="delete")
    products = db.relationship("Product", cascade="delete")

    @validates("name")
    def validate_name(self, key, name):
        if not name or not name.replace(" ", ""):
            raise ValidationError("Distributor name is not valid")

        distributor = Distributor.query.filter_by(name=name).one_or_none()

        if distributor is not None and distributor.id != self.id:
            raise ValidationError("Distributor name already exists")

        return name
