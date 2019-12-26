from schematics import schema, models


class ExportLibSchemaOptions(schema.SchemaOptions):
    """
    Adds export lib options for automatic template building.
    """
    def __init__(self, namespace=None, roles=None, export_level=schema.DEFAULT,
                 serialize_when_none=None, export_order=False, fields=None,
                 verbose_name=None, preformat=None, offset_top=None, inline=None,
                 offset_item=None, titles=None, fold_nested=None, title_each=None,
                 extras=None, normalize=None):
        super(ExportLibSchemaOptions, self).__init__(namespace, roles, export_level, serialize_when_none, export_order,
                                                     extras)

        self.fields = fields
        self.preformat = preformat

        self.titles = titles
        self.title_each = title_each

        self.offset_top = offset_top
        self.offset_item = offset_item

        self.inline = inline
        self.fold_nested = fold_nested
        self.verbose_name = verbose_name

        self.normalize = normalize


class ExportableModelMeta(models.ModelMeta):
    def __new__(mcs, name, bases, attrs):
        attrs['__optionsclass__'] = ExportLibSchemaOptions
        return super().__new__(mcs, name, bases, attrs)


__all__ = ['ExportLibSchemaOptions', 'ExportableModelMeta']
