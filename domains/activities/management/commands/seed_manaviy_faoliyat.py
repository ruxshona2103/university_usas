"""
python manage.py seed_manaviy_faoliyat

Ma'naviy-marifiy faoliyat uchun:
  - 1 ta root IlmiyFaoliyatCategory  (slug="manaviy-faoliyat")
  - 1 ta child  IlmiyFaoliyatCategory (kartochka)
  - Kartochkada namunali IlmiyFaoliyat itemlar
"""

import uuid

from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

ROOT = {
    "id":             "c3d4e5f6-0003-0003-0003-000000000003",
    "slug":           "manaviy-faoliyat",
    "title_uz":       "Ma'naviy-marifiy faoliyat",
    "title_ru":       "Духовно-просветительская деятельность",
    "title_en":       "Spiritual and Educational Activity",
    "description_uz": "Ma'naviyat va tarbiya bo'yicha rasmiy sahifa.",
    "description_ru": "Официальная страница по духовности и воспитанию.",
    "description_en": "Official page on spirituality and education.",
    "order":          4,
}

SUBCATEGORIES = [
    {
        "id":             "c3d4e5f6-0003-0003-0003-000000000031",
        "slug":           "manaviyat-rukni",
        "title_uz":       "Ma'naviyat rukni",
        "title_ru":       "Уголок духовности",
        "title_en":       "Spirituality Corner",
        "description_uz": "Ma'naviy-ma'rifiy tadbirlar va materiallar.",
        "description_ru": "Духовно-просветительские мероприятия и материалы.",
        "description_en": "Spiritual and educational events and materials.",
        "icon":           "heart",
        "order":          1,
        "items": [
            {
                "title_uz": "Milliy qadriyatlar va ma'naviyat dasturi",
                "title_ru": "Программа национальных ценностей и духовности",
                "title_en": "National Values and Spirituality Program",
                "description_uz": "Akademiya talabalarida milliy g'urur va ma'naviyatni shakllantirish dasturi.",
                "order": 1,
            },
            {
                "title_uz": "Ma'naviy-axloqiy tarbiya uslubiyati",
                "title_ru": "Методология духовно-нравственного воспитания",
                "title_en": "Spiritual and Moral Education Methodology",
                "description_uz": "Talabalar tarbiyasida qo'llaniladigan ma'naviy usullar to'plami.",
                "order": 2,
            },
            {
                "title_uz": "Vatanparvarlik tadbirlari rejasi 2025",
                "title_ru": "План патриотических мероприятий 2025",
                "title_en": "Patriotic Events Plan 2025",
                "description_uz": "2025-yil uchun rejalashtirilgan vatanparvarlik tadbirlari.",
                "order": 3,
            },
            {
                "title_uz": "Yoshlar bilan ishlash bo'yicha yo'riqnoma",
                "title_ru": "Руководство по работе с молодёжью",
                "title_en": "Youth Engagement Guide",
                "description_uz": "Yoshlar bilan ma'naviy ishlashning samarali yo'llari.",
                "order": 4,
            },
            {
                "title_uz": "Ma'naviy tadbirlar hisoboti 2024",
                "title_ru": "Отчёт о духовных мероприятиях 2024",
                "title_en": "Spiritual Events Report 2024",
                "description_uz": "2024-yilda o'tkazilgan barcha ma'naviy tadbirlarning yakuniy hisoboti.",
                "order": 5,
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Ma'naviy-marifiy faoliyat kategoriyasi va namunali itemlarni DB ga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Avval manaviy-faoliyat slug bo'yicha mavjud categorylarni o'chiradi",
        )

    def handle(self, *args, **options):
        if options['clear']:
            IlmiyFaoliyatCategory.objects.filter(slug=ROOT['slug']).delete()
            self.stdout.write(self.style.WARNING("Mavjud manaviy-faoliyat ma'lumotlari o'chirildi."))

        root, created = IlmiyFaoliyatCategory.objects.update_or_create(
            slug=ROOT['slug'],
            defaults={
                'id':             uuid.UUID(ROOT['id']),
                'title_uz':       ROOT['title_uz'],
                'title_ru':       ROOT['title_ru'],
                'title_en':       ROOT['title_en'],
                'description_uz': ROOT['description_uz'],
                'description_ru': ROOT['description_ru'],
                'description_en': ROOT['description_en'],
                'parent':         None,
                'order':          ROOT['order'],
            },
        )
        action = 'Yaratildi' if created else 'Yangilandi'
        self.stdout.write(f"[{action}] Root: {root.title_uz}")

        for sub_data in SUBCATEGORIES:
            sub, s_created = IlmiyFaoliyatCategory.objects.update_or_create(
                slug=sub_data['slug'],
                defaults={
                    'id':             uuid.UUID(sub_data['id']),
                    'title_uz':       sub_data['title_uz'],
                    'title_ru':       sub_data['title_ru'],
                    'title_en':       sub_data['title_en'],
                    'description_uz': sub_data['description_uz'],
                    'description_ru': sub_data['description_ru'],
                    'description_en': sub_data['description_en'],
                    'icon':           sub_data['icon'],
                    'parent':         root,
                    'order':          sub_data['order'],
                },
            )
            s_action = 'Yaratildi' if s_created else 'Yangilandi'
            self.stdout.write(f"  [{s_action}] Sub: {sub.title_uz}")

            for item_data in sub_data.get('items', []):
                item, i_created = IlmiyFaoliyat.objects.update_or_create(
                    category=sub,
                    order=item_data['order'],
                    defaults={
                        'title_uz':       item_data['title_uz'],
                        'title_ru':       item_data['title_ru'],
                        'title_en':       item_data['title_en'],
                        'description_uz': item_data.get('description_uz', ''),
                        'is_active':      True,
                    },
                )
                i_action = 'Yaratildi' if i_created else 'Yangilandi'
                self.stdout.write(f"    [{i_action}] Item: {item.title_uz}")

        self.stdout.write(self.style.SUCCESS("\nMa'naviy faoliyat ma'lumotlari muvaffaqiyatli qo'shildi!"))
