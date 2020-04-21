import mimesis
import random
from safrs import DB as db

from src import models


class DistributorSeeder:
    @staticmethod
    def seed():
        address = mimesis.Address()
        business = mimesis.Business()
        person = mimesis.Person()

        for _ in range(1, 6):
            distributor = models.Distributor(
                name=business.company(),
                email=person.email(),
                address=address.address(),
                campaign_cost=random.uniform(0, 10),
                max_sales_count=random.uniform(2, 10),
                ow_cost=random.uniform(0, 10),
            )
            db.session.add(distributor)

        db.session.commit()
