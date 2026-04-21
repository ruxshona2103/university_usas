"""
python manage.py seed_academy_stats          # yaratadi / yangilaydi
python manage.py seed_academy_stats --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.academic.models import AcademyStat

# (order, label_uz, label_ru, label_en, value_uz, value_ru, value_en)
STATS = [
    # (order, label_uz, label_ru, label_en, value_uz, value_ru, value_en)
    (
        1,
        "Fakultetlar soni",
        "Количество факультетов",
        "Number of Faculties",
        "1 ta",
        "1",
        "1",
    ),
    (
        2,
        "Kafedralar soni",
        "Количество кафедр",
        "Number of Departments",
        "2 ta",
        "2",
        "2",
    ),
    (
        3,
        "Ta'lim yo'nalishlari soni",
        "Количество направлений обучения",
        "Number of Study Directions",
        "2 ta (14 ta sport turi va 4 ta magistratura mutaxassisligi)",
        "2 (14 видов спорта и 4 специальности магистратуры)",
        "2 (14 sports types and 4 master's specialisations)",
    ),
    (
        4,
        "Professor-o'qituvchilar soni",
        "Количество ППС",
        "Number of Academic Staff",
        "31 nafar",
        "31 человек",
        "31",
    ),
    (
        5,
        "Talabalar soni",
        "Количество студентов",
        "Number of Students",
        "159 nafar (2026-yil 2-aprel holatiga ko'ra)",
        "159 человек (по состоянию на 2 апреля 2026 г.)",
        "159 (as of 2 April 2026)",
    ),
    (
        6,
        "O'quv binolari soni",
        "Количество учебных корпусов",
        "Number of Buildings",
        "1 ta",
        "1",
        "1",
    ),
    (
        7,
        "Auditoriyalar soni",
        "Количество аудиторий",
        "Number of Classrooms",
        "22 ta (umumiy sig'im 900 o'rin)",
        "22 (общая вместимость 900 мест)",
        "22 (total capacity 900 seats)",
    ),
    (
        8,
        "Qo'shma dasturlar soni",
        "Количество совместных программ",
        "Number of Joint Programmes",
        "Mavjud emas",
        "Нет",
        "None",
    ),
    (
        9,
        "O'quv-uslubiy adabiyotlar fondi",
        "Фонд учебно-методической литературы",
        "Educational Resource Fund",
        "8 260 dona (546 nom)",
        "8 260 экземпляров (546 наименований)",
        "8,260 copies (546 titles)",
    ),
]


class Command(BaseCommand):
    help = "AcademyStat jadvalini to'ldiradi (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib, qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = AcademyStat.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        created = updated = 0
        for order, lbl_uz, lbl_ru, lbl_en, val_uz, val_ru, val_en in STATS:
            _, is_new = AcademyStat.objects.update_or_create(
                order=order,
                defaults=dict(
                    label_uz=lbl_uz, label_ru=lbl_ru, label_en=lbl_en,
                    value_uz=val_uz, value_ru=val_ru, value_en=val_en,
                    is_active=True,
                ),
            )
            if is_new:
                created += 1
            else:
                updated += 1
            self.stdout.write(f"  {'[+]' if is_new else '[~]'} {lbl_uz}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created} yangi, {updated} yangilandi. Jami {len(STATS)} ta ko'rsatkich."
        ))
