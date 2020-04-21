from safrs import DB as db
from sqlalchemy.orm import validates

from src.exceptions import ValidationError
from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, SearchMixin, UpdateMixin


class Vendor(SearchMixin, SAFRSMixin, db.Model, RoleMixin, UpdateMixin):
    __tablename__ = "vendors"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String)
    address = db.Column(db.String)
    is_supplier = db.Column(db.Boolean, default=False)
    is_pick_pack = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_decorator = db.Column(db.Boolean, default=False)

    # relationships
    campaigns = db.relationship("Campaign", cascade="delete")

    @validates("name")
    def validate_name(self, key, name):
        if not name or not name.replace(" ", ""):
            raise ValidationError("Name is not valid")

        vendor = Vendor.query.filter_by(name=name).one_or_none()

        if vendor is not None and vendor.id != self.id:
            raise ValidationError("Vendor name already exists")

        return name

    @validates("address")
    def validate_address(self, key, address):
        if not address or not address.replace(" ", ""):
            raise ValidationError("Address is not valid")

        return address

    @validates("email")
    def validate_email(self, key, email):
        # FIXME: actually validate e-mail addresses
        if not email or not email.replace(" ", ""):
            raise ValidationError("E-mail is not valid")

        return email

    @validates("product_types")
    def validate_product_types(self, key, value):
        if not value:
            raise ValidationError("You must select at least one product type")

        return value

    @validates("is_decorator", "is_pick_pack", "is_supplier")
    def validate_vendor_role(self, key, value):
        should_raise = False

        if value is False:
            if key == "is_supplier" and self.is_decorator is False and self.is_pick_pack is False:
                should_raise = True
            elif key == "is_decorator" and self.is_supplier is False and self.is_pick_pack is False:
                should_raise = True
            elif key == "is_pick_pack" and self.is_decorator is False and self.is_supplier is False:
                should_raise = True

        if should_raise:
            raise ValidationError("You must select one of: decorator, supplier, or pick pack")

        return value
