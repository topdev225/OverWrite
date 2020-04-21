from safrs import DB as db

from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, UpdateMixin


class Role(SAFRSMixin, db.Model, RoleMixin, UpdateMixin):
    __tablename__ = "roles"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    # relationships
    accounts = db.relationship("Account", cascade="delete")
