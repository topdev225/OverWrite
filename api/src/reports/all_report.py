from src.reports.types import CampaignReport

from src.reports.campaign_product_list_report import CampaignProductListTable
from src.reports.decorator_po_report import BFLTable, DecoratorPOTable, DecoratorsTable
from src.reports.itemized_shopper_report import ItemizedShopperTable
from src.reports.label_report import LabelTable
from src.reports.location_po_report import LocationPOTable
from src.reports.payroll_deduction_report import PayrollDeductionTable
from src.reports.pick_pack_and_bag_report import PickPackAndBagTable
from src.reports.sales_executives_shopper_report import SalesExecutivesShopperTable
from src.reports.shopper_summary_report import ShopperSummaryTable
from src.reports.vendor_po_report import VendorPOTable


class AllReport(CampaignReport):
    name = "All"
    tables = [
        CampaignProductListTable,
        DecoratorPOTable,
        BFLTable,
        DecoratorsTable,
        ItemizedShopperTable,
        LocationPOTable,
        PayrollDeductionTable,
        PickPackAndBagTable,
        LabelTable,
        SalesExecutivesShopperTable,
        ShopperSummaryTable,
        VendorPOTable,
    ]
