

class NestedDict(dict):
    """
    Returns soft python-dictionary each item of which
    can be set easily without setting parent dictionary.

        >> s = NestedDict()
        >> s['a']['b']['c'] = 1
        {'a': {'b': {'c': 1}}}

    """
    def __getitem__(self, item):
        if item not in self:
            self[item] = NestedDict()

        return super(NestedDict, self).__getitem__(item)
