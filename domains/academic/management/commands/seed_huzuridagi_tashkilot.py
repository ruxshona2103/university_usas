"""
python manage.py seed_huzuridagi_tashkilot
python manage.py seed_huzuridagi_tashkilot --clear
"""
from django.core.management.base import BaseCommand
from domains.academic.models import HuzuridagiTashkilot

TASHKILOTLAR = [
    {
        "name_uz": "Jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish instituti hamda uning Nukus, Samarqand va Farg'ona filiallari",
        "name_ru": "Институт переподготовки и повышения квалификации специалистов по физической культуре и спорту и его филиалы в Нукусе, Самарканде и Фергане",
        "name_en": "Institute for Retraining and Advanced Training of Physical Culture and Sports Specialists and its branches in Nukus, Samarkand and Fergana",
        "description_uz": (
            "Institut jismoniy tarbiya va sport sohasida ishlayotgan mutaxassislarning malakasini oshirish va qayta tayyorlash bo'yicha ixtisoslashtirilgan ta'lim muassasasi hisoblanadi. "
            "Respublika bo'ylab trener, sport o'qituvchisi va boshqa sport mutaxassislariga ilg'or bilim va ko'nikmalar beriladi. "
            "Nukus, Samarqand va Farg'ona filliallari orqali butun O'zbekiston bo'ylab xizmat ko'rsatiladi."
        ),
        "description_ru": (
            "Институт является специализированным учебным заведением по повышению квалификации и переподготовке специалистов в области физической культуры и спорта. "
            "Тренерам, преподавателям физической культуры и другим спортивным специалистам по всей республике предоставляются передовые знания и навыки. "
            "Через филиалы в Нукусе, Самарканде и Фергане обслуживается весь Узбекистан."
        ),
        "description_en": (
            "The Institute is a specialised educational institution for advanced training and retraining of specialists in the field of physical culture and sports. "
            "Coaches, physical education teachers and other sports specialists across the republic are provided with advanced knowledge and skills. "
            "Services are provided throughout Uzbekistan through branches in Nukus, Samarkand and Fergana."
        ),
        "address_uz": "Toshkent shahri",
        "address_ru": "г. Ташкент",
        "address_en": "Tashkent city",
        "order": 1,
    },
    {
        "name_uz": "Jismoniy tarbiya va sport ilmiy-tadqiqotlar instituti",
        "name_ru": "Научно-исследовательский институт физической культуры и спорта",
        "name_en": "Research Institute of Physical Culture and Sports",
        "description_uz": (
            "Institut jismoniy tarbiya va sport sohasida fundamental va amaliy ilmiy tadqiqotlar olib boradi. "
            "Sport fiziologiyasi, biomexanika, sport psixologiyasi va boshqa yo'nalishlar bo'yicha innovatsion tadqiqotlar amalga oshiriladi. "
            "Ilmiy natijalar amaliyotga tatbiq etilib, sport samaradorligini oshirishga xizmat qiladi."
        ),
        "description_ru": (
            "Институт проводит фундаментальные и прикладные научные исследования в области физической культуры и спорта. "
            "Осуществляются инновационные исследования в области спортивной физиологии, биомеханики, спортивной психологии и других направлений. "
            "Научные результаты внедряются в практику и служат повышению эффективности спорта."
        ),
        "description_en": (
            "The Institute conducts fundamental and applied scientific research in the field of physical culture and sports. "
            "Innovative research is carried out in sports physiology, biomechanics, sports psychology and other areas. "
            "Scientific results are implemented in practice and serve to improve sports performance."
        ),
        "address_uz": "Toshkent shahri",
        "address_ru": "г. Ташкент",
        "address_en": "Tashkent city",
        "order": 2,
    },
    {
        "name_uz": "Davlat sport tibbiyoti ilmiy amaliy markazi",
        "name_ru": "Государственный научно-практический центр спортивной медицины",
        "name_en": "State Scientific and Practical Centre of Sports Medicine",
        "description_uz": (
            "Markaz sport tibbiyoti sohasida ilmiy-amaliy faoliyat yuritadi. "
            "Sportchilarning sog'liq holatini kuzatish, tibbiy reabilitatsiya va sport travmatologiyasi bo'yicha xizmat ko'rsatiladi. "
            "Milliy terma jamoalar va professional sportchilar uchun maxsus tibbiy dasturlar ishlab chiqiladi."
        ),
        "description_ru": (
            "Центр осуществляет научно-практическую деятельность в области спортивной медицины. "
            "Оказываются услуги по мониторингу состояния здоровья спортсменов, медицинской реабилитации и спортивной травматологии. "
            "Разрабатываются специальные медицинские программы для национальных сборных команд и профессиональных спортсменов."
        ),
        "description_en": (
            "The Centre conducts scientific and practical activities in the field of sports medicine. "
            "Services are provided for monitoring athletes' health status, medical rehabilitation and sports traumatology. "
            "Special medical programmes are developed for national teams and professional athletes."
        ),
        "address_uz": "Toshkent shahri",
        "address_ru": "г. Ташкент",
        "address_en": "Tashkent city",
        "order": 3,
    },
    {
        "name_uz": "O'zbekiston tarixi va xorijiy tillarni o'qitish markazi",
        "name_ru": "Центр преподавания истории Узбекистана и иностранных языков",
        "name_en": "Centre for Teaching History of Uzbekistan and Foreign Languages",
        "description_uz": (
            "Markaz O'zbekiston tarixi va xorijiy tillarni chuqur o'rgatish bo'yicha ixtisoslashgan. "
            "Talabalar va xodimlar uchun ingliz, rus, xitoy va boshqa tillar bo'yicha kurslar tashkil etiladi. "
            "Xalqaro hamkorlikni kengaytirish va kadrlarning til malakasini oshirish asosiy maqsad hisoblanadi."
        ),
        "description_ru": (
            "Центр специализируется на углублённом преподавании истории Узбекистана и иностранных языков. "
            "Для студентов и сотрудников организуются курсы по английскому, русскому, китайскому и другим языкам. "
            "Основной целью является расширение международного сотрудничества и повышение языковой квалификации кадров."
        ),
        "description_en": (
            "The Centre specialises in in-depth teaching of the history of Uzbekistan and foreign languages. "
            "Courses in English, Russian, Chinese and other languages are organised for students and staff. "
            "The main goal is to expand international cooperation and improve the language proficiency of personnel."
        ),
        "address_uz": "Toshkent shahri, O'zbekiston davlat sport akademiyasi hududida",
        "address_ru": "г. Ташкент, территория Государственной академии спорта Узбекистана",
        "address_en": "Tashkent city, territory of the State Academy of Sports of Uzbekistan",
        "order": 4,
    },
    {
        "name_uz": "Axborot kutubxona markazi",
        "name_ru": "Информационно-библиотечный центр",
        "name_en": "Information and Library Centre",
        "description_uz": (
            "Markaz keng ko'lamli kitob fondi va elektron resurslar bazasiga ega zamonaviy kutubxona hisoblanadi. "
            "Jismoniy tarbiya, sport, tibbiyot va boshqa sohalardagi 50 000 dan ortiq nashrlar mavjud. "
            "Talabalar va o'qituvchilar uchun elektron katalog, ma'lumotlar bazalari va onlayn resurslardan foydalanish imkoniyati yaratilgan."
        ),
        "description_ru": (
            "Центр является современной библиотекой с обширным книжным фондом и базой электронных ресурсов. "
            "Имеется более 50 000 изданий по физической культуре, спорту, медицине и другим отраслям. "
            "Для студентов и преподавателей созданы возможности использования электронного каталога, баз данных и онлайн-ресурсов."
        ),
        "description_en": (
            "The Centre is a modern library with an extensive book collection and electronic resources database. "
            "More than 50,000 publications on physical culture, sports, medicine and other fields are available. "
            "Students and teachers have access to an electronic catalogue, databases and online resources."
        ),
        "address_uz": "Toshkent shahri, O'zbekiston davlat sport akademiyasi hududida",
        "address_ru": "г. Ташкент, территория Государственной академии спорта Узбекистана",
        "address_en": "Tashkent city, territory of the State Academy of Sports of Uzbekistan",
        "order": 5,
    },
]


class Command(BaseCommand):
    help = "Akademiya huzuridagi tashkilotlar ma'lumotlarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = HuzuridagiTashkilot.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        created = updated = 0
        for d in TASHKILOTLAR:
            obj, is_new = HuzuridagiTashkilot.objects.update_or_create(
                name_uz=d['name_uz'],
                defaults=d,
            )
            if is_new:
                created += 1
            else:
                updated += 1
            self.stdout.write(f"  [{'+'if is_new else '~'}] {obj.name_uz[:70].encode('ascii', 'replace').decode()}")

        self.stdout.write(self.style.SUCCESS(f"\nNatija: {created} yangi, {updated} yangilandi"))
