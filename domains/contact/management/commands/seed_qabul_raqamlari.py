"""
python manage.py seed_qabul_raqamlari
python manage.py seed_qabul_raqamlari --clear
"""
from django.core.management.base import BaseCommand
from domains.contact.models import QabulRaqami

NUMBER = "+998 71 236 60 40"


class Command(BaseCommand):
    help = "Qabul raqamini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            QabulRaqami.objects.all().delete()
            self.stdout.write(self.style.WARNING("O'chirildi"))

        obj, created = QabulRaqami.objects.update_or_create(
            number=NUMBER,
            defaults={'is_active': True},
        )
        self.stdout.write(self.style.SUCCESS(f"[{'+'if created else '~'}] {obj.number}"))
