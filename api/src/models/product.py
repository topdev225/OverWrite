from safrs import DB as db
from sqlalchemy.orm import validates

from src.exceptions import ValidationError
from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SearchMixin, SAFRSMixin, SoftDeleteMixin, UpdateMixin


class Product(SearchMixin, SAFRSMixin, db.Model, RoleMixin, SoftDeleteMixin, UpdateMixin):
    __tablename__ = "products"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    item_number = db.Column(db.String)

    # relationships
    product_type_id = db.Column(db.Integer, db.ForeignKey("product_types.id"))
    product_type = db.relationship("ProductType", foreign_keys=[product_type_id])

    distributor_id = db.Column(db.Integer, db.ForeignKey("distributors.id"))
    distributor = db.relationship("Distributor", foreign_keys=[distributor_id])

    product_variants = db.relationship("ProductVariant", cascade="delete")

    @validates("name")
    def validate_name(self, key, value):
        if not value:
            raise ValidationError("Name is empty")

        return value

    @validates("product_type", "product_type_id")
    def validate_product_type(self, key, value):
        if not value:
            setattr(self, f"_{key}_empty", True)

            if (key == "product_type" and getattr(self, "_product_type_id_empty", False)) or (
                key == "product_type_id" and getattr(self, "_product_type_empty", False)
            ):
                raise ValidationError("Product type not selected")

        return value

    @validates("distributor", "distributor_id")
    def validate_distributor(self, key, value):
        if not value:
            setattr(self, f"_{key}_empty", True)

            if (key == "distributor" and getattr(self, "_distributor_id_empty", False)) or (
                key == "distributor_id" and getattr(self, "_distributor_empty", False)
            ):
                raise ValidationError("Distributor not selected")

        return value
