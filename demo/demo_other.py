import os
import json
import time

from export_util import Exporter
from export_util import template as tpl
from export_util.normalize import Normalizer
from export_util.writer import XLSXBytesOutputWriter, OutputTemplate


BASE_DIR = os.path.dirname(__file__)
RESOURCES = os.path.join(BASE_DIR, 'resources')


class WriterTemplate(OutputTemplate):
    """
    Let's build some table on an existing xlsx document.
    """
    template_file = os.path.join(RESOURCES, 'template.xlsx')
    table_start = 'A2'


def format_timestamp(seconds, object_source=None):
    """
    This function formats seconds into readable 00:00:00
    view.
    :param seconds:
    :param object_source:
    :return:
    """
    return time.strftime('%H:%M:%S', time.gmtime(seconds))


def create_duration(start_time, object_source):
    """
    This function formats duration column depending on the object
    `cuesheet_start_time.$date` and `cuesheet_end_time.$date`.

    When we know the amount of seconds duration, we formatting it into
    the HH:MM:SS format.
    :param start_time:
    :param DataGetter object_source:
    :return:
    """
    return format_timestamp(object_source.get('cuesheet_end_time.$date') - start_time)


def get_year_from_timestamp(milliseconds, object_source):
    """
    This function returns year from the provided timestamp.
    :param milliseconds:
    :param object_source:
    :return:
    """
    return time.strftime('%Y', time.gmtime(int(milliseconds / 1000)))


def verbose_boolean(boolean, object_source):
    """
    This function returns "NO" if `boolean` is False, and
    returns "YES" if `boolean` is True.
    :param boolean:
    :param object_source:
    :return:
    """
    return 'YES' if boolean else 'NO'


def verbose_list(list_objects, object_source):
    """
    This function formats list of an objects into single string.
    :param list_objects:
    :param object_source:
    :return:
    """
    return ', '.join(map(lambda x: str(x), list_objects))


def verbose_object_list(output_format=None, default='---'):
    """
    This function joins list of dicts into single line.
    :param output_format:
    :param default:
    :return:
    """
    def _formatter(list_objects, object_source):
        if not list_objects:
            return default
        if output_format is None:
            return ', '.join(map(str, list_objects))
        return ', '.join(map(lambda x: output_format.format(**x), list_objects))
    return _formatter


def create_finish_value(start_time, object_source):
    """
    This function simply adds start_time to object_source.length
    :param start_time:
    :param object_source:
    :return:
    """
    return format_timestamp(start_time + int(object_source.get('length', 0)))


if __name__ == '__main__':
    ex = Exporter(
        normalizer=Normalizer(tpl.Object(col=1, titles=False, path='cuesheet.cues', fields=[
            tpl.Field(1, 'Work ID', 'work_id'),
            tpl.Field(2, 'Music Title', 'music_work.music_title'),
            tpl.Field(3, 'Start Time', 'start_time', preformat=format_timestamp, default=0),
            tpl.Field(4, 'Finish', 'start_time', preformat=create_finish_value, default=0),
            tpl.Field(5, 'Duration seconds', 'length', preformat=format_timestamp, default=0),
            tpl.Field(5, 'Duration', 'length', default=0),
            tpl.Field(6, 'Authors', 'music_work.author', preformat=verbose_object_list('{name} ({rolle})', 'N/A'), default=[]),
            tpl.Field(7, 'Track number', 'UNDEFINED_YET', default='N/A'),
            tpl.Field(8, 'Type of use', 'use'),
            tpl.Field(9, 'Origin', 'music_work.origin'),
            tpl.Field(10, 'Publisher', 'music_work.publisher', preformat=verbose_object_list('{name} ({rolle})', 'N/A'), default=[]),
            tpl.Field(11, 'CD-Title', 'UNDEFINED_YET', default='N/A'),
            tpl.Field(12, 'Interpreter', 'music_work.interpreter', preformat=verbose_object_list('{name} ({rolle})', 'N/A'), default=[]),
            tpl.Field(13, 'Label', 'music_work.sound_recording_id.label'),
            tpl.Field(14, 'Label Code', 'music_work.sound_recording_id.label_code'),
            tpl.Field(15, 'Gema number', 'music_work.work_id.gema_work_nr'),
            tpl.Field(16, 'CD Catalog number', 'UNDEFINED_YET', default='N/A'),
            tpl.Field(17, 'ISRC', 'music_work.sound_recording_id.isrc'),
            tpl.Field(18, 'ISWC', 'music_work.work_id.iswc'),
            tpl.Field(19, 'BMAT ID', 'monitoring_id.fingerprint_id'),
            tpl.Field(20, 'Video Link', 'UNDEFINED_YET', default='N/A'),
        ])),
        output=XLSXBytesOutputWriter(template=WriterTemplate)
    )

    with open('demo_result.xlsx', 'wb') as f:
        data = [json.load(open(os.path.join(RESOURCES, 'input.json'), 'r'))]
        filename, mime, data = ex.generate(data)
        f.write(data)
