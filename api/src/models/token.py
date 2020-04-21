from safrs import DB as db

from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, UpdateMixin


class Token(SAFRSMixin, db.Model, RoleMixin, UpdateMixin):
    __tablename__ = "tokens"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String)
    token_type = db.Column(db.String)

    # relationships
    account_id = db.Column(db.Integer, db.ForeignKey("accounts.id"))
