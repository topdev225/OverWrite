from flask import g

from src.exceptions import LoginRequired, OrderWriteException, RoleException


# these roles have access to all models
ADMIN_ROLES = {"Super Admin"}

# these roles have access to any models associated with a given distributor
DISTRIBUTOR_ROLES = {"Distributor Manager", "Sales Executive"}

# these roles have access only to models associated with a specific campaign
CAMPAIGN_ROLES = {"Admin Buyer", "Shopper"}


class RoleMixin(object):
    """Provide role-gated access to instances of a given SQLAlchemy model.

    This is the primary mechanism by which access to models is restricted. Admins can access all
    models. Distributor roles can access campaigns they explicitly have access to, or models
    associated with their distributor. Campaign roles can access only models associated with a
    campaign they explicitly have access to.
    """

    @property
    def query(self):
        if not hasattr(g, "account"):
            raise LoginRequired

        if g.account.role.name not in ADMIN_ROLES.union(DISTRIBUTOR_ROLES).union(CAMPAIGN_ROLES):
            raise RoleException(f"{g.account.role.name} role unknown")

        if g.account.role.name in ADMIN_ROLES:
            return self.query

        if g.account.role.name in DISTRIBUTOR_ROLES:
            if hasattr(self, "distributor"):
                return self.query.filter_by(distributor=g.account.distributor)

        # if the user has a distributor-level role, but the requested model does not have
        # a distributor field, we fall through to checking if it has a campaign field
        from src.models.account import account_campaigns

        # is this model a Campaign?
        if self.__class__.__name__ == "Campaign":
            return self.query.join(
                account_campaigns, account_campaigns.campaign_id == self.__class__.id
            ).filter(account_campaigns.account_id == g.account.id)

        # does this model have a one-to-one relationship with campaigns?
        if hasattr(self, "campaign_id"):
            return self.query.join(
                account_campaigns, account_campaigns.campaign_id == self.__class__.campaign_id
            ).filter(account_campaigns.account_id == g.account.id)

        # does this model have a one-to-many relationship with campaigns?
        if hasattr(self, "campaigns"):
            raise NotImplementedError

        raise OrderWriteException(f"Model has unknown permissions for {g.account.role.name} role")
