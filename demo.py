import os
import json
import time

from export_util import Exporter
from export_util.writer import XLSXBytesOutputWriter
from export_util.normalize import Normalizer
from export_util import template as tpl


BASE_DIR = os.path.dirname(__file__)
RESOURCES = os.path.join(BASE_DIR, 'demo_resources')


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
    return time.strftime(
        '%H:%M:%S',
        time.gmtime(
            object_source.get('cuesheet_end_time.$date') - start_time
        )
    )


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


if __name__ == '__main__':
    ex = Exporter(
        normalizer=Normalizer(tpl.Object(col=1, titles=True, fields=[
            tpl.Field(1, 'Production ID', '_id.$oid'),
            tpl.Field(2, 'Source', 'cuesheet_channel'),
            tpl.Field(3, 'Duration', 'cuesheet_start_time.$date', create_duration),
            tpl.Field(4, 'Year', 'updated_at.$date', get_year_from_timestamp),
            tpl.Field(5, 'Free Music', 'free_music', verbose_boolean),
            tpl.Field(6, 'Title', 'category.other_production.original_title'),
            tpl.Field(7, 'Gema AVR', 'cuesheet_progress'),
            tpl.Field(8, 'Country', 'production_country', verbose_list),
            tpl.Object(
                col=1,
                offset_top=5,
                verbose_name='Cuesheets',
                path='cuesheet.cues',
                titles=True,
                # title_each=True,
                fold_nested=True,
                offset_item=1,
                fields=[
                    tpl.Field(1, 'Start Time', 'start_time'),
                    tpl.Field(2, 'Work ID', 'work_id'),
                    tpl.Field(3, 'Length', 'length'),
                    tpl.Field(4, 'Music Type', 'music_type'),
                    tpl.Field(5, 'Use', 'use'),
                    tpl.Field(6, 'Music Title', 'music_work.music_title'),
                    tpl.Field(7, 'Origin', 'music_work.origin'),
                    tpl.Field(8, 'Label', 'music_work.sound_recording_id.label'),
                    tpl.Field(9, 'Label Code', 'music_work.sound_recording_id.label_code'),
                    tpl.Field(10, 'EAN UPC', 'music_work.sound_recording_id.ean_upc'),
                    tpl.Field(11, 'ISRC', 'music_work.sound_recording_id.isrc'),
                    tpl.Field(12, 'Work ID', 'music_work.work_id.mpn_id'),
                    tpl.Field(13, 'Work ID Type', 'music_work.work_id.iswc'),
                    tpl.Object(
                        col=14,
                        verbose_name='Authors',
                        path='music_work.author',
                        inline=True,
                        titles=False,
                        fields=[
                            tpl.Field(1, 'Name', 'name'),
                            tpl.Field(2, 'Rolle', 'rolle'),
                        ]
                    ),
                    tpl.Object(
                        col=16,
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
                        col=18,
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
        ])),
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
            'K': 29.45,
            'L': 29.00,
            'M': 14.72,
            'N': 29.03,
            'O': 8.67,
            'P': 29.03,
            'R': 29.03
        })
    )

    with open('demo_result.xlsx', 'wb') as f:
        data = [json.load(open(os.path.join(RESOURCES, 'input.json'), 'r'))]
        filename, mime, data = ex.generate(data)
        f.write(data)
