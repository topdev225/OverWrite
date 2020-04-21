import json

from src.models import OrderItem, ProductVariant
from src.reports.helpers import attributes
from src.reports.types import CampaignReport, Table


class ItemizedShopperTable(Table):
    name = "Itemized Shopper"
    params = []
    filters = []
    sortings = []

    def generate(self, *args, **kwargs):
        # Define helpers
        report = kwargs.get("report")
        campaign = report.campaign

        # Define storage
        columns = []
        rows = []
        meta = {}

        # Define main query
        query = OrderItem.query
        order_ids = [o.id for o in campaign.orders]
        query = query.filter(OrderItem.order_id.in_(order_ids))

        # Apply modificators
        query = self.apply_filters(query)
        query = self.apply_sort(query)

        # Determine checkout fields
        checkout_fields = campaign.checkout_fields["properties"].keys()
        # Determine possible attributes
        pvs_query = ProductVariant.query.filter_by(campaign=campaign)
        attributes_ = attributes(pvs_query)

        # Set columns
        columns += checkout_fields
        columns += ["Order #", "Product Name"]
        columns += list(set([pa.name for pa in attributes_]))
        columns += ["Quantity", "Price/EA.", "Price/Total"]

        # Set rows
        order_number = None
        total_quantity = 0
        total_price = 0
        for order_item in query.all():
            if order_item.order.id != order_number:
                if order_number is None:
                    pass
                else:
                    if len(attributes_) > 0:
                        rows.append(
                            {
                                list(set([pa.name for pa in attributes_]))[-1]: "Totals",
                                "Quantity": total_quantity,
                                "Price/Total": round(total_price, 2),
                            }
                        )
                    else:
                        rows.append(
                            {"Quantity": total_quantity, "Price/Total": round(total_price, 2)}
                        )

                order_number = order_item.order.id
                total_quantity = 0
                total_price = 0
            row = {}
            row["Order #"] = order_item.order.id
            row["Product Name"] = order_item.product_variant.product.name
            row["Quantity"] = order_item.quantity
            row["Price/EA."] = round(order_item.product_variant.price, 2)
            row["Price/Total"] = round(order_item.product_variant.price * order_item.quantity, 2)
            for checkout_field in checkout_fields:
                try:
                    row[checkout_field] = order_item.order.checkout_fields[checkout_field]
                except Exception as e:
                    print(e)
            for attr in order_item.product_variant.attributes:
                row[attr["name"]] = attr["value"]
            rows.append(row)
            total_quantity += order_item.quantity
            total_price += round(order_item.product_variant.price * order_item.quantity, 2)
        # Last total
        if len(attributes_) > 0:
            rows.append(
                {
                    list(set([pa.name for pa in attributes_]))[-1]: "Totals",
                    "Quantity": total_quantity,
                    "Price/Total": round(total_price, 2),
                }
            )
        else:
            rows.append({"Quantity": total_quantity, "Price/Total": round(total_price, 2)})

        # Set meta
        meta = {
            "Total Quantity": sum(
                [row["Quantity"] for row in rows if "Totals" not in json.dumps(row)]
            ),
            "Sum of Price/Total": round(
                sum([row["Price/Total"] for row in rows if "Totals" not in json.dumps(row)]), 2
            ),
        }

        # Add signs
        for index, row in enumerate(rows):
            if "Totals" not in json.dumps(row):
                try:
                    rows[index]["Price/EA."] = self.format_price(row["Price/EA."])
                except Exception:
                    pass
            rows[index]["Price/Total"] = self.format_price(row["Price/Total"])
        meta["Sum of Price/Total"] = self.format_price(meta["Sum of Price/Total"])

        # Return
        return columns, rows, meta


class ItemizedShopperReport(CampaignReport):
    name = "Itemized Shopper"
    tables = [ItemizedShopperTable]
