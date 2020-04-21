from safrs import DB as db

from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, SoftDeleteMixin, TimestampMixin, UpdateMixin


product_type_distributors = db.Table(
    "product_type_distributors",
    db.Model.metadata,
    db.Column("product_type_id", db.Integer, db.ForeignKey("product_types.id")),
    db.Column("distributor_id", db.Integer, db.ForeignKey("distributors.id")),
)

product_type_vendors = db.Table(
    "product_type_vendors",
    db.Model.metadata,
    db.Column("product_type_id", db.Integer, db.ForeignKey("product_types.id")),
    db.Column("vendor_id", db.Integer, db.ForeignKey("vendors.id")),
)

product_type_attributes = db.Table(
    "product_type_attributes",
    db.Model.metadata,
    db.Column("product_type_id", db.Integer, db.ForeignKey("product_types.id")),
    db.Column("product_attribute_id", db.Integer, db.ForeignKey("product_attributes.id")),
)


class ProductType(SAFRSMixin, db.Model, RoleMixin, SoftDeleteMixin, TimestampMixin, UpdateMixin):
    __tablename__ = "product_types"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # relationships
    products = db.relationship("Product")
    product_attributes = db.relationship(
        "ProductAttribute", product_type_attributes, backref="product_types"
    )

    distributors = db.relationship(
        "Distributor", product_type_distributors, backref="product_types"
    )
    vendors = db.relationship("Vendor", product_type_vendors, backref="product_types")
