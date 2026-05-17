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
        "id":             "a1b2c3d4-0001-0001-0001-000000000012",
        "slug":           "sport-activity-results",
        "title_uz":       "Sport natijalari",
        "title_ru":       "Спортивные результаты",
        "title_en":       "Sports results",
        "description_uz": "Talabalar va sportchilarning xalqaro va respublika musobaqalaridagi natijalari.",
        "description_ru": "Результаты студентов и спортсменов на международных и республиканских соревнованиях.",
        "description_en": "Results of students and athletes at international and national competitions.",
        "icon":           "trophy",
        "order":          1,
        "items": [],
    },
    {
        "id":             "a1b2c3d4-0001-0001-0001-000000000013",
        "slug":           "sport-activity-calendar",
        "title_uz":       "Kutilayotgan sport tadbirlari va musobaqalari",
        "title_ru":       "Предстоящие спортивные мероприятия и соревнования",
        "title_en":       "Upcoming sports events and competitions",
        "description_uz": "Yil davomida rejalashtirilgan xalqaro va mahalliy sport musobaqalari taqvimi.",
        "description_ru": "Календарь запланированных международных и местных спортивных соревнований.",
        "description_en": "Calendar of planned international and local sports competitions.",
        "icon":           "calendar",
        "order":          2,
        "items": [],
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
