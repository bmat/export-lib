[![Build Status](https://travis-ci.org/bmat/export-lib.svg?branch=master)](https://travis-ci.org/bmat/export-lib)
Export library
==============

This library allows to build nice data export process.



export_util.template.Field()
----------------------------

Template field description.

|Argument|Required|Default|Comment|
|---|---|---|---|
|col|Yes|---|Column number|
|verbose_name|Yes|---|Column name|
|path|No|None|Column value path, separated by dot for nested objects|
|preformat|No|None|Callable callback to preprocess value before rendering|
|default|No|'---'|Default field value|
|translate|No|dict()|Dict of translations to replace child fields names.|



export_util.template.Object()
----------------------------

Template object description.

|Argument|Required|Default|Comment|
|---|---|---|---|
|col|Yes|---|Column number|
|fields|Yes|---|List of `Field` instances which are describes object.|
|verbose_name|No|---|Column name. MUST BE EMPTY for the first parent object which passed to Normalizer.|
|path|No|None|Object list path, separated by dot for nested objects|
|preformat|No|None|Callable callback to preprocess value before passing to `fields`|
|offset_top|No|0|How much rows should be kept before rendering table of this objects|
|offset_item|No|0|How much rows should be kept before rendering each object in this table|
|titles|No|False|Is there should be rendered titles of this table|
|fold_nested|No|False|Folds more than one nested objects into single table instead of "stair" rendering|
|inline|No|False|If `True` - renders child objects verbose name in the related cell.|
|title_each|No|False|If `True` - titles would be rendered for each object row.|
|translate|No|dict()|Dict of translations to replace child fields names.|



export_util.template.NestedSet()
----------------------------

Folds rows which are not overlaps. By rows I mean arrays of strings which are represents table cells.

It's hard to explain, better take a look at the example.


**Example**:


    ns = NestedSet()
    
    ns.add(['', 'Hello', 'World'])
    ns.add(['This is', '', ''])
    
    print(ns.get_rows())
    >> [['This is', 'Hello', 'World']]
    
    ns.add(['hi', '', ''])
    print(ns.get_rows())
    >> [['This is', 'Hello', 'World'], ['hi', '', '']]
    
    ns.add(['foo', '', 'bar'])
    print(ns.get_rows())
    >> [['This is', 'Hello', 'World'], ['hi', '', ''], ['foo', '', 'bar']]


export_util.template.DataGetter()
----------------------------

|Argument|Required|Default|Comment|
|---|---|---|---|
|source|Yes|---|An python `dict`|

Allows to get value of infinite nested objects. 

**Example**:

    dg = DataGetter({'a': {'b': {'c': 1}}})
    print(dg.get('a.b.c'))
    >> 1

export_util.Exporter()
--------------------

Export data utility.

This tool requires data normalizer and the output handler.

You can provide default one from the .templator and .writer packages.

**Example**:

        ex = Exporter(
            normalizer=normalize.Normalizer({
                'Title': {

                    # Required. Path of value which should be get from
                    # data source.
                    'path': 'title',

                    # Optional. Ascending order number of this column.
                    'col': 0,

                    # Optional. Default value if the value is unavailable
                    # in source object.
                    'default: 'Untitled'

                },
                'Description: {
                    'path': 'some_obj_property.description',
                    'col': 1,
                    'default': '---'
                }
            }),

            output=writer.XLSXBytesColsWriter()
        )

        # Then get output bytes
        ex.generate()
        
        
export_util.normalize.Normalizer()
----------------------------------

Normalizer object formats data into ordered rows using provided template. Templates are building
using `export_lib.template` functionality. First what should be passed into nomralizer constructor
is the `export_lib.template.Object` instance. This is the way to say how to format each object
at the provided data list.

Each `export_lib.template.Object` takes `export_lib.template.Field` as an `field` argument, which
allows to understand which fields and in which order they should be rendered. Also `Object` has
other properties which are allows to specify how they should looks like in a table.

**Example**:

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
                
                # If you want to translate or rename some fields - use `translate` option. Note: 
                # 1. Keys of this dict would be used as field name and values as a replacement.
                # 2. Keys are case-sensitive. So the field named `duration` will not be replaced in this example.
                # 3. Translation dict will be automatically converted to DataGetter object. So you can pass not only
                #    field names, but path to replacement as of `DataGetter` specification too.
                translate={
                    'Duration': 'Length',
                    'fields': {
                        'year': {
                            'title': 'Year
                        }
                    }
                },

                # This is the object fields
                fields=[
                    # Required. First argument of the Field object is the column number. It's related to parent Object
                    # col number, and always starts from 1.
                    tpl.Field(1, 'Production ID', '_id.$oid'),

                    # Required. The second argument is the field title / verbose_name.
                    tpl.Field(2, 'Source', 'cuesheet_channel'),

                    # Optional. The third argument is the where values is stored at the object. If you keep it empty -
                    # title will be renderred instead.
                    # Field title `Duration` will be replaced by `Length` as it's defined above in a `translate` dict.
                    tpl.Field(3, 'Duration', 'cuesheet_start_time.$date', create_duration),

                    # Optional. The fourth argument is the callable function which takes field value as the first arg
                    # and the whole object `DataGetter` instance as the second argument. So you can compute absolutely
                    # new value from field value and any amount of other objects values.
                    tpl.Field(4, 'Year', 'updated_at.$date', get_year_from_timestamp),
                    # Or you can use translatin label instead of simple string for year field, which we have defined
                    # above:
                    # tpl.Field(4, 'fields.year.title', 'updated_at.$date', get_year_from_timestamp),
                    
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


export_util.normalize.SchematicsNormalizer()
--------------------------------------------

Allows to build rendering template automatically from the existing `schematics` model.

**Example**:

    class Track(schematics.Model):
        ...
    
    tracks = [Track(...), ...]

    ex = Exporter(
        normalizer=normalize.SchematicsNormalizer(Track),
        output=writer.XLSXBytesOutputWriter()
    )

    filename, mime, xls_data = ex.generate(tracks, "report")
    with open(f'{filename}.xlsx', 'wb') as f:
        f.write(xls_data)


Extended schematics exporting
-----------------------------

As it's a report, you may want to convert some fields values to readable format. Export library already has some basic
implemented formatters in `export_util.value` package. These basic formatters allows to convert some complex values into
more simple ones.

But how to configure these formatters for the specific fields? For this reason, `export_util.utility` has extended
metaclass for schematics models `export_util.utility.ExportableModelMeta`. It's optional to use, but if you want to
preformat some fields, this is the required case.

**To get extended exporter functionality - use ExportableModelMeta class as metaclass**:

    from schematics.models import metaclass
    from export_util.utility import ExportableModelMeta
    
    
    @metaclass(ExportableModelMeta)
    class Track(schematics.Model):
        ...

Any model extended with metaclass `ExportableModelMeta` can be configured as `export_util.template.Object` in `Options`
subclass. Let's say we have a `Track` model with the `duration` property in seconds and we want to get it converted
into readable HH:MM:SS format.


**Example**:


    from schematics import types
    from schematics.models import metaclass
    from export_util.utility import ExportableModelMeta
    from export_util import value
    
    
    @metaclass(ExportableModelMeta)
    class Track(schematics.Model):
        duration = types.IntType()
        
        class Options:
            preformat = {
                'duration': value.seconds_to_time
            }
    

Now each track's duration field would be passed to `value.seconds_to_time` function first, before rendering into output.

`Options` subclass takes all the default schematics properties, and also few new properties provided by `ExportableModelMeta`
class:

|Argument|Required|Default|Comment|
|---|---|---|---|
|col|No|---|`int` Column number|
|fields|No|---|`List[str]` list of fields which are would be rendered.|
|inline|No|---|`bool` If `True` - renders child objects verbose name in the related cell.|
|titles|No|---|`bool` Is there should be rendered titles of this table.|
|title_each|No|---|`bool` If `True` - titles would be rendered for each object row.|
|offset_top|No|---|`int` How much rows should be kept before rendering table of this objects.|
|offset_item|No|---|`int` How much rows should be kept before rendering each object in this table.|
|preformat|No|---|`Dict[str, callable]` or `Dict[str, Iterable[callable]]` Dict of callable formatters for model fields.|
|fold_nested|No|---|`bool` Folds more than one nested objects into single table instead of "stair" rendering|
|verbose_name|No|---|`str` Used only for the nested objects rendering. Alternative to `serialized_name`.|


Extended schematics exporting: Preformatting
--------------------------------------------

Nested objects also would be rendered, and theirs `Options` would be used as main options to build a template of nested
objects block. So let's take a look into another example:

    @metaclass(ExportableModelMeta)
    class OrderedModel(Model):
        class Options:
            export_order = True
            serialize_when_none = False
    
    
    class Composer(OrderedModel):
        first_name = types.StringType(serialized_name="First Name")
        last_name = types.StringType(serialized_name="Last Name")
        gender = types.StringType(choices=('male', 'female'))
    
        class Options:
            inline = True
            title_each = False
            verbose_name = "Composers"
            preformat = {
                'gender': lambda x, y: x.capitalize()
            }
    
    
    class Codes(OrderedModel):
        isan = types.StringType(serialized_name="ISAN")
        gema = types.StringType(serialized_name="GEMA")
    
        class Options:
            inline = True
            title_each = False
            verbose_name = "Codes"
    
    
    class Track(OrderedModel):
        name = types.StringType(serialized_name="Name")
        duration = types.IntType(serialized_name="Length")
        modes = types.ListType(types.IntType)
        composers = types.ListType(types.ModelType(Composer))
        codes = types.ModelType(Codes)
    
        class Options:
            preformat = {
                'modes': value.list_to_string,
                'duration': value.seconds_to_time,
            }

When we will export list of `Track` objects, each `Track.composer.gender` would be passed into `Composer.Options.preformat['gender']`
function firstly, before rendering into output. We can also describe settings in `Composer.Options` to let exporter
know, how to render `Track.composers`.

We also can preformat related objects into single row. Let's say, we want to render `Track.composers` in the single cell
separated by commas:

    class Track(OrderedModel):
        name = types.StringType(serialized_name="Name")
        duration = types.IntType(serialized_name="Length")
        modes = types.ListType(types.IntType)
        composers = types.ListType(types.ModelType(Composer))
        codes = types.ModelType(Codes)
    
        class Options:
            preformat = {
                'modes': value.list_to_string,
                'duration': value.seconds_to_time,
                'composers': value.list_dicts_to_string('{first_name} {last_name} ({gender})')
            }

In this case - `value.list_dicts_to_string` takes format of each `composers` item which are will be concatenated with 
comma after formatting.

What if it's simple `ModelType` relation and not `ListType`?


    class Track(OrderedModel):
        name = types.StringType(serialized_name="Name")
        duration = types.IntType(serialized_name="Length")
        modes = types.ListType(types.IntType)
        composers = types.ListType(types.ModelType(Composer))
        codes = types.ModelType(Codes)
    
        class Options:
            preformat = {
                'modes': value.list_to_string,
                'duration': value.seconds_to_time,
                'codes': value.dict_to_string('I:{isan} / G:{gema}')
            }

For this reason we have `value.dict_to_string` formatter constructor.

Preformat can also take several formatters for every single field. Let's say we must increase duration by `1` and only
after it, we need to convert it to the readable format.


    class Track(OrderedModel):
        name = types.StringType(serialized_name="Name")
        duration = types.IntType(serialized_name="Length")
        modes = types.ListType(types.IntType)
        composers = types.ListType(types.ModelType(Composer))
        codes = types.ModelType(Codes)
    
        class Options:
            preformat = {
                'modes': value.list_to_string,
                'duration': [lambda a,b: a+1, value.seconds_to_time],
                'codes': value.dict_to_string('I:{isan} / G:{gema}')
            }
            
Preformat method can also be the `Model` staticmethod member. Simply pass the string name of this member, and schematics 
normalizer will get it to format value.

    class Track(OrderedModel):
        name = types.StringType(serialized_name="Name")
        duration = types.IntType(serialized_name="Length")
        modes = types.ListType(types.IntType)
        composers = types.ListType(types.ModelType(Composer))
        codes = types.ModelType(Codes)
    
        class Options:
            preformat = {
                'modes': value.list_to_string,
                'duration': ['increase_duration_by_one', value.seconds_to_time],
                'codes': value.dict_to_string('I:{isan} / G:{gema}')
            }
        
        @staticmethod
        def increase_duration_by_one(value, obj: DataGetter):
            return value + 1

Extended schematics exporting: Custom fields
--------------------------------------------

Another complex case. Let's say we want to create absolutely new custom field from an existing properties of an object.
We can provide list of fields which would be rendered at the output in the `Options.fields`. When we declare an field
which is not exists, schematic normalizer will take a look for gettter staticmethod named `get_{field_name}`. So we can
do the next:


    class User(OrderedModel):
        first_name = types.StringType(serialized_name="First Name")
        last_name = types.StringType(serialized_name="Last Name")
        gender = types.StringType(choices=('male', 'female'))
        
        class Options:
            fields = ('full_name', 'gender')
         
        @staticmethod
        def get_full_name(value, obj: DataGetter):
            return '{} {}'.format(obj.get('first_name'), obj.get('last_name'))

As you can see `get_full_name` also takes `value` argument which is always `obj.get('field_name')`. In this case it's
`None`. But you can still use `obj` argument which is `DataGetter` instance of currently rendering object to compose
any value of the cell.

 