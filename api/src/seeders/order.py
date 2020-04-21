from datetime import datetime, timedelta
from random import randint

from mimesis import Datetime, Person
from safrs import DB as db

from src import models


class OrderSeeder:
    @staticmethod
    def seed():

        # Data
        m_datetime = Datetime()
        person = Person()
        dates_range = dict(
            start=(datetime.utcnow() - timedelta(days=366)).year, end=datetime.utcnow().year
        )

        _role = models.Role.query.filter_by(name="Shopper").first()
        accounts = models.Account.query.filter_by(role=_role).all()

        for account in accounts:
            # only make orders for accounts with at least one campaign
            if not account.campaign:
                continue

            # Generate and save orders
            for _ in range(randint(0, 4)):
                order = models.Order(
                    account=account,
                    campaign=account.campaign,
                    created_at=m_datetime.datetime(
                        start=dates_range["start"], end=dates_range["end"]
                    ),
                    checkout_fields={"First Name": person.name(), "Last Name": person.last_name()},
                )
                db.session.add(order)

        db.session.commit()
