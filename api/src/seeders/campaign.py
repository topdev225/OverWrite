import random

import mimesis
from safrs import DB as db

from src import models


class CampaignSeeder:
    @staticmethod
    def seed():
        business = mimesis.Business()
        datetime = mimesis.Datetime()
        text = mimesis.Text()

        default_checkout_fields = ["First Name", "Last Name"]

        distributors = models.Distributor.query.all()

        for distributor in distributors:
            campaign = models.Campaign(
                name=f"{business.company()} Distributor - {distributor.id}",
                company_name=f"Campaign distributor {distributor.id}",
                start_date=datetime.datetime(start=2018, end=2019),
                end_date=datetime.datetime(start=2020, end=2021),
                storefront_pricing=random.choice((True, False)),
                company_allowance=random.randrange(30, 200),
                company_allowance_personal_pay=random.choice((True, False)),
                items_count_limit=1000,
                price_limit=10000,
                email_shopper=random.choice((True, False)),
                checkout_fields=default_checkout_fields,
                departments=None,
                managers=None,
                message=text.sentence(),
                bfl_cost=0.0,
                distributor_po=None,
                pick_pack_partner_message=text.sentence(),
                created_by_id=1,  # we must specify this manually, since no user is logged in
                pick_pack_partner=None,
                distributor=distributor,
            )
            db.session.add(campaign)

            shopper_role = models.Role.query.filter_by(name="Shopper").first()
            admin_buyer_role = models.Role.query.filter_by(name="Admin Buyer").first()

            # swap the existing shopper account over to this campaign
            shopper = models.Account.query.filter_by(
                distributor_id=distributor.id, role=shopper_role
            ).first()
            shopper.distributor = None
            shopper.campaign = campaign
            db.session.add(shopper)

            # swap the existing admin buyer account over to this campaign
            admin_buyer = models.Account.query.filter_by(
                distributor_id=distributor.id, role=admin_buyer_role
            ).first()
            admin_buyer.distributor = None
            admin_buyer.campaign = campaign
            admin_buyer.reports_enabled = True
            db.session.add(admin_buyer)

        db.session.commit()
