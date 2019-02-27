

class DataGetter:
    """
    Data getter allows to get value of an nested attribute or item of a dictionary object.

    Example:

        >> dg = DataGetter({'a': {'b': {'c': 'hello'}}})
        >> print(dg.get('a.b.c'))
        hello


        >> dg = DataGetter(an_object_without_getitem)
        >> print(dg.get('a.b.c'))
        # This will make next call trace
        # v = getattr(an_object_without_getitem, 'a')
        # v = getattr(v, 'b')
        # v = getattr(v, 'c')
        # return v
    """
    def __init__(self, source):
        """
        :param source:
        """
        self.source = source

    def get(self, path, default=None):
        """
        Get attribute or item value from source object.
        :param path:
        :param default:
        :return:
        """
        if isinstance(self.source, dict):
            return self._get_items(path, default)
        return self._get_attributes(path, default)

    def _get_attributes(self, path, default=None):
        """
        Get attribute value
        :param path:
        :param default:
        :return:
        """
        if '.' not in path:
            return getattr(self.source, path, default)

        path, nested = path.split('.', 1)
        value = getattr(self.source, path)
        while '.' in nested:
            path, nested = nested.split('.', 1)
            value = getattr(value, path, default)

        if nested:
            value = getattr(value, nested, default)

        return value

    def _get_items(self, path, default=None):
        """
        Get item value
        :param path:
        :param default:
        :return:
        """
        if '.' not in path:
            try:
                return self.source[path]
            except KeyError:
                return default

        path, nested = path.split('.', 1)
        try:
            value = self.source[path]
        except KeyError:
            value = default

        while '.' in nested:
            path, nested = nested.split('.', 1)
            try:
                value = value[path]
            except Exception:
                value = default

        if nested:
            try:
                value = value[nested]
            except Exception:
                value = default

        return value


class Normalizer:
    """
    Normalizer object formats data into ordered rows using provided template.

    Example:

        normalizer = Normalizer({
            'Title': {

                # Required. Path of value which should be get from
                # data source.
                'path': 'title',

                # Optional. Ascending order number of this column.
                'col': 0,

                # Optional. Default value if the value is unavailable
                # in source object.
                'default: 'Untitled'

                # Optional. Preformat value for the endless data.
                'preformat': lambda val: str(val),

                # Optional. Nested rows format
                'nested': {
                    # Keys in this case is the path of object source data.
                    # Ex. this keys will take data from: `row[N].authors`
                    'authors': {
                        'First Name': {
                            # And this will take a look at the `row[N].authors[J].first_name`
                            'path': 'first_name'
                        }
                    }
                }
            },
            'Description: {
                'path': 'some_obj_property.description',
                'position': 1,
                'default': '---'
            },

            'Date': {
                'path': 'created_date',
                'preformat': lambda x: x.strftime('%Y-%d')
            }
        })

        normalizer.parse_columns()

    *Keys* of the template dictionary is the verbose name of the column.
    *Values* should be dictionaries which must contain `path` of the data at the source row.

    """
    def __init__(self, template):
        """
        :param dict template:
        """
        self.template = template

    @property
    def sorted_template(self):
        """
        Returns ordered dict of the template.
        :return:
        """
        return sorted(filter(lambda x: x[0].lower() != 'nested', self.template.items()), key=lambda x: x[1].get('col', 0))

    def preformat_columns(self, columns):
        """
        :param columns:
        :return:
        """
        result = []
        for col, data in zip(columns, self.sorted_template):
            key, col_info = data
            if 'preformat' in col_info and callable(col_info['preformat']):
                col = col_info['preformat'](col)

            if len(result) <= col_info.get('col', 0) - 1:
                result += ['']*(col_info.get('col', 0) - len(result))

            result.append(col)
        return result

    def normalize_row(self, row):
        """
        :param row:
        :return:
        """
        data_getter = DataGetter(row)
        yield self.preformat_columns([
            data_getter.get(
                path=v['path'],
                default=v.get('default', None)
            ) for k, v in self.sorted_template
        ])

        for nested_path, nested_template in self.template.get('nested', {}).items():
            for nested_row in data_getter.get(nested_path):
                normalizer = Normalizer(nested_template)
                yield from normalizer.normalize_row(nested_row)

    def get_headers(self):
        """
        Parses columns headers.
        :return:
        """
        return self.preformat_columns([x[0] for x in self.sorted_template])


__all__ = ['Normalizer']
