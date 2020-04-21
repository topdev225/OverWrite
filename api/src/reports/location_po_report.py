from src.models import Location
from src.reports.types import CampaignReport, Table


class LocationPOTable(Table):
    name = "Location PO"
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
        query = Location.query
        query = query.filter_by(campaign_id=campaign.id)

        # Apply modificators
        query = self.apply_filters(query)
        query = self.apply_sort(query)

        # Set columns
        columns = [
            "Nickname",
            "Company Name",
            "Street and Number",
            "City",
            "Zip Code",
            "Delivery Contact",
            "Suite/Unit/etc.",
            "Region",
            "Country",
        ]

        # Set rows
        for location in query.all():  # type: Location
            row = {}
            row["Nickname"] = location.nickname
            row["Company Name"] = location.company_name
            row["Street and Number"] = location.street_and_number
            row["City"] = location.city
            row["Zip Code"] = location.zip_code
            row["Delivery Contact"] = location.delivery_contact
            row["Suite/Unit/etc."] = location.suite_unit_etc
            row["Region"] = location.region
            row["Country"] = location.country
            rows.append(row)

        # Set meta
        meta = {"Total Locations": len(rows)}

        # Return
        return columns, rows, meta


class LocationPOReport(CampaignReport):
    name = "Location PO"
    tables = [LocationPOTable]
