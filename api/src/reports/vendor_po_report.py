from src.models import OrderItem, ProductVariant
from src.reports.helpers import attributes
from src.reports.types import CampaignReport, Table, Filter


class VendorPOTable(Table):
    name = "Vendor PO"
    params = []
    filters = [
        Filter(
            name="Vendor",
            table=name,
            model="ProductVariant",
            separator=":",
            field="vendor_name",
            op="==",
            variants="/legacy/vendors",
        )
    ]
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

        # Determine possible attributes
        pvs_query = ProductVariant.query.filter_by(campaign=campaign)
        attributes_ = attributes(pvs_query)

        # Set columns
        columns += ["Item #", "Vendor", "Product Name"]
        columns += list(set([pa.name for pa in attributes_]))
        columns += ["Quantity", "Cost", "Total Cost"]

        if self.filters[0].value:
            columns.remove("Vendor")

        # gen not repeat dict and total ordering numb
        non_repeating_data = []
        dict_total_ordering = {}
        for order_item_index, order_item in enumerate(query.all()):
            if any(
                order_item.product_variant_id == x.product_variant_id for x in non_repeating_data
            ):
                dict_total_ordering[order_item.product_variant_id] += order_item.quantity
            else:
                non_repeating_data.append(order_item)
                dict_total_ordering[order_item.product_variant_id] = order_item.quantity

        # Set rows
        for order_item in non_repeating_data:
            if order_item.order.status not in "canceled":
                row = {}
                row["Item #"] = order_item.product_variant.product.item_number
                row["Vendor"] = order_item.product_variant.vendor_name
                row["Product Name"] = order_item.product_variant.product.name
                row["Quantity"] = dict_total_ordering[order_item.product_variant_id]
                row["Cost"] = round(order_item.product_variant.vendor_cost, 2)
                row["Total Cost"] = round(
                    order_item.product_variant.vendor_cost
                    * dict_total_ordering[order_item.product_variant_id],
                    2,
                )
                for attr in order_item.product_variant.attributes:
                    row[attr["name"]] = attr["value"]
                rows.append(row)

        # Set meta
        meta["Total Quantity"] = sum([x["Quantity"] for x in rows])
        meta["Sum of Total Cost"] = round(sum([x["Total Cost"] for x in rows]), 2)

        # Add signs
        for index, row in enumerate(rows):
            rows[index]["Cost"] = self.format_price(row["Cost"])
            rows[index]["Total Cost"] = self.format_price(row["Total Cost"])
        meta["Sum of Total Cost"] = self.format_price(meta["Sum of Total Cost"])

        rows = sorted(rows, key=lambda i: i["Vendor"])

        # Return
        return columns, rows, meta


class VendorPOReport(CampaignReport):
    name = "Vendor PO"
    tables = [VendorPOTable]
