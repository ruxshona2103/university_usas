"""
python manage.py seed_xalqaro_reyting_bolim
python manage.py seed_xalqaro_reyting_bolim --clear
"""
from django.core.management.base import BaseCommand
from domains.international.models import XalqaroReytingBolim

DATA = [
    # ── Sportchilar reytingi ───────────────────────────────────────────────────
    {
        "bolim_type": "sport",
        "order": 1,
        "title_uz": "Xalqaro dzyudo federatsiyasi reytingi",
        "title_ru": "Рейтинг Международной федерации дзюдо",
        "title_en": "International Judo Federation World Ranking",
        "description_uz": (
            "Xalqaro dzyudo federatsiyasi (IJF) tomonidan yuritiladigan jahon reytingi "
            "ro'yxati. Erkaklar va ayollar bo'yicha og'irlik kategoriyalarida sportchilarning "
            "xalqaro musobaqalardagi natijalari asosida hisoblanadi."
        ),
        "description_ru": (
            "Мировой рейтинговый список, ведущийся Международной федерацией дзюдо (IJF). "
            "Рассчитывается на основе результатов спортсменов на международных соревнованиях "
            "по весовым категориям среди мужчин и женщин."
        ),
        "description_en": (
            "The World Ranking List maintained by the International Judo Federation (IJF). "
            "Calculated based on athletes' results in international competitions by weight "
            "categories for men and women."
        ),
        "link": "https://www.ijf.org/wrl?category=all_male&nation=uzb",
    },
    {
        "bolim_type": "sport",
        "order": 2,
        "title_uz": "Xalqaro boks assotsiatsiyasi reytingi",
        "title_ru": "Рейтинг Международной ассоциации бокса",
        "title_en": "World Boxing Association Ranking",
        "description_uz": (
            "Xalqaro boks assotsiatsiyasi (IBA/AIBA) tomonidan yuritiladigan jahon reytingi. "
            "O'zbekiston bokschilari jahon reytingida yetakchi o'rinlarni egallab kelmoqda."
        ),
        "description_ru": (
            "Мировой рейтинг, ведущийся Международной ассоциацией бокса (IBA/AIBA). "
            "Боксёры Узбекистана занимают ведущие позиции в мировом рейтинге."
        ),
        "description_en": (
            "The world ranking maintained by the International Boxing Association (IBA/AIBA). "
            "Uzbekistan's boxers consistently hold top positions in the world ranking."
        ),
        "link": "https://www.iba.sport/rankings/",
    },
    {
        "bolim_type": "sport",
        "order": 3,
        "title_uz": "Xalqaro kurash federatsiyasi reytingi",
        "title_ru": "Рейтинг Международной федерации борьбы",
        "title_en": "United World Wrestling World Ranking",
        "description_uz": (
            "United World Wrestling (UWW) tomonidan yuritiladigan jahon kurash reytingi. "
            "Erkin kurash, klassik kurash va ayollar kurashi bo'yicha alohida reytinglar yuritiladi."
        ),
        "description_ru": (
            "Мировой рейтинг по борьбе, ведущийся United World Wrestling (UWW). "
            "Ведутся отдельные рейтинги по вольной борьбе, греко-римской борьбе и женской борьбе."
        ),
        "description_en": (
            "The world wrestling ranking maintained by United World Wrestling (UWW). "
            "Separate rankings are maintained for freestyle wrestling, Greco-Roman wrestling, "
            "and women's wrestling."
        ),
        "link": "https://uww.org/rankings",
    },
    # ── Professor-o'qituvchilar reytingi ──────────────────────────────────────
    {
        "bolim_type": "professor",
        "order": 1,
        "title_uz": "Google Scholar — ilmiy indekslash",
        "title_ru": "Google Scholar — научное индексирование",
        "title_en": "Google Scholar — Scientific Indexing",
        "description_uz": (
            "Google Scholar — olimlar va tadqiqotchilarning ilmiy nashrlari, iqtibosnomalar "
            "va h-indeksini ko'rsatuvchi xalqaro platforma. Akademiya professor-o'qituvchilari "
            "ushbu platformada o'z ilmiy faoliyatlarini kuzatib boradilar."
        ),
        "description_ru": (
            "Google Scholar — международная платформа, отображающая научные публикации, "
            "цитирования и h-индекс учёных и исследователей. Преподаватели академии "
            "отслеживают свою научную деятельность на данной платформе."
        ),
        "description_en": (
            "Google Scholar is an international platform displaying the scientific publications, "
            "citations, and h-index of scholars and researchers. The Academy's teaching staff "
            "monitor their academic activity on this platform."
        ),
        "link": "https://scholar.google.com/",
    },
    {
        "bolim_type": "professor",
        "order": 2,
        "title_uz": "Scopus — xalqaro ilmiy ma'lumotlar bazasi",
        "title_ru": "Scopus — международная научная база данных",
        "title_en": "Scopus — International Scientific Database",
        "description_uz": (
            "Scopus — Elsevier kompaniyasining xalqaro ilmiy ma'lumotlar bazasi. "
            "Peer-reviewed jurnallardagi maqolalar, konferentsiya materiallari va "
            "kitoblar indekslanadi. Akademiya olimlari Scopus da indekslangan nashrlarga ega."
        ),
        "description_ru": (
            "Scopus — международная научная база данных компании Elsevier. "
            "Индексируются статьи в рецензируемых журналах, материалы конференций и книги. "
            "Учёные академии имеют публикации, индексированные в Scopus."
        ),
        "description_en": (
            "Scopus is Elsevier's international scientific database. Peer-reviewed journal "
            "articles, conference proceedings, and books are indexed. The Academy's researchers "
            "have publications indexed in Scopus."
        ),
        "link": "https://www.scopus.com/",
    },
    {
        "bolim_type": "professor",
        "order": 3,
        "title_uz": "Web of Science — yuqori ta'sirli jurnallar indeksi",
        "title_ru": "Web of Science — индекс высокоцитируемых журналов",
        "title_en": "Web of Science — High-Impact Journal Index",
        "description_uz": (
            "Web of Science (WoS) — Clarivate Analytics kompaniyasining xalqaro ilmiy "
            "indekslash tizimi. Eng nufuzli ilmiy jurnallardagi maqolalar indekslanadi."
        ),
        "description_ru": (
            "Web of Science (WoS) — международная система научного индексирования компании "
            "Clarivate Analytics. Индексируются статьи в наиболее авторитетных научных журналах."
        ),
        "description_en": (
            "Web of Science (WoS) is Clarivate Analytics' international scientific indexing "
            "system. Articles in the most prestigious scientific journals are indexed."
        ),
        "link": "https://www.webofscience.com/",
    },
]


class Command(BaseCommand):
    help = "Xalqaro reyting bo'limlarini seed qiladi (sport va professor)"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Eski ma'lumotlarni o'chirib qayta yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = XalqaroReytingBolim.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        created = updated = 0
        for d in DATA:
            obj, is_new = XalqaroReytingBolim.objects.update_or_create(
                bolim_type=d['bolim_type'],
                order=d['order'],
                defaults={**d, 'is_active': True},
            )
            if is_new:
                created += 1
            else:
                updated += 1
            label = '+' if is_new else '~'
            title_safe = obj.title_uz.encode('ascii', 'replace').decode()
            self.stdout.write(f"  [{label}] [{obj.bolim_type}] {title_safe}")

        self.stdout.write(self.style.SUCCESS(f"\nNatija: {created} yangi, {updated} yangilandi"))
