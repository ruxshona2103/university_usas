"""
python manage.py seed_xorijlik_professorlar
python manage.py seed_xorijlik_professorlar --clear
"""
from django.core.management.base import BaseCommand
from domains.international.models import XorijlikProfessor

DATA = [
    {
        'full_name':        'Xu Xianqyang',
        'country':          'Xitoy',
        'from_year':        2025,
        'bio_uz': (
            "2025-yildan Akademiyada Xorijiy mutaxassis lavozimida faoliyat olib boradi.\n"
            "2018-yil-xozirgi vaqtgacha Shandong sport universitetida badminton bo'yicha katta murabbiy "
            "va professional jismoniy tarbiya bo'yicha murabbiy"
        ),
        'bio_ru': (
            "С 2025 года работает в Академии в должности иностранного специалиста.\n"
            "С 2018 года по настоящее время — старший тренер по бадминтону и тренер по профессиональной "
            "физической культуре в Шаньдунском спортивном университете."
        ),
        'bio_en': (
            "Since 2025, working at the Academy as a Foreign Specialist.\n"
            "From 2018 to the present — Senior Badminton Coach and Professional Physical Education Coach "
            "at Shandong Sport University."
        ),
        'education_uz': (
            "2008-2012-yy. - Shangqi pedagogika universiteti (bakalavr)\n"
            "2013-2015-yy. - Shandong sport universiteti (magistr)"
        ),
        'education_ru': (
            "2008-2012 гг. — Шанцюйский педагогический университет (бакалавр)\n"
            "2013-2015 гг. — Шаньдунский спортивный университет (магистр)"
        ),
        'education_en': (
            "2008-2012 — Shangqiu Normal University (Bachelor)\n"
            "2013-2015 — Shandong Sport University (Master)"
        ),
        'specialty_uz':       "Sport faoliyati",
        'specialty_ru':       "Спортивная деятельность",
        'specialty_en':       "Sports activities",
        'academic_degree_uz': "Jismoniy tarbiya va sport fanlari",
        'academic_degree_ru': "Физическое воспитание и спортивные науки",
        'academic_degree_en': "Physical Education and Sports Sciences",
        'academic_title_uz':  "professor",
        'academic_title_ru':  "профессор",
        'academic_title_en':  "professor",
        'order': 1,
    },
]


class Command(BaseCommand):
    help = "Xorijlik professor-o'qituvchilar seed"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            XorijlikProfessor.objects.all().delete()
            self.stdout.write(self.style.WARNING("O'chirildi"))

        for item in DATA:
            obj, created = XorijlikProfessor.objects.update_or_create(
                full_name=item['full_name'],
                defaults=item,
            )
            self.stdout.write(self.style.SUCCESS(
                f"[{'+'if created else '~'}] {obj.full_name} ({obj.country})"
            ))
