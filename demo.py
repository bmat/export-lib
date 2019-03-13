import os
import json
import time
import datetime

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

    # ex = Exporter(
    #     normalizer=Normalizer({
    #         # Object start
    #         'Production ID': {'path': '_id.$oid', 'col': 1},
    #         'Source': {'path': 'cuesheet_channel', 'col': 2},
    #         'Duration': {'path': 'cuesheet_start_time.$date', 'col': 3, 'preformat': create_duration},
    #         'Year': {'path': 'updated_at.$date', 'col': 4, 'preformat': get_year_from_timestamp},
    #         'Free Music': {'path': 'free_music', 'col': 5, 'preformat': verbose_boolean},
    #         'Title': {'path': 'category.other_production.original_title', 'col': 6},
    #         'Gema AVR': {'path': 'cuesheet_progress', 'col': 6},
    #         'Country': {'path': 'production_country', 'col': 8, 'preformat': verbose_list},
    #
    #         # Nested objects
    #         'nested': {
    #             # Describe specific behaviour of this nested field
    #             '__meta': {
    #                 # Skip few rows before nested table
    #                 'margin': 5,
    #
    #                 # Enable headers
    #                 'headers': True,
    #             },
    #
    #             # Nested cues
    #             'cuesheet.cues': {
    #                 'Start Time': {'path': 'start_time', 'col': 1},
    #                 'Work ID': {'path': 'work_id', 'col': 2},
    #                 'Length': {'path': 'length', 'col': 3},
    #                 'Music Type': {'path': 'music_type', 'col': 4},
    #                 'Use': {'path': 'use', 'col': 4},
    #                 'Music Title': {'path': 'music_work.music_title', 'col': 5},
    #                 'Origin': {'path': 'music_work.origin', 'col': 6},
    #
    #                 # I have added one more space to avoid keys duplicate
    #                 'Work ID ': {'path': 'music_work.work_id.mpn_id', 'col': 7},
    #                 ' ': {'path': 'music_work.work_id.iswc', 'col': 8},
    #
    #                 # Render nested lists
    #                 'nested': {
    #                     # Describe specific behaviour of this nested field
    #                     '__meta': {
    #                         # Skip few rows before nested table
    #                         'margin': 5,
    #
    #                         # Enable headers
    #                         'headers': True,
    #                     },
    #
    #                     'music_work.author': {
    #                         'Name': {'path': 'name', 'col': 9+1},
    #                         'Rolle': {'path': 'rolle', 'col': 10+1}
    #                     },
    #                     'music_work.publisher': {
    #                         'Name': {'path': 'name', 'col': 11+1},
    #                         'Rolle': {'path': 'rolle', 'col': 12+1},
    #                     },
    #                     'music_work.interpreter': {
    #                         'Name': {'path': 'name', 'col': 13+1},
    #                         'Rolle': {'path': 'rolle', 'col': 14+1},
    #                     },
    #                 },
    #             }
    #         }
    #     }),
    #     output=XLSXBytesOutputWriter()
    # )

    ex = Exporter(
        normalizer=Normalizer(tpl.Object(col=1, titles=True, fields=[
            tpl.Field(1, 'Production ID', '_id.$oid'),
            tpl.Field(2, 'Source', 'cuesheet_channel'),
            tpl.Field(3, 'Duration', 'cuesheet_start_time.$date', create_duration),
            tpl.Field(4, 'Year', 'updated_at.$date', get_year_from_timestamp),
            tpl.Field(5, 'Free Music', 'free_music', verbose_boolean),
            tpl.Field(6, 'Title', 'category.other_production.original_title', verbose_boolean),
            tpl.Field(7, 'Gema AVR', 'cuesheet_progress'),
            tpl.Field(8, 'Country', 'production_country', verbose_list),
            tpl.Object(
                col=1,
                offset_top=5,
                verbose_name='Cuesheets',
                path='cuesheet.cues',
                titles=True,
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
                    tpl.Field(8, 'Work ID', 'music_work.work_id.mpn_id'),
                    tpl.Field(9, 'Work ID Type', 'music_work.work_id.iswc'),
                    tpl.Object(
                        col=10,
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
            'K': 8.67,
            'L': 28.76,
            'M': 8.67,
            'N': 29.03,
            'O': 8.67
        })
    )

    with open('demo_result.xlsx', 'wb') as f:
        data = [json.load(open(os.path.join(RESOURCES, 'input.json'), 'r'))]
        filename, mime, data = ex.generate(data)
        f.write(data)
