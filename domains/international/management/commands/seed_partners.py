"""
python manage.py seed_partners          # yaratadi / yangilaydi
python manage.py seed_partners --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.international.models import PartnerOrganization

FOREIGN = [
    {
        "title_uz": "Sankt-Peterburg P.F.Lesgaft nomidagi jismoniy tarbiya va sport milliy davlat instituti",
        "title_ru": "Национальный государственный университет физической культуры, спорта и здоровья имени П.Ф. Лесгафта",
        "title_en": "Lesgaft National State University of Physical Education, Sport and Health, St. Petersburg",
        "country_uz": "Rossiya Federatsiyasi", "country_ru": "Российская Федерация", "country_en": "Russian Federation",
        "website": "https://lesgaft.spb.ru", "order": 1,
    },
    {
        "title_uz": "L.Gumilyov nomidagi Yevroosiyo milliy universiteti",
        "title_ru": "Евразийский национальный университет имени Л.Н. Гумилёва",
        "title_en": "L.N. Gumilyov Eurasian National University",
        "country_uz": "Qozog'iston", "country_ru": "Казахстан", "country_en": "Kazakhstan",
        "website": "https://www.enu.kz", "order": 2,
    },
    {
        "title_uz": "Kyoln sport universiteti (Deutsche Sporthochschule Köln)",
        "title_ru": "Немецкий спортивный университет Кёльна",
        "title_en": "German Sport University Cologne (Deutsche Sporthochschule Köln)",
        "country_uz": "Germaniya", "country_ru": "Германия", "country_en": "Germany",
        "website": "https://www.dshs-koeln.de", "order": 3,
    },
    {
        "title_uz": "Trento universiteti",
        "title_ru": "Университет Тренто",
        "title_en": "University of Trento",
        "country_uz": "Italiya", "country_ru": "Италия", "country_en": "Italy",
        "website": "https://www.unitn.it", "order": 4,
    },
    {
        "title_uz": "Rossiya Milliy Davlat Jismoniy Tarbiya, Sport va Turizm Universiteti (GTSOLIFK)",
        "title_ru": "Российский государственный университет физической культуры, спорта, молодёжи и туризма",
        "title_en": "Russian State University of Physical Education, Sport, Youth and Tourism",
        "country_uz": "Rossiya Federatsiyasi", "country_ru": "Российская Федерация", "country_en": "Russian Federation",
        "website": "https://www.gtsolifk.ru", "order": 5,
    },
    {
        "title_uz": "Belarus Davlat Jismoniy Tarbiya Universiteti",
        "title_ru": "Белорусский государственный университет физической культуры",
        "title_en": "Belarusian State University of Physical Culture",
        "country_uz": "Belarussiya", "country_ru": "Беларусь", "country_en": "Belarus",
        "website": "https://sportedu.by", "order": 6,
    },
    {
        "title_uz": "Pekin Sport Universiteti",
        "title_ru": "Пекинский спортивный университет",
        "title_en": "Beijing Sport University",
        "country_uz": "Xitoy", "country_ru": "Китай", "country_en": "China",
        "website": "https://www.bsu.edu.cn", "order": 7,
    },
    {
        "title_uz": "Koreya Sport va Olimpiya Qo'mitasi",
        "title_ru": "Комитет по спорту и Олимпийский комитет Кореи",
        "title_en": "Korea Sport & Olympic Committee",
        "country_uz": "Janubiy Koreya", "country_ru": "Южная Корея", "country_en": "South Korea",
        "website": "https://www.ksoc.or.kr", "order": 8,
    },
    {
        "title_uz": "Turk Milliy Olimpiya Qo'mitasi",
        "title_ru": "Национальный олимпийский комитет Турции",
        "title_en": "Turkish National Olympic Committee",
        "country_uz": "Turkiya", "country_ru": "Турция", "country_en": "Turkey",
        "website": "https://www.olimpiyat.org.tr", "order": 9,
    },
    {
        "title_uz": "Yaponiya Sport Agentligi",
        "title_ru": "Агентство по спорту Японии",
        "title_en": "Japan Sport Agency",
        "country_uz": "Yaponiya", "country_ru": "Япония", "country_en": "Japan",
        "website": "https://www.mext.go.jp/sports", "order": 10,
    },
    {
        "title_uz": "Ozarbayjon Olimpiya Qo'mitasi",
        "title_ru": "Национальный олимпийский комитет Азербайджана",
        "title_en": "National Olympic Committee of Azerbaijan",
        "country_uz": "Ozarbayjon", "country_ru": "Азербайджан", "country_en": "Azerbaijan",
        "website": "https://www.noc-aze.org", "order": 11,
    },
]

DOMESTIC = [
    {
        "title_uz": "O'zbekiston dzyudo federatsiyasi",
        "title_ru": "Федерация дзюдо Узбекистана",
        "title_en": "Uzbekistan Judo Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.judo.uz", "order": 1,
    },
    {
        "title_uz": "Respublika olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Республиканский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Republican Centre for Training in Olympic and Paralympic Sports",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 2,
    },
    {
        "title_uz": "Jizzax olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Джизакский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Jizzakh Olympic and Paralympic Sports Training Centre",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 3,
    },
    {
        "title_uz": "Chirchiq olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Чирчикский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Chirchiq Olympic and Paralympic Sports Training Centre",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 4,
    },
    {
        "title_uz": "O'zbekiston Milliy Olimpiya Qo'mitasi",
        "title_ru": "Национальный олимпийский комитет Узбекистана",
        "title_en": "National Olympic Committee of Uzbekistan",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.olympic.uz", "order": 5,
    },
    {
        "title_uz": "O'zbekiston Respublikasi Sport vazirligi",
        "title_ru": "Министерство спорта Республики Узбекистан",
        "title_en": "Ministry of Sport of the Republic of Uzbekistan",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.sport.uz", "order": 6,
    },
    {
        "title_uz": "O'zbekiston Paralimpiya Qo'mitasi",
        "title_ru": "Паралимпийский комитет Узбекистана",
        "title_en": "Paralympic Committee of Uzbekistan",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.paralympic.uz", "order": 7,
    },
    {
        "title_uz": "O'zbekiston Boks Federatsiyasi",
        "title_ru": "Федерация бокса Узбекистана",
        "title_en": "Uzbekistan Boxing Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.boxing.uz", "order": 8,
    },
    {
        "title_uz": "O'zbekiston Kurash Assotsiatsiyasi",
        "title_ru": "Ассоциация кураша Узбекистана",
        "title_en": "Uzbekistan Kurash Association",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.kurash.uz", "order": 9,
    },
    {
        "title_uz": "O'zbekiston Taekvondo Federatsiyasi (WT)",
        "title_ru": "Федерация таэквондо Узбекистана (WT)",
        "title_en": "Uzbekistan Taekwondo Federation (WT)",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.taekwondo.uz", "order": 10,
    },
    {
        "title_uz": "O'zbekiston Yengil Atletika Federatsiyasi",
        "title_ru": "Федерация лёгкой атлетики Узбекистана",
        "title_en": "Uzbekistan Athletics Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.athletics.uz", "order": 11,
    },
    {
        "title_uz": "O'zbekiston Suzish Federatsiyasi",
        "title_ru": "Федерация плавания Узбекистана",
        "title_en": "Uzbekistan Swimming Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 12,
    },
    {
        "title_uz": "O'zbekiston Gimnastika Federatsiyasi",
        "title_ru": "Федерация гимнастики Узбекистана",
        "title_en": "Uzbekistan Gymnastics Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.gymnastics.uz", "order": 13,
    },
    {
        "title_uz": "O'zbekiston O'g'ir Atletika Federatsiyasi",
        "title_ru": "Федерация тяжёлой атлетики Узбекистана",
        "title_en": "Uzbekistan Weightlifting Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 14,
    },
]


class Command(BaseCommand):
    help = "Hamkor tashkilotlar (xalqaro va mahalliy) fake ma'lumotlarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = PartnerOrganization.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        self.stdout.write("\n--- XALQARO HAMKORLAR ---")
        f_created = f_updated = 0
        for d in FOREIGN:
            obj, is_new = PartnerOrganization.objects.update_or_create(
                title_uz=d['title_uz'],
                partner_type='foreign',
                defaults=d,
            )
            if is_new:
                f_created += 1
            else:
                f_updated += 1
            self.stdout.write(f"  [{'+'if is_new else '~'}] {obj.title_uz[:65].encode('ascii','replace').decode()} — {obj.country_uz}")

        self.stdout.write("\n--- MAHALLIY HAMKORLAR ---")
        d_created = d_updated = 0
        for d in DOMESTIC:
            obj, is_new = PartnerOrganization.objects.update_or_create(
                title_uz=d['title_uz'],
                partner_type='domestic',
                defaults={**d, 'partner_type': 'domestic'},
            )
            if is_new:
                d_created += 1
            else:
                d_updated += 1
            self.stdout.write(f"  [{'+'if is_new else '~'}] {obj.title_uz[:65]}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: Xalqaro — {f_created} yangi, {f_updated} yangilandi | "
            f"Mahalliy — {d_created} yangi, {d_updated} yangilandi"
        ))
