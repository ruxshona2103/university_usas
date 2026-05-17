"""
python manage.py seed_sport_faoliyat
python manage.py seed_sport_faoliyat --clear
"""

from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

ROOT_SLUG = "sport-faoliyat"

ROOT = {
    "slug":     ROOT_SLUG,
    "title_uz": "Sport faoliyat",
    "title_ru": "Спортивная деятельность",
    "title_en": "Sports Activity",
    "order":    1,
}

# Eski sluglar — --clear da tozalanadi
OLD_SLUGS = [
    "sport-faoliyati",
    "sport-klublari-hayoti",
    "ekologik-faol-talabalar",
]

SUBCATEGORIES = [
    {
        "slug":           "sport-activity-results",
        "title_uz":       "Sport natijalari",
        "title_ru":       "Спортивные результаты",
        "title_en":       "Sports results",
        "description_uz": "Talabalar va sportchilarning xalqaro va respublika musobaqalaridagi natijalari.",
        "description_ru": "Результаты студентов и спортсменов на международных и республиканских соревнованиях.",
        "description_en": "Results of students and athletes at international and national competitions.",
        "icon":           "trophy",
        "order":          1,
    },
    {
        "slug":           "sport-activity-calendar",
        "title_uz":       "Kutilayotgan sport tadbirlari va musobaqalari",
        "title_ru":       "Предстоящие спортивные мероприятия и соревнования",
        "title_en":       "Upcoming sports events and competitions",
        "description_uz": "Yil davomida rejalashtirilgan xalqaro va mahalliy sport musobaqalari taqvimi.",
        "description_ru": "Календарь запланированных международных и местных спортивных соревнований.",
        "description_en": "Calendar of planned international and local sports competitions.",
        "icon":           "calendar",
        "order":          2,
    },
]


class Command(BaseCommand):
    help = "Sport faoliyat kategoriyalarini DB ga qo'shadi (faqat 2 ta karta)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Barcha sport-faoliyat categoriyalarini o'chirib qayta yozadi",
        )

    def handle(self, *args, **options):
        if options['clear']:
            # Eski sluglarni to'g'ridan-to'g'ri o'chirish
            deleted_old = IlmiyFaoliyatCategory.objects.filter(slug__in=OLD_SLUGS).delete()
            # Root va uning cascade children larini o'chirish
            deleted_root = IlmiyFaoliyatCategory.objects.filter(slug=ROOT_SLUG).delete()
            # Yangi sluglar ham bo'lsa o'chirish (re-run uchun)
            IlmiyFaoliyatCategory.objects.filter(
                slug__in=[s['slug'] for s in SUBCATEGORIES]
            ).delete()
            self.stdout.write(self.style.WARNING(
                f"O'chirildi: eski={deleted_old[0]}, root+children={deleted_root[0]}"
            ))

        root, created = IlmiyFaoliyatCategory.objects.update_or_create(
            slug=ROOT['slug'],
            defaults={
                'title_uz': ROOT['title_uz'],
                'title_ru': ROOT['title_ru'],
                'title_en': ROOT['title_en'],
                'parent':   None,
                'order':    ROOT['order'],
            },
        )
        self.stdout.write(f"[{'Yaratildi' if created else 'Yangilandi'}] Root: {root.title_uz}")

        for sub_data in SUBCATEGORIES:
            sub, s_created = IlmiyFaoliyatCategory.objects.update_or_create(
                slug=sub_data['slug'],
                defaults={
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
            self.stdout.write(f"  [{'Yaratildi' if s_created else 'Yangilandi'}] {sub.title_uz}")

        self.stdout.write(self.style.SUCCESS("\nSport faoliyat muvaffaqiyatli yangilandi!"))
