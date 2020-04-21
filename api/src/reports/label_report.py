from src.const import SORT_ORDER
from src.models import OrderItem, ProductVariant
from src.reports.helpers import attributes
from src.reports.types import CampaignReport, Table


class LabelTable(Table):
    name = "Label Report"
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
        # Determine possible attributes
        pvs_query = ProductVariant.query.filter_by(
            campaign=campaign
        )  # .order_by(ProductVariant.vendor_name)
        attributes_ = attributes(pvs_query)

        # Set columns
        # columns += ['SKU', 'Item #', 'Vendor', 'Product Name']
        columns += [f"Bin Number", "Item #", "Vendor", "Product Name"]
        columns += list(set([pa.name for pa in attributes_]))
        columns += [f"Logo Position"]

        # gen list of bin(the same product)
        dict_bin = {}
        index = 1
        for order_item_index, order_item in enumerate(query.all()):
            for order_item_quantity in range(order_item.quantity):
                item = dict_bin.get(order_item.product_variant_id, None)
                if item is None:
                    bin_name = "Bin " + str(index)
                    dict_bin[order_item.product_variant_id] = bin_name
                    index += 1

        # Set rows
        for order_item_index, order_item in enumerate(query.all()):
            for order_item_quantity in range(order_item.quantity):
                row = {}
                # row[f'Bin Number'] = 'Bin ' + str(order_item_index +1)
                # row[f'Bin Number'] = dict_bin.get(order_item.product_variant_id)
                row[f"Bin Number"] = order_item.product_variant.bin
                row["Item #"] = order_item.product_variant.product.item_number
                row["Vendor"] = order_item.product_variant.vendor_name
                row["Product Name"] = order_item.product_variant.product.name
                for attr in order_item.product_variant.attributes:
                    row[attr["name"]] = attr["value"]
                decorationsSet = []
                for decoration in order_item.product_variant.decorations:
                    decorationsSet.append(decoration["decoration_location"])
                row[f"Logo Position"] = " ,".join(set(decorationsSet))
                rows.append(row)

        # sorting by Vendor
        # rows = sorted(rows, key = lambda i: i['Vendor'])

        # sorting by size
        size = "Size" if "Size" in columns else None
        if size is None:
            size = "size" if "size" in columns else None
        if size:
            rows = sorted(rows, key=lambda x: (SORT_ORDER.index(x.get(size) or "")))

        # ????
        # refresh bin number
        for order_item_index, order_item in enumerate(rows):
            rows[order_item_index][f"Bin Number"] = "Bin " + str(order_item_index + 1)

        rows = sorted(
            rows,
            key=lambda x: (x["Vendor"], int(x[f"Bin Number"].replace("Bin ", ""))),
            reverse=True,
        )

        # Return
        return columns, rows, meta


class LabelReport(CampaignReport):
    name = "Label Report"
    tables = [LabelTable]
