from safrs import DB as db

from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, UpdateMixin


# FIXME: is this model obsolete?
class Location(SAFRSMixin, db.Model, RoleMixin, UpdateMixin):
    __tablename__ = "locations"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String)
    company_name = db.Column(db.String)
    street_and_number = db.Column(db.String)
    city = db.Column(db.String)
    zip_code = db.Column(db.String)
    delivery_contact = db.Column(db.String)
    suite_unit_etc = db.Column(db.String)
    region = db.Column(db.String)
    country = db.Column(db.String)

    # relationships
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaigns.id"))
