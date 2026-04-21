"""
python manage.py seed_academy_stats          # yaratadi / yangilaydi
python manage.py seed_academy_stats --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.academic.models import AcademyStat

# (order, label_uz, label_ru, label_en, value_uz, value_ru, value_en)
STATS = [
    (
        1,
        "Fakultetlar soni",
        "Количество факультетов",
        "Number of Faculties",
        "1 ta — «Sport va parasport turlari fakulteti»",
        "1 — «Факультет спортивных и параспортивных видов»",
        "1 — «Faculty of Sports and Para-sports»",
    ),
    (
        2,
        "Kafedralar soni",
        "Количество кафедр",
        "Number of Departments",
        "2 ta: «Yakkakurash va suv sport turlari» hamda «Parasport va umumkasbiy fanlar»",
        "2: кафедра «Единоборства и водные виды спорта» и кафедра «Параспорт и общепрофессиональные дисциплины»",
        "2: «Combat Sports & Aquatics» and «Para-sports & General Professional Disciplines»",
    ),
    (
        3,
        "Ta'lim yo'nalishlari soni",
        "Количество направлений обучения",
        "Number of Study Directions",
        "2 ta ta'lim yo'nalishi negizida 14 ta sport turi va 4 ta magistratura mutaxassisligi",
        "На базе 2 направлений — 14 видов спорта и 4 специальности магистратуры",
        "2 directions covering 14 sports types and 4 master's specialisations",
    ),
    (
        4,
        "Professor-o'qituvchilar soni",
        "Количество профессорско-преподавательского состава",
        "Number of Academic Staff",
        "31 nafar: 13 nafar asosiy, 4 nafar ichki o'rindosh, 14 nafar tashqi o'rindosh",
        "31 человек: 13 штатных, 4 внутренних совместителя, 14 внешних совместителей",
        "31 staff: 13 full-time, 4 internal part-time, 14 external part-time",
    ),
    (
        5,
        "Talabalar soni",
        "Количество студентов",
        "Number of Students",
        "159 nafar: 146 nafar bakalavriat, 13 nafar magistratura (2026-yil 2-aprel holatiga ko'ra)",
        "159 студентов: 146 — бакалавриат, 13 — магистратура (по состоянию на 2 апреля 2026 г.)",
        "159 students: 146 bachelor's, 13 master's (as of 2 April 2026)",
    ),
    (
        6,
        "O'quv binolari va auditoriyalar soni",
        "Учебные корпуса и аудитории",
        "Buildings and Classrooms",
        "1 ta o'quv binosi, 22 ta o'quv auditoriyasi, umumiy sig'im — 900 o'rin",
        "1 учебный корпус, 22 аудитории, общая вместимость — 900 мест",
        "1 building, 22 classrooms, total capacity — 900 seats",
    ),
    (
        7,
        "Qo'shma dasturlar soni",
        "Количество совместных программ",
        "Number of Joint Programmes",
        "Hozirda qo'shma dasturlar mavjud emas",
        "Совместных программ на данный момент нет",
        "No joint programmes at present",
    ),
    (
        8,
        "O'quv-uslubiy adabiyotlar fondi",
        "Фонд учебно-методической литературы",
        "Educational Resource Fund",
        "546 nomdagi 8 260 dona: 3 752 dona darslik, 3 474 dona o'quv qo'llanma, 440 dona monografiya, 105 dona badiiy adabiyot, 489 dona boshqa adabiyot",
        "8 260 экземпляров 546 наименований: 3 752 учебника, 3 474 учебных пособия, 440 монографий, 105 художественных изданий, 489 прочих изданий",
        "8,260 copies of 546 titles: 3,752 textbooks, 3,474 study guides, 440 monographs, 105 fiction, 489 other",
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
