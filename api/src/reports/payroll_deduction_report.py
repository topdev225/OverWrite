from src.models import Order
from src.reports.helpers import identifier
from src.reports.types import CampaignReport, Table


class PayrollDeductionTable(Table):
    name = "Payroll Deduction"
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
        query = Order.query.filter_by(campaign=campaign)

        # Apply modificators
        query = self.apply_filters(query)
        query = self.apply_sort(query)

        # Determine checkout fields
        checkout_fields = campaign.checkout_fields["properties"].keys()
        # Determine totals per person
        total_per_person = {}
        for order in query.all():
            pid = identifier.encode(order.checkout_fields)
            if pid not in total_per_person:
                total_per_person[pid] = 0.0
            total_per_person[pid] += order.total

        # Set columns
        columns += checkout_fields
        columns += ["Order #", "Total Price", "Allowance", "Payroll Deduction"]

        company_allowance = 0
        if campaign.company_allowance:
            company_allowance = campaign.company_allowance

        # Set rows
        for order in query.all():
            if round(order.total, 2) > company_allowance:
                pid = identifier.encode(order.checkout_fields)
                from src.plugins import logger

                logger.info(pid)
                row = {}
                row["Order #"] = order.id
                row["Total Price"] = round(order.total, 2)
                row["Allowance"] = company_allowance
                row["Payroll Deduction"] = (
                    round(total_per_person[pid] - company_allowance, 2) if company_allowance else 0
                )
                for checkout_field in checkout_fields:
                    try:
                        row[checkout_field] = order.checkout_fields[checkout_field]
                    except Exception as e:
                        print(e)
                rows.append(row)

        meta = {
            "Total people": len(rows),
            "Total PO Amounts": self.format_price(
                round(sum([r["Payroll Deduction"] for r in rows]), 2)
            ),
        }

        # Add signs
        for index, row in enumerate(rows):
            rows[index]["Total Price"] = self.format_price(row["Total Price"])
            rows[index]["Allowance"] = self.format_price(row["Allowance"])
            if row["Payroll Deduction"] and row["Payroll Deduction"] < 0:
                rows[index][
                    "Payroll Deduction"
                ] = f'-{self.format_price(-row["Payroll Deduction"])}'
            else:
                rows[index]["Payroll Deduction"] = self.format_price(row["Payroll Deduction"])

        # Return
        return columns, rows, meta


class PayrollDeductionReport(CampaignReport):
    name = "Payroll Deduction"
    tables = [PayrollDeductionTable]
