import json

from src.models import OrderItem, ProductVariant
from src.reports.helpers import attributes
from src.reports.types import CampaignReport, Table


class SalesExecutivesShopperTable(Table):

    name = "Sales Executives' Shopper"
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

        # Group order items by order
        orders = {}
        for oi in query.all():
            if not orders.get(str(oi.order.id)):
                orders[str(oi.order.id)] = []
            orders[str(oi.order.id)].append(oi)

        from src.plugins import logger

        logger.info(orders)

        # Set columns
        columns += checkout_fields
        columns += ["Order #", "SKU", "Item #", "Vendor", "Product Name"]
        columns += list(set([pa.name for pa in attributes_]))
        columns += ["Quantity", "Price/EA.", "Price/Total"]

        # Set rows
        for order_id, order_items in orders.items():
            total_qty = 0
            total_price = 0
            is_canceled = False
            for order_item in order_items:
                if order_item.order.status not in "canceled":
                    row = {}
                    row["Order #"] = order_item.order.id
                    row["SKU"] = order_item.product_variant.sku
                    row["Item #"] = order_item.product_variant.product.item_number
                    row["Vendor"] = order_item.product_variant.vendor_name
                    row["Product Name"] = order_item.product_variant.product.name
                    row["Quantity"] = order_item.quantity
                    row["Price/EA."] = round(order_item.product_variant.price, 2)
                    row["Price/Total"] = round(
                        order_item.product_variant.price * order_item.quantity, 2
                    )
                    for checkout_field in checkout_fields:
                        try:
                            row[checkout_field] = order_item.order.checkout_fields[checkout_field]
                        except Exception as e:
                            print(e)
                    for attr in order_item.product_variant.attributes:
                        row[attr["name"]] = attr["value"]
                    total_qty += order_item.quantity
                    total_price += round(order_item.product_variant.price * order_item.quantity, 2)
                    rows.append(row)
                else:
                    is_canceled = True

            # Totals for order
            if not is_canceled:
                row = {}
                if len(attributes_) > 0:
                    row[list(set([pa.name for pa in attributes_]))[-1]] = "Totals"
                row["Quantity"] = total_qty
                row["Price/Total"] = round(total_price, 2)
                rows.append(row)

        # Set meta
        meta = {
            "Total Quantity": sum(
                [row["Quantity"] for row in rows if "Totals" not in json.dumps(row)]
            ),
            "Sum of Price/Total": round(
                sum([row["Price/Total"] for row in rows if "Totals" not in json.dumps(row)]), 2
            ),
        }

        # Format and add signs
        for index, row in enumerate(rows):
            if "Price/EA." in row:
                rows[index]["Price/EA."] = self.format_price(row["Price/EA."])
            rows[index]["Price/Total"] = self.format_price(row["Price/Total"])
        meta["Sum of Price/Total"] = self.format_price(meta["Sum of Price/Total"])

        # Return
        return columns, rows, meta


class SalesExecutivesShopperReport(CampaignReport):
    name = "Sales Executives' Shopper"
    tables = [SalesExecutivesShopperTable]
