import time

import schematics

from export_util.template import DataGetter


def schema_model_to_dict(value):
    """
    Converts schemtics model to dict.
    :param value:
    :return:
    """
    if isinstance(value, schematics.Model):
        return value.to_primitive()
    return value


def any_to_string(value, obj: DataGetter = None):
    """
    This function converts any value to string.
    :param value:
    :param obj:
    :return:
    """
    return str(value)


def seconds_to_time(seconds, obj: DataGetter = None):
    """
    This function formats seconds into readable 00:00:00
    view.
    """
    return time.strftime('%H:%M:%S', time.gmtime(seconds))


def seconds_to_year(seconds, obj: DataGetter = None):
    """
    This function returns year from the provided timestamp.
    """
    return time.strftime('%Y', time.gmtime(seconds))


def milliseconds_to_time(milliseconds, obj: DataGetter = None):
    """
    This function formats milliseconds into readable 00:00:00
    view.
    """
    return time.strftime('%H:%M:%S', time.gmtime(int(milliseconds / 1000)))


def milliseconds_to_year(milliseconds, obj: DataGetter = None):
    """
    This function returns year from the provided timestamp.
    """
    return time.strftime('%Y', time.gmtime(int(milliseconds / 1000)))


def boolean_to_yn(boolean, obj: DataGetter = None):
    """
    This function returns "NO" if `boolean` is False, and
    returns "YES" if `boolean` is True.
    """
    return 'YES' if boolean else 'NO'


def boolean_to_10(boolean, obj: DataGetter = None):
    """
    This function returns "NO" if `boolean` is False, and
    returns "YES" if `boolean` is True.
    """
    return '1' if boolean else '0'


def boolean_to_sign(boolean, obj: DataGetter = None):
    """
    This function returns "NO" if `boolean` is False, and
    returns "YES" if `boolean` is True.
    """
    return '+' if boolean else '-'


def boolean_to_string(boolean, obj: DataGetter = None):
    """
    This function returns "NO" if `boolean` is False, and
    returns "YES" if `boolean` is True.
    """
    return str(boolean)


def list_to_string(list_objects, obj: DataGetter = None):
    """
    This function formats list of an objects into single string.
    """
    return ', '.join(map(lambda x: str(x), list_objects))


def list_dicts_to_string(output_format=None, default='---'):
    """
    This function creates formatter which joins list of dicts
    into single line.
    """
    def _formatter(list_objects, obj: DataGetter = None):
        if not list_objects:
            return default
        if output_format is None:
            return ', '.join(map(str, list_objects))
        return ', '.join(map(lambda x: output_format.format(**schema_model_to_dict(x)), list_objects))
    return _formatter


def dict_to_string(output_format=None, default='---'):
    """
    This function creates formatter which joins list of dicts
    into single line.
    """
    def _formatter(dict_o, obj: DataGetter = None):
        if not dict_o:
            return default
        if output_format is None:
            return str(dict_o)
        return output_format.format(**schema_model_to_dict(dict_o))
    return _formatter


__all__ = [
    'seconds_to_time', 'seconds_to_year',
    'milliseconds_to_time', 'milliseconds_to_year',
    'boolean_to_yn', 'boolean_to_10', 'boolean_to_sign', 'boolean_to_string',
    'list_to_string', 'list_dicts_to_string',
    'dict_to_string',
]
