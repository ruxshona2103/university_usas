"""
python manage.py seed_about_academy
python manage.py seed_about_academy --clear   # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand

from domains.pages.models import (
    AboutAcademy,
    AboutAcademySection,
    AboutAcademySectionItem,
    AboutAcademyProgram,
)


DESCRIPTION = {
    "uz": (
        "O'zbekiston davlat sport akademiyasi, O'zbekiston Respublikasi "
        "Prezidentining 2024-yil 28-maydagi \"O'zbekiston davlat sport akademiyasi "
        "faoliyatini tashkil qilish chora-tadbirlari to'g'risida\"gi PQ–197-son "
        "qaroriga muvofiq tashkil etilgan."
    ),
    "ru": (
        "Государственная спортивная академия Узбекистана создана в соответствии с "
        "постановлением Президента Республики Узбекистан от 28 мая 2024 года "
        "«О мерах по организации деятельности Государственной спортивной академии "
        "Узбекистана» №ПП–197."
    ),
    "en": (
        "The Uzbekistan State Sports Academy was established in accordance with "
        "the Decree of the President of the Republic of Uzbekistan dated May 28, 2024 "
        "\"On measures to organize the activities of the Uzbekistan State Sports Academy\" "
        "No. PP–197."
    ),
}

SECTIONS = [
    {
        "key": "goals",
        "order": 1,
        "title": {
            "uz": "Akademiyaning asosiy Maqsadi",
            "ru": "Основная цель Академии",
            "en": "Main Goals of the Academy",
        },
        "items": [
            {
                "uz": "Yuqori malakali sport mutaxassislari va kadrlarini zamon talablaridan kelib chiqib mutlaqo yangi sharoitlarda tayyorlash;",
                "ru": "Подготовка высококвалифицированных спортивных специалистов и кадров в принципиально новых условиях, отвечающих требованиям времени;",
                "en": "Training highly qualified sports specialists and personnel in fundamentally new conditions meeting the demands of the time;",
            },
            {
                "uz": "Yangi avlod sportchilari va trenerlarini yetishtirish orqali sportdagi yutuqlarimizni yanada kengaytirish;",
                "ru": "Расширение достижений в спорте путём воспитания спортсменов и тренеров нового поколения;",
                "en": "Expanding achievements in sports by nurturing a new generation of athletes and coaches;",
            },
            {
                "uz": "Jismoniy tarbiya va sport sohasida o'quv va ilmiy-tadqiqot jarayonini xalqaro standartlar asosida tashkil qilish.",
                "ru": "Организация учебного и научно-исследовательского процесса в сфере физической культуры и спорта на основе международных стандартов.",
                "en": "Organizing the educational and scientific research process in the field of physical education and sports based on international standards.",
            },
        ],
    },
    {
        "key": "tasks",
        "order": 2,
        "title": {
            "uz": "Akademiyaning asosiy Vazifalari",
            "ru": "Основные задачи Академии",
            "en": "Main Tasks of the Academy",
        },
        "items": [
            {
                "uz": "Sport sohasida natijalari yuqori bo'lgan davlatlarning yetakchi oliy sport-ta'lim tashkilotlari tajribasi asosida zamonaviy kadrlarni tayyorlash;",
                "ru": "Подготовка современных кадров на основе опыта ведущих высших спортивно-образовательных организаций государств с высокими результатами в спорте;",
                "en": "Training modern personnel based on the experience of leading higher sports education institutions of countries with high sporting achievements;",
            },
            {
                "uz": "Kadrlarni tayyorlash jarayoniga xorijiy tajribalarni qo'llagan holda o'quv jarayonini tashkil qilish hamda ilmiy asoslangan metodikalarini yaratish;",
                "ru": "Организация учебного процесса с применением зарубежного опыта в подготовке кадров и разработка научно обоснованных методик;",
                "en": "Organizing the educational process using international experience in personnel training and developing scientifically based methodologies;",
            },
            {
                "uz": "Sport sohasida kompleks ilmiy tadqiqotlar, eksperimentlar hamda laborator sinovlar tashkil etish;",
                "ru": "Организация комплексных научных исследований, экспериментов и лабораторных испытаний в сфере спорта;",
                "en": "Organizing comprehensive scientific research, experiments and laboratory tests in the field of sports;",
            },
            {
                "uz": "Jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirishning zamonaviy o'qitish mexanizmlarini joriy etish;",
                "ru": "Внедрение современных механизмов обучения по переподготовке и повышению квалификации специалистов в области физической культуры и спорта;",
                "en": "Introducing modern teaching mechanisms for retraining and advanced training of specialists in physical education and sports;",
            },
            {
                "uz": "Respublikada sport sohasida zamonaviy nazariya va amaliyot tizimini joriy qilish usullari hamda xususiyatlarini o'rganish orqali yuqori mahoratli sportchilarni tayyorlab borish;",
                "ru": "Подготовка высококвалифицированных спортсменов путём изучения методов и особенностей внедрения современной системы теории и практики в сфере спорта в республике;",
                "en": "Training highly skilled athletes by studying the methods and features of implementing a modern system of theory and practice in sports in the republic;",
            },
            {
                "uz": "Musobaqalar natijalarini chuqur ilmiy yondashuv asosida tahlil qilib borish, ular natijasida sportdagi yutuqlarni yanada kengaytirish bo'yicha tavsiyalar ishlab chiqish.",
                "ru": "Глубокий научный анализ результатов соревнований и разработка рекомендаций по дальнейшему расширению достижений в спорте.",
                "en": "In-depth scientific analysis of competition results and developing recommendations for further expanding achievements in sports.",
            },
        ],
    },
    {
        "key": "system",
        "order": 3,
        "title": {
            "uz": "Akademiya tizimiga kiruvchi tashkilotlar",
            "ru": "Организации, входящие в систему Академии",
            "en": "Organizations within the Academy System",
        },
        "items": [
            {
                "uz": "Jismoniy tarbiya va sport ilmiy tadqiqotlar instituti;",
                "ru": "Институт научных исследований в области физической культуры и спорта;",
                "en": "Institute of Scientific Research in Physical Education and Sports;",
            },
            {
                "uz": "Jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish instituti hamda uning tegishli filiallari;",
                "ru": "Институт переподготовки и повышения квалификации специалистов в области физической культуры и спорта и его соответствующие филиалы;",
                "en": "Institute for Retraining and Advanced Training of Specialists in Physical Education and Sports and its branches;",
            },
            {
                "uz": "Axborot-kutubxona markazini o'z ichiga oluvchi yuridik shaxs maqomiga ega bo'lmagan O'zbekiston tarixi va xorijiy tillarni o'qitish markazi;",
                "ru": "Центр обучения истории Узбекистана и иностранным языкам, включающий информационно-библиотечный центр, не имеющий статуса юридического лица;",
                "en": "Center for Teaching Uzbekistan History and Foreign Languages including the Information and Library Center, without the status of a legal entity;",
            },
            {
                "uz": "Davlat sport tibbiyoti ilmiy-amaliy markazi.",
                "ru": "Государственный научно-практический центр спортивной медицины.",
                "en": "State Scientific and Practical Center of Sports Medicine.",
            },
        ],
    },
    {
        "key": "international",
        "order": 4,
        "title": {
            "uz": "Xalqaro hamkorlik",
            "ru": "Международное сотрудничество",
            "en": "International Cooperation",
        },
        "items": [
            {
                "uz": "Italiyaning Trento universiteti bilan hamkorlik;",
                "ru": "Сотрудничество с Университетом Тренто (Италия);",
                "en": "Cooperation with the University of Trento (Italy);",
            },
            {
                "uz": "Vengriya sport fanlari universiteti bilan hamkorlik;",
                "ru": "Сотрудничество с Венгерским университетом спортивных наук;",
                "en": "Cooperation with the Hungarian University of Sports Sciences;",
            },
            {
                "uz": "Sankt-Peterburg P.F.Lesgaft nomidagi jismoniy tarbiya va sport milliy davlat instituti bilan hamkorlik;",
                "ru": "Сотрудничество с Национальным государственным институтом физической культуры и спорта им. П.Ф.Лесгафта (Санкт-Петербург);",
                "en": "Cooperation with the National State Institute of Physical Education and Sports named after P.F. Lesgaft (Saint-Petersburg);",
            },
            {
                "uz": "L.Gumilyov nomidagi Yevroosiyo milliy universiteti bilan hamkorlik;",
                "ru": "Сотрудничество с Евразийским национальным университетом им. Л.Гумилёва;",
                "en": "Cooperation with the L.Gumilyov Eurasian National University;",
            },
            {
                "uz": "Avstraliya sport instituti tajribasi asosida sport tayyorgarligi, ilmiy-tahliliy yondashuv va yuqori natijadorlikka erishish mexanizmlari o'rganilmoqda.",
                "ru": "На основе опыта Австралийского института спорта изучаются механизмы спортивной подготовки, научно-аналитического подхода и достижения высоких результатов.",
                "en": "Based on the experience of the Australian Institute of Sport, mechanisms for sports preparation, scientific-analytical approach and achieving high performance are being studied.",
            },
        ],
    },
]

PROGRAMS = [
    # ── BAKALAVRIAT ──────────────────────────────────────────────────────────
    {
        "program_type": "bachelor",
        "order": 1,
        "direction": {
            "uz": "Sport faoliyati (faoliyat turlari bo'yicha)",
            "ru": "Спортивная деятельность (по видам деятельности)",
            "en": "Sports Activity (by types of activity)",
        },
        "profession": {
            "uz": "Trener",
            "ru": "Тренер",
            "en": "Coach",
        },
    },
    {
        "program_type": "bachelor",
        "order": 2,
        "direction": {
            "uz": "Adaptiv jismoniy tarbiya va sport (parasport)",
            "ru": "Адаптивная физическая культура и спорт (параспорт)",
            "en": "Adaptive Physical Education and Sports (parasport)",
        },
        "profession": {
            "uz": "Trener",
            "ru": "Тренер",
            "en": "Coach",
        },
    },
    {
        "program_type": "bachelor",
        "order": 3,
        "direction": {
            "uz": "Sport menejmenti",
            "ru": "Спортивный менеджмент",
            "en": "Sports Management",
        },
        "profession": {
            "uz": "Sport menejeri va sport tahlilchisi",
            "ru": "Спортивный менеджер и спортивный аналитик",
            "en": "Sports Manager and Sports Analyst",
        },
    },
    # ── MAGISTRATURA ─────────────────────────────────────────────────────────
    {
        "program_type": "master",
        "order": 1,
        "direction": {
            "uz": "Sport faoliyati (faoliyat turlari bo'yicha)",
            "ru": "Спортивная деятельность (по видам деятельности)",
            "en": "Sports Activity (by types of activity)",
        },
        "profession": {
            "uz": "Trener, sport sohasida tashkiliy boshqaruv mutaxassisi",
            "ru": "Тренер, специалист по организационному управлению в сфере спорта",
            "en": "Coach, Specialist in Organizational Management in Sports",
        },
    },
    {
        "program_type": "master",
        "order": 2,
        "direction": {
            "uz": "Adaptiv jismoniy tarbiya va sport (parasport)",
            "ru": "Адаптивная физическая культура и спорт (параспорт)",
            "en": "Adaptive Physical Education and Sports (parasport)",
        },
        "profession": {
            "uz": "Trener, sport sohasida tashkiliy boshqaruv mutaxassisi",
            "ru": "Тренер, специалист по организационному управлению в сфере спорта",
            "en": "Coach, Specialist in Organizational Management in Sports",
        },
    },
    {
        "program_type": "master",
        "order": 3,
        "direction": {
            "uz": "Sport huquqi",
            "ru": "Спортивное право",
            "en": "Sports Law",
        },
        "profession": {
            "uz": "Sport huquqshunosi",
            "ru": "Спортивный юрист",
            "en": "Sports Lawyer",
        },
    },
    {
        "program_type": "master",
        "order": 4,
        "direction": {
            "uz": "Sport menejmenti",
            "ru": "Спортивный менеджмент",
            "en": "Sports Management",
        },
        "profession": {
            "uz": "Sport menejeri",
            "ru": "Спортивный менеджер",
            "en": "Sports Manager",
        },
    },
    {
        "program_type": "master",
        "order": 5,
        "direction": {
            "uz": "Sport marketingi",
            "ru": "Спортивный маркетинг",
            "en": "Sports Marketing",
        },
        "profession": {
            "uz": "Sport marketologi",
            "ru": "Спортивный маркетолог",
            "en": "Sports Marketer",
        },
    },
    {
        "program_type": "master",
        "order": 6,
        "direction": {
            "uz": "Sport psixologiyasi",
            "ru": "Спортивная психология",
            "en": "Sports Psychology",
        },
        "profession": {
            "uz": "Sport psixologi",
            "ru": "Спортивный психолог",
            "en": "Sports Psychologist",
        },
    },
]


class Command(BaseCommand):
    help = "Akademiya haqida sahifasi ma'lumotlarini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Mavjud ma'lumotlarni o'chirib qaytadan yozadi",
        )

    def handle(self, *args, **options):
        if options['clear']:
            AboutAcademySection.objects.all().delete()
            AboutAcademyProgram.objects.all().delete()
            self.stdout.write(self.style.WARNING("Eski ma'lumotlar o'chirildi."))

        # ── Singleton yaratish / yangilash ────────────────────────────────
        about, created = AboutAcademy.objects.update_or_create(
            pk=AboutAcademy.SINGLETON_PK,
            defaults={
                "description_uz": DESCRIPTION["uz"],
                "description_ru": DESCRIPTION["ru"],
                "description_en": DESCRIPTION["en"],
            },
        )
        action = "Yaratildi" if created else "Yangilandi"
        self.stdout.write(self.style.SUCCESS(f"[OK] AboutAcademy {action}"))

        # ── Bo'limlar ─────────────────────────────────────────────────────
        for sec_data in SECTIONS:
            section, _ = AboutAcademySection.objects.update_or_create(
                about=about,
                key=sec_data["key"],
                defaults={
                    "title_uz": sec_data["title"]["uz"],
                    "title_ru": sec_data["title"]["ru"],
                    "title_en": sec_data["title"]["en"],
                    "order":    sec_data["order"],
                },
            )
            # Eski elementlarni o'chirib yangilarini yozamiz
            section.items.all().delete()
            for i, item in enumerate(sec_data["items"], start=1):
                AboutAcademySectionItem.objects.create(
                    section=section,
                    text_uz=item["uz"],
                    text_ru=item["ru"],
                    text_en=item["en"],
                    order=i,
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f"  [OK] Bo'lim '{sec_data['key']}': {len(sec_data['items'])} element"
                )
            )

        # ── Ta'lim dasturlari ─────────────────────────────────────────────
        if not options['clear']:
            AboutAcademyProgram.objects.filter(about=about).delete()

        for prog in PROGRAMS:
            AboutAcademyProgram.objects.create(
                about=about,
                program_type=prog["program_type"],
                direction_uz=prog["direction"]["uz"],
                direction_ru=prog["direction"]["ru"],
                direction_en=prog["direction"]["en"],
                profession_uz=prog["profession"]["uz"],
                profession_ru=prog["profession"]["ru"],
                profession_en=prog["profession"]["en"],
                order=prog["order"],
            )

        bachelor_count = sum(1 for p in PROGRAMS if p["program_type"] == "bachelor")
        master_count   = sum(1 for p in PROGRAMS if p["program_type"] == "master")
        self.stdout.write(self.style.SUCCESS(
            f"  [OK] Ta'lim dasturlari: {bachelor_count} bakalavr, {master_count} magistr"
        ))

        self.stdout.write(self.style.SUCCESS(
            "\n=== seed_about_academy muvaffaqiyatli bajarildi ==="
        ))
