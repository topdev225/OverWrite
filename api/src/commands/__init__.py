from .seed import seed
from .drop import drop
from .create_account import create_account


def init(app):
    app.cli.command("seed")(seed)
    app.cli.command("drop")(drop)
    app.cli.command("create:account")(create_account)
