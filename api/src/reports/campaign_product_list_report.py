from src.models import ProductVariant

from src.const import SORT_ORDER
from src.reports.helpers import attributes, max_decorations
from src.reports.types import CampaignReport, Table


class CampaignProductListTable(Table):
    name = "Campaign Product List"
    params = []
    filters = []
    sortings = []

    def generate(self, *args, **kwargs):
        # Define helpers
        report = kwargs.get("report")
        campaign = report.campaign

        # Define main query
        query = ProductVariant.query.filter_by(campaign_id=campaign.id)

        # Apply modificators
        query = self.apply_filters(query)
        query = self.apply_sort(query)

        # Determine possible attributes
        attributes_ = attributes(query)
        # Determine maximum decorations count
        max_decorations_ = max_decorations(query)

        # Set columns
        columns = self.get_columns(attributes_, max_decorations_)

        # Set rows
        rows = self.get_rows(query, campaign)

        # sort by name color and size
        key_size, status_size = self.is_size(rows)
        key_color, status_color = self.is_color(rows)
        if status_size and status_color:
            rows = self.sort_by_name_color_size(rows, key_size, key_color)
        elif status_color:
            rows = self.sort_by_name_color(rows, key_color)
        elif status_size:
            rows = self.sort_by_name_size(rows, key_size)
        else:
            rows = self.sort_by_name(rows)

        # Format and add signs
        for index, row in enumerate(rows):
            rows[index]["Net Cost"] = self.format_price(row["Net Cost"])
            rows[index]["F/B/L"] = self.format_price(row["F/B/L"])
            rows[index]["OW Cost"] = self.format_price(row["OW Cost"])
            rows[index]["Total Cost"] = self.format_price(row["Total Cost"])
            rows[index]["Profit Margin"] = f'{row["Profit Margin"]}%'
            rows[index]["Sales Price"] = self.format_price(row["Sales Price"])
            for i in range(max_decorations_):
                try:
                    if rows[index][f"Logo Price {i + 1}"]:
                        rows[index][f"Logo Price {i + 1}"] = self.format_price(
                            rows[index][f"Logo Price {i + 1}"]
                        )
                except Exception as e:
                    print(e)

        # Return
        return columns, rows, {}

    def get_columns(self, attributes_, max_decorations_):
        # Set columns
        columns = []
        columns += ["SKU", "Item #", "Vendor", "Product Name"]
        columns += list(set([pa.name for pa in attributes_]))
        for i in range(max_decorations_):
            columns += [f"Logo Position {i + 1}", f"Logo Price {i + 1}"]
        columns += ["Net Cost", "F/B/L", "OW Cost", "Total Cost", "Profit Margin", "Sales Price"]
        return columns

    def get_rows(self, query, campaign):
        rows = []
        for pv in query.all():
            color = False
            size = False
            row = {}
            row["SKU"] = pv.sku
            row["Item #"] = pv.product.item_number
            row["Vendor"] = pv.vendor_name
            row["Product Name"] = pv.product.name
            row["Net Cost"] = round(pv.vendor_cost, 2)
            row["F/B/L"] = round(campaign.bfl_cost, 2)
            row["OW Cost"] = round(campaign.distributor.ow_cost, 2)
            row["Total Cost"] = round(pv.total, 2)
            row["Profit Margin"] = round(pv.margin, 2)
            row["Sales Price"] = round(pv.price, 2)
            for attr in pv.attributes:
                row[attr["name"]] = attr["value"]
                if attr["name"].lower() in "color":
                    color = True
                if attr["name"].lower() in "size":
                    size = True
            if not color:
                row["color"] = ""
            if not size:
                row["size"] = ""

            for index, decoration in enumerate(pv.decorations):
                row[f"Logo Position {index + 1}"] = decoration["decoration_location"]
                row[f"Logo Price {index + 1}"] = round(decoration["decoration_cost"], 2)
            rows.append(row)
        return rows

    def sort_by_name_color_size(self, rows, key_size, key_color):
        return sorted(
            rows, key=lambda x: ((x["Product Name"]), SORT_ORDER.index(x[key_size]), (x[key_color]))
        )

    def sort_by_name_color(self, rows, key_color):
        return sorted(rows, key=lambda x: ((x["Product Name"]), (x[key_color])))

    def sort_by_name_size(self, rows, key_size):
        return sorted(rows, key=lambda x: ((x["Product Name"]), SORT_ORDER.index(x[key_size])))

    def sort_by_name(self, rows):
        return sorted(rows, key=lambda x: (x["Product Name"]))

    def is_size(self, rows):
        key = None
        status = False
        for items in rows:
            for item in items:
                if item.lower() in "size":
                    key = item
                    status = True
                    return key, status
        return key, status

    def is_color(self, rows):
        key = None
        status = False
        for items in rows:
            for item in items:
                if item.lower() in "color":
                    key = item
                    status = True
                    return key, status
        return key, status


class CampaignProductListReport(CampaignReport):
    name = "Campaign Product List"
    tables = [CampaignProductListTable]
