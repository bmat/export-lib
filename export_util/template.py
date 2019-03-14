

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
        if not path:
            return default
        
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


class NestedSet:
    """
    NestedSet is the utility which allows to fold rows depending on
    cells overlapping.
    """
    def __init__(self):
        self._length = 0
        self._nested = []

    def add(self, row):
        """
        Adds new row
        :param row:
        :return:
        """
        self._check_size(row)

        if not self._nested or self._is_overlaps(self._nested[-1], row):
            return self._append(row)

        for i, ln in enumerate(reversed(self._nested)):
            if self._is_overlaps(ln, row):
                merge_index = (i or 1)*-1
                break
        else:
            merge_index = 0
        self._nested[merge_index] = self._merge(self._nested[merge_index], row)

    def get_rows(self):
        """
        Returns folded rows.
        :return list:
        """
        return self._nested

    def _append(self, row):
        """
        Appends row into rows list.
        :param row:
        :return:
        """
        self._nested.append(row)

    def _check_size(self, row):
        """
        Checks size of a new row and adjusts existing rows
        to this size.
        :param row:
        :return:
        """
        if not self._length:
            self._length = len(row)
        elif len(row) > self._length:
            new_length = len(row)
            add = new_length - self._length
            self._length = new_length
            for i, r in enumerate(self._nested):
                self._nested[i] = r + ([''] * add)

    def _is_overlaps(self, first, second):
        """
        Checks if the rows are overlaps in some cells.
        :param first:
        :param second:
        :return:
        """
        return any(x and y for x, y in zip(first, second))

    def _merge(self, first, second):
        """
        Merges two not overlapped rows.
        :param first:
        :param second:
        :return:
        """
        return [x or y for x, y in zip(first, second)]


class Field:
    """
    This is the field of the object representation. It's used to understand
    how and where should be renderred provided field.
    """
    def __init__(self, col, verbose_name, path=None, preformat=None, default='---'):
        """
        :param col:
        :param verbose_name:
        :param path:
        :param preformat:
        """
        self.verbose_name = verbose_name
        self.column = col
        self.value_path = path
        self.format = preformat if callable(preformat) else lambda a, b: a
        self.default = default
        self.is_object = False
        self.inline = True

    def __str__(self):
        return 'Field("{}", val="{}")'.format(self.verbose_name, self.value_path)

    def __repr__(self):
        return str(self)
        
    def render(self, dg):
        """
        :param DataGetter dg: 
        :return: 
        """
        
        # Get field value
        value = self._get_field_value(dg)
        
        return value

    def _get_field_value(self, dg):
        """
        Returns field value depending on value path and format callback.
        :param dg:
        :return:
        """
        if not self.value_path:
            return self.verbose_name

        return self.format(dg.get(self.value_path, self.default), dg)


class Object:
    """
    This is the object template which is describes how the object should be
    renderred at the table.
    """
    def __init__(self, col, fields, verbose_name=None, path=None, preformat=None, **options):
        """
        :param col:
        :param verbose_name:
        :param fields:
        :param path:
        :param preformat:
        :param options:
        """
        self.fields = fields
        self.verbose_name = verbose_name
        self.column = col
        self.value_path = path
        self.format = preformat if callable(preformat) else lambda a: a
        self.is_object = True
        
        self.offset_top = 0
        self._renderred_offset_top = False
        if 'offset_top' in options:
            self.offset_top = int(options.pop('offset_top'))

        self.offset_item = 0
        self._renderred_offset_item = False
        if 'offset_item' in options:
            self.offset_item = int(options.pop('offset_item'))
        
        self.render_titles = False
        self._renderred_titles = False
        if 'titles' in options:
            self.render_titles = bool(options.pop('titles'))

        self.fold_nested = False
        if 'fold_nested' in options:
            self.fold_nested = bool(options.pop('fold_nested'))

        self.inline = verbose_name is None
        if 'inline' in options:
            self.inline = bool(options.pop('inline'))

        self.each_title = False
        if 'title_each' in options:
            self.each_title = bool(options.pop('title_each'))

    def __str__(self):
        return 'Object("{}", fields={})'.format(self.verbose_name or 'ROOT', ', '.join([str(x) for x in self.sorted_items]))

    def __repr__(self):
        return str(self)
    
    @property
    def sorted_items(self):
        """
        Returns sorted fields.
        :return:
        """
        return sorted(self.fields, key=lambda x: x.column)

    @property
    def sorted_fields(self):
        """
        Returns sorted field templates.
        :return:
        """
        return sorted(filter(lambda y: not y.is_object, self.fields), key=lambda x: x.column)

    @property
    def sorted_nested(self):
        """
        Returns sorted nested objects templates.
        :return:
        """
        return sorted(filter(lambda y: y.is_object, self.fields), key=lambda x: x.column)

    def render(self, data):
        """
        Renders objects or an single object.
        :param data:
        :return:
        """
        # Get object data
        obj = self._get_object_value(data)

        # Make it iterable if needed
        if not isinstance(obj, list):
            obj = [obj]

        # Render each object
        self._renderred_titles = False
        for o in obj:
            for row in self._render(o):
                yield row
            if self.offset_item > 0:
                yield self._set_offset_row([''])
    
    def _render(self, obj):
        """
        :param dict obj:
        :return: 
        """
        # Render offset top
        if self.offset_top > 0 and not self._renderred_offset_top:
            self._renderred_offset_top = True
            yield from [['']]*self.offset_top
        
        # Render header if needs
        if self.render_titles and not self._renderred_titles:
            self._renderred_titles = not self.each_title
            yield self._set_offset_row(self._render_titles())
            
        # Render row
        yield self._set_offset_row(self._render_fields(obj))
        
        # Create nested folder
        ns = NestedSet()

        # Render nested table
        for child in self.sorted_nested:
            for row in child.render(obj):
                if self.fold_nested is True:
                    ns.add(row)
                else:
                    yield self._set_offset_row(row)

        # Throw nested rows if exists
        if self.fold_nested is True:
            for row in ns.get_rows():
                yield self._set_offset_row(row)

    def _set_offset_row(self, row):
        """
        Adds left margin to any row depending on `self.column` value.
        :param row:
        :return:
        """
        if self.column <= 1:
            return row
        return (['']*(self.column-1)) + row
        
    def _get_object_value(self, data):
        """
        Returns object using value_path and data formatter.
        :param data:
        :return:
        """
        return self.format(DataGetter(data).get(self.value_path, data))

    def _render_fields(self, obj):
        """
        Returns current object fields list.
        :param: dict obj:
        :return list:
        """
        object_data_getter = DataGetter(obj)
        result = []
        for field in self.sorted_items:
            if not field.inline:
                continue

            if field.column - 1 > len(result):
                result += [''] * (field.column - len(result) - 1)

            if field.is_object is True:
                result.append(field.verbose_name)
            else:
                result.append(field.render(object_data_getter))
        return result

    def _render_titles(self):
        """
        Returns current object fields list.
        :param: dict obj:
        :return list:
        """
        result = []
        for field in self.sorted_items:
            if not field.inline:
                continue

            if field.column - 1 > len(result):
                result += [''] * (field.column - len(result) - 1)

            result.append(field.verbose_name)

        return result
