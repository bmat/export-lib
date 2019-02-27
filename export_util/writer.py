from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED

from openpyxl import Workbook
from openpyxl.writer.excel import ExcelWriter


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
    COLS_MAP = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, cols_dimensions=None):
        super(XLSXBytesOutputWriter, self).__init__()
        self.wb = Workbook()
        self.ws = self.wb.active

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

    def write(self, *cols):
        self.ws.append(cols)

    def get_data(self):
        archive = ZipFile(self.output, 'w', ZIP_DEFLATED, allowZip64=True)
        writer = ExcelWriter(self.wb, archive)
        try:
            writer.write_data()
        finally:
            archive.close()

        return self.output.getvalue()


__all__ = ['BytesOutputWriter', 'XLSXBytesOutputWriter']
