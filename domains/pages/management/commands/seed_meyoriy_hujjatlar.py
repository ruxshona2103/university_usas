"""
python manage.py seed_meyoriy_hujjatlar
python manage.py seed_meyoriy_hujjatlar --clear
"""
from django.core.management.base import BaseCommand
from django.core.files import File
from pathlib import Path

from domains.pages.models import MeyoriyHujjat, NavbarSubItem

FILES = [
    {
        'title_uz': "Jismoniy tarbiya va sport to'g'risida (O'RQ-1123, 24.03.2026)",
        'title_ru': "О физической культуре и спорте (O'RQ-1123, 24.03.2026)",
        'title_en': "On Physical Culture and Sports (O'RQ-1123, 24.03.2026)",
        'filename': "1- Jismoniy tarbiya va sport toʻgʻrisida O'RQ-1123 24.03.2026.doc",
        'order': 1,
    },
    {
        'title_uz': "Ta'lim to'g'risida (O'RQ-637, 23.09.2020)",
        'title_ru': "Об образовании (O'RQ-637, 23.09.2020)",
        'title_en': "On Education (O'RQ-637, 23.09.2020)",
        'filename': "2- Ta'lim to'g'risida O'RQ-637 23.09.2020.doc",
        'order': 2,
    },
    {
        'title_uz': "O'zbekiston davlat sport akademiyasi (PQ-197, 28.05.2024)",
        'title_ru': "Государственная спортивная академия Узбекистана (PQ-197, 28.05.2024)",
        'title_en': "Uzbekistan State Sports Academy (PQ-197, 28.05.2024)",
        'filename': "3- Oʻzbekiston davlat sport akademiyasi PQ-197 28.05.2024.doc",
        'order': 3,
    },
    {
        'title_uz': "2028-yil Los-Anjeles XXXIV Yozgi Olimpiya va XVIII Paralimpiya o'yinlari (PQ-221, 08.07.2025)",
        'title_ru': "XXXIV летние Олимпийские и XVIII Паралимпийские игры Лос-Анджелес 2028 (PQ-221, 08.07.2025)",
        'title_en': "2028 Los Angeles XXXIV Summer Olympic and XVIII Paralympic Games (PQ-221, 08.07.2025)",
        'filename': "4- 2028-yil Los-Anjeles shahrida (AQSH) boʻlib oʻtadigan XXXIV yozgi Olimpiya va XVIII Paralimpiya oʻyinlari PQ-221 08.07.2025.doc",
        'order': 4,
    },
]

MEDIA_DIR = Path(__file__).resolve().parents[5] / 'media' / 'documents' / 'meyoriy'


class Command(BaseCommand):
    help = "Me'yoriy hujjatlarni bazaga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        try:
            page = NavbarSubItem.objects.get(slug='academy-regulations')
        except NavbarSubItem.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "'academy-regulations' sahifasi topilmadi. Avval navbar seed ni ishga tushiring."
            ))
            return

        if options['clear']:
            MeyoriyHujjat.objects.filter(navbar_items=page).delete()
            self.stdout.write(self.style.WARNING("Eski me'yoriy hujjatlar o'chirildi."))

        created = updated = 0
        for data in FILES:
            filename = data['filename']
            filepath = MEDIA_DIR / filename

            obj, is_new = MeyoriyHujjat.objects.get_or_create(
                title_uz=data['title_uz'],
                defaults={
                    'title_ru':   data['title_ru'],
                    'title_en':   data['title_en'],
                    'block_type': 'file-list',
                    'order':      data['order'],
                    'is_active':  True,
                }
            )

            if filepath.exists():
                with open(filepath, 'rb') as f:
                    obj.document_file.save(f'documents/meyoriy/{filename}', File(f), save=True)
                self.stdout.write(f"  [{'+'  if is_new else '~'}] Fayl yuklandi: {filename[:60]}")
            else:
                self.stdout.write(self.style.WARNING(f"  [!] Fayl topilmadi: {filepath}"))

            obj.navbar_items.add(page)

            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created} yangi, {updated} yangilandi."
        ))
