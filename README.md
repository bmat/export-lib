Export library
==============

This library allows to build nice data export process.



export_util.Exporter()
--------------------

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
            'col': 1,
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