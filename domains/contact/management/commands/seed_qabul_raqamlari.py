"""
python manage.py seed_qabul_raqamlari
python manage.py seed_qabul_raqamlari --clear
"""
from django.core.management.base import BaseCommand
from domains.contact.models import QabulRaqami

DATA = [
    {"order": 1, "label_uz": "Rektor qabul raqami",          "label_ru": "Телефон приёмной ректора",          "label_en": "Rector's reception",          "number": "+998 71 236 60 40"},
    {"order": 2, "label_uz": "Ishonch telefoni",              "label_ru": "Телефон доверия",                   "label_en": "Hotline",                      "number": "+998 71 236 60 41"},
    {"order": 3, "label_uz": "Qabul bo'limi",                 "label_ru": "Приёмная комиссия",                 "label_en": "Admissions office",            "number": "+998 71 236 60 42"},
    {"order": 4, "label_uz": "Axborot xizmati",               "label_ru": "Информационная служба",             "label_en": "Information service",          "number": "+998 71 236 60 43"},
    {"order": 5, "label_uz": "Xalqaro hamkorlik bo'limi",     "label_ru": "Отдел международного сотрудничества","label_en": "International cooperation dept","number": "+998 71 236 60 44"},
]


class Command(BaseCommand):
    help = "Qabul raqamlarini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            n = QabulRaqami.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta"))

        for d in DATA:
            obj, created = QabulRaqami.objects.update_or_create(
                number=d['number'],
                defaults={**d, 'is_active': True},
            )
            self.stdout.write(f"  [{'+'if created else '~'}] {obj.label_uz} — {obj.number}")

        self.stdout.write(self.style.SUCCESS("Tayyor!"))
