"""
python manage.py seed_meyoriy_hujjatlar
python manage.py seed_meyoriy_hujjatlar --clear
"""
from django.core.management.base import BaseCommand
from domains.pages.models import MeyoriyHujjat, NavbarSubItem

FILES = [
    {
        'title_uz': "Jismoniy tarbiya va sport to'g'risida (O'RQ-1123, 24.03.2026)",
        'title_ru': "О физической культуре и спорте (O'RQ-1123, 24.03.2026)",
        'title_en': "On Physical Culture and Sports (O'RQ-1123, 24.03.2026)",
        'link': "https://ik.imagekit.io/cliq9vzilx/django-imagekitio-storage/documents/2026/05/1_Jismoniy_tarbiya_va_sport_to%CA%BBg%CA%BBrisida_ORQ_1123_24_03_2026.doc",
        'order': 1,
    },
    {
        'title_uz': "Ta'lim to'g'risida (O'RQ-637, 23.09.2020)",
        'title_ru': "Об образовании (O'RQ-637, 23.09.2020)",
        'title_en': "On Education (O'RQ-637, 23.09.2020)",
        'link': "",
        'order': 2,
    },
    {
        'title_uz': "O'zbekiston davlat sport akademiyasi (PQ-197, 28.05.2024)",
        'title_ru': "Государственная спортивная академия Узбекистана (PQ-197, 28.05.2024)",
        'title_en': "Uzbekistan State Sports Academy (PQ-197, 28.05.2024)",
        'link': "",
        'order': 3,
    },
    {
        'title_uz': "2028-yil Los-Anjeles XXXIV Yozgi Olimpiya va XVIII Paralimpiya o'yinlari (PQ-221, 08.07.2025)",
        'title_ru': "XXXIV летние Олимпийские и XVIII Паралимпийские игры Лос-Анджелес 2028 (PQ-221, 08.07.2025)",
        'title_en': "2028 Los Angeles XXXIV Summer Olympic and XVIII Paralympic Games (PQ-221, 08.07.2025)",
        'link': "",
        'order': 4,
    },
]


class Command(BaseCommand):
    help = "Me'yoriy hujjatlarni bazaga qo'shadi (link orqali)"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        try:
            page = NavbarSubItem.objects.get(slug='academy-regulations')
        except NavbarSubItem.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "'academy-regulations' sahifasi topilmadi."
            ))
            return

        if options['clear']:
            MeyoriyHujjat.objects.filter(navbar_items=page).delete()
            self.stdout.write(self.style.WARNING("Eski me'yoriy hujjatlar o'chirildi."))

        created = updated = 0
        for data in FILES:
            obj, is_new = MeyoriyHujjat.objects.update_or_create(
                title_uz=data['title_uz'],
                defaults={
                    'title_ru':   data['title_ru'],
                    'title_en':   data['title_en'],
                    'link':       data['link'],
                    'block_type': 'file-list',
                    'order':      data['order'],
                    'is_active':  True,
                }
            )
            obj.navbar_items.add(page)
            label = '[+]' if is_new else '[~]'
            self.stdout.write(f"  {label} {data['title_uz'][:70]}")
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created} yangi, {updated} yangilandi."
        ))
