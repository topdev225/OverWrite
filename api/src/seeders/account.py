import mimesis
import random
from safrs import DB as db

from src import models


class AccountSeeder:
    @staticmethod
    def seed():
        person = mimesis.Person()

        super_admin_role = models.Role.query.filter_by(name="Super Admin").first()
        account = models.Account(
            username="admin",
            password="admin",
            email="admin@gmail.com",
            first_name="admin",
            last_name="admin",
            role=super_admin_role,
        )
        db.session.add(account)
        db.session.commit()

        distributors = models.Distributor.query.all()
        user_roles = models.Role.query.filter(models.Role.name != "Super Admin").all()

        for distributor in distributors:
            for user_role in user_roles:
                num_accounts = 2 if user_role.name not in {"Shopper", "Admin Buyer"} else 1

                for _ in range(num_accounts):
                    first_name = person.first_name()
                    last_name = person.last_name()
                    username = f"{first_name[0]}{last_name}{random.randint(1, 9)}"

                    account = models.Account(
                        username=username.lower(),
                        password="password",
                        email=person.email(),
                        first_name=first_name,
                        last_name=last_name,
                        distributor_id=distributor.id,
                        role=user_role,
                    )
                    db.session.add(account)

        db.session.commit()
