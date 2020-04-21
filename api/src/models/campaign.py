from flask import g
from safrs import DB as db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from src.exceptions import ValidationError
from src.models.decorators import login_required, role_policy
from src.models.mixins import RoleMixin, SAFRSMixin, TimestampMixin, UpdateMixin


class Campaign(SAFRSMixin, db.Model, RoleMixin, TimestampMixin, UpdateMixin):
    __tablename__ = "campaigns"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]

    # columns are listed in groups by which page in the campaign creator they are filled in
    id = db.Column(db.Integer, primary_key=True)
    _status = db.Column(db.String, default="Active")
    complete = db.Column(db.Boolean, default=False)

    name = db.Column(db.String, unique=True)
    company_name = db.Column(db.String)
    start_date = db.Column(db.DateTime(timezone=True))
    end_date = db.Column(db.DateTime(timezone=True))

    storefront_pricing = db.Column(db.Boolean)
    company_allowance = db.Column(db.Float)
    company_allowance_personal_pay = db.Column(db.String)
    items_count_limit = db.Column(db.Integer)
    price_limit = db.Column(db.Float)
    email_shopper = db.Column(db.Boolean)

    checkout_fields = db.Column(db.JSON)
    departments = db.Column(db.JSON)
    managers = db.Column(db.JSON)

    message = db.Column(db.String)
    bfl_cost = db.Column(db.Float, default=0)
    distributor_po = db.Column(db.String)
    pick_pack_partner_message = db.Column(db.String)

    # relationships
    created_by_id = db.Column(db.Integer, db.ForeignKey("accounts.id"), nullable=True)
    created_by = db.relationship("Account", foreign_keys=[created_by_id])

    pick_pack_partner_id = db.Column(db.Integer, db.ForeignKey("vendors.id"))
    pick_pack_partner = db.relationship("Vendor", foreign_keys=[pick_pack_partner_id])

    distributor_id = db.Column(db.Integer, db.ForeignKey("distributors.id"))
    distributor = db.relationship("Distributor", foreign_keys=[distributor_id])

    campaign_product_variants = db.relationship(
        "CampaignProductVariant", cascade="delete", backref="campaign"
    )
    orders = db.relationship("Order", cascade="delete", backref="campaign")
    locations = db.relationship("Location", cascade="delete", backref="campaign")

    def __init__(self, *args, **kwargs):
        # set the default value of created_by_id to the account.id of the currently-logged in user.
        # if you are creating a Campaign model in e.g., the flask shell, you will have to manually
        # specify created_by_id in the kwargs, or this will raise (as g.account.id does not exist)
        if "created_by_id" not in kwargs or kwargs["created_by_id"] is None:
            kwargs["created_by_id"] = g.account.id

        super().__init__(*args, **kwargs)

    @validates("name")
    def validate_name(self, key, name):
        if not name or not name.replace(" ", ""):
            raise ValidationError("Campaign name is not valid")

        campaign = Campaign.query.filter_by(name=name).one_or_none()

        if campaign is not None:
            raise ValidationError("Campaign name already exists")

        return name

    @validates("end_date")
    def validate_end_date(self, key, end_date):
        if self.start_date and self.start_date > end_date:
            raise ValidationError("Start date cannot occur before end date")

        return end_date

    @hybrid_property
    def status(self):
        return self._status

    # FIXME: rewrite
    # @status.setter
    # def status(self, value):
    #     print("status")
    #     # Set status
    #     self._status = value
    #     # Determine Draft
    #     required = ["name", "company_name", "start_date", "end_date", "message"]
    #     for required_field in required:
    #         if not getattr(self, required_field):
    #             self._status = "Draft"
    #     if len(self.accounts) < 2:
    #         self._status = "Draft"

    # FIXME: rewrite
    # @hybrid_property
    # def ready_for_using(self):
    #     # Pass if already escaped Draft status
    #     if self.status != "Draft":
    #         return True

    #     # Determine ready status
    #     required = ["name", "company_name", "start_date", "end_date", "message"]
    #     ready = True
    #     for required_field in required:
    #         if not getattr(self, required_field):
    #             ready = False
    #     if len(self.accounts) < 2:
    #         ready = False

    #     try:
    #         # print(self.checkout_fields)
    #         properties = self.checkout_fields["properties"]
    #         if properties["Manager"]:
    #             managers = [a for a in self.accounts if a.role.name == "Manager"]
    #             if len(managers) == 0:
    #                 return False
    #     except Exception as e:
    #         print(e)

    #     try:
    #         properties = self.checkout_fields["properties"]
    #         if properties["Location"]:
    #             if len(self.locations) == 0:
    #                 return False
    #     except Exception as e:
    #         print(e)

    #     try:
    #         properties = self.checkout_fields["properties"]
    #         if properties["Department"]:
    #             if len(self.departments) == 0:
    #                 return False
    #     except Exception as e:
    #         print(e)

    #     return ready
