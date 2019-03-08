import os
from bson import ObjectId

from export_util import Exporter
from export_util.writer import XLSXBytesOutputWriter
from export_util.normalize import Normalizer


data = [{
    "_id" : ObjectId("5c6d8445d152492485db693c"),
    "created_at" : str("2019-02-20T16:45:57.025Z"),
    "updated_at" : str("2019-02-21T10:44:46.657Z"),
    "category" : {
        "other_production" : {
            "original_title" : "la-la-land-original-soundtrack"
        }
    },
    "production_country" : [],
    "production_person" : [],
    "additional_info" : [],
    "cuesheet_owner" : ObjectId("5be06278cfa74f11ce84570a"),
    "file_info" : "5c6d844497efa3001418c884",
    "cuesheet" : {
        "cues" : [ 
            {
                "start_time" : 1,
                "work_id" : 1,
                "length" : 227,
                "reference_start_time" : 0,
                "reference_id" : 118041800,
                "service_id" : "00602557100549_1_1_USUG11600653",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c42f440577c65a0cd4",
                "music_work" : ObjectId("5c4afa7fdd536700c1210c77"),
                "phonogram_id" : "8e855e15-fa86-42d5-b5a0-85719820865b",
                "match_id" : 8,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "6d1c6b09-ab51-4afa-be83-3d453c5e67f0"
                },
                "use" : "ILLM",
                "index" : "sun justin soundtrack) la cast land another none day paul (from benj pasek land\" of vton \"la hurwitz",
                "_author" : "justin none paul pasek benj hurwitz",
                "_interpreter" : "la cast land none",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 229,
                "work_id" : 2,
                "length" : 259,
                "reference_start_time" : 0,
                "reference_id" : 118046398,
                "service_id" : "00602557100549_1_2_USUG11600662",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c32f440577c65a04e9",
                "music_work" : ObjectId("5c6e810f859abd0013899d61"),
                "phonogram_id" : "2a0d5ee3-8dda-448a-b3dd-a340c31a944d",
                "match_id" : 26,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "2653509c-00d8-4e36-b8df-6925aa00bd0a"
                },
                "use" : "ILLM",
                "index" : "soundtrack) in (from callie \"la hernandez crowd paul emma pasek someone benj rothe mizuno stone justin none land\" jessica the vton sonoya hurwitz la",
                "_author" : "justin none paul pasek benj hurwitz",
                "_interpreter" : "mizuno stone none emma rothe callie jessica hernandez sonoya",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 489,
                "work_id" : 3,
                "length" : 95,
                "reference_start_time" : 0,
                "reference_id" : 118047654,
                "service_id" : "00602557100549_1_3_USUG11600660",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c52f440577c65a12c3",
                "music_work" : ObjectId("5c6e8111859abd0013899d62"),
                "phonogram_id" : "3e1ea0e2-a6be-4495-a443-e608f6b55a35",
                "match_id" : 24,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "1b470822-d7d9-4db1-b457-5d785fee3d45"
                },
                "use" : "ILLM",
                "index" : "justin soundtrack) la none & sebastian's (from theme land\" vton \"la mia hurwitz",
                "_author" : "none justin hurwitz",
                "_interpreter" : "none justin hurwitz",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 586,
                "work_id" : 4,
                "length" : 236,
                "reference_start_time" : 0,
                "reference_id" : 118041388,
                "service_id" : "00602557100549_1_4_USUG11600652",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c42f440577c65a0cb2",
                "music_work" : ObjectId("5c6e8112859abd0013899d63"),
                "phonogram_id" : "ef66d284-604c-40c7-956d-16eb8c80b5f1",
                "match_id" : 30,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "052ff471-5e62-4557-9f10-5b44bb8397c2"
                },
                "use" : "ILLM",
                "index" : "a ryan gosling justin stone soundtrack) la none lovely emma night (from land\" vton \"la hurwitz",
                "_author" : "none justin hurwitz",
                "_interpreter" : "ryan gosling stone none emma",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 823,
                "work_id" : 5,
                "length" : 110,
                "reference_start_time" : 0,
                "reference_id" : 122937778,
                "service_id" : "00602557100549_1_5_USUG11600659",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c52f440577c65a11d7",
                "music_work" : ObjectId("5c6e8114859abd0013899d64"),
                "phonogram_id" : "144e47b5-a0df-4e84-ba5c-1a35bc48d25b",
                "match_id" : 28,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "43214a79-fc25-49a4-966e-ae73e3106978"
                },
                "use" : "ILLM",
                "index" : "justin soundtrack) la habit none (from land\" vton herman's \"la hurwitz",
                "_author" : "none justin hurwitz",
                "_interpreter" : "none justin hurwitz",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 935,
                "work_id" : 6,
                "length" : 106,
                "reference_start_time" : 0,
                "reference_id" : 99744917,
                "service_id" : "00602557091717_1_1_USUM71606369",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335272f440577c655779b",
                "music_work" : ObjectId("5c6e8115859abd0013899d65"),
                "phonogram_id" : "6f037971-9f45-4b90-a202-56a8e67f1ea8",
                "match_id" : 32,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "1a4c325d-5809-433c-97aa-a2085c06a5b7"
                },
                "use" : "ILLM",
                "index" : "ryan gosling justin stars none city of vton hurwitz",
                "_author" : "none justin hurwitz",
                "_interpreter" : "ryan gosling none",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 1046,
                "work_id" : 7,
                "length" : 256,
                "reference_start_time" : 0,
                "reference_id" : 119322402,
                "service_id" : "00602557100549_1_7_USUG11600661",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c52f440577c65a10d4",
                "music_work" : ObjectId("5c4afb9cdd53670128210b73"),
                "phonogram_id" : "92df4a32-a273-4741-a0e6-c90f6b1dfca1",
                "match_id" : 20,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "30654ebd-445a-4e1d-908d-545d592455d5"
                },
                "use" : "ILLM",
                "index" : "justin soundtrack) la planetarium none (from land\" vton \"la hurwitz",
                "_author" : "none justin hurwitz",
                "_interpreter" : "none justin hurwitz",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 1303,
                "work_id" : 8,
                "length" : 124,
                "reference_start_time" : 0,
                "reference_id" : 118044468,
                "service_id" : "00602557100549_1_8_USUG11600663",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c52f440577c65a12df",
                "music_work" : ObjectId("5c6356ae04cdda0180ec4e32"),
                "phonogram_id" : "692f83dc-821b-4d55-95bb-c493e1ddae8e",
                "match_id" : 22,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "3018feec-b4e5-4f1a-9b9d-b48167c8c57f"
                },
                "use" : "ILLM",
                "index" : "summer damien madeline soundtrack) la justin none chazelle (from land\" / vton montage \"la hurwitz",
                "_author" : "damien justin none chazelle hurwitz",
                "_interpreter" : "none justin hurwitz",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 1428,
                "work_id" : 9,
                "length" : 148,
                "reference_start_time" : 0,
                "reference_id" : 116458090,
                "service_id" : "00602557281033_1_1_USUG11600656",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "5973356b2f440577c65765de",
                "music_work" : ObjectId("5c587a94dbe502067bc56d18"),
                "phonogram_id" : "898f0e20-63fc-42a2-a20f-dcca73dd6fbe",
                "match_id" : 34,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "810f1372-04a8-4793-90d6-146a90206f30"
                },
                "use" : "ILLM",
                "index" : "ryan stone justin gosling stars la soundtrack) none city paul (from benj pasek land\" emma of vton \"la hurwitz",
                "_author" : "justin none paul pasek benj hurwitz",
                "_interpreter" : "ryan gosling stone none emma",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 1578,
                "work_id" : 10,
                "length" : 189,
                "reference_start_time" : 0,
                "reference_id" : 119324676,
                "service_id" : "00602557100549_1_10_USUG11600664",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c52f440577c65a120f",
                "music_work" : ObjectId("5c6e8119859abd0013899d66"),
                "phonogram_id" : "bd823a17-2d97-4622-b72a-d6c3ed1b67b6",
                "match_id" : 18,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "1daaf91f-7257-408f-aeff-77879dc4abcf"
                },
                "use" : "ILLM",
                "index" : "a justin vries stephens none start fire vton angelique marius de john cinelu legend hurwitz",
                "_author" : "justin vries stephens none angelique marius de john cinelu hurwitz",
                "_interpreter" : "john none legend",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 1770,
                "work_id" : 11,
                "length" : 86,
                "reference_start_time" : 1,
                "reference_id" : 119322942,
                "service_id" : "00602557100549_1_11_USUG11600657",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c52f440577c65a12ce",
                "music_work" : ObjectId("5c6e811b859abd0013899d67"),
                "phonogram_id" : "c06754ad-45c9-4c70-bdfa-23312d14aeff",
                "match_id" : 10,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "bbed69cc-38fa-4b63-bbd5-f4303d1c980e"
                },
                "use" : "ILLM",
                "index" : "party justin soundtrack) la none (from engagement land\" vton \"la hurwitz",
                "_author" : "none justin hurwitz",
                "_interpreter" : "none justin hurwitz",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 1858,
                "work_id" : 12,
                "length" : 227,
                "reference_start_time" : 0,
                "reference_id" : 118042842,
                "service_id" : "00602557100549_1_12_USUG11600654",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c52f440577c65a10e0",
                "music_work" : ObjectId("5c6dfb671d283a0594f518f8"),
                "phonogram_id" : "b6afa1bc-f185-4307-8c13-fead8f4f2e43",
                "match_id" : 12,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "1ee1a036-c82e-467e-b843-863099c1ca37"
                },
                "use" : "ILLM",
                "index" : "fools justin stone soundtrack) la audition none (the who paul emma (from benj pasek land\" dream) vton \"la hurwitz",
                "_author" : "justin none paul pasek benj hurwitz",
                "_interpreter" : "emma stone none",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 2086,
                "work_id" : 13,
                "length" : 458,
                "reference_start_time" : 0,
                "reference_id" : 116489944,
                "service_id" : "00602557100549_1_13_USUG11600658",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c32f440577c65a04e1",
                "music_work" : ObjectId("5c6606d88cdd1d0471948d9a"),
                "phonogram_id" : "88eb920b-3a40-4551-962c-ea7bbaa21c90",
                "match_id" : 14,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "b139f49b-8c23-4f92-a72d-bf128814f13b"
                },
                "use" : "ILLM",
                "index" : "justin soundtrack) la none (from land\" vton epilogue \"la hurwitz",
                "_author" : "none justin hurwitz",
                "_interpreter" : "none justin hurwitz",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 2546,
                "work_id" : 14,
                "length" : 43,
                "reference_start_time" : 0,
                "reference_id" : 115489719,
                "service_id" : "00602557100549_1_14_USUG11601142",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c62f440577c65a1b17",
                "music_work" : ObjectId("5c6e811d859abd0013899d68"),
                "phonogram_id" : "037ec294-97b2-4237-a942-316a7eab9287",
                "match_id" : 16,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "63120ff1-9a63-4644-abbd-95f7b14b1c39"
                },
                "use" : "ILLM",
                "index" : "justin soundtrack) la none (from end land\" the vton \"la hurwitz",
                "_author" : "none justin hurwitz",
                "_interpreter" : "none justin hurwitz",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }, 
            {
                "start_time" : 2592,
                "work_id" : 15,
                "length" : 159,
                "reference_start_time" : 0,
                "reference_id" : 119323388,
                "service_id" : "00602557100549_1_15_USUG11600655",
                "source" : "crawler_universaldigitalcontent",
                "single_view_id" : "597335c52f440577c65a10fb",
                "music_work" : ObjectId("5c4aee6bdd53670061210b7c"),
                "phonogram_id" : "ae7819bf-0733-48e0-b0fb-7cbde01cc6f0",
                "match_id" : 6,
                "music_type" : "music",
                "monitoring_id" : {
                    "fingerprint_id" : "243713bb-3545-4183-b837-ee1d8729dcb3"
                },
                "use" : "ILLM",
                "index" : "feat. (humming) stone justin stars la soundtrack) none city emma (from benj pasek land\" paul of vton \"la hurwitz",
                "_author" : "justin none paul pasek benj hurwitz",
                "_interpreter" : "none justin hurwitz",
                "_origin" : "VTON",
                "metadata_complete" : 100
            }
        ]
    },
    "free_music" : False
}]



class BmatTemplate:
    template_file = os.path.join(
        os.path.dirname(__file__),
        'demo_resources',
        'tpl.xlsx'
    )

    images_positions = {
        "A1": {
            "name": os.path.join(
                        os.path.dirname(__file__),
                        'demo_resources',
                        'logo.png'
            ),
            "size": (300, None)
        }
    }

    worksheet_index = 0
    table_start = 'A7'
    # table_fields = BmatFields._fields

    # other_fields_positions = BmatOtherFields(
    #     title='B1',
    #     type='C2',
    #     air_date='C3',
    #     company='C4',
    #     duration='G2',
    #     network_station='G3',
    #     created='G4',
    #     updated='K2'
    # )._asdict()


if __name__ == '__main__':
    ex = Exporter(
        normalizer=Normalizer({
            'file_info': {'path': 'file_info', 'col': 1},
            'nested': {
                'cuesheet.cues': {
                    'Title': {'path': 'index', 'col': 3},
                    'Author': {'path': '_author', 'col': 4},
                    'fingerprint_id': {'path': 'monitoring_id.fingerprint_id', 'col': 5}
                }
            }
        }),
        output=XLSXBytesOutputWriter(template=BmatTemplate)
    )

    with open('demo_result.xlsx', 'wb') as f:
        filename, mime, data = ex.generate(data)
        f.write(data)
