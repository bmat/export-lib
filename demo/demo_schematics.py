from schematics import Model, types, models

from export_util import normalize, writer, Exporter, utility


@models.metaclass(utility.ExportableModelMeta)
class OrderedModel(Model):
    class Options:
        export_order = True
        serialize_when_none = False


class Composer(OrderedModel):
    first_name = types.StringType(serialized_name="First Name")
    last_name = types.StringType()


class Codes(OrderedModel):
    isan = types.StringType(serialized_name="ISAN")
    gema = types.StringType(serialized_name="GEMA")


class Track(OrderedModel):
    name = types.StringType(serialized_name="Name")
    duration = types.IntType(serialized_name="Length")
    modes = types.ListType(types.IntType)
    composers = types.ListType(types.ModelType(Composer), serialized_name="Composers")
    codes = types.ModelType(Codes)


if __name__ == '__main__':
    tracks = [
        Track({
            "name": "First Track",
            "duration": 44,
            "modes": [1, 2, 3],
            "codes": {
                "isan": "ISAN_CODE",
                "GEMA": "GEMA_CODE",
            },
            "composers": [{
                "first_name": "Composer1",
                "last_name": "John",
            }, {
                "first_name": "Composer2",
                "last_name": "Doe",
            }]
        }),
        Track({
            "name": "Second Track",
            "duration": 21,
            "modes": [2, 3, 4],
            "codes": {
                "isan": "ISAN_CODE2",
                "GEMA": "GEMA_CODE2",
            },
            "composers": [{
                "first_name": "Composer2.1",
                "last_name": "John2",
            }, {
                "first_name": "Composer2.2",
                "last_name": "Doe2",
            }]
        }),
    ]

    ex = Exporter(
        normalizer=normalize.SchematicsNormalizer(
            model=Track,
            translate={
                # If the field has `serialized_name` provided in a
                # model property, it must be used as a key to rename
                # it.
                'Name': 'Track Name Renamed',
                'First Name': 'First Name',

                # Otherwise - use the property name as a key. So we can
                # use `last_name` key to override this field name in
                # a result table.
                'last_name': 'Last Name',
            }
        ),
        output=writer.XLSXBytesOutputWriter()
    )

    filename, mime, xls_data = ex.generate(tracks, "metadata")
    with open('demo_schematics.xlsx', 'wb') as f:
        f.write(xls_data)
