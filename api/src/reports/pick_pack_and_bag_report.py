from src.models import Order, OrderItem
from src.reports.types import CampaignReport, Table


class PickPackAndBagTable(Table):
    name = "Pick, Pack and Bag"
    params = []
    filters = []
    sortings = []

    # Additional settings
    items_per_row = 0

    def generate(self, *args, **kwargs):
        # Define helpers
        report = kwargs.get("report")
        campaign = report.campaign

        # Define storage
        columns = []
        rows = []
        meta = {}

        # Base query
        query = Order.query.filter_by(campaign=campaign)

        # Apply modificators
        query = self.apply_filters(query)
        query = self.apply_sort(query)

        # Determine checkout fields
        checkout_fields = campaign.checkout_fields["properties"].keys()

        # create dict with a bin
        dict_bin = self.create_bin_dic(campaign)

        # calculation rows
        self.items_per_row += self.calc_rows(query)

        # Set columns
        columns = self.get_columns(checkout_fields)

        # get all rows with data
        rows = self.gen_report(query, checkout_fields, dict_bin)

        # Return
        return columns, rows, meta

    # get all rows with data
    def gen_report(self, query, checkout_fields, dict_bin):
        rows = []
        for order_id, order in enumerate(query.all()):
            row = {}
            totals = 0

            for checkout_field in checkout_fields:
                try:
                    row[checkout_field] = order.checkout_fields[checkout_field]
                except Exception as e:
                    print(e)

            order_items = OrderItem.query.filter(OrderItem.order_id == order.id).all()

            # sorting by bin
            order_items = sorted(order_items, key=lambda x: dict_bin.get(x.product_variant_id))

            for order_item_index, order_item in enumerate(order_items):
                # bin = "Bin #" + str(dict_bin.get(order_item.product_variant_id))
                bin = "Bin #" + str(order_item.product_variant.bin)
                row[f"Product {order_item_index + 1}"] = bin
                row[f"Quantity {order_item_index + 1}"] = "Pick " + str(order_item.quantity)
                totals += order_item.quantity

            row["Totals"] = totals
            rows.append(row)
        return rows

    # Set columns
    def get_columns(self, checkout_fields):
        columns = []
        columns += checkout_fields
        for i in range(self.items_per_row):
            columns.append(f"Product {i + 1}")
            columns.append(f"Quantity {i + 1}")
        columns += ["Totals"]

        return columns

    # calculation rows
    def calc_rows(self, query):
        max_order_item = 0
        for order_id, order in enumerate(query.all()):
            order_items = OrderItem.query.filter(OrderItem.order_id == order.id).all()
            if len(order_items) > max_order_item:
                max_order_item = len(order_items)
                print(max_order_item)

        return max_order_item

    # create dict with a bin
    def create_bin_dic(self, campaign):
        dict_bin = {}
        order_q = OrderItem.query
        order_ids = [o.id for o in campaign.orders]
        order_q = order_q.filter(OrderItem.order_id.in_(order_ids))
        index = 1
        for order_index, order_item in enumerate(order_q.all()):
            for order_item_quantity in range(order_item.quantity):
                item = dict_bin.get(order_item.product_variant_id, None)
                if item is None:
                    bin_name = index
                    dict_bin[order_item.product_variant_id] = bin_name
                    index += 1
        return dict_bin


class PickPackAndBagReport(CampaignReport):
    name = "Pick, Pack and Bag"
    tables = [PickPackAndBagTable]
