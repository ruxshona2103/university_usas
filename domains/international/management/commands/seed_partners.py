"""
python manage.py seed_partners          # yaratadi / yangilaydi
python manage.py seed_partners --clear  # o'chirib qaytadan yozadi
python manage.py seed_partners --force-logos  # logolarni qayta yozadi
"""
import os
import base64
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from domains.international.models import PartnerOrganization


def _svg(letter, bg, fg="#FFFFFF"):
    """Oddiy SVG logo — harf + rang."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <rect width="200" height="200" rx="16" fill="{bg}"/>
  <text x="100" y="135" text-anchor="middle" font-family="Arial Black,Arial,sans-serif"
        font-size="{72 if len(letter)<=2 else 48}" font-weight="900" fill="{fg}">{letter}</text>
</svg>'''.encode()


# ── Logolar: (filename, svg_bytes) ───────────────────────────────────────────
LOGOS = {
    # Xorijiy universitetlar — mamlakat kodi + rang
    "lesgaft_ru":       ("lesgaft_ru.svg",       _svg("RU",  "#003580")),
    "enu_kz":           ("enu_kz.svg",            _svg("KZ",  "#00AFCA")),
    "dshs_de":          ("dshs_de.svg",           _svg("DE",  "#DD0000")),
    "unitn_it":         ("unitn_it.svg",          _svg("IT",  "#009246")),
    "gtsolifk_ru":      ("gtsolifk_ru.svg",       _svg("RU",  "#B22222")),
    "bgufk_by":         ("bgufk_by.svg",          _svg("BY",  "#CF101A")),
    "bsu_cn":           ("bsu_cn.svg",            _svg("CN",  "#DE2910")),
    "ksoc_kr":          ("ksoc_kr.svg",           _svg("KR",  "#003478")),
    "tnoc_tr":          ("tnoc_tr.svg",           _svg("TR",  "#E30A17")),
    "jsa_jp":           ("jsa_jp.svg",            _svg("JP",  "#BC002D")),
    "noc_az":           ("noc_az.svg",            _svg("AZ",  "#0092BC")),
    # Mahalliy tashkilotlar
    "noc_uz":           ("noc_uz.svg",            _svg("NOC", "#003DA5")),
    "sport_ministry":   ("sport_ministry.svg",    _svg("SM",  "#1A237E")),
    "para_uz":          ("para_uz.svg",           _svg("PAR", "#6A1B9A")),
    "rep_center":       ("rep_center.svg",        _svg("RC",  "#0057A8")),
    "jizzax_center":    ("jizzax_center.svg",     _svg("JZ",  "#2E7D32")),
    "chirchiq_center":  ("chirchiq_center.svg",   _svg("CH",  "#1565C0")),
    "fed_judo":         ("fed_judo.svg",          _svg("JUD", "#1B3A6B")),
    "fed_boxing":       ("fed_boxing.svg",        _svg("BOX", "#B71C1C")),
    "fed_kurash":       ("fed_kurash.svg",        _svg("KUR", "#4E342E")),
    "fed_taekwondo":    ("fed_taekwondo.svg",     _svg("TKD", "#0D47A1")),
    "fed_athletics":    ("fed_athletics.svg",     _svg("ATH", "#F57F17")),
    "fed_swimming":     ("fed_swimming.svg",      _svg("SWM", "#0288D1")),
    "fed_gymnastics":   ("fed_gymnastics.svg",    _svg("GYM", "#AD1457")),
    "fed_weightlift":   ("fed_weightlift.svg",    _svg("WLT", "#37474F")),
}

# Serverda real logo fayllari bo'lsa ularni ishlatadi, yo'q bo'lsa SVG fallback
def _logo_path(key):
    from django.conf import settings
    for ext in ('png', 'jpg', 'jpeg', 'webp', 'svg'):
        p = os.path.join(settings.MEDIA_ROOT, 'international', 'logos', '2026', f"{key}.{ext}")
        if os.path.isfile(p):
            return p
    return None


def _get_logo_content(key):
    """Real fayl bo'lsa o'sha, yo'q bo'lsa SVG inline qaytaradi."""
    path = _logo_path(key)
    if path:
        ext = os.path.splitext(path)[1]
        with open(path, 'rb') as f:
            return f"{key}{ext}", f.read()
    if key in LOGOS:
        fname, content = LOGOS[key]
        return fname, content
    return None, None


FOREIGN = [
    {
        "title_uz": "Sankt-Peterburg P.F.Lesgaft nomidagi jismoniy tarbiya va sport milliy davlat instituti",
        "title_ru": "Национальный государственный университет физической культуры, спорта и здоровья имени П.Ф. Лесгафта",
        "title_en": "Lesgaft National State University of Physical Education, Sport and Health, St. Petersburg",
        "country_uz": "Rossiya Federatsiyasi", "country_ru": "Российская Федерация", "country_en": "Russian Federation",
        "website": "https://lesgaft.spb.ru", "order": 1, "_logo_key": "lesgaft_ru",
    },
    {
        "title_uz": "L.Gumilyov nomidagi Yevroosiyo milliy universiteti",
        "title_ru": "Евразийский национальный университет имени Л.Н. Гумилёва",
        "title_en": "L.N. Gumilyov Eurasian National University",
        "country_uz": "Qozog'iston", "country_ru": "Казахстан", "country_en": "Kazakhstan",
        "website": "https://www.enu.kz", "order": 2, "_logo_key": "enu_kz",
    },
    {
        "title_uz": "Kyoln sport universiteti (Deutsche Sporthochschule Köln)",
        "title_ru": "Немецкий спортивный университет Кёльна",
        "title_en": "German Sport University Cologne (Deutsche Sporthochschule Köln)",
        "country_uz": "Germaniya", "country_ru": "Германия", "country_en": "Germany",
        "website": "https://www.dshs-koeln.de", "order": 3, "_logo_key": "dshs_de",
    },
    {
        "title_uz": "Trento universiteti",
        "title_ru": "Университет Тренто",
        "title_en": "University of Trento",
        "country_uz": "Italiya", "country_ru": "Италия", "country_en": "Italy",
        "website": "https://www.unitn.it", "order": 4, "_logo_key": "unitn_it",
    },
    {
        "title_uz": "Rossiya Milliy Davlat Jismoniy Tarbiya, Sport va Turizm Universiteti (GTSOLIFK)",
        "title_ru": "Российский государственный университет физической культуры, спорта, молодёжи и туризма",
        "title_en": "Russian State University of Physical Education, Sport, Youth and Tourism",
        "country_uz": "Rossiya Federatsiyasi", "country_ru": "Российская Федерация", "country_en": "Russian Federation",
        "website": "https://www.gtsolifk.ru", "order": 5, "_logo_key": "gtsolifk_ru",
    },
    {
        "title_uz": "Belarus Davlat Jismoniy Tarbiya Universiteti",
        "title_ru": "Белорусский государственный университет физической культуры",
        "title_en": "Belarusian State University of Physical Culture",
        "country_uz": "Belarussiya", "country_ru": "Беларусь", "country_en": "Belarus",
        "website": "https://sportedu.by", "order": 6, "_logo_key": "bgufk_by",
    },
    {
        "title_uz": "Pekin Sport Universiteti",
        "title_ru": "Пекинский спортивный университет",
        "title_en": "Beijing Sport University",
        "country_uz": "Xitoy", "country_ru": "Китай", "country_en": "China",
        "website": "https://www.bsu.edu.cn", "order": 7, "_logo_key": "bsu_cn",
    },
    {
        "title_uz": "Koreya Sport va Olimpiya Qo'mitasi",
        "title_ru": "Комитет по спорту и Олимпийский комитет Кореи",
        "title_en": "Korea Sport & Olympic Committee",
        "country_uz": "Janubiy Koreya", "country_ru": "Южная Корея", "country_en": "South Korea",
        "website": "https://www.ksoc.or.kr", "order": 8, "_logo_key": "ksoc_kr",
    },
    {
        "title_uz": "Turk Milliy Olimpiya Qo'mitasi",
        "title_ru": "Национальный олимпийский комитет Турции",
        "title_en": "Turkish National Olympic Committee",
        "country_uz": "Turkiya", "country_ru": "Турция", "country_en": "Turkey",
        "website": "https://www.olimpiyat.org.tr", "order": 9, "_logo_key": "tnoc_tr",
    },
    {
        "title_uz": "Yaponiya Sport Agentligi",
        "title_ru": "Агентство по спорту Японии",
        "title_en": "Japan Sport Agency",
        "country_uz": "Yaponiya", "country_ru": "Япония", "country_en": "Japan",
        "website": "https://www.mext.go.jp/sports", "order": 10, "_logo_key": "jsa_jp",
    },
    {
        "title_uz": "Ozarbayjon Olimpiya Qo'mitasi",
        "title_ru": "Национальный олимпийский комитет Азербайджана",
        "title_en": "National Olympic Committee of Azerbaijan",
        "country_uz": "Ozarbayjon", "country_ru": "Азербайджан", "country_en": "Azerbaijan",
        "website": "https://www.noc-aze.org", "order": 11, "_logo_key": "noc_az",
    },
]

DOMESTIC = [
    {
        "title_uz": "O'zbekiston dzyudo federatsiyasi",
        "title_ru": "Федерация дзюдо Узбекистана",
        "title_en": "Uzbekistan Judo Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.judo.uz", "order": 1, "_logo_key": "fed_judo",
    },
    {
        "title_uz": "Respublika olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Республиканский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Republican Centre for Training in Olympic and Paralympic Sports",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 2, "_logo_key": "rep_center",
    },
    {
        "title_uz": "Jizzax olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Джизакский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Jizzakh Olympic and Paralympic Sports Training Centre",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 3, "_logo_key": "jizzax_center",
    },
    {
        "title_uz": "Chirchiq olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Чирчикский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Chirchiq Olympic and Paralympic Sports Training Centre",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 4, "_logo_key": "chirchiq_center",
    },
    {
        "title_uz": "O'zbekiston Milliy Olimpiya Qo'mitasi",
        "title_ru": "Национальный олимпийский комитет Узбекистана",
        "title_en": "National Olympic Committee of Uzbekistan",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.olympic.uz", "order": 5, "_logo_key": "noc_uz",
    },
    {
        "title_uz": "O'zbekiston Respublikasi Sport vazirligi",
        "title_ru": "Министерство спорта Республики Узбекистан",
        "title_en": "Ministry of Sport of the Republic of Uzbekistan",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.sport.uz", "order": 6, "_logo_key": "sport_ministry",
    },
    {
        "title_uz": "O'zbekiston Paralimpiya Qo'mitasi",
        "title_ru": "Паралимпийский комитет Узбекистана",
        "title_en": "Paralympic Committee of Uzbekistan",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.paralympic.uz", "order": 7, "_logo_key": "para_uz",
    },
    {
        "title_uz": "O'zbekiston Boks Federatsiyasi",
        "title_ru": "Федерация бокса Узбекистана",
        "title_en": "Uzbekistan Boxing Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.boxing.uz", "order": 8, "_logo_key": "fed_boxing",
    },
    {
        "title_uz": "O'zbekiston Kurash Assotsiatsiyasi",
        "title_ru": "Ассоциация кураша Узбекистана",
        "title_en": "Uzbekistan Kurash Association",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.kurash.uz", "order": 9, "_logo_key": "fed_kurash",
    },
    {
        "title_uz": "O'zbekiston Taekvondo Federatsiyasi (WT)",
        "title_ru": "Федерация таэквондо Узбекистана (WT)",
        "title_en": "Uzbekistan Taekwondo Federation (WT)",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.taekwondo.uz", "order": 10, "_logo_key": "fed_taekwondo",
    },
    {
        "title_uz": "O'zbekiston Yengil Atletika Federatsiyasi",
        "title_ru": "Федерация лёгкой атлетики Узбекистана",
        "title_en": "Uzbekistan Athletics Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.athletics.uz", "order": 11, "_logo_key": "fed_athletics",
    },
    {
        "title_uz": "O'zbekiston Suzish Federatsiyasi",
        "title_ru": "Федерация плавания Узбекистана",
        "title_en": "Uzbekistan Swimming Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 12, "_logo_key": "fed_swimming",
    },
    {
        "title_uz": "O'zbekiston Gimnastika Federatsiyasi",
        "title_ru": "Федерация гимнастики Узбекистана",
        "title_en": "Uzbekistan Gymnastics Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "https://www.gymnastics.uz", "order": 13, "_logo_key": "fed_gymnastics",
    },
    {
        "title_uz": "O'zbekiston O'g'ir Atletika Federatsiyasi",
        "title_ru": "Федерация тяжёлой атлетики Узбекистана",
        "title_en": "Uzbekistan Weightlifting Federation",
        "country_uz": "O'zbekiston", "country_ru": "Узбекистан", "country_en": "Uzbekistan",
        "website": "", "order": 14, "_logo_key": "fed_weightlift",
    },
]


def _attach_logo(obj, logo_key, force=False):
    if obj.logo and not force:
        return False
    fname, content = _get_logo_content(logo_key)
    if not content:
        return False
    cf = ContentFile(content)
    obj.logo.save(fname, cf, save=False)
    obj.image.save(fname, ContentFile(content), save=True)
    return True


def _seed_list(stdout, records, partner_type, force=False):
    created = updated = logos = 0
    for d in records:
        logo_key = d.pop('_logo_key', None)
        obj, is_new = PartnerOrganization.objects.update_or_create(
            title_uz=d['title_uz'],
            partner_type=partner_type,
            defaults={**d, 'partner_type': partner_type},
        )
        if is_new:
            created += 1
        else:
            updated += 1
        logo_saved = _attach_logo(obj, logo_key, force=force) if logo_key else False
        if logo_saved:
            logos += 1
        mark = " [logo+]" if logo_saved else (" [logo]" if obj.logo else " [no logo]")
        name_safe = obj.title_uz[:58].encode('ascii', 'replace').decode()
        stdout.write(f"  [{'+'if is_new else '~'}] {name_safe}{mark}")
    return created, updated, logos


class Command(BaseCommand):
    help = "Hamkor tashkilotlar ma'lumotlari va logolarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")
        parser.add_argument('--force-logos', action='store_true', help="Mavjud logolarni ham qayta yozadi")

    def handle(self, *args, **options):
        force = options['force_logos']

        if options['clear']:
            n = PartnerOrganization.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        self.stdout.write("\n--- XALQARO HAMKORLAR ---")
        fc, fu, fl = _seed_list(self.stdout, FOREIGN, 'foreign', force=force)

        self.stdout.write("\n--- MAHALLIY HAMKORLAR ---")
        dc, du, dl = _seed_list(self.stdout, DOMESTIC, 'domestic', force=force)

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: Xalqaro — {fc} yangi, {fu} yangilandi, {fl} logo | "
            f"Mahalliy — {dc} yangi, {du} yangilandi, {dl} logo"
        ))
