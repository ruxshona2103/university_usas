"""
python manage.py seed_all           # hamma seedlarni ishlatadi
python manage.py seed_all --clear   # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


# Tartib muhim: bog'liq seedlar keyinroq keladi
COMMANDS = [
    # ── Sahifalar va navigatsiya ────────────────────────────────────────
    ('seed_navbar',        {}),
    ('seed_org_structure', {}),   # tashkiliy tuzilma
    ('seed_page_content',  {}),
    ('seed_rekvizit',      {}),   # tashkilot rekvizitlari
    ('seed_about_academy', {}),   # akademiya haqida sahifasi

    # ── Akademik ma'lumotlar ────────────────────────────────────────────
    ('seed_academy_stats', {}),
    ('seed_kafedra',       {}),

    # ── Shaxslar ───────────────────────────────────────────────────────
    ('seed_rektorat',      {}),
    ('seed_axborot',       {}),   # axborot xizmati xodimlari + vazifalar

    # ── Talaba ma'lumotlari ─────────────────────────────────────────────
    ('seed_student_info',  {}),
    ('seed_stipendiya',    {}),   # stipendiya jadvali

    # ── Faoliyat va tadbirlar ───────────────────────────────────────────
    ('seed_oquv_faoliyat', {}),
    ('seed_events',        {}),

    # ── Infratuzilma ───────────────────────────────────────────────────
    ('seed_velodrom',      {}),   # velodrom pasporti
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

        self.stdout.write(self.style.WARNING("\n=== SEED ALL BOSHLANDI ===\n"))

        ok_count   = 0
        fail_count = 0

        for cmd, kwargs in COMMANDS:
            self.stdout.write(self.style.HTTP_INFO(f"\n--- {cmd} ---"))
            try:
                if clear:
                    kwargs = {**kwargs, 'clear': True}
                call_command(cmd, **kwargs)
                self.stdout.write(self.style.SUCCESS(f"[OK] {cmd}"))
                ok_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"[XATO] {cmd}: {e}"))
                fail_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n=== SEED ALL TUGADI: {ok_count} muvaffaqiyatli"
            + (f", {fail_count} xato" if fail_count else "") + " ==="
        ))
