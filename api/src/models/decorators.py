from functools import wraps
from flask import abort, request, g

from src.exceptions import LoginRequired, RoleException


def login_required(func):
    """Require that a user is logged in (i.e., is presenting a bearer token).

    This is a decorator intended to be used on REST API routes.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        from src.models import Account, Token

        if not hasattr(g, "account"):
            auth_header = request.headers.get("Authorization")
            api_key = request.args.get("api_key")

            # no api key, no auth token, no access
            if api_key:
                token = api_key
            elif auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]
            else:
                abort(401)

            token = Token.query.filter_by(token=token).one_or_none()

            # bearer token must exist in the database
            if not token:
                abort(401)

            account = Account.query.filter_by(id=token.account_id).one_or_none()

            # account must exist in the database and be active
            if not account:
                abort(401)

            if not account.active:
                abort(403, "Account is not active")

            # FIXME: this may not be the appropriate role to apply this to. the previous code had
            # hardcoded role.id == 4 and idk what that is
            if account.role.name in {"Shopper"}:
                if not any("Active" in c.status for c in account.campaigns):
                    abort(403, "At least one campaign must be active to login")

            g.account = account
            g.token = token

        return func(*args, **kwargs)

    return wrapper


def role_policy(default=None, create=None, update=None, delete=None, view=None):
    """Require a user to have certain permissions (or greater) to access an API endpoint.

    This is a decorator intended to be used on REST API routes.

    Parameters
    ----------
    default : `str`
    create : `str`
    update : `str`
    delete : `str`
    view : `str`
        The name of the role to require. Certain roles (like Super Admin) encompass many roles that
        have more restrictive permission. Provide the least restrictive permission when using this
        decorator.

    Examples
    --------
    Restrict access to Admin Buyers and any roles with more extensive permissions.

        class Campaigns(SAFRSBase):
            custom_decorators = [role_policy(default="Admin Buyers"), login_required]

    IMPORTANT: the login_required decorator must come /AFTER/ the role_policy decorator!

    Raises
    ------
    Will raise `LoginRequired` if no user is logged in. Will raise `RoleException` if current user
    does not have the correct role.
    """
    if not (create and update and delete and view) and not default:
        raise RoleException("Must specify either all permissions, or default")

    permissions = {
        "Super Admin": [
            "Super Admin",
            "Distributor Manager",
            "Sales Executive",
            "Admin Buyer",
            "Shopper",
        ],
        "Distributor Manager": ["Distributor Manager", "Sales Executive", "Admin Buyer", "Shopper"],
        "Sales Executive": ["Sales Executive", "Admin Buyer", "Shopper"],
        "Admin Buyer": ["Admin Buyer"],
        "Shopper": ["Shopper"],
    }

    policy = {
        "GET": view or default,
        "POST": create or default,
        "PATCH": update or default,
        "DELETE": delete or default,
    }

    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            required_role = policy.get(request.method)

            if not required_role:
                raise RoleException(f"Model has unknown policy for {request.method}")

            if not hasattr(g, "account"):
                raise LoginRequired(f"{required_role} role is required but user is not logged in")

            if g.account.role.name not in permissions:
                raise RoleException(f"Logged in user has unknown {required_role} role")

            if required_role not in permissions[g.account.role.name]:
                raise RoleException(f"Needs {required_role} role, has {g.account.role.name} role")

            return func(*args, **kwargs)

        return inner

    return outer
