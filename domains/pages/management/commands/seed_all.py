"""
python manage.py seed_all           # hamma seedlarni ishlatadi
python manage.py seed_all --clear   # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


COMMANDS = [
    # (command_name, extra_kwargs)
    ('seed_navbar',        {}),
    ('seed_page_content',  {}),
    ('seed_academy_stats', {}),
    ('seed_rektorat',      {}),
    ('seed_student_info',  {}),
    ('seed_oquv_faoliyat', {}),
]


class Command(BaseCommand):
    help = "Barcha seed commandlarni ketma-ket ishlatadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Mavjud ma'lumotlarni o'chirib qaytadan yozadi",
        )

    def handle(self, *args, **options):
        clear = options['clear']

        self.stdout.write(self.style.WARNING(
            "\n=== SEED ALL BOSHLANDI ===\n"
        ))

        for cmd, kwargs in COMMANDS:
            self.stdout.write(self.style.HTTP_INFO(f"\n--- {cmd} ---"))
            try:
                if clear:
                    kwargs['clear'] = True
                call_command(cmd, **kwargs)
                self.stdout.write(self.style.SUCCESS(f"[OK] {cmd}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[XATO] {cmd}: {e}"))

        self.stdout.write(self.style.SUCCESS(
            "\n=== SEED ALL TUGADI ===\n"
        ))
