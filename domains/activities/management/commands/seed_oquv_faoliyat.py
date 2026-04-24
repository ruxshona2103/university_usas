"""
python manage.py seed_oquv_faoliyat

index.json dagi ma'lumotlarni DB ga qo'shadi:
  - 4 ta root IlmiyFaoliyatCategory (parent=None)
  - Har bir blok uchun child IlmiyFaoliyatCategory
  - Har bir link uchun IlmiyFaoliyat item (file URL saqlandi)
"""

import uuid
from urllib.parse import urlparse, urlunparse

from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

IMAGEKIT_PREFIX = "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/"


def _extract_path(url):
    """Imagekit URL dan storage path ni ajratib oladi."""
    if not url:
        return None
    parsed = urlparse(url)
    path = parsed.path
    prefix = "/django-imagekitio-storage/"
    if prefix in path:
        path = path[path.index(prefix) + len(prefix):]
    return path


DATA = [
    {
        "id": "c8ddf791-05c5-4c70-83ba-84998c95ef9c",
        "slug": "malaka-talablari",
        "title_uz": "Malaka talablari",
        "order": 1,
        "blocks": [
            {
                "title_uz": "Bakalavriat",
                "links": [
                    {"label_uz": "61010200 — Sport faoliyati (Bakalavr) Malaka talabi", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_fc0a146f697d4f798f748efa3aea541a.pdf?updatedAt=1776860690312", "order": 1},
                    {"label_uz": "61010300 — Adaptiv jismoniy tarbiya (Bakalavr) Malaka talabi", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_cae60f01d88048f0a24759d605c378d7.pdf?updatedAt=1776860752901", "order": 2},
                    {"label_uz": "60411800 — Menejment (Bakalavr) Malaka talabi", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_1b9ad9a9dd7e4a83aab475de32dded59.pdf?updatedAt=1776860804636", "order": 3},
                ],
            },
            {
                "title_uz": "Magistratura",
                "links": [
                    {"label_uz": "Magistratura Malaka talabi", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_6cca2413799b4d7a912eb690d7094029.pdf?updatedAt=1776860883308", "order": 4},
                ],
            },
        ],
    },
    {
        "id": "d8af1618-b977-492e-a896-3fdd7cb4187e",
        "slug": "oquv-dasturlar",
        "title_uz": "O'quv dasturlar",
        "order": 2,
        "blocks": [
            {
                "title_uz": "Bakalavriat",
                "links": [
                    {"label_uz": "O'quv dastur 1 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_8407d88dbcb341498fd9b88641fbb6c2.pdf?updatedAt=1776861873364", "order": 1},
                    {"label_uz": "O'quv dastur 2 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_b7af2406dd034d4e9f5719dd54126c72.pdf?updatedAt=1776861920643", "order": 2},
                    {"label_uz": "O'quv dastur 3 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_774189ec67ba43c1aa6c3a8cadb44bfc.pdf?updatedAt=1776861963711", "order": 3},
                    {"label_uz": "O'quv dastur 4 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_4a71e0094d714d4c9a162e7c68f1416a.pdf?updatedAt=1776862735201", "order": 4},
                    {"label_uz": "O'quv dastur 5 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_0d8ec7a586504219b5f382bb89abdbf5.pdf?updatedAt=1776862789802", "order": 5},
                    {"label_uz": "O'quv dastur 6 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_18248710e6c14653a7570500488bbbfa.pdf?updatedAt=1776862844461", "order": 6},
                    {"label_uz": "O'quv dastur 7 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_9615570425de4ead83aa3aa5cd895ba7.pdf?updatedAt=1776862895554", "order": 7},
                    {"label_uz": "O'quv dastur 8 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_c1c8bd95bdb646019e936d9de379663b.pdf?updatedAt=1776862948696", "order": 8},
                    {"label_uz": "O'quv dastur 9 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_4fd831f5fdfd4eedaa7639fc8a71e2b1.pdf?updatedAt=1776863031527", "order": 9},
                    {"label_uz": "O'quv dastur 10 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_011cc966cf3f47e6ba229009e1d380ea.pdf?updatedAt=1776863082742", "order": 10},
                    {"label_uz": "O'quv dastur 11 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_fb022a2f1457481eb71850c670bb3b47.pdf?updatedAt=1776863139703", "order": 11},
                    {"label_uz": "O'quv dastur 12 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_ae7fa88236a44c94951e702dd59322ba.pdf?updatedAt=1776863188358", "order": 12},
                    {"label_uz": "O'quv dastur 13 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_0eec0e1cbf1e4bbfa1abea55743521ed.pdf?updatedAt=1776863296319", "order": 13},
                    {"label_uz": "O'quv dastur 14 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_258f09091e204ccfadfdb9a643ac56cd.pdf?updatedAt=1776863245461", "order": 14},
                    {"label_uz": "O'quv dastur 15 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_823fd3d017ba4156ac9654c15e929942.pdf?updatedAt=1776863446683", "order": 15},
                    {"label_uz": "O'quv dastur 16 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_1202023a2c764b50aac4d0eb853febfe.pdf?updatedAt=1776863497572", "order": 16},
                    {"label_uz": "O'quv dastur 17 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_e66e801d994b42d2b2b9aa654112814f.pdf?updatedAt=1776863556373", "order": 17},
                    {"label_uz": "O'quv dastur 18 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_f6d6d5d23922489bb6ad3f5611f40046.pdf?updatedAt=1776863641849", "order": 18},
                    {"label_uz": "O'quv dastur 19 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_f7a1668e17864842bdbffc7d548c8f21.pdf?updatedAt=1776863712744", "order": 19},
                    {"label_uz": "O'quv dastur 20 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_957499945e2f434c836e4bf5fd3ecf7c.pdf?updatedAt=1776863779313", "order": 20},
                    {"label_uz": "O'quv dastur 21 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_05082d49062c4040a9a0f721cf0c5f43.pdf?updatedAt=1776863830072", "order": 21},
                    {"label_uz": "O'quv dastur 22 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_cd83e66b813d4b56959cf3122a238219.pdf?updatedAt=1776863896803", "order": 22},
                    {"label_uz": "O'quv dastur 24 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_b9b9702ea9ab41319d226d0b9507e9fd.pdf?updatedAt=1776864004921", "order": 24},
                    {"label_uz": "O'quv dastur 25 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_7ba33c2dc4314311958cc327f3162f52.pdf?updatedAt=1776864069880", "order": 25},
                    {"label_uz": "O'quv dastur 26 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_4595e095a155469281858c88d5dde925.pdf?updatedAt=1776864132215", "order": 26},
                    {"label_uz": "O'quv dastur 27 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_09a7b8843a584e279ec0020e22d0c976.pdf?updatedAt=1776864189649", "order": 27},
                    {"label_uz": "O'quv dastur 28 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_a92e8302a7484993a8a8e0771a13a198.pdf?updatedAt=1776864243447", "order": 28},
                    {"label_uz": "O'quv dastur 29 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_58a38ecab37a48f28d9a998212ffe3af.pdf?updatedAt=1776864298502", "order": 29},
                    {"label_uz": "O'quv dastur 30 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_59fa6ee2e8bf473cb0ae5457277b4ddf.pdf?updatedAt=1776864365838", "order": 30},
                    {"label_uz": "O'quv dastur 31 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_4150440b5b1b4b17b93fe7c155fcd548.pdf?updatedAt=1776864419714", "order": 31},
                    {"label_uz": "O'quv dastur 32 (Bakalavr)", "url": "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/ilmiy_faoliyat/files/media_ilmiy_faoliyat_files_953f9fdadfd944b680184bcdba348059.pdf?updatedAt=1776864482784", "order": 32},
                ],
            },
        ],
    },
    {
        "id": "ef26ed78-e363-4a5f-a319-a70327975d43",
        "slug": "oquv-grafigi",
        "title_uz": "O'quv grafigi",
        "order": 3,
        "blocks": [],
    },
    {
        "id": "ed9b431b-7e29-44c8-8d98-a1679e3e9039",
        "slug": "oquv-rejalari",
        "title_uz": "O'quv rejalari",
        "order": 4,
        "blocks": [],
    },
]


class Command(BaseCommand):
    help = "index.json dagi o'quv faoliyat ma'lumotlarini DB ga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Avval mavjud IlmiyFaoliyat va IlmiyFaoliyatCategory larni o\'chiradi',
        )

    def handle(self, *args, **options):
        if options['clear']:
            IlmiyFaoliyat.objects.all().delete()
            IlmiyFaoliyatCategory.objects.all().delete()
            self.stdout.write(self.style.WARNING('Barcha mavjud ma\'lumotlar o\'chirildi.'))

        for root_data in DATA:
            root_cat, created = IlmiyFaoliyatCategory.objects.update_or_create(
                slug=root_data['slug'],
                defaults={
                    'id': uuid.UUID(root_data['id']),
                    'title_uz': root_data['title_uz'],
                    'parent': None,
                    'order': root_data['order'],
                },
            )
            action = 'Yaratildi' if created else 'Yangilandi'
            self.stdout.write(f"  [{action}] Root: {root_cat.title_uz}")

            for block_idx, block in enumerate(root_data.get('blocks', []), start=1):
                block_slug = block['title_uz'].lower().replace(' ', '-').replace("'", '').replace("'", '')
                child_slug = f"{root_data['slug']}-{block_slug}"
                child_cat, c_created = IlmiyFaoliyatCategory.objects.update_or_create(
                    slug=child_slug,
                    defaults={
                        'title_uz': block['title_uz'],
                        'parent': root_cat,
                        'order': block_idx,
                    },
                )
                c_action = 'Yaratildi' if c_created else 'Yangilandi'
                self.stdout.write(f"    [{c_action}] Child: {child_cat.title_uz} (slug={child_slug})")

                for link in block.get('links', []):
                    file_path = _extract_path(link['url'])
                    item, i_created = IlmiyFaoliyat.objects.update_or_create(
                        category=child_cat,
                        order=link['order'],
                        defaults={
                            'title_uz': link['label_uz'],
                            'is_active': True,
                        },
                    )
                    if file_path:
                        item.file.name = file_path
                        item.save(update_fields=['file'])
                    i_action = 'Yaratildi' if i_created else 'Yangilandi'
                    self.stdout.write(f"      [{i_action}] Item: {item.title_uz[:60]}")

        self.stdout.write(self.style.SUCCESS('\nBarcha ma\'lumotlar muvaffaqiyatli qo\'shildi!'))
