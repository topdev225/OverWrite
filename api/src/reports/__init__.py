# flake8: noqa
from src.reports.types.campaign_report import CampaignReport

from src.reports.all_report import AllReport
from src.reports.bin_report import BinReport
from src.reports.campaign_product_list_report import CampaignProductListReport
from src.reports.decorator_po_report import DecoratorPOReport
from src.reports.itemized_shopper_report import ItemizedShopperReport
from src.reports.label_report import LabelReport
from src.reports.location_po_report import LocationPOReport
from src.reports.payroll_deduction_report import PayrollDeductionReport
from src.reports.pick_pack_and_bag_report import PickPackAndBagReport
from src.reports.sales_executives_shopper_report import SalesExecutivesShopperReport
from src.reports.shopper_summary_report import ShopperSummaryReport
from src.reports.vendor_po_report import VendorPOReport


campaign_reports = list(CampaignReport.__subclasses__())
