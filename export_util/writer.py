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

    INTCOL_MAP = {i: c for i, c in enumerate(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))}
    COLINT_MAP = {c: i for i, c in enumerate(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))}

    def __init__(self, cols_dimensions=None, template=None):
        super(XLSXBytesOutputWriter, self).__init__()
        self.start_col = 0
        self.start_row = 0
        self._current_row = 0

        if template is not None:
            if hasattr(template, 'template_file'):
                self.wb = load_workbook(filename=template.template_file, keep_vba=True)
            else:
                self.wb = Workbook()

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
        if hasattr(template, 'worksheet_index') and template.worksheet_index is not None:
            self.ws = self.wb.worksheets[template.worksheet_index]

        if hasattr(template, 'table_start') and template.table_start is not None:
            col, row = tuple(template.table_start)
            self.start_col = self.COLINT_MAP.get(col)
            self.start_row = int(row) - 1

        if hasattr(template, 'images_positions'):
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

            try:
                self.ws.cell(row=self._current_row + self.start_row + 1, column=i+1, value=val)
            except Exception as e:
                print(e)

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


__all__ = ['BytesOutputWriter', 'XLSXBytesOutputWriter']
