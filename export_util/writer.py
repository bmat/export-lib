from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

import openpyxl
from openpyxl.writer.excel import ExcelWriter
from openpyxl import Workbook, load_workbook


class BytesOutputWriter:
    """
    Simple data writer.

    Data writer `write_row` calls when we already have the formatted columns list.
    """
    mime_type = 'application/octet-stream'
    extension = 'bin'

    def __init__(self):
        self.output = BytesIO()

    def write(self, *cols):
        self.output.write(b''.join([x.encode() if isinstance(x, str) else x for x in cols]))

    def get_data(self):
        return self.output.getvalue()


class XLSXBytesOutputWriter(BytesOutputWriter):
    """
    Returns bytes of the XLSX workbook object.
    """
    mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.template'
    extension = 'xlsx'

    INTCOL_MAP = {i+1: c for i, c in enumerate(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))}
    COLINT_MAP = {c: i+1 for i, c in enumerate(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))}

    def __init__(self, cols_dimensions=None, template=None):
        super(XLSXBytesOutputWriter, self).__init__()
        self.start_col = 1
        self.start_row = 1
        self._current_row = 0

        if template is not None:
            self.wb = load_workbook(filename=template.template_file, keep_vba=True)
            self.ws = self.wb.active
            self.from_template(template)
        else:
            self.wb = Workbook()
            self.ws = self.wb.active
            self.resize_columns(cols_dimensions)

    def resize_columns(self, cols_dimensions):
        for col, dimension in (cols_dimensions or {}).items():
            if isinstance(dimension, dict):
                width = dimension.get('width')
                height = dimension.get('height')
            else:
                width = dimension
                height = None

            if width:
                self.ws.column_dimensions[col].width = width
            if height:
                self.ws.column_dimensions[col].height = height

    def from_template(self, template=None):
        if template.worksheet_index is not None:
            self.ws = self.wb.worksheets[template.worksheet_index]

        col, row = tuple(template.table_start)

        self.start_col = self.COLINT_MAP.get(col)
        self.start_row = int(row)

        if template.images_positions:
            for cell, image in template.images_positions.items():
                xlimg = openpyxl.drawing.image.Image(image['name'])
                if image['size']:
                    if image['size'][0]:
                        xlimg.width = image['size'][0]
                    if image['size'][1]:
                        xlimg.height = image['size'][1]
                self.ws.add_image(xlimg, cell)

    def write(self, *cols):
        for i, val in enumerate(cols):
            if not val:
                continue

            self.ws[self._get_cell_path(i)] = val

        self._current_row += 1

    def get_data(self):
        archive = ZipFile(self.output, 'w', ZIP_DEFLATED, allowZip64=True)
        writer = ExcelWriter(self.wb, archive)
        try:
            writer.write_data()
        finally:
            archive.close()

        return self.output.getvalue()

    def _get_column_name(self, cell_name):
        return cell_name[0]

    def _get_cell_path(self, col_number):
        return '{}{}'.format(self.INTCOL_MAP.get(col_number + self.start_col), self._current_row + self.start_row)


__all__ = ['BytesOutputWriter', 'XLSXBytesOutputWriter']
