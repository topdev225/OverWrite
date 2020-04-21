import random

import mimesis
from safrs import DB as db

from src import models


class OrderNoteSeeder:
    @staticmethod
    def seed():
        text = mimesis.Text()

        orders = models.Order.query.all()
        accounts = models.Account.query.all()

        for order in orders:
            for _ in range(3):
                order_note = models.OrderNote(
                    order=order, account=random.choice(accounts), note=text.sentence()
                )
                db.session.add(order_note)

        db.session.commit()
