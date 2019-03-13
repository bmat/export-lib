from datetime import datetime


class Exporter:
    """
    Export data utility.

    This tool requires data normalizer and the output handler.

    You can provide default one from the .templator and .writer packages.

    Example:

        ex = Exporter(
            normalizer=normalize.Normalizer({
                'Title': {

                    # Required. Path of value which should be get from
                    # data source.
                    'path': 'title',

                    # Optional. Ascending order number of this column.
                    'position': 0,

                    # Optional. Default value if the value is unavailable
                    # in source object.
                    'default: 'Untitled'

                },
                'Description: {
                    'path': 'some_obj_property.description',
                    'position': 1,
                    'default': '---'
                }
            }),

            output=writer.XLSXBytesOutputWriter()
        )

        # Then get output bytes
        ex.generate()

    """
    def __init__(self, normalizer, output):
        """
        :param export_util.normalize.Normalizer normalizer:
        :param export_util.writer.BytesOutputWriter output:
        """
        self.normal = normalizer
        self.output = output

    def generate(self, data, filename=None):
        """
        Generate response.

        @returns tuple(
            (str) file name,
            (str) file mime type,
            (bytes) file content
        )

        :param data:
        :param filename:
        :return tuple:
        """
        return (
            self._get_file_name(filename),
            self._get_content_mime_type(),
            self._get_content_data(data),
        )

    def _get_file_name(self, filename=None):
        """
        :param filename:
        :return str:
        """
        if filename is None:
            return '{}.{}'.format(datetime.now().strftime('%Y-%m-%d'), self.output.extension)
        return '{}.{}'.format(filename, self.output.extension)

    def _get_content_mime_type(self):
        """
        :return str:
        """
        return self.output.mime_type

    def _get_content_data(self, data):
        """
        :param data:
        :return bytes:
        """
        for cols in self._get_content(data):
            self.output.write(*cols)
        return self.output.get_data()

    def _get_content(self, data):
        """
        :param data:
        :return generator:
        """
        for row in data:
            for r in self.normal.build_table(row):
                yield r


__all__ = ['Exporter']
