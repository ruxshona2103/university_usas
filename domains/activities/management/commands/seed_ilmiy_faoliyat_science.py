"""
python manage.py seed_ilmiy_faoliyat_science
python manage.py seed_ilmiy_faoliyat_science --clear
"""

from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

ROOT_SLUG = "ilmiy-faoliyat"

ROOT = {
    "slug":     ROOT_SLUG,
    "title_uz": "Ilmiy faoliyat",
    "title_ru": "Научная деятельность",
    "title_en": "Scientific Activity",
    "order":    2,
}

SUBCATEGORIES = [
    {
        "slug":           "ilmiy-loyihalar",
        "title_uz":       "Ilmiy loyihalar",
        "title_ru":       "Научные проекты",
        "title_en":       "Scientific Projects",
        "description_uz": "Amalga oshirilayotgan va rejalashtirilgan ilmiy loyihalar.",
        "description_ru": "Реализуемые и планируемые научные проекты.",
        "description_en": "Ongoing and planned scientific projects.",
        "icon":           "flask-conical",
        "order":          1,
        "items": [],
    },
    {
        "slug":           "doktorantura",
        "title_uz":       "Doktorantura",
        "title_ru":       "Докторантура",
        "title_en":       "Doctoral Studies",
        "description_uz": "Doktorantura bo'yicha yo'riqnomalar va ma'lumotlar.",
        "description_ru": "Руководства и информация по докторантуре.",
        "description_en": "Guidance and information on doctoral studies.",
        "icon":           "graduation-cap",
        "order":          2,
        "items": [],
    },
    {
        "slug":           "ilmiy-konferensiyalar",
        "title_uz":       "Ilmiy konferensiyalar",
        "title_ru":       "Научные конференции",
        "title_en":       "Scientific Conferences",
        "description_uz": "Konferensiyalar, tezislar va ilmiy tadbirlar.",
        "description_ru": "Конференции, тезисы и научные мероприятия.",
        "description_en": "Conferences, theses and scientific events.",
        "icon":           "calendar-days",
        "order":          3,
        "items": [],
    },
    {
        "slug":           "ilmiy-ishlar-va-innovatsiyalar",
        "title_uz":       "Ilmiy ishlar va innovatsiyalar",
        "title_ru":       "Научные работы и инновации",
        "title_en":       "Scientific Works and Innovations",
        "description_uz": "Tadqiqot natijalari va innovatsion loyihalar.",
        "description_ru": "Результаты исследований и инновационные проекты.",
        "description_en": "Research results and innovative projects.",
        "icon":           "lightbulb",
        "order":          4,
        "items": [],
    },
    {
        "slug":           "gifted-students",
        "title_uz":       "Iqtidorli talabalar bilan ishlash bo'limi",
        "title_ru":       "Отдел работы с одарёнными студентами",
        "title_en":       "Department for Working with Gifted Students",
        "description_uz": "Iqtidorli talabalarni ilmiy faoliyatga jalb etish, olimpiada va tanlovlarga tayyorlash.",
        "description_ru": "Привлечение одарённых студентов к научной деятельности, подготовка к олимпиадам и конкурсам.",
        "description_en": "Engaging gifted students in research, preparing them for olympiads and competitions.",
        "icon":           "lightbulb",
        "order":          5,
        "items": [],
    },
]


class Command(BaseCommand):
    help = "Ilmiy faoliyat kategoriyalarini DB ga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Barcha ilmiy-faoliyat kategoriyalarini o'chirib qayta yozadi",
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted_subs = IlmiyFaoliyatCategory.objects.filter(
                slug__in=[s['slug'] for s in SUBCATEGORIES]
            ).delete()
            deleted_root = IlmiyFaoliyatCategory.objects.filter(slug=ROOT_SLUG).delete()
            self.stdout.write(self.style.WARNING(
                f"O'chirildi: sub={deleted_subs[0]}, root={deleted_root[0]}"
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

        self.stdout.write(self.style.SUCCESS("\nIlmiy faoliyat muvaffaqiyatli yangilandi!"))
