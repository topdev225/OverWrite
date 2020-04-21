from src.models import OrderItem, ProductVariant

from src.const import SORT_ORDER

from src.reports.helpers import attributes, identifier, max_decorations
from src.reports.types import CampaignReport, Table


def total_items_ordered(campaign):
    query_order = OrderItem.query
    order_ids = [o.id for o in campaign.orders]
    query_order = query_order.filter(OrderItem.order_id.in_(order_ids))
    # Group order items by order
    orders = {}
    for oi in query_order.all():
        if not orders.get(str(oi.order.id)):
            orders[str(oi.order.id)] = []
        orders[str(oi.order.id)].append(oi)

    total = 0
    for order_id, order_items in orders.items():
        for order_item in order_items:
            if order_item.order.status not in "canceled":
                total += order_item.quantity

    return total


class DecoratorPOTable(Table):
    name = "Decorator PO"
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

        # Define a main order query
        query_order = OrderItem.query
        order_ids = [o.id for o in campaign.orders]
        query_order = query_order.filter(OrderItem.order_id.in_(order_ids))
        # Group order items by order
        orders = {}
        for oi in query_order.all():
            if not orders.get(str(oi.order.id)):
                orders[str(oi.order.id)] = []
            orders[str(oi.order.id)].append(oi)

        # Define main query
        query = ProductVariant.query.filter_by(campaign=campaign)

        # Apply modificators
        query = self.apply_filters(query)
        query = self.apply_sort(query)

        # Determine possible attributes
        attributes_ = attributes(query)
        # Determine maximum number of decorations
        max_decorations_ = max_decorations(query)

        # Set columns
        columns += ["Item Name", "Vendor Name", "Item Number"]
        columns += list(set([pa.name for pa in attributes_]))
        for i in range(max_decorations_):
            columns += [f"Decorator Name {i+1}", f"Logo Description {i+1}", f"Logo Position {i+1}"]
        columns += ["Total ordered in campaign"]

        # gen not repeat dict and total ordering numb
        non_repeating_data = []
        dict_total_ordering = {}
        for order_id, order_items in orders.items():
            for order_item_index, order_item in enumerate(order_items):
                if any(
                    order_item.product_variant_id == x.product_variant_id
                    for x in non_repeating_data
                ):
                    dict_total_ordering[order_item.product_variant_id] += order_item.quantity
                else:
                    non_repeating_data.append(order_item)
                    dict_total_ordering[order_item.product_variant_id] = order_item.quantity

        for order_item_index, order_item in enumerate(non_repeating_data):
            # for order_id, order_items in orders.items():
            #     for order_item in order_items:
            # print(order_item.product_variant.total_ordered)
            print("---")
            if order_item.order.status not in "canceled":
                row = {}
                size = False
                row["Item Name"] = order_item.product_variant.product.name
                row["Vendor Name"] = order_item.product_variant.vendor_name
                row["Item Number"] = order_item.product_variant.product.item_number
                # row['Total ordered in campaign'] = order_item.quantity
                row["Total ordered in campaign"] = dict_total_ordering.get(
                    order_item.product_variant_id
                )
                for attr in order_item.product_variant.attributes:
                    row[attr["name"]] = attr["value"]
                    if attr["name"].lower() in "size":
                        size = True
                if not size:
                    row["size"] = ""
                for i, decoration in enumerate(order_item.product_variant.decorations):
                    row[f"Decorator Name {i + 1}"] = decoration["decorator_name"]
                    row[f"Logo Description {i + 1}"] = decoration["logo_description"]
                    row[f"Logo Position {i + 1}"] = decoration["decoration_location"]
                rows.append(row)

        key_size = self.get_key_size(rows)
        rows = sorted(
            rows,
            key=lambda x: ((x["Vendor Name"]), x["Item Number"], SORT_ORDER.index(x[key_size])),
        )
        # Set rows
        # for pv in query.all():
        #     if pv.total_ordered:
        #         row = {}
        #         row['Item Name'] = pv.product.name
        #         row['Vendor Name'] = pv.vendor_name
        #         row['Item Number'] = pv.product.item_number
        #         row['Total ordered in campaign'] = pv.total_ordered
        #         for attr in pv.attributes:
        #             row[attr['name']] = attr['value']
        #         for i, decoration in enumerate(pv.decorations):
        #             row[f'Decorator Name {i+1}'] = decoration['decorator_name']
        #             row[f'Logo Description {i+1}'] = decoration['logo_description']
        #             row[f'Logo Position {i+1}'] = decoration['decoration_location']
        #         rows.append(row)

        meta = {
            "Total Number of items Order in Campaign": sum(
                [r["Total ordered in campaign"] for r in rows]
            )
        }

        return columns, rows, meta

    def get_key_size(self, rows):
        key = None
        for items in rows:
            for item in items:
                if item.lower() in "size":
                    key = item
                    return key
        return key


class BFLTable(Table):
    name = "Bag/Fold/Label PO"
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

        # Set columns
        columns = [
            "PO Name",
            "Total #items ordered in campaign",
            "Bag/Fold/Label Costs",
            "PO AMOUNTS",
        ]

        total = total_items_ordered(campaign)

        # Set rows
        rows.append(
            {
                "PO Name": "Bag/Fold/Label",
                "Total #items ordered in campaign": total,
                # "Total #items ordered in campaign": sum(
                #     [pv.total_ordered for pv in campaign.product_variants]
                # ),
                "Bag/Fold/Label Costs": campaign.bfl_cost,
                # "PO AMOUNTS": sum([pv.total_ordered for pv in campaign.product_variants])
                # * campaign.bfl_cost,
                "PO AMOUNTS": total * campaign.bfl_cost,
            }
        )

        # Format and add signs
        for index, row in enumerate(rows):
            rows[index]["Bag/Fold/Label Costs"] = self.format_price(row["Bag/Fold/Label Costs"])
            rows[index]["PO AMOUNTS"] = self.format_price(row["PO AMOUNTS"])

        return columns, rows, meta


class DecoratorsTable(Table):
    name = "Decorators PO"
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

        # Count ordered items by decoration
        oi_by_decorations_count = {}
        for order in campaign.orders:
            for oi in order.order_items:
                pv = oi.product_variant
                for decoration in pv.decorations:
                    dec_id = identifier.encode(decoration)
                    if not oi_by_decorations_count.get(dec_id):
                        oi_by_decorations_count[dec_id] = 0
                    oi_by_decorations_count[dec_id] += oi.quantity

        # Set columns
        columns = [
            "Decorators Name",
            "Logo Description",
            "Decoration Location",
            "Total # of items, ordered in Campaign w. this decoration",
            "Decoration Cost",
            "PO AMOUNTS",
        ]

        # Set rows
        used_dec_ids = []
        for order in campaign.orders:
            for oi in order.order_items:
                if oi.order.status not in "canceled":
                    pv = oi.product_variant
                    for decoration in pv.decorations:
                        dec_id = identifier.encode(decoration)
                        if dec_id in used_dec_ids:
                            continue
                        row = {}
                        row["Decorators Name"] = decoration["decorator_name"]
                        row["Logo Description"] = decoration["logo_description"]
                        row["Decoration Location"] = decoration["decoration_location"]
                        row["Decoration Cost"] = round(decoration["decoration_cost"], 2)
                        row[
                            "Total # of items, ordered in Campaign w. this decoration"
                        ] = oi_by_decorations_count[dec_id]
                        row["PO AMOUNTS"] = round(
                            oi_by_decorations_count[dec_id] * decoration["decoration_cost"], 2
                        )
                        rows.append(row)
                        used_dec_ids.append(dec_id)

        # Set meta
        total_po_amounts = round(sum([r["PO AMOUNTS"] for r in rows]), 2)
        total_io = total_items_ordered(campaign)
        meta = {
            "Total PO Amounts": total_po_amounts,
            "Total PO Amounts and Bag/Fold/Label PO": round(
                (total_io * campaign.bfl_cost) + total_po_amounts, 2
            ),
        }
        meta["Total PO Amounts"] = self.format_price(meta["Total PO Amounts"])
        meta["Total PO Amounts and Bag/Fold/Label PO"] = self.format_price(
            meta["Total PO Amounts and Bag/Fold/Label PO"]
        )

        # Add signs
        for index, row in enumerate(rows):
            rows[index]["Decoration Cost"] = self.format_price(row["Decoration Cost"])
            rows[index]["PO AMOUNTS"] = self.format_price(row["PO AMOUNTS"])

        return columns, rows, meta


class DecoratorPOReport(CampaignReport):
    name = "Decorator PO"
    tables = [DecoratorPOTable, BFLTable, DecoratorsTable]
