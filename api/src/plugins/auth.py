from uuid import uuid4

from flask import abort, jsonify, g, make_response, request
from safrs import DB as db

from src.models.helpers import hash_password


def add_auth_endpoints(app):
    @app.route("/auth/login", methods=["POST"])
    def login():
        from src.models.account import Account
        from src.models.token import Token

        try:
            args = request.json
        except ValueError:
            abort(400)

        account = Account.query.filter_by(username=args.get("username")).one_or_none()

        # account must exist in the database and be active
        if not account or account.password != hash_password(args.get("password")):
            abort(make_response(jsonify(message="Bad username or password"), 401))

        if not account.active:
            abort(make_response(jsonify(message="Account is not active"), 401))

        # FIXME: this may not be the appropriate role to apply this to. the previous code had
        # hardcoded role.id == 4 and idk what that is
        if account.role.name in {"Shopper"}:
            if not any("Active" in c.status for c in account.campaigns):
                abort(
                    make_response(
                        jsonify(message="At least one campaign must be active to login"), 401
                    )
                )

        # FIXME: deny access if campaign dates have passed

        # create token in database and return to user
        token = Token(account_id=account.id, token=uuid4().hex, token_type="Bearer")
        db.session.add(token)
        db.session.commit()

        return jsonify({"token": token.token, "account_id": account.id})

    @app.route("/auth/logout", methods=["POST"])
    def logout(cls):
        from src.models.token import Token

        if not hasattr(g, "token"):
            abort(make_response(jsonify(message="Not logged in"), 400))

        token = Token.query.filter_by(token=g.token.token).one_or_none()

        if token is None:
            abort(make_response(jsonify(message="Not logged in"), 400))

        db.session.delete(token)
        db.session.commit()

        return jsonify({"message": "Logged out"})
