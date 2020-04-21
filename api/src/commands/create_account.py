import click
from safrs import DB as db


@click.option("--username", "-u")
@click.option("--password", "-p")
@click.option("--role", "-r")
def create_account(**kwargs):
    # FIXME: make this do something eventually
    # Extract role
    # kwargs['role'] = models.Role.query.get_or_404(int(kwargs['role']))
    # account = models.Account.create(kwargs)
    # db.session.add(account)
    db.session.commit()
