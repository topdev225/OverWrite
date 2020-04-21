import random

from safrs import DB as db
from safrs.errors import GenericError

from src import models


class OrderItemSeeder:
    @staticmethod
    def seed():
        orders = models.Order.query.all()

        for order in orders:
            campaign_product_variants = order.campaign.campaign_product_variants

            for _ in range(random.randint(1, 5)):
                try:
                    order_item = models.OrderItem(
                        order=order,
                        campaign_product_variant=random.choice(campaign_product_variants),
                        quantity=random.randint(1, 3),
                    )
                    db.session.add(order_item)
                    db.session.commit()
                except GenericError:
                    # FIXME: this means we just randomly fill orders with items until the item or
                    # price limits are reached. possibly that's okay.
                    db.session.rollback()
