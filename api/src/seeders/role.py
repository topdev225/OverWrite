from safrs import DB as db

from src import models


class RoleSeeder:
    @staticmethod
    def seed():
        names = [
            "Super Admin",
            "Distributor Manager",
            "Sales Executive",
            "Admin Buyer",
            "Shopper",
        ]

        for name in names:
            role = models.Role(name=name)
            db.session.add(role)
            db.session.flush()

        db.session.commit()
