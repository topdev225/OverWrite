from flask import abort, request
from safrs import DB as db, jsonapi_rpc
from sqlalchemy.ext.orderinglist import OrderingList
from sqlalchemy.orm import validates

from src.exceptions import ValidationError
from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, TimestampMixin, UpdateMixin


class SAFRSCompatibleOrderingList(OrderingList):
    """Hack to get OrderingList working with SAFRS.

    Notes
    -----
    It looks like SAFRS works explicitly with `InstrumentedList` due to an isinstance call in its
    `get_included()` method. It falls back on calling `hash()` on the list in question. This fails
    on `OrderingList` because, well, lists are not hashable. This hack makes our OrderingList appear
    to be hashable.
    """

    def __hash__(self):
        return -1


def safrs_compatible_ordering_list(attr, **kwargs):
    return lambda: SAFRSCompatibleOrderingList(attr, **kwargs)


class ProductAttribute(SAFRSMixin, db.Model, RoleMixin, TimestampMixin, UpdateMixin):
    __tablename__ = "product_attributes"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    distributors_enabled = db.Column(db.Boolean, default=False)
    sales_execs_enabled = db.Column(db.Boolean, default=False)

    # FIXME: these fields might be entirely obsolete
    assoc_product_image = db.Column(db.Boolean, default=False)
    assoc_added_costs = db.Column(db.Boolean, default=False)
    assoc_bin_id = db.Column(db.Boolean, default=False)

    # relationships
    values = db.relationship(
        "ProductAttributeValue",
        order_by="ProductAttributeValue.position",
        collection_class=safrs_compatible_ordering_list("position"),
        backref="product_attribute",
    )

    @validates("name")
    def validate_name(self, key, name):
        if not name or not name.replace(" ", ""):
            raise ValidationError("Name is not valid")

        attribute = ProductAttribute.query.filter_by(name=name).one_or_none()

        if attribute is not None and attribute.id != self.id:
            raise ValidationError("Name already exists")

        return name

    @jsonapi_rpc(http_methods=["POST"])
    def set_values_keep_order(self):
        """Set this model's ProductAttribute.values relationship, maintaining order of models.

        Notes
        -----
        Expects data to be in the following format in the request's JSON:

            {
                "data": [
                    {
                        "id": 1,
                        "type": "ProductAttributeValue"
                    },
                    {
                        "id": 4,
                        "type": "ProductAttributeValue"
                    },
                ]
            }

        This is the way that it would be specified in JSON:API if the spec (or packages we are
        using) cared about order. Since they do not, this method will have to suffice.
        """
        from src.models.product_attribute_value import ProductAttributeValue

        try:
            args = request.json
            args = args.get("data", [])
        except ValueError:
            abort(400)

        new_list = SAFRSCompatibleOrderingList("position", reorder_on_append=True)

        for spec in args:
            new_list.append(ProductAttributeValue.query.get_or_404(spec["id"]))

        self.values = new_list

        db.session.add(self)
        db.session.commit()
