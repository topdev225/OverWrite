from abc import ABC, abstractmethod
import csv
from typing import List
import json
import io
from . import Table
from src.plugins import logger
from reportlab.platypus import Paragraph, TableStyle, SimpleDocTemplate
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class CampaignReport(ABC):
    def __init__(self, campaign, timezone):
        self.campaign = campaign
        self.timezone = timezone

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def tables(self) -> List[object]:
        pass

    def generate(self) -> List[dict]:
        results = []
        for table in self.tables:
            columns, rows, meta = table().generate(report=self)
            results.append({"columns": columns, "rows": rows, "meta": meta, "name": table.name})
        return results

    def to_dict(self) -> dict:
        raise NotImplementedError

    def to_json(self) -> str:
        tables = self.generate()
        return json.dumps({"tables": tables})

    def to_csv(self) -> List[dict]:
        tables_raw = self.generate()
        tables_csv = []

        for table_raw in tables_raw:
            if "Vendor" not in table_raw["columns"]:
                for row in table_raw["rows"]:
                    try:
                        del row["Vendor"]
                    except Exception:
                        pass

        logger.info(tables_raw)
        for table_raw in tables_raw:
            try:
                out = io.StringIO()
                writer = csv.DictWriter(out, table_raw["columns"])
                writer.writeheader()
                writer.writerows(table_raw["rows"])
                meta_rows = []
                # add empty row
                meta_rows.append({table_raw["columns"][0]: ""})
                # add meta data in specific colums
                for key in table_raw["meta"]:
                    meta_rows.append(
                        {
                            table_raw["columns"][len(table_raw["columns"]) - 2]: key,
                            table_raw["columns"][len(table_raw["columns"]) - 1]: table_raw["meta"][
                                key
                            ],
                        }
                    )
                logger.info(meta_rows)
                writer.writerows(meta_rows)
                out.seek(0, 0)
                tables_csv.append({"name": table_raw["name"], "data": out.read()})
            except Exception as e:
                logger.info(e)

        return tables_csv

    def to_pdf(self, name_of_report, path_to_csv, resource):
        t = "Label Report"
        with open(f'{resource.uuid}/{t.replace("/", "-")}.pdf', "wb") as f:

            # read csv file
            with open(path_to_csv, "r") as csvfile:
                data = list(csv.reader(csvfile))

            elements = []

            # PDF Text
            # PDF Text - Styles
            styles = getSampleStyleSheet()
            styleNormal = styles["Normal"]

            # PDF Text - Content
            line1 = "TITLE"

            elements.append(Paragraph(line1, styleNormal))

            # PDF Table
            # PDF Table - Styles
            # [(start_column, start_row), (end_column, end_row)]
            all_cells = [(0, 0), (-1, -1)]
            header = [(0, 0), (-1, 0)]
            # column0 = [(0, 0), (0, -1)]
            # column1 = [(1, 0), (1, -1)]
            # column2 = [(2, 0), (2, -1)]
            # column3 = [(3, 0), (3, -1)]
            # column4 = [(4, 0), (4, -1)]
            # column5 = [(5, 0), (5, -1)]
            # column6 = [(6, 0), (6, -1)]
            table_style = TableStyle(
                [
                    ("VALIGN", all_cells[0], all_cells[1], "TOP"),
                    ("LINEBELOW", header[0], header[1], 1, colors.black),
                    # ('ALIGN', column0[0], column0[1], 'LEFT'),
                    # ('ALIGN', column1[0], column1[1], 'LEFT'),
                    # ('ALIGN', column2[0], column2[1], 'LEFT'),
                    # ('ALIGN', column3[0], column3[1], 'RIGHT'),
                    # ('ALIGN', column4[0], column4[1], 'RIGHT'),
                    # ('ALIGN', column5[0], column5[1], 'LEFT'),
                    # ('ALIGN', column6[0], column6[1], 'RIGHT'),
                ]
            )

            # PDF Table - Column Widths
            colWidths = [
                5 * cm,  # Column 0
                5 * cm,  # Column 1
                5 * cm,  # Column 2
                5 * cm,  # Column 3
                5 * cm,  # Column 4
                5 * cm,  # Column 5
                5 * cm,  # Column 6
            ]

            # PDF Table - Strip '[]() and add word wrap to column 5
            for index, row in enumerate(data):
                for col, val in enumerate(row):
                    if col != 5 or index == 0:
                        data[index][col] = val.strip("'[]()")
                    else:
                        data[index][col] = Paragraph(val, styles["Normal"])

            # Add table to elements
            t = Table(data, colWidths=colWidths)
            t.setStyle(table_style)
            elements.append(t)

            # Generate PDF
            buffer = io.BytesIO()
            archivo_pdf = SimpleDocTemplate(
                buffer,
                pagesize=(800 * mm, 350 * mm),
                rightMargin=40,
                leftMargin=40,
                topMargin=40,
                bottomMargin=28,
            )
            archivo_pdf.build(elements)
            f.write(buffer.getvalue())
            buffer.close()
