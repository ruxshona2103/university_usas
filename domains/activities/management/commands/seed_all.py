"""
python manage.py seed_all

Barcha activities ma'lumotlarini DB ga qo'shadi:
  - Sport stats (3 ta)
  - Sport yo'nalishlar (6 ta)
  - Sport tadbirlar (8 ta)
  - Sport faoliyat kategoriyalar + itemlar (3 sub + 9 item)
  - Ilmiy faoliyat kategoriyalar + itemlar (4 sub + 15 item)
  - Manaviy faoliyat kategoriyalar + itemlar (1 sub + 5 item)
  - Fake ru/en descriptions + image/file URLs (29 item)
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = "Barcha activities fake datalarini bir buyruq bilan DB ga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Avval mavjud barcha Sport* va faoliyat ma'lumotlarini o'chiradi",
        )

    def handle(self, *args, **options):
        clear = options['clear']

        steps = [
            ('seed_sport_section_data',    {'clear': clear}),
            ('seed_sport_faoliyat',        {'clear': clear}),
            ('seed_ilmiy_faoliyat_science',{'clear': clear}),
            ('seed_manaviy_faoliyat',      {'clear': clear}),
            ('seed_fake_data_complete',    {}),
        ]

        for cmd, kwargs in steps:
            self.stdout.write(self.style.MIGRATE_HEADING(f'\n>>> {cmd}'))
            call_command(cmd, **kwargs)

        self.stdout.write(self.style.SUCCESS('\nBarcha ma\'lumotlar muvaffaqiyatli qo\'shildi!'))
