from src.models import OrderItem, ProductVariant

from src.const import SORT_ORDER
from src.reports.helpers import attributes
from src.reports.types import CampaignReport, Table


class BinTable(Table):
    name = "Bin"
    params = []
    filters = []
    sortings = []

    def generate(self, *args, **kwargs):

        # Define helpers#
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
        pvs_query = ProductVariant.query.filter_by(
            campaign=campaign
        )  # .order_by(ProductVariant.attributes['size'].cast(String))
        attributes_ = attributes(pvs_query)

        # Set columns
        # columns += ['SKU', 'Item #', 'Vendor', 'Product Name']
        columns = self.make_columns(columns, attributes_)

        # gen not repeat dict and total ordering numb
        non_repeating_data, dict_total_ordering = self.get_dict(query)

        # Set rows
        for order_item_index, order_item in enumerate(non_repeating_data):
            row = {}
            row["SKU"] = order_item.product_variant.sku
            row["Product Name"] = order_item.product_variant.product.name
            for attr in order_item.product_variant.attributes:
                row[attr["name"]] = attr["value"]
            for index, decoration in enumerate(order_item.product_variant.decorations):
                if index == 0:
                    row[f"Logo Position"] = ""
                else:
                    row[f"Logo Position"] += ", "
                row[f"Logo Position"] += decoration["decoration_location"]

            row[f"Bin Number"] = "Bin " + str(order_item.product_variant.bin)
            row[f"bin_num"] = (
                666 if order_item.product_variant.bin is None else order_item.product_variant.bin
            )
            row[f"Total Ordered in Campaign"] = dict_total_ordering.get(
                order_item.product_variant_id
            )
            rows.append(row)

        # sorting by size
        rows = self.sorting_by_size(columns, rows)

        # Return
        return columns, rows, meta

    def sorting_by_size(self, columns, rows):
        size = "Size" if "Size" in columns else None
        if size is None:
            size = "size" if "size" in columns else None
        if size:
            rows = sorted(rows, key=lambda x: (SORT_ORDER.index(x.get(size) or "")), reverse=True)
        return rows

    def make_columns(self, columns, attributes_):
        # columns += ['SKU', 'Item #', 'Vendor', 'Product Name']
        columns += ["SKU", "Product Name"]
        columns += list(set([pa.name for pa in attributes_]))
        columns += [f"Logo Position"]
        columns += [f"Bin Number"]
        columns += [f"Total Ordered in Campaign"]
        return columns

    def get_dict(self, query):
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

        return non_repeating_data, dict_total_ordering


class BinReport(CampaignReport):
    name = "Bin"
    tables = [BinTable]
