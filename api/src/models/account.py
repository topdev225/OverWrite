import copy
import json

from flask import g, request
from safrs import jsonapi_rpc, DB as db, SAFRSBase
from safrs.errors import GenericError
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

from src.exceptions import ValidationError
from src.models.decorators import login_required, role_policy
from src.models.helpers import hash_password
from src.models.mixins import RoleMixin, SAFRSMixin, SearchMixin, UpdateMixin


account_campaigns = db.Table(
    "account_campaigns",
    db.Model.metadata,
    db.Column("account_id", db.Integer, db.ForeignKey("accounts.id")),
    db.Column("campaign_id", db.Integer, db.ForeignKey("campaigns.id")),
)


class Account(SearchMixin, SAFRSMixin, db.Model, RoleMixin, UpdateMixin):
    __tablename__ = "accounts"

    custom_decorators = [role_policy(default="Sales Executive", view="Shopper"), login_required]
    exclude_attrs = ["_password"]

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password = db.Column(db.String)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    active = db.Column(db.Boolean, default=True)
    reports_enabled = db.Column(db.Boolean, default=True)

    # FIXME: drop basket from model. will prevent multiple shoppers from using the same account.
    basket = db.Column(db.JSON, default={})

    # relationships
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    role = db.relationship("Role", foreign_keys=[role_id])

    distributor_id = db.Column(db.Integer, db.ForeignKey("distributors.id"))
    distributor = db.relationship("Distributor", foreign_keys=[distributor_id])

    campaigns = db.relationship("Campaign", account_campaigns, backref="accounts")
    orders = db.relationship("Order", cascade="delete", backref="account")
    order_notes = db.relationship("OrderNote", cascade="delete", backref="account")
    tokens = db.relationship("Token", cascade="delete", backref="account")

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = hash_password(value)

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def campaign(self):
        return self.campaigns[0] if self.campaigns else None

    @campaign.setter
    def campaign(self, value):
        if value is None:
            self.campaigns = []
        else:
            self.campaigns = [value]

    @property
    def campaign_id(self):
        return self.campaigns[0].id if self.campaigns else None

    @campaign_id.setter
    def campaign_id(self, value):
        from src.models.campaign import Campaign

        self.campaign = Campaign.query.get(value)

    def _s_patch(self, **kwargs):
        """Patch this model in SAFRS API.

        Notes
        -----
        Allow PATCH in the SAFRS API to set the password and campaign_id. Both are custom properties
        which are (apparently) not recognized by the auto-field-generating ability of SAFRS.
        """
        SAFRSBase._s_patch(self, **kwargs)

        campaign_id = kwargs.pop("campaign_id", None)

        if campaign_id:
            self.campaign_id = campaign_id

        password = kwargs.pop("password", None)

        if password:
            self.password = password

    @classmethod
    def _s_filter(cls, args):
        """Filter this model in SAFRS API.

        Notes
        -----
        This is overloading the method in SearchMixin to allow filtering by Campaign.name. This
        relationship is a one-to-many (account to campaigns) using a join table. Unlike attributes
        that are directly on this model, or simple joins, this requires a complicated join using
        that secondary table in order to filter by Campaign.name.
        """
        from src.models.campaign import Campaign

        # pop off searching by campaign name, which requires a special join
        json_args = json.loads(args)

        for idx, term in enumerate(json_args):
            if term["field"] == "campaign_name":
                del json_args[idx]
                break
        else:
            return super()._s_filter(args)

        query = super()._s_filter(json.dumps(json_args))
        query = (
            query.join(account_campaigns, account_campaigns.c.account_id == Account.id)
            .join(Campaign, account_campaigns.c.campaign_id == Campaign.id)
            .filter(Campaign.name.ilike(f"%{term['value']}%"))
        )

        return query

    def to_dict(self):
        """Serialize this class into a SAFRS-compatible dictionary.

        Notes
        -----
        This is where we expose additional fields that are either 1) not in the model or 2) not
        automatically put in the model by SAFRS because it does not work with custom properties.
        """
        result = SAFRSBase.to_dict(self)
        result.update({"campaign_id": self.campaign_id, "password": None})

        return result

    @validates("username")
    def validate_username(self, key, username):
        if not username or not username.replace(" ", ""):
            raise ValidationError("Username is not valid")

        account = Account.query.filter_by(username=username).one_or_none()

        if account is not None and account.id != self.id:
            raise ValidationError("Username already exists")

        return username

    @validates("_password")
    def validate_password(self, key, value):
        # if nothing was specified, assume the password is to be kept and not changed
        if value is None:
            return self._password

        # password cannot be blank/empty
        if not value.replace(" ", ""):
            raise ValidationError("Password can not be empty")

        return value

    @validates("role", "role_id")
    def validate_role(self, key, role, campaign=None, distributor=None):
        if key == "role_id":
            from src.models.role import Role

            self.role = Role.query.get(role)

            return role

        # can not run this validator if there is no role
        if role is None:
            return

        if campaign is None:
            campaign = self.campaign

        if distributor is None:
            distributor = self.distributor

        # raise if there are too many sales execs associated with this distributor. we can only run
        # this validator if there is a distributor relationship loaded in this model
        if role.name == "Sales Executive" and distributor:
            sales_execs = Account.query.filter_by(
                distributor_id=distributor.id, role_id=role.id
            ).count()

            if sales_execs + 1 > distributor.max_sales_count:
                raise ValidationError(
                    f"You may only create {distributor.max_sales_count} "
                    f"Sales Executive(s) for this distributor"
                )

        # raise if we are putting this user in a campaign that already has a shopper or buyer. we
        # can only run this validator if a campaign is loaded in this model
        if role.name in {"Shopper", "Admin Buyer"} and campaign:
            for account in campaign.accounts:
                if account.id != self.id and account.role.name == role.name:
                    raise ValidationError(
                        f"Campaign {campaign.id} already has a user with the {role.name} role"
                    )

        return role

    @validates("campaigns")
    def validate_campaigns(self, key, campaign):
        # this must trigger revalidation of the user's role in relation to any new campaigns
        self.validate_role(None, self.role, campaign=campaign)

        return campaign

    @validates("distributor", "distributor_id")
    def validate_distributor(self, key, distributor):
        if key == "distributor_id":
            from src.models.distributor import Distributor

            self.distributor = Distributor.query.get(distributor)

            return distributor

        # this triggers re-validation of the user's role in consideration of this distributor
        self.validate_role(None, self.role, distributor=distributor)

        return distributor

    @jsonapi_rpc(http_methods=["GET"])
    def get_basket(self):
        """Return contents of basket as JSON.

        Removes ProductVariants which are no longer accessible to the user. This can happen if,
        for example, an item sells out or is removed from a campaign after a user has added it but
        before they have checked out.

        Returns
        -------
        `str` containing JSON dict mapping ProductVariant.id to `int` quantity
        """
        from src.models.product_variant import ProductVariant

        stripped_basket = {}

        for product_variant_id, quantity in self.basket.items():
            if ProductVariant.query.get(product_variant_id):
                stripped_basket[product_variant_id] = quantity

        self.basket = stripped_basket
        db.session.commit()

        return self.basket

    @jsonapi_rpc(http_methods=["POST"])
    def add_item_to_basket(self, product_variant_id, quantity):
        from src.models.product_variant import ProductVariant

        # this just checks that the ProductVariant exists
        ProductVariant.query.get_or_404(product_variant_id)

        new_basket = copy.deepcopy(g.account.basket)

        if quantity == 0:
            del new_basket[product_variant_id]
        else:
            new_basket[product_variant_id] = quantity

        # abort if new quantity would put cart over the price limit or total item count limit
        basket_total = 0
        basket_count = 0

        for basket_pv_id, basket_pv_quantity in new_basket.items():
            basket_pv = ProductVariant.query.get_or_404(basket_pv_id)

            basket_total += basket_pv.price * basket_pv_quantity
            basket_count += basket_pv_quantity

        if self.campaign.price_limit and basket_total > self.campaign.price_limit:
            raise GenericError("Basket total price limit exceeded", 400)

        if self.campaign.items_count_limit and basket_count > self.campaign.items_count_limit:
            raise GenericError("Basket contains more items than allowed", 400)

        self.basket = new_basket
        db.session.commit()

        return self.basket

    @jsonapi_rpc(http_methods=["POST"])
    def delete_basket(self):
        self.basket = {}
        db.session.commit()

        return self.basket

    @jsonapi_rpc(http_methods=["POST"])
    def checkout(self):
        # FIXME: this probably needs to be completely rewritten
        from src.models import Order, OrderItem
        from src.plugins import logger, mail

        basket = request.json.get("basket")

        logger.info(basket)

        order = Order(
            account=g.account,
            campaign=g.account.campaign,
            checkout_fields=request.json.get("checkout_fields"),
        )

        basketImgs = {}
        for item in basket:
            order_item = OrderItem(
                product_variant_id=int(item["product_variant_id"]), quantity=int(item["quantity"])
            )
            basketImgs[int(item["product_variant_id"])] = item["img_url"]
            db.session.add(order_item)
            order.order_items.append(order_item)

        g.account.basket = {}

        db.session.add(order)
        db.session.commit()

        basketSizes = {}
        for order_item in order.order_items:
            basketSizes[order_item.product_variant_id] = next(
                (
                    x["value"]
                    for x in order_item.product_variant.attributes
                    if x["name"] == "size" or x["name"] == "Size"
                ),
                "no size",
            )

        # send confirmation email to shopper
        if order.checkout_fields.get("Company Email"):
            try:
                mail.order_email_to_shopper(order, basketImgs, basketSizes)
            except Exception as e:
                print(e)

        return order
