from . import template as tpl


class Normalizer:
    """
    Normalizer object formats data into ordered rows using provided template. Templates are building
    using `export_lib.template` functionality. First what should be passed into nomralizer constructor
    is the `export_lib.template.Object` instance. This is the way to say how to format each object
    at the provided data list.

    Each `export_lib.template.Object` takes `export_lib.template.Field` as an `field` argument, which
    allows to understand which fields and in which order they should be rendered. Also `Object` has
    other properties which are allows to specify how they should looks like in a table.

    Example:

        def create_duration(start_time, object_source):
            ""
            This function formats duration column depending on the object
            `cuesheet_start_time.$date` and `cuesheet_end_time.$date`.

            When we know the amount of seconds duration, we formatting it into
            the HH:MM:SS format.
            :param start_time:
            :param DataGetter object_source:
            :return:
            ""
            return time.strftime(
                '%H:%M:%S',
                time.gmtime(
                    int((object_source.get('cuesheet_end_time.$date') - start_time) / 1000)
                )
            )


        def get_year_from_timestamp(milliseconds, object_source):
            ""
            This function returns year from the provided timestamp.
            :param milliseconds:
            :param DataGetter object_source:
            :return:
            ""
            return time.strftime('%Y', time.gmtime(int(milliseconds / 1000)))


        def verbose_boolean(boolean, object_source):
            ""
            This function returns "NO" if `boolean` is False, and
            returns "YES" if `boolean` is True.
            :param boolean:
            :param DataGetter object_source:
            :return:
            ""
            return 'YES' if boolean else 'NO'


        def verbose_list(list_objects, object_source):
            ""
            This function formats list of an objects into single string.
            :param list_objects:
            :param DataGetter object_source:
            :return:
            ""
            return ', '.join(map(lambda x: str(x), list_objects))


        # This is how the data exporter should be initialized.
        ex = Exporter(normalizer=Normalizer(
            # This name - `OBJ_1`, will be used to describe hard logic.
            tpl.Object(
                # This is the number of column where the object should start render
                col=1,

                # If `titles` is True, then all headers of each field will be rendered before objects list.
                titles=True,

                # This is the object fields
                fields=[
                    # Required. First argument of the Field object is the column number. It's related to parent Object
                    # col number, and always starts from 1.
                    tpl.Field(1, 'Production ID', '_id.$oid'),

                    # Required. The second argument is the field title / verbose_name.
                    tpl.Field(2, 'Source', 'cuesheet_channel'),

                    # Optional. The third argument is the where values is stored at the object. If you keep it empty -
                    # title will be renderred instead.
                    tpl.Field(3, 'Duration', 'cuesheet_start_time.$date', create_duration),

                    # Optional. The fourth argument is the callable function which takes field value as the first arg
                    # and the whole object `DataGetter` instance as the second argument. So you can compute absolutely
                    # new value from field value and any amount of other objects values.
                    tpl.Field(4, 'Year', 'updated_at.$date', get_year_from_timestamp),
                    tpl.Field(5, 'Free Music', 'free_music', verbose_boolean),
                    tpl.Field(6, 'Title', 'category.other_production.original_title'),
                    tpl.Field(7, 'Gema AVR', 'cuesheet_progress'),
                    tpl.Field(8, 'Country', 'production_country', verbose_list),

                    # Then we rendering child objects list starting from the first column of table. Each nested object
                    # is rendering under the parent object. So if you have more than one nested objects list to be
                    # rendered, you need to fold them in a one table, see description below.
                    #
                    # This name - `OBJ_2`, will be used to describe hard logic.
                    tpl.Object(
                        # Nested objects table start column
                        col=1,

                        # How much rows should be kept empty before rendering this table.
                        offset_top=5,

                        # This is the Object verbose_name. It's required for all nested objects but should be empty
                        # for the root.
                        verbose_name='Cuesheets',

                        # This is the path of the list of objects which are will be rendered.
                        path='cuesheet.cues',

                        # If `titles` is True, then all headers of each field will be rendered before objects list.
                        titles=True,

                        # This is the way to render multiple nested objects lists in a one table and not one under
                        # other. If you kept it empty or set it to False, child `Objects` will be rendered as stairs.
                        fold_nested=True,

                        # Let's say, we want to keep one row empty before rendering next nested object, to get more
                        # readable table.
                        offset_item=1,

                        # Object also has optional `preformat` parameter, which allows to pass callable object
                        # preprocessor. For example if you want to change something in the object before rendering.

                        # This is the nested object template fields.
                        fields=[
                            tpl.Field(1, 'Start Time', 'start_time'),
                            tpl.Field(2, 'Work ID', 'work_id'),
                            tpl.Field(3, 'Length', 'length'),
                            tpl.Field(4, 'Music Type', 'music_type'),
                            tpl.Field(5, 'Use', 'use'),
                            tpl.Field(6, 'Music Title', 'music_work.music_title'),
                            tpl.Field(7, 'Origin', 'music_work.origin'),
                            tpl.Field(8, 'Work ID', 'music_work.work_id.mpn_id'),
                            tpl.Field(9, 'Work ID Type', 'music_work.work_id.iswc'),

                            # This name - `OBJ_3`, will be used to describe hard logic.
                            tpl.Object(
                                col=10,
                                verbose_name='Authors',
                                path='music_work.author',

                                # Inline option is the way to render nested object title in a one line with the
                                # parent object. If you keep it empty, then parent object will have empty cells
                                # before this table.
                                inline=True,

                                titles=False,
                                fields=[
                                    # Each field of this nested object, has numeration of columns starting from 1.
                                    # It's made to simplify templates building. Nested objects column numbers are
                                    # always relative to the parent object.

                                    # This column number will be calculated in a next way:
                                    # OBJ_1.column + OBJ_2.column + OBJ_3.column + self.column = 10
                                    # It's hard to explain, just believe me it works as described.
                                    tpl.Field(1, 'Name', 'name'),
                                    tpl.Field(2, 'Rolle', 'rolle'),
                                ]
                            ),


                            # In the previous object, we have two fields placed horizontally. This means that previous
                            # object will take two columns of space. Then we need to give him a place and place next
                            # nested object on a column `prev.column+2`
                            tpl.Object(
                                col=12,
                                verbose_name='Publishers',
                                path='music_work.publisher',
                                inline=True,
                                titles=False,
                                fields=[
                                    tpl.Field(1, 'Name', 'name'),
                                    tpl.Field(2, 'Rolle', 'rolle'),
                                ]
                            ),
                            tpl.Object(
                                col=14,
                                verbose_name='Interpreters',
                                path='music_work.interpreter',
                                inline=True,
                                titles=False,
                                fields=[
                                    tpl.Field(1, 'Name', 'name'),
                                    tpl.Field(2, 'Rolle', 'rolle'),
                                ]
                            ),
                        ]
                    )
                ]
            )),
            output=XLSXBytesOutputWriter(cols_dimensions={
                'A': 28.06,
                'B': 27.65,
                'C': 10.0,
                'D': 13.19,
                'E': 11.25,
                'F': 43.9,
                'G': 13.89,
                'H': 30.7,
                'I': 14.72,
                'J': 29.45,
                'K': 8.67,
                'L': 28.76,
                'M': 8.67,
                'N': 29.03,
                'O': 8.67
            })
        )

    *Preformat* argument is a function which takes two arguments. First - os the this column value, and the Second
    is the whole object `DataGetter`. So you can compute any difficult values which are depends on other object values.

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
