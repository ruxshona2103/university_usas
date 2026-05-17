"""
python manage.py seed_iqtidorli          # yaratadi / yangilaydi
python manage.py seed_iqtidorli --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand

from domains.pages.models.iqtidorli_talabalar import IqtidorliTalabalar, IqtidorliVazifa


BOSHLIQ = {
    "boshliq_lavozim_uz": "Sektor boshlig'i",
    "boshliq_lavozim_ru": "Руководитель сектора",
    "boshliq_lavozim_en": "Sector Head",
    "boshliq_fio_uz": "Azimova Nilufar Alisherovna",
    "boshliq_fio_ru": "Азимова Нилуфар Алишеровна",
    "boshliq_fio_en": "Azimova Nilufar Alisherovna",
    "qabul_kunlari_uz": "Dushanba-Juma 9:00-17:00",
    "qabul_kunlari_ru": "Понедельник–Пятница 9:00–17:00",
    "qabul_kunlari_en": "Monday–Friday 9:00–17:00",
    "telefon": "+998900540311",
    "email": "nazimova0311@gmail.com",
    "bolim_title_uz": "Bo'lim vazifalari:",
    "bolim_title_ru": "Задачи отдела:",
    "bolim_title_en": "Department tasks:",
}

VAZIFALAR = [
    {
        "order": 1,
        "text_uz": "Iqtidorli talabalarni izlash va aniqlashni tashkil etish;",
        "text_ru": "Организация поиска и выявления одарённых студентов;",
        "text_en": "Organizing the search and identification of gifted students;",
    },
    {
        "order": 2,
        "text_uz": "Iqtidorli talabalarni intellektual salohiyatini aniqlab borish;",
        "text_ru": "Определение интеллектуального потенциала одарённых студентов;",
        "text_en": "Identifying the intellectual potential of gifted students;",
    },
    {
        "order": 3,
        "text_uz": "Iqtidorli talabalarni qobiliyati va qanday yo'nalishga moyilligiga qarab maqsadli tayyorlashni tashkil etish;",
        "text_ru": "Организация целевой подготовки одарённых студентов в соответствии с их способностями и склонностями;",
        "text_en": "Organizing targeted training of gifted students according to their abilities and inclinations;",
    },
    {
        "order": 4,
        "text_uz": "Iqtidorli talabalar uchun O'zbekiston tarixi, chet tili, axborot texnologiyalari va internetdan foydalanish bo'yicha maxsus mashg'ulotlarni tashkil etishni nazorat qilish;",
        "text_ru": "Контроль за организацией специальных занятий для одарённых студентов по истории Узбекистана, иностранным языкам, информационным технологиям и использованию интернета;",
        "text_en": "Supervising the organisation of special classes for gifted students on the history of Uzbekistan, foreign languages, information technology and internet use;",
    },
    {
        "order": 5,
        "text_uz": "Iqtidorli talabalarni ilmiy va amaliy anjumanlarga, Respublika va xalqaro konferensiya, simpozium, olimpiada va tanlovlarda qatnashishlarini tashkil etish;",
        "text_ru": "Организация участия одарённых студентов в научных и практических конференциях, республиканских и международных конференциях, симпозиумах, олимпиадах и конкурсах;",
        "text_en": "Organising the participation of gifted students in scientific and practical conferences, republican and international conferences, symposia, olympiads and competitions;",
    },
    {
        "order": 6,
        "text_uz": "Iqtidorli talabalar orasidan O'zbekiston Respublikasi Prezidentining Davlat stipendiyasi va nomli Davlat stipendiyalariga, fan olimpiadalariga nomzodlarni tayyorlash, ularning sovrindor bo'lishiga erishish;",
        "text_ru": "Подготовка кандидатов из числа одарённых студентов на Государственную стипендию Президента Республики Узбекистан, именные государственные стипендии и олимпиады по наукам, достижение призовых мест;",
        "text_en": "Preparing candidates from gifted students for the State Scholarship of the President of the Republic of Uzbekistan, named state scholarships and subject olympiads, achieving prize places;",
    },
    {
        "order": 7,
        "text_uz": "Reytingi yuqori iqtidorli talabalar va ularning rahbarlarini moddiy va ma'naviy qo'llab-quvvatlash bo'yicha rahbariyatga takliflar berish;",
        "text_ru": "Внесение предложений руководству по материальной и моральной поддержке высокорейтинговых одарённых студентов и их руководителей;",
        "text_en": "Making proposals to management on material and moral support for highly rated gifted students and their supervisors;",
    },
    {
        "order": 8,
        "text_uz": "Iqtidorli talabalarni ilm-fan namoyondalari, Akademiya rahbarlari, tajribali professor-o'qituvchilar bilan davra suhbatlarini tashkil etish;",
        "text_ru": "Организация круглых столов одарённых студентов с представителями науки, руководством Академии и опытными профессорами;",
        "text_en": "Organising round-table discussions of gifted students with scientists, Academy leadership and experienced professors;",
    },
    {
        "order": 9,
        "text_uz": "Xorijiy tillar bo'yicha to'garaklar tashkil etish va nazorat qilish;",
        "text_ru": "Организация и контроль кружков по иностранным языкам;",
        "text_en": "Organising and supervising foreign language clubs;",
    },
    {
        "order": 10,
        "text_uz": "Talabalar uchun dastlabki kurslardanoq ilmiy-nazariy seminarlar tashkil etish;",
        "text_ru": "Организация научно-теоретических семинаров для студентов с первых курсов;",
        "text_en": "Organising scientific-theoretical seminars for students from the first courses;",
    },
    {
        "order": 11,
        "text_uz": "Iqtidorli yoshlarni ilmiy ishlarini hududiy va xalqaro jurnallarda chop etishda amaliy yordam ko'rsatish;",
        "text_ru": "Оказание практической помощи одарённой молодёжи в публикации научных работ в региональных и международных журналах;",
        "text_en": "Providing practical assistance to gifted young people in publishing scientific work in regional and international journals;",
    },
    {
        "order": 12,
        "text_uz": "Doimiy ravishda kafedralardan olingan iqtidorli talabalarning natijalari to'g'risidagi ma'lumotlarni tahlil qilish.",
        "text_ru": "Регулярный анализ данных о результатах одарённых студентов, полученных с кафедр.",
        "text_en": "Regularly analysing data on the performance of gifted students received from departments.",
    },
]


class Command(BaseCommand):
    help = "Iqtidorli talabalar bo'limi ma'lumotlarini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Eski ma'lumotlarni o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            IqtidorliVazifa.objects.all().delete()
            IqtidorliTalabalar.objects.all().delete()
            self.stdout.write(self.style.WARNING("Eski iqtidorli talabalar ma'lumotlari o'chirildi."))

        obj, created = IqtidorliTalabalar.objects.update_or_create(
            pk=IqtidorliTalabalar.SINGLETON_PK,
            defaults=BOSHLIQ,
        )
        action = "Yaratildi" if created else "Yangilandi"
        self.stdout.write(f"  {action}: {obj.boshliq_fio_uz}")

        for v in VAZIFALAR:
            vazifa, vcreated = IqtidorliVazifa.objects.update_or_create(
                parent=obj,
                order=v["order"],
                defaults={
                    "text_uz": v["text_uz"],
                    "text_ru": v["text_ru"],
                    "text_en": v["text_en"],
                },
            )
            vaction = "Yaratildi" if vcreated else "Yangilandi"
            self.stdout.write(f"  {vaction} vazifa #{v['order']}: {v['text_uz'][:60]}")

        self.stdout.write(self.style.SUCCESS(
            f"Iqtidorli talabalar ma'lumotlari muvaffaqiyatli saqlandi "
            f"({len(VAZIFALAR)} ta vazifa)."
        ))
