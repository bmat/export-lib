from . import template as tpl


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
                'preformat': lambda value, whole_object: value.strftime('%Y-%d')
            }
        })

        normalizer.parse_columns()

    *Keys* of the template dictionary is the verbose name of the column.

    *Values* should be dictionaries which must contain `path` of the data at the source row.

    *Preformat* argument is a function which takes two arguments. First - os the this column value, and the Second
    is the whole object source. So you can compute any difficult values which are depends on other object values.

    """
    def __init__(self, template, *args, **kwargs):
        """
        :param tpl.Object template:
        """
        self.template = template

    def build_table(self, obj):
        """
        Returns N rows which are representing this object due to provided
        template.
        :param obj:
        :return:
        """
        yield from self.template.render(obj)


__all__ = ['Normalizer']
