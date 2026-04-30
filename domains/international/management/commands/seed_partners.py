"""
python manage.py seed_partners          # yaratadi / yangilaydi
python manage.py seed_partners --clear  # o'chirib qaytadan yozadi
"""
import os
import io
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from domains.international.models import PartnerOrganization

# SVG logo generator helpers
def _flag_svg(emoji_text, bg_color, text_color="#fff"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="120" height="80" viewBox="0 0 120 80">
  <rect width="120" height="80" fill="{bg_color}" rx="6"/>
  <text x="60" y="50" text-anchor="middle" font-family="Arial,sans-serif" font-size="32" fill="{text_color}">{emoji_text}</text>
</svg>'''.encode()

def _sport_svg(letter, bg_color, text_color="#fff"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120">
  <circle cx="60" cy="60" r="56" fill="{bg_color}"/>
  <circle cx="60" cy="60" r="56" fill="none" stroke="{text_color}" stroke-width="3" opacity="0.3"/>
  <text x="60" y="78" text-anchor="middle" font-family="Arial Black,Arial,sans-serif" font-size="52" font-weight="bold" fill="{text_color}">{letter}</text>
</svg>'''.encode()


FOREIGN = [
    {
        "title_uz": "Sankt-Peterburg P.F.Lesgaft nomidagi jismoniy tarbiya va sport milliy davlat instituti",
        "title_ru": "Национальный государственный университет физической культуры, спорта и здоровья имени П.Ф. Лесгафта",
        "title_en": "Lesgaft National State University of Physical Education, Sport and Health, St. Petersburg",
        "country_uz": "Rossiya Federatsiyasi", "country_ru": "Российская Федерация", "country_en": "Russian Federation",
        "website": "https://lesgaft.spb.ru", "order": 1,
        "_logo": ("lesgaft_ru.svg", _flag_svg("RU", "#003580")),
    },
    {
        "title_uz": "L.Gumilyov nomidagi Yevroosiyo milliy universiteti",
        "title_ru": "Евразийский национальный университет имени Л.Н. Гумилёва",
        "title_en": "L.N. Gumilyov Eurasian National University",
        "country_uz": "Qozog'iston", "country_ru": "Казахстан", "country_en": "Kazakhstan",
        "website": "https://www.enu.kz", "order": 2,
        "_logo": ("enu_kz.svg", _flag_svg("KZ", "#00AFCA")),
    },
    {
        "title_uz": "Kyoln sport universiteti (Deutsche Sporthochschule Köln)",
        "title_ru": "Немецкий спортивный университет Кёльна",
        "title_en": "German Sport University Cologne (Deutsche Sporthochschule Köln)",
        "country_uz": "Germaniya", "country_ru": "Германия", "country_en": "Germany",
        "website": "https://www.dshs-koeln.de", "order": 3,
        "_logo": ("dshs_de.svg", _flag_svg("DE", "#DD0000")),
    },
    {
        "title_uz": "Trento universiteti",
        "title_ru": "Университет Тренто",
        "title_en": "University of Trento",
        "country_uz": "Italiya", "country_ru": "Италия", "country_en": "Italy",
        "website": "https://www.unitn.it", "order": 4,
        "_logo": ("unitn_it.svg", _flag_svg("IT", "#009246")),
    },
    {
        "title_uz": "Rossiya Milliy Davlat Jismoniy Tarbiya, Sport va Turizm Universiteti (GTSOLIFK)",
        "title_ru": "Российский государственный университет физической культуры, спорта, молодёжи и туризма",
        "title_en": "Russian State University of Physical Education, Sport, Youth and Tourism",
        "country_uz": "Rossiya Federatsiyasi", "country_ru": "Российская Федерация", "country_en": "Russian Federation",
        "website": "https://www.gtsolifk.ru", "order": 5,
        "_logo": ("gtsolifk_ru.svg", _flag_svg("RU", "#CC0000")),
    },
    {
        "title_uz": "Belarus Davlat Jismoniy Tarbiya Universiteti",
        "title_ru": "Белорусский государственный университет физической культуры",
        "title_en": "Belarusian State University of Physical Culture",
        "country_uz": "Belarussiya", "country_ru": "Беларусь", "country_en": "Belarus",
        "website": "https://sportedu.by", "order": 6,
        "_logo": ("bgufk_by.svg", _flag_svg("BY", "#CF101A")),
    },
    {
        "title_uz": "Pekin Sport Universiteti",
        "title_ru": "Пекинский спортивный университет",
        "title_en": "Beijing Sport University",
        "country_uz": "Xitoy", "country_ru": "Китай", "country_en": "China",
        "website": "https://www.bsu.edu.cn", "order": 7,
        "_logo": ("bsu_cn.svg", _flag_svg("CN", "#DE2910")),
    },
    {
        "title_uz": "Koreya Sport va Olimpiya Qo'mitasi",
        "title_ru": "Комитет по спорту и Олимпийский комитет Кореи",
        "title_en": "Korea Sport & Olympic Committee",
        "country_uz": "Janubiy Koreya", "country_ru": "Южная Корея", "country_en": "South Korea",
        "website": "https://www.ksoc.or.kr", "order": 8,
        "_logo": ("ksoc_kr.svg", _flag_svg("KR", "#003478")),
    },
    {
        "title_uz": "Turk Milliy Olimpiya Qo'mitasi",
        "title_ru": "Национальный олимпийский комитет Турции",
        "title_en": "Turkish National Olympic Committee",
        "country_uz": "Turkiya", "country_ru": "Турция", "country_en": "Turkey",
        "website": "https://www.olimpiyat.org.tr", "order": 9,
        "_logo": ("tnoc_tr.svg", _flag_svg("TR", "#E30A17")),
    },
    {
        "title_uz": "Yaponiya Sport Agentligi",
        "title_ru": "Агентство по спорту Японии",
        "title_en": "Japan Sport Agency",
        "country_uz": "Yaponiya", "country_ru": "Япония", "country_en": "Japan",
        "website": "https://www.mext.go.jp/sports", "order": 10,
        "_logo": ("jsa_jp.svg", _flag_svg("JP", "#BC002D")),
    },
    {
        "title_uz": "Ozarbayjon Olimpiya Qo'mitasi",
        "title_ru": "Национальный олимпийский комитет Азербайджана",
        "title_en": "National Olympic Committee of Azerbaijan",
        "country_uz": "Ozarbayjon", "country_ru": "Азербайджан", "country_en": "Azerbaijan",
        "website": "https://www.noc-aze.org", "order": 11,
        "_logo": ("noc_az.svg", _flag_svg("AZ", "#0092BC")),
    },
]

DOMESTIC = [
    {
        "title_uz": "O'zbekiston dzyudo federatsiyasi",
        "title_ru": "Федерация дзюдо Узбекистана",
        "title_en": "Uzbekistan Judo Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.judo.uz", "order": 1,
        "_logo": ("fed_judo.svg", _sport_svg("J", "#1B3A6B")),
    },
    {
        "title_uz": "Respublika olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Республиканский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Republican Centre for Training in Olympic and Paralympic Sports",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 2,
        "_logo": ("rep_olympic_center.svg", _sport_svg("O", "#0057A8")),
    },
    {
        "title_uz": "Jizzax olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Джизакский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Jizzakh Olympic and Paralympic Sports Training Centre",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 3,
        "_logo": ("jizzax_center.svg", _sport_svg("Jz", "#2E7D32")),
    },
    {
        "title_uz": "Chirchiq olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Чирчикский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Chirchiq Olympic and Paralympic Sports Training Centre",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 4,
        "_logo": ("chirchiq_center.svg", _sport_svg("Ch", "#1565C0")),
    },
    {
        "title_uz": "O'zbekiston Milliy Olimpiya Qo'mitasi",
        "title_ru": "Национальный олимпийский комитет Узбекистана",
        "title_en": "National Olympic Committee of Uzbekistan",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.olympic.uz", "order": 5,
        "_logo": ("noc_uz.svg", _sport_svg("NOC", "#003DA5")),
    },
    {
        "title_uz": "O'zbekiston Respublikasi Sport vazirligi",
        "title_ru": "Министерство спорта Республики Узбекистан",
        "title_en": "Ministry of Sport of the Republic of Uzbekistan",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.sport.uz", "order": 6,
        "_logo": ("sport_ministry.svg", _sport_svg("SM", "#1A237E")),
    },
    {
        "title_uz": "O'zbekiston Paralimpiya Qo'mitasi",
        "title_ru": "Паралимпийский комитет Узбекистана",
        "title_en": "Paralympic Committee of Uzbekistan",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.paralympic.uz", "order": 7,
        "_logo": ("para_uz.svg", _sport_svg("P", "#6A1B9A")),
    },
    {
        "title_uz": "O'zbekiston Boks Federatsiyasi",
        "title_ru": "Федерация бокса Узбекистана",
        "title_en": "Uzbekistan Boxing Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.boxing.uz", "order": 8,
        "_logo": ("fed_boxing.svg", _sport_svg("B", "#B71C1C")),
    },
    {
        "title_uz": "O'zbekiston Kurash Assotsiatsiyasi",
        "title_ru": "Ассоциация кураша Узбекистана",
        "title_en": "Uzbekistan Kurash Association",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.kurash.uz", "order": 9,
        "_logo": ("fed_kurash.svg", _sport_svg("K", "#4E342E")),
    },
    {
        "title_uz": "O'zbekiston Taekvondo Federatsiyasi (WT)",
        "title_ru": "Федерация таэквондо Узбекистана (WT)",
        "title_en": "Uzbekistan Taekwondo Federation (WT)",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.taekwondo.uz", "order": 10,
        "_logo": ("fed_taekwondo.svg", _sport_svg("T", "#0D47A1")),
    },
    {
        "title_uz": "O'zbekiston Yengil Atletika Federatsiyasi",
        "title_ru": "Федерация лёгкой атлетики Узбекистана",
        "title_en": "Uzbekistan Athletics Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.athletics.uz", "order": 11,
        "_logo": ("fed_athletics.svg", _sport_svg("A", "#F57F17")),
    },
    {
        "title_uz": "O'zbekiston Suzish Federatsiyasi",
        "title_ru": "Федерация плавания Узбекистана",
        "title_en": "Uzbekistan Swimming Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 12,
        "_logo": ("fed_swimming.svg", _sport_svg("S", "#0288D1")),
    },
    {
        "title_uz": "O'zbekiston Gimnastika Federatsiyasi",
        "title_ru": "Федерация гимнастики Узбекистана",
        "title_en": "Uzbekistan Gymnastics Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.gymnastics.uz", "order": 13,
        "_logo": ("fed_gymnastics.svg", _sport_svg("G", "#AD1457")),
    },
    {
        "title_uz": "O'zbekiston O'g'ir Atletika Federatsiyasi",
        "title_ru": "Федерация тяжёлой атлетики Узбекистана",
        "title_en": "Uzbekistan Weightlifting Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 14,
        "_logo": ("fed_weightlifting.svg", _sport_svg("W", "#37474F")),
    },
]


def _save_logo(obj, filename, content):
    """SVG logoni ob'ektga saqlaydi (faqat bo'sh bo'lsa yoki --force)."""
    obj.logo.save(filename, ContentFile(content), save=True)


class Command(BaseCommand):
    help = "Hamkor tashkilotlar (xalqaro va mahalliy) ma'lumotlarini va logolarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")
        parser.add_argument('--force-logos', action='store_true', help="Mavjud logolarni ham qayta yozadi")

    def handle(self, *args, **options):
        force = options['force_logos']

        if options['clear']:
            n = PartnerOrganization.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        self.stdout.write("\n--- XALQARO HAMKORLAR ---")
        f_created = f_updated = 0
        for d in FOREIGN:
            logo_data = d.pop('_logo', None)
            obj, is_new = PartnerOrganization.objects.update_or_create(
                title_uz=d['title_uz'],
                partner_type='foreign',
                defaults=d,
            )
            if is_new:
                f_created += 1
            else:
                f_updated += 1

            if logo_data and (not obj.logo or force):
                fname, fcontent = logo_data
                _save_logo(obj, fname, fcontent)
                logo_mark = " [logo+]"
            else:
                logo_mark = ""

            name_safe = obj.title_uz[:60].encode('ascii', 'replace').decode()
            self.stdout.write(f"  [{'+'if is_new else '~'}] {name_safe} — {obj.country_uz}{logo_mark}")

        self.stdout.write("\n--- MAHALLIY HAMKORLAR ---")
        d_created = d_updated = 0
        for d in DOMESTIC:
            logo_data = d.pop('_logo', None)
            obj, is_new = PartnerOrganization.objects.update_or_create(
                title_uz=d['title_uz'],
                partner_type='domestic',
                defaults={**d, 'partner_type': 'domestic'},
            )
            if is_new:
                d_created += 1
            else:
                d_updated += 1

            if logo_data and (not obj.logo or force):
                fname, fcontent = logo_data
                _save_logo(obj, fname, fcontent)
                logo_mark = " [logo+]"
            else:
                logo_mark = ""

            name_safe = obj.title_uz[:60].encode('ascii', 'replace').decode()
            self.stdout.write(f"  [{'+'if is_new else '~'}] {name_safe}{logo_mark}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: Xalqaro — {f_created} yangi, {f_updated} yangilandi | "
            f"Mahalliy — {d_created} yangi, {d_updated} yangilandi"
        ))
