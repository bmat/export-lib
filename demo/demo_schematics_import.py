from schematics import Model, types, models

from export_util import normalize, Importer, utility, value


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

    class Options:
        normalize = {
            'modes': value.string_to_any
        }


if __name__ == '__main__':
    im = Importer(
        normalizer=normalize.SchematicsParseNormalizer(
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
        )
    )

    objects = im.parse('demo/demo_schematics_import.xlsx')
    for o in objects:
        print(value.schema_model_to_dict(o))
