"""
IlmiyYonalish modeliga 'ilmiy-bolim' slug bilan yozuv qo'shadi.
Frontend /page/ilmiy-yonalishlar/ilmiy-bolim URL uchun.

Mazmun: Desktop/file/Ilmiy bolim.doc dan to'liq ma'lumot.
"Ilmiy tadqiqotlar, innovatsiyalar va ilmiy pedagogik kadrlar tayyorlash sektori"
"""
from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyYonalish, IlmiyYonalishItem


YONALISH = {
    "name_uz": "Ilmiy tadqiqotlar, innovatsiyalar va ilmiy pedagogik kadrlar tayyorlash sektori",
    "name_ru": "Сектор научных исследований, инноваций и подготовки научно-педагогических кадров",
    "name_en": "Sector of Scientific Research, Innovation and Training of Scientific-Pedagogical Personnel",
    "slug": "ilmiy-bolim",
    "order": 100,
}

ITEMS = [
    {
        "name_uz": "Sektor haqida",
        "name_ru": "О секторе",
        "name_en": "About the Sector",
        "description_uz": (
            "Manzil: Toshkent shahar, Yashnabod tumani, Olimpiya shaharchasi. "
            "Ish vaqti: Dushanba-Juma, 14:00-17:00. "
            "O'zbekiston davlat sport akademiyasi Ilmiy tadqiqotlar, innovatsiyalar va ilmiy pedagogik kadrlar tayyorlash sektori "
            "(bundan keyin – Sektor) Akademiyaning doimiy faoliyat yurituvchi tarkibiy bo'limi hisoblanadi. "
            "Sektor O'zbekiston Respublikasi Konstitutsiyasi va qonunlari, O'zbekiston Respublikasi Prezidentining Farmon, "
            "qaror va farmoyishlari, O'zbekiston Respublikasi Vazirlar Mahkamasining qaror va farmoyishlari, Sport vazirligi "
            "va Oliy ta'lim, fan va innovatsiyalar vazirligining Hay'at qarorlari va buyruqlari, Oliy ta'lim to'g'risidagi Nizom, "
            "O'zbekiston davlat sport akademiyasi Ustavi asosida faoliyat yuritadi."
        ),
        "description_ru": (
            "Адрес: г. Ташкент, Яшнабадский район, Олимпийский городок. "
            "Часы работы: Понедельник-Пятница, 14:00-17:00. "
            "Сектор научных исследований, инноваций и подготовки научно-педагогических кадров — постоянное структурное подразделение Академии."
        ),
        "description_en": (
            "Address: Tashkent city, Yashnabad district, Olympic town. "
            "Working hours: Monday-Friday, 14:00-17:00. "
            "Sector of Scientific Research, Innovation and Training of Scientific-Pedagogical Personnel — permanent structural division of the Academy."
        ),
        "order": 1,
    },
    {
        "name_uz": "Ilmiy tadqiqot ishlarining samaradorligi nazorati",
        "name_ru": "Контроль эффективности научно-исследовательских работ",
        "name_en": "Monitoring effectiveness of research work",
        "description_uz": "Akademiyada olib borilayotgan ilmiy tadqiqot ishlarining samaradorligi yuzasidan umumiy nazorat olib borish.",
        "description_ru": "Общий контроль за эффективностью научно-исследовательских работ, проводимых в Академии.",
        "description_en": "General supervision of the effectiveness of scientific research conducted at the Academy.",
        "order": 2,
    },
    {
        "name_uz": "Iqtidorli yoshlarni qidirish va Prezident stipendiyalari",
        "name_ru": "Поиск одарённой молодёжи и Президентские стипендии",
        "name_en": "Talent search and Presidential scholarships",
        "description_uz": (
            "Iqtidorli yoshlarni qidirish, saralash va ularga ko'maklashish, talabalar (nomli davlat stipendiyalari) "
            "orasidan O'zbekiston Respublikasi Prezidentining davlat stipendiyalari talabgorlarini tayyorlash jarayonida "
            "faol ishtirok etish."
        ),
        "description_ru": "Поиск, отбор одарённой молодёжи и подготовка кандидатов на государственные стипендии Президента.",
        "description_en": "Searching for and selecting talented youth and training candidates for Presidential state scholarships.",
        "order": 3,
    },
    {
        "name_uz": "Talabalar innovatsion g'oyalari va ilmiy faoliyati",
        "name_ru": "Инновационные идеи и научная деятельность студентов",
        "name_en": "Students' innovative ideas and scientific activity",
        "description_uz": (
            "Talabalarning innovatsion g'oyalari, ilmiy-tadqiqotlari va ijodiy faoliyatlari orqali fanni taraqqiy ettirish, "
            "olingan natijalardan ta'lim jarayonida foydalanish ishlariga ko'maklashish."
        ),
        "description_ru": "Развитие науки через инновационные идеи и научно-исследовательскую деятельность студентов.",
        "description_en": "Advancing science through students' innovative ideas and research activities.",
        "order": 4,
    },
    {
        "name_uz": "Talabalar ilmiy faoliyatini tashkil etish va nazorat",
        "name_ru": "Организация и контроль научной деятельности студентов",
        "name_en": "Organization and supervision of students' scientific activity",
        "description_uz": "Talabalarning ilmiy faoliyati va o'quv-tarbiyaviy jarayonini tashkil etish hamda nazorat qilish.",
        "description_ru": "Организация и контроль научной деятельности и учебно-воспитательного процесса студентов.",
        "description_en": "Organizing and monitoring students' scientific activity and educational process.",
        "order": 5,
    },
    {
        "name_uz": "Akademiyani ilmiy-uslubiy ta'minlash",
        "name_ru": "Научно-методическое обеспечение Академии",
        "name_en": "Scientific-methodological support of the Academy",
        "description_uz": "Akademiyani ilmiy-uslubiy ta'minlash va o'quv-uslubiy hujjatlarni ishlab chiqishda ko'maklashish.",
        "description_ru": "Научно-методическое обеспечение Академии и помощь в разработке учебно-методических документов.",
        "description_en": "Providing scientific-methodological support and assisting in the development of educational-methodological documents.",
        "order": 6,
    },
    {
        "name_uz": "Ilmiy va ilmiy-amaliy anjumanlar",
        "name_ru": "Научные и научно-практические конференции",
        "name_en": "Scientific and scientific-practical conferences",
        "description_uz": (
            "Ilmiy va ilmiy-amaliy anjumanlar o'tkazishni rejalashtirish va mazkur anjumanlarda pedagog xodimlar "
            "va talaba yoshlarning maqolalari bilan ishtirok etishini ta'minlash."
        ),
        "description_ru": "Планирование научных конференций и обеспечение участия профессорско-преподавательского состава и студентов.",
        "description_en": "Planning scientific conferences and ensuring participation of teaching staff and students with their papers.",
        "order": 7,
    },
    {
        "name_uz": "Ilmiy-tadqiqot ishlarini nazorat qilish",
        "name_ru": "Контроль научно-исследовательских работ",
        "name_en": "Supervision of research works",
        "description_uz": "Akademiya pedagog xodimlari tomonidan olib borilayotgan ilmiy, ilmiy-uslubiy va ilmiy tadqiqot ishlarini nazorat qilish.",
        "description_ru": "Контроль научных, научно-методических и научно-исследовательских работ преподавателей.",
        "description_en": "Monitoring scientific, scientific-methodological and research works carried out by Academy teaching staff.",
        "order": 8,
    },
    {
        "name_uz": "Iqtidorli talabalar bilan ishlash",
        "name_ru": "Работа с одарёнными студентами",
        "name_en": "Working with talented students",
        "description_uz": (
            "Ilmiy-tadqiqot faoliyati bilan shug'ullanishga xohishi va qobiliyati bo'lgan iqtidorli talabalarni aniqlash, "
            "ularni ilmiy-tadqiqotlarga jalb etish, ilmiy-tadqiqot ishlarini individual va jamoa bo'lib bajarishga o'rgatish "
            "orqali ularning ilmiy-ijodiy qobiliyatlarini ro'yobga chiqarish uchun tashkiliy, metodik va moddiy-texnikaviy "
            "shart-sharoitlar yaratish."
        ),
        "description_ru": "Выявление одарённых студентов, привлечение их к научным исследованиям, создание организационных и материально-технических условий.",
        "description_en": "Identifying talented students, engaging them in research, creating organizational and material-technical conditions.",
        "order": 9,
    },
    {
        "name_uz": "Talabalar ilmiy ijodini rivojlantirish",
        "name_ru": "Развитие научного творчества студентов",
        "name_en": "Developing students' scientific creativity",
        "description_uz": (
            "Ilmiy-tadqiqot ishlarida talabalarning keng ishtirokini ta'minlash, yoshlarga turli shakldagi "
            "ilmiy ijodini rivojlantirishning samarali mexanizmlarini yaratish."
        ),
        "description_ru": "Обеспечение широкого участия студентов в научных исследованиях и развитие механизмов их научного творчества.",
        "description_en": "Ensuring broad student participation in research and developing mechanisms for their scientific creativity.",
        "order": 10,
    },
    {
        "name_uz": "Laboratoriyalar, markazlar va ilmiy to'garaklar",
        "name_ru": "Лаборатории, центры и научные кружки",
        "name_en": "Laboratories, centers and scientific clubs",
        "description_uz": (
            "Kafedralar va fakultetlarda talabalarning ilmiy-ijodiy qobiliyatlarini rivojlantirish va ro'yobga chiqarish "
            "imkonini beruvchi o'quv-ilmiy laboratoriyalar, markazlar, turli ilmiy-ijodiy to'garaklarni faoliyatini yaxshilash, "
            "yangi zamonaviy jihozlar bilan jihozlash bo'yicha Akademiya rahbariyatiga takliflar kiritish."
        ),
        "description_ru": "Улучшение работы учебно-научных лабораторий, центров и научных кружков на кафедрах и факультетах.",
        "description_en": "Improving the work of educational-scientific laboratories, centers and scientific clubs at departments and faculties.",
        "order": 11,
    },
    {
        "name_uz": "O'quv mashg'ulotlari va ilmiy tadqiqot integratsiyasi",
        "name_ru": "Интеграция учебных занятий и научных исследований",
        "name_en": "Integration of academic studies and research",
        "description_uz": (
            "Talabalarning o'quv mashg'ulotlari va ilmiy-tadqiqot ishlari integratsiyasini ta'minlash, mustaqil ish, "
            "kurs loyihasi, malakaviy bitiruv ishi doirasida turli xildagi faol o'quv-tadqiqot jarayonlarini tashkil etish."
        ),
        "description_ru": "Обеспечение интеграции учебных занятий и научно-исследовательской работы студентов.",
        "description_en": "Ensuring integration of students' academic studies and research work.",
        "order": 12,
    },
]


class Command(BaseCommand):
    help = "IlmiyYonalish'ga 'ilmiy-bolim' slug bilan to'liq mazmun qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Avval o'chirib qayta yozish")

    def handle(self, *args, **options):
        clear = options.get("clear", False)

        yonalish, created = IlmiyYonalish.objects.update_or_create(
            slug=YONALISH["slug"],
            defaults={
                "name_uz": YONALISH["name_uz"],
                "name_ru": YONALISH["name_ru"],
                "name_en": YONALISH["name_en"],
                "order": YONALISH["order"],
                "is_active": True,
            },
        )
        self.stdout.write(self.style.SUCCESS(
            f"Yo'nalish: {yonalish.name_uz[:60]}... ({'yaratildi' if created else 'yangilandi'})"
        ))

        if clear:
            yonalish.items.all().delete()
            self.stdout.write(self.style.WARNING("Eski items o'chirildi"))

        for item in ITEMS:
            obj, created = IlmiyYonalishItem.objects.update_or_create(
                yonalish=yonalish,
                name_uz=item["name_uz"],
                defaults={
                    "name_ru": item["name_ru"],
                    "name_en": item["name_en"],
                    "description_uz": item["description_uz"],
                    "description_ru": item["description_ru"],
                    "description_en": item["description_en"],
                    "order": item["order"],
                    "is_active": True,
                },
            )
            mark = "+" if created else "~"
            self.stdout.write(self.style.SUCCESS(f"  {mark} {obj.name_uz[:60]}"))

        self.stdout.write(self.style.SUCCESS(f"\nJami: {len(ITEMS)} ta items"))
        self.stdout.write(
            f"URL: /page/ilmiy-yonalishlar/{yonalish.slug}\n"
            f"API: /api/ilmiy-yonalishlar/{yonalish.slug}/?lang=uz"
        )
