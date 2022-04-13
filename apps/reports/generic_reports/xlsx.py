import io

import xlsxwriter
from reports.generic_reports.common import get_func_from_path
from xlsxwriter.workbook import Workbook
from xlsxwriter.worksheet import Worksheet, convert_cell_args


def xlsx_renderer(data: dict, **kwargs):
    data_transformer = get_func_from_path(kwargs["data_transformer"])
    transformed = data_transformer(data)
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {"in_memory": True})
    worksheet = workbook.add_worksheet()

    for row, data_row in enumerate(transformed["data"]):
        for col, data_cell in enumerate(data_row):
            format = {}

            if isinstance(data_cell, tuple):  # cell has a value and a style
                data_cell, format = data_cell

            worksheet.write(row, col, data_cell, workbook.add_format(format))

    if widths := transformed.get("widths", None):
        for col, width in enumerate(widths):
            worksheet.set_column(col, col, width)

    if merges := transformed.get("merges", None):
        for merge in merges:
            first_row, first_col, last_row, last_col = merge
            data_cell = transformed["data"][first_row][first_col]
            format = {}
            if isinstance(data_cell, tuple):  # cell has a value and a style
                data_cell, format = data_cell

            worksheet.merge_range(
                first_row,
                first_col,
                last_row,
                last_col,
                data_cell,
                cell_format=workbook.add_format(format),
            )

    workbook.close()
    output.seek(0)
    return output.read()
