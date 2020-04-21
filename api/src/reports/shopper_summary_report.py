import pytz

from src.models import Order
from src.reports.types import CampaignReport, Table


class ShopperSummaryTable(Table):
    name = "Shopper Summary"
    params = []
    filters = []
    sortings = []

    def generate(self, *args, **kwargs):
        # Define helpers
        report = kwargs.get("report")
        campaign = report.campaign
        timezone = report.timezone
        print("timezone")
        print(timezone)

        # Define storage
        columns = []
        rows = []
        meta = {}

        # Define main query
        query = Order.query.filter_by(campaign=campaign)

        # Apply modificators
        query = self.apply_filters(query)
        query = self.apply_sort(query)

        # Determine checkout fields
        checkout_fields = campaign.checkout_fields["properties"].keys()

        # Set columns
        columns += checkout_fields
        columns += ["Order #", "Date Order Placed", "Items", "Sales"]
        fmt = "%m/%d/%Y, %H:%M:%S"

        # Set rows
        for order in query.all():
            if not len(order.order_items):
                continue
            row = {}
            row["Order #"] = order.id
            # row['Date Order Placed'] = order.created_at \
            #     .strftime('%m/%d/%Y, %H:%M:%S')
            custom_zone = pytz.timezone(timezone)
            local_dt = order.created_at.replace(tzinfo=pytz.utc).astimezone(custom_zone)
            row["Date Order Placed"] = local_dt.strftime(fmt)

            row["Items"] = sum([oi.quantity for oi in order.order_items])
            row["Sales"] = round(order.total, 2)
            for checkout_field in checkout_fields:
                try:
                    row[checkout_field] = order.checkout_fields[checkout_field]
                except Exception as e:
                    print(e)
            rows.append(row)

        # Set meta
        meta = {
            "Total Orders": len(rows),
            "Total Items": sum([row["Items"] for row in rows]),
            "Total Sales": round(sum([row["Sales"] for row in rows]), 2),
        }
        meta["Total Sales"] = self.format_price(meta["Total Sales"])

        # Add signs
        for index, row in enumerate(rows):
            rows[index]["Sales"] = self.format_price(row["Sales"])

        # Return
        return columns, rows, meta


class ShopperSummaryReport(CampaignReport):
    name = "Shopper Summary"
    tables = [ShopperSummaryTable]
