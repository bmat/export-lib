import collections

import schematics

from export_util import (
    template as tpl,
    value as val
)


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
    def __init__(self, template: tpl.Object, *args, **kwargs):
        """
        Create normalizer instance.
        """
        self.template = template

    def build_table(self, obj):
        """
        Returns N rows which are representing this object due to provided.
        template.
        """
        yield from self.template.render(obj)


class SchematicsNormalizer(Normalizer):
    """
    Creates object template from the schematics model.
    """
    root_object_options = dict(
        col=1,
        titles=True,
        fold_nested=True,
    )

    nested_object_options = dict(
        titles=True,
        inline=True,
        fold_nested=True,
    )

    def __init__(self, model: schematics.Model, *args, **kwargs):
        """
        Create objects template from schematics model.
        """
        super(SchematicsNormalizer, self).__init__(self._build_template(model), *args, **kwargs)

    def _build_template(self, model: schematics.Model, **kwargs) -> tpl.Object:
        """
        Creates object template from model.
        """
        template = tpl.Object(**(kwargs or self.root_object_options))

        for field, preformat in self._get_model_renderable_fields(model):
            options = {}
            if preformat is not None:
                options['preformat'] = preformat

            template.add_field(
                field=self._create_field_template(
                    field=field,
                    parent=kwargs.get('parent'),
                    previous=template.fields[-1] if template.fields else None,
                    **options
                )
            )

        return template

    def _create_field_template(self, field: schematics.types.BaseType, parent=None, previous=None, **kwargs):
        if isinstance(field, schematics.types.ListType) and not kwargs.get('preformat'):
            return self._type_list_related_field(field, parent, previous, **kwargs)

        if isinstance(field, schematics.types.ModelType) and not kwargs.get('preformat'):
            return self._type_related_field(field, parent, previous, **kwargs)

        return self._type_base_field(field, parent, previous, **kwargs)

    def _type_base_field(self, field: schematics.types.BaseType, parent=None, previous=None, **kwargs):
        if 'col' in kwargs:
            column = kwargs.pop('col')
        else:
            column = self._get_next_column_number(previous)

        preformat = None
        if 'preformat' in kwargs:
            preformat = kwargs.pop('preformat')
        if preformat is None:
            preformat = val.any_to_string

        return tpl.Field(
            col=column,
            path=self._get_field_path(parent, field.name),
            preformat=preformat,
            verbose_name=self._get_field_verbose_name(field),
            **kwargs
        )

    def _type_list_related_field(self, field: schematics.types.BaseType, parent=None, previous=None, **kwargs):
        if hasattr(field, 'model_class'):
            return self._type_related_field(field, parent, previous, **kwargs)

        if 'col' in kwargs:
            column = kwargs.pop('col')
        else:
            column = self._get_next_column_number(previous)

        preformat = None
        if 'preformat' in kwargs:
            preformat = kwargs.pop('preformat')
        if preformat is None:
            preformat = val.any_to_string

        return self._type_base_field(
            col=column,
            field=field,
            parent=parent,
            previous=previous,
            preformat=preformat,
            **kwargs
        )

    def _type_related_field(self, field: schematics.types.BaseType, parent=None, previous=None, **kwargs):
        options = kwargs or self._get_model_template_options(field.model_class)

        if 'col' in options:
            column = options.pop('col')
        else:
            column = self._get_next_column_number(previous)

        return self._build_template(
            col=column,
            path=self._get_field_path(parent, field.name),
            model=field.model_class,
            parent=parent,
            verbose_name=self._get_field_verbose_name(field),
            **options
        )

    def _get_model_template_options(self, model) -> dict:
        o = self.nested_object_options.copy()
        o.update({
            k: v for k, v in model._options
            if k in tpl.Object.supported_options and v is not None
        })
        return dict(filter(lambda x: x[1] is not None, o.items()))

    def _get_model_renderable_fields(self, model: schematics.models.Model):
        if 'fields' in dict(model._options) and model._options.fields is not None:
            for field_name in model._options.fields:
                # Get model field
                if field_name in model.fields:
                    yield model.fields[field_name], self._get_model_preformat_field(model, field_name)
                    continue

                # Get custom report field
                getter = f'get_{field_name}'
                if not hasattr(model, getter):
                    raise NotImplementedError(f'{model.__name__}.{getter} is not implemented')

                getter = getattr(model, getter)
                getter.name = field_name
                getter.serialized_name = field_name.replace('_', ' ').capitalize()

                # Define preformatters and prepend getter
                preformatters = self._get_model_preformat_field(model, field_name)
                if not preformatters:
                    preformatters = [getter]
                elif isinstance(preformatters, collections.Iterable):
                    preformatters = [getter] + list(preformatters)
                elif callable(preformatters):
                    preformatters = [getter, preformatters]
                yield getter, preformatters
            return

        yield from (
            (v, self._get_model_preformat_field(model, k))
            for k, v in model.fields.items()
        )

    def _get_model_preformat_field(self, model: schematics.models.Model, field_name):
        if 'preformat' in dict(model._options) and model._options.preformat is not None:
            source_formatters = model._options.preformat.get(field_name)
            if callable(source_formatters) or not source_formatters:
                return source_formatters

            callable_formatters = []
            if isinstance(source_formatters, collections.Iterable):
                for formatter in source_formatters:
                    if isinstance(formatter, str):
                        callable_formatters.append(getattr(model, formatter))
                    elif callable(formatter):
                        callable_formatters.append(formatter)
                    else:
                        raise TypeError(f'{field_name} formatter must be callable or iterable of callable')
                return callable_formatters

        return None

    def _get_next_column_number(self, previous_field=None):
        if previous_field is None:
            return 1

        return previous_field.column + previous_field.length

    def _get_field_verbose_name(self, field):
        return field.serialized_name or field.name.capitalize()

    def _get_field_path(self, parent, field_name):
        return '.'.join([parent or '', field_name]).strip('.')


__all__ = [
    'Normalizer',
    'SchematicsNormalizer',
]
