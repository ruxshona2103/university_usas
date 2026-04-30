"""
python manage.py seed_jamoat_tashkilotlar
python manage.py seed_jamoat_tashkilotlar --clear
"""
from django.core.management.base import BaseCommand
from domains.academic.models import HuzuridagiTashkilot

DATA = [
    {
        "name_uz": "Yoshlar ittifoqi",
        "name_ru": "Союз молодёжи",
        "name_en": "Youth Union",
        "description_uz": "Akademiyaning Yoshlar ittifoqi talaba yoshlarning ijtimoiy faolligini oshirish, sport va madaniy-ommaviy tadbirlarni tashkil etish, hamda yoshlarning vatanparvarlik ruhini shakllantirish yo'lida faoliyat olib boradi.",
        "description_ru": "Союз молодёжи академии работает по повышению социальной активности студентов, организации спортивных и культурно-массовых мероприятий, а также формированию патриотического духа молодёжи.",
        "description_en": "The Youth Union of the Academy works to increase the social activity of students, organize sports and cultural events, and foster a spirit of patriotism among youth.",
        "about_uz": "",
        "about_ru": "",
        "about_en": "",
        "phone": "",
        "email": "",
        "order": 1,
    },
    {
        "name_uz": "Kasaba uyushmasi",
        "name_ru": "Профсоюз",
        "name_en": "Trade Union",
        "description_uz": "Akademiyaning Kasaba uyushmasi xodimlar va talabalarning mehnat huquqlari, ijtimoiy kafolatlari va dam olish sharoitlarini himoya qilish maqsadida faoliyat yuritadi.",
        "description_ru": "Профсоюз академии осуществляет деятельность в целях защиты трудовых прав, социальных гарантий и условий отдыха работников и студентов.",
        "description_en": "The Trade Union of the Academy operates to protect the labor rights, social guarantees, and recreational conditions of employees and students.",
        "about_uz": "",
        "about_ru": "",
        "about_en": "",
        "phone": "",
        "email": "",
        "order": 2,
    },
    {
        "name_uz": "Xotin-qizlar masalalari bo'yicha maslahat kengashi",
        "name_ru": "Консультативный совет по вопросам женщин",
        "name_en": "Women's Advisory Council",
        "description_uz": (
            "Akademiya xotin-qizlar kengashi raisiga O'zbekiston Respublikasi Oliy va o'rta maxsus ta'lim vazirining "
            "2020-yil 17-iyun 326-buyrug'iga asosan xotin-qizlar masalalari bo'yicha rektor maslahatchisi maqomi berilgan.\n\n"
            "O'zbekiston davlat sport akademiyasi jamoasida 1023 ga yaqin ayollar faoliyat ko'rsatmoqdalar. Ulardan: "
            "501 ta professor o'qituvchilar bo'lib, 522 xodimlar. Talaba qizlarimiz soni 11714 tani, shundan 2150 tasi oilali qizlarni tashkil qiladi.\n\n"
            "Akademiya xotin-qizlar kengashining nizomi mavjud bo'lib, ushbu nizom bo'yicha faoliyat olib boradi. "
            "Xotin-qizlar kengashi jamoat tashkiloti sifatida o'z faoliyatini O'zbekiston Respublikasi Konstitutsiyasi, "
            "\"Nodavlat notijorat tashkilotlari to'g'risida\"gi va \"O'zbekiston Respublikasida jamoat birlashmalari "
            "to'g'risida\"gi Qonunlarga muvofiq olib boradi."
        ),
        "description_ru": (
            "Председателю женского совета академии присвоен статус советника ректора по вопросам женщин "
            "согласно приказу № 326 министра высшего и среднего специального образования Республики Узбекистан от 17 июня 2020 года.\n\n"
            "В коллективе Узбекистанской государственной спортивной академии работают около 1 023 женщин: "
            "501 преподаватель и 522 сотрудника. Число студенток составляет 11 714, из которых 2 150 — замужем.\n\n"
            "Женский совет осуществляет деятельность на основании своего устава в соответствии с Конституцией "
            "Республики Узбекистан и соответствующими законами об НКО и общественных объединениях."
        ),
        "description_en": (
            "The chairperson of the Academy's Women's Council was granted the status of Rector's Adviser on Women's Issues "
            "under Order No. 326 of the Minister of Higher and Secondary Specialised Education of the Republic of Uzbekistan "
            "dated 17 June 2020.\n\n"
            "Approximately 1,023 women work at the Uzbekistan State Sports Academy: 501 teaching staff and 522 administrative staff. "
            "The number of female students is 11,714, of whom 2,150 are married.\n\n"
            "The Women's Council operates under its own charter in accordance with the Constitution of the Republic of Uzbekistan "
            "and relevant laws on non-commercial and public organisations."
        ),
        "about_uz": (
            "Xotin-qizlarni qo'llab-quvvatlash, gender tenglikni ta'minlash va oila institutini mustahkamlash maqsadida "
            "kengash quyidagi asosiy yo'nalishlarda faoliyat olib boradi:\n"
            "1. Xotin-qizlarni kasbiy o'sishda qo'llab-quvvatlash\n"
            "2. Oilaviy munosabatlarni mustahkamlash\n"
            "3. Reproduktiv salomatlikni yaxshilash\n"
            "4. Huquqiy savodxonlikni oshirish\n"
            "5. Ijtimoiy faollikni kuchaytirish"
        ),
        "about_ru": "",
        "about_en": "",
        "phone": "95 080 7001",
        "email": "xudayberdiyeva89@mail.ru",
        "order": 3,
    },
]


class Command(BaseCommand):
    help = "Jamoat tashkilotlari ma'lumotlarini HuzuridagiTashkilot modeliga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Jamoat tashkilotlarini o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = HuzuridagiTashkilot.objects.filter(org_type='jamoat').delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta jamoat tashkiloti"))

        created = updated = 0
        for d in DATA:
            obj, is_new = HuzuridagiTashkilot.objects.update_or_create(
                name_uz=d['name_uz'],
                org_type='jamoat',
                defaults={**d, 'org_type': 'jamoat', 'is_active': True},
            )
            if is_new:
                created += 1
            else:
                updated += 1
            name_safe = obj.name_uz.encode('ascii', 'replace').decode()
            self.stdout.write(f"  [{'+'if is_new else '~'}] {name_safe}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created} yangi, {updated} yangilandi"
        ))
