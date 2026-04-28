"""
python manage.py seed_sport_faoliyat

Sport faoliyat uchun:
  - 1 ta root IlmiyFaoliyatCategory  (slug="sport-faoliyat")
  - 3 ta child  IlmiyFaoliyatCategory (kartochkalar)
  - Har bir kartochkada namunali IlmiyFaoliyat itemlar
"""

import uuid

from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

ROOT = {
    "id":       "a1b2c3d4-0001-0001-0001-000000000001",
    "slug":     "sport-faoliyat",
    "title_uz": "Sport faoliyat",
    "title_ru": "Спортивная деятельность",
    "title_en": "Sports Activity",
    "order":    1,
}

SUBCATEGORIES = [
    {
        "id":             "a1b2c3d4-0001-0001-0001-000000000011",
        "slug":           "sport-faoliyati",
        "title_uz":       "Sport faoliyati",
        "title_ru":       "Спортивная деятельность",
        "title_en":       "Sports Activities",
        "description_uz": "Akademiyada sport tadbirlari, musobaqalar va talabalarning jismoniy tarbiyasi.",
        "description_ru": "Спортивные мероприятия, соревнования и физическое воспитание студентов в академии.",
        "description_en": "Sports events, competitions and physical education of students in the academy.",
        "icon":           "trophy",
        "order":          1,
        "items": [
            {
                "title_uz": "2025-yil sport tadbirlari rejasi",
                "title_ru": "План спортивных мероприятий 2025 года",
                "title_en": "Sports Events Plan 2025",
                "description_uz": "Akademiyada o'tkaziladigan sport tadbirlarining yillik rejasi.",
                "order": 1,
            },
            {
                "title_uz": "Jismoniy tarbiya bo'yicha uslubiy qo'llanma",
                "title_ru": "Методическое пособие по физической культуре",
                "title_en": "Physical Education Methodological Guide",
                "description_uz": "Talabalar uchun jismoniy tarbiya darslari uslubiyati.",
                "order": 2,
            },
            {
                "title_uz": "Sport musobaqalari natijalari 2025",
                "title_ru": "Результаты спортивных соревнований 2025",
                "title_en": "Sports Competition Results 2025",
                "description_uz": "2025-yilgi barcha sport musobaqalarining yakuniy natijalari.",
                "order": 3,
            },
        ],
    },
    {
        "id":             "a1b2c3d4-0001-0001-0001-000000000012",
        "slug":           "sport-klublari-hayoti",
        "title_uz":       "Sport klublari hayoti",
        "title_ru":       "Жизнь спортивных клубов",
        "title_en":       "Sports Club Life",
        "description_uz": "Klublar faoliyati, tadbirlar va jamoatchilik hayoti.",
        "description_ru": "Деятельность клубов, мероприятия и общественная жизнь.",
        "description_en": "Club activities, events and community life.",
        "icon":           "dumbbell",
        "order":          2,
        "items": [
            {
                "title_uz": "Futbol klubi faoliyati hisoboti",
                "title_ru": "Отчёт о деятельности футбольного клуба",
                "title_en": "Football Club Activity Report",
                "description_uz": "Akademiya futbol jamoasining 2025-yilgi faoliyat hisoboti.",
                "order": 1,
            },
            {
                "title_uz": "Kurash va judo klublari",
                "title_ru": "Клубы борьбы и дзюдо",
                "title_en": "Wrestling and Judo Clubs",
                "description_uz": "Kurash va judo bo'yicha sport klublari faoliyati.",
                "order": 2,
            },
            {
                "title_uz": "Suzish bo'yicha musobaqalar",
                "title_ru": "Соревнования по плаванию",
                "title_en": "Swimming Competitions",
                "description_uz": "Suzish sport klubi va musobaqalar natijalari.",
                "order": 3,
            },
            {
                "title_uz": "Velosiped sport klubi",
                "title_ru": "Велосипедный спортивный клуб",
                "title_en": "Cycling Sports Club",
                "description_uz": "Velosiped sportchilar klubi va tayyorlov mashg'ulotlari.",
                "order": 4,
            },
        ],
    },
    {
        "id":             "a1b2c3d4-0001-0001-0001-000000000013",
        "slug":           "ekologik-faol-talabalar",
        "title_uz":       "Ekologik faol talabalar",
        "title_ru":       "Экологически активные студенты",
        "title_en":       "Ecologically Active Students",
        "description_uz": "Yashil sport va ekologik tashabbuslar.",
        "description_ru": "Зелёный спорт и экологические инициативы.",
        "description_en": "Green sports and ecological initiatives.",
        "icon":           "leaf",
        "order":          3,
        "items": [
            {
                "title_uz": "Yashil sport tashabbusi 2025",
                "title_ru": "Зелёная спортивная инициатива 2025",
                "title_en": "Green Sports Initiative 2025",
                "description_uz": "Ekologik tozalikka bag'ishlangan sport tadbirlari rejasi.",
                "order": 1,
            },
            {
                "title_uz": "Ko'kalamzorlashtirish loyihasi",
                "title_ru": "Проект озеленения",
                "title_en": "Greening Project",
                "description_uz": "Akademiya hududini ko'kalamzorlashtirish bo'yicha talabalar loyihasi.",
                "order": 2,
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Sport faoliyat kategoriyalari va namunali itemlarni DB ga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Avval sport-faoliyat slug bo'yicha mavjud categorylarni o'chiradi",
        )

    def handle(self, *args, **options):
        if options['clear']:
            IlmiyFaoliyatCategory.objects.filter(slug=ROOT['slug']).delete()
            self.stdout.write(self.style.WARNING("Mavjud sport-faoliyat ma'lumotlari o'chirildi."))

        root, created = IlmiyFaoliyatCategory.objects.update_or_create(
            slug=ROOT['slug'],
            defaults={
                'id':       uuid.UUID(ROOT['id']),
                'title_uz': ROOT['title_uz'],
                'title_ru': ROOT['title_ru'],
                'title_en': ROOT['title_en'],
                'parent':   None,
                'order':    ROOT['order'],
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

        self.stdout.write(self.style.SUCCESS("\nSport faoliyat ma'lumotlari muvaffaqiyatli qo'shildi!"))
