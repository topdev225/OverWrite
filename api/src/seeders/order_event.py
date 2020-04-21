from safrs import DB as db

from src import models


class OrderEventSeeder:
    @staticmethod
    def seed():
        orders = models.Order.query.all()

        for order in orders:
            order_event = models.OrderEvent(order=order, note="Order created")
            db.session.add(order_event)

        db.session.commit()
