"""
python manage.py seed_velodrom          # yaratadi / yangilaydi
python manage.py seed_velodrom --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand

from domains.infra.models import (
    SportMajmua, SportMajmuaStat,
    SportMajmuaSportTuri, SportMajmuaTadbir,
)


VELODROM = {
    "name_uz": "Velodrom",
    "name_ru": "Велодром",
    "name_en": "Velodrome",
    "location_uz": "Olimpiya shaharchasi hududidagi",
    "location_ru": "На территории Олимпийского городка",
    "location_en": "Located in the Olympic Village",
    "slug": "velodrom",
    "order": 1,
    "is_active": True,
}

STATS = [
    {
        "order": 1,
        "label_uz": "Qurilish maydoni",
        "label_ru": "Площадь строительства",
        "label_en": "Construction area",
        "value_uz": "15 793 kv.m",
        "value_ru": "15 793 кв.м",
        "value_en": "15,793 sq.m",
    },
    {
        "order": 2,
        "label_uz": "Bino qavatlar soni",
        "label_ru": "Количество этажей",
        "label_en": "Number of floors",
        "value_uz": "3 qavat",
        "value_ru": "3 этажа",
        "value_en": "3 floors",
    },
    {
        "order": 3,
        "label_uz": "Majmua balandligi",
        "label_ru": "Высота комплекса",
        "label_en": "Complex height",
        "value_uz": "30,7 m",
        "value_ru": "30,7 м",
        "value_en": "30.7 m",
    },
    {
        "order": 4,
        "label_uz": "Sig'imi",
        "label_ru": "Вместимость",
        "label_en": "Capacity",
        "value_uz": "2 187 o'rin",
        "value_ru": "2 187 мест",
        "value_en": "2,187 seats",
    },
    {
        "order": 5,
        "label_uz": "Velo yo'lak (144 km/s tezlik)",
        "label_ru": "Велодорожка (скорость 144 км/ч)",
        "label_en": "Cycling track (speed 144 km/h)",
        "value_uz": "250 m",
        "value_ru": "250 м",
        "value_en": "250 m",
    },
    {
        "order": 6,
        "label_uz": "Majmua markazdagi maydon",
        "label_ru": "Центральная площадка комплекса",
        "label_en": "Central arena",
        "value_uz": "86x31 m",
        "value_ru": "86x31 м",
        "value_en": "86x31 m",
    },
    {
        "order": 7,
        "label_uz": "Ternajor zali o'lchami",
        "label_ru": "Размер тренажёрного зала",
        "label_en": "Training hall dimensions",
        "value_uz": "130 kv.m",
        "value_ru": "130 кв.м",
        "value_en": "130 sq.m",
    },
    {
        "order": 8,
        "label_uz": "Yuqori darajadagi mehmonlar uchun o'rinlar",
        "label_ru": "Места для VIP-гостей высокого уровня",
        "label_en": "High-level guest seats",
        "value_uz": "15 ta",
        "value_ru": "15 мест",
        "value_en": "15 seats",
    },
    {
        "order": 9,
        "label_uz": "VIP uchun o'rinlar",
        "label_ru": "VIP места",
        "label_en": "VIP seats",
        "value_uz": "42 ta",
        "value_ru": "42 места",
        "value_en": "42 seats",
    },
    {
        "order": 10,
        "label_uz": "OAB va transaltsiya uchun xonalar",
        "label_ru": "Помещения для СМИ и трансляции",
        "label_en": "Media and broadcast rooms",
        "value_uz": "3 ta",
        "value_ru": "3 помещения",
        "value_en": "3 rooms",
    },
    {
        "order": 11,
        "label_uz": "Mamuriy xonalar va \"open space\"",
        "label_ru": "Административные помещения и \"open space\"",
        "label_en": "Administrative rooms and open space",
        "value_uz": "17 ta",
        "value_ru": "17 помещений",
        "value_en": "17 rooms",
    },
    {
        "order": 12,
        "label_uz": "Konferensiya zali",
        "label_ru": "Конференц-зал",
        "label_en": "Conference hall",
        "value_uz": "40 o'rin",
        "value_ru": "40 мест",
        "value_en": "40 seats",
    },
    {
        "order": 13,
        "label_uz": "Yordamchi va texnik xonalar",
        "label_ru": "Вспомогательные и технические помещения",
        "label_en": "Auxiliary and technical rooms",
        "value_uz": "20 ta",
        "value_ru": "20 помещений",
        "value_en": "20 rooms",
    },
]

SPORT_TYPES = [
    {"order": 1, "name_uz": "Velasport (trek)",    "name_ru": "Велоспорт (трек)",      "name_en": "Cycling (track)"},
    {"order": 2, "name_uz": "Stol tennis",         "name_ru": "Настольный теннис",     "name_en": "Table tennis"},
    {"order": 3, "name_uz": "Para velasport",      "name_ru": "Пара-велоспорт",        "name_en": "Para cycling"},
    {"order": 4, "name_uz": "Qilichbozlik",        "name_ru": "Фехтование",            "name_en": "Fencing"},
    {"order": 5, "name_uz": "Para stol tennis",    "name_ru": "Пара-настольный теннис","name_en": "Para table tennis"},
    {"order": 6, "name_uz": "Og'ir atletika",      "name_ru": "Тяжёлая атлетика",      "name_en": "Weightlifting"},
    {"order": 7, "name_uz": "Para qilichbozlik",   "name_ru": "Пара-фехтование",       "name_en": "Para fencing"},
]

EVENTS = [
    # ── Xalqaro ──────────────────────────────────────────────────────────────
    {
        "level": "xalqaro", "order": 1,
        "title_uz": "Velasport (trek) bo'yicha jahon chempionati va kubgi",
        "title_ru": "Чемпионат мира и Кубок мира по велоспорту (трек)",
        "title_en": "Cycling (track) World Championship and World Cup",
    },
    {
        "level": "xalqaro", "order": 2,
        "title_uz": "Velasport (trek) UCI Reyting musobaqalari",
        "title_ru": "Рейтинговые соревнования UCI по велоспорту (трек)",
        "title_en": "Cycling (track) UCI Rating Competitions",
    },
    {
        "level": "xalqaro", "order": 3,
        "title_uz": "Yuqoridagi barcha sport turlari bo'yicha Osiyo chempionati va kubgi",
        "title_ru": "Чемпионат Азии и Кубок Азии по всем вышеуказанным видам спорта",
        "title_en": "Asian Championship and Asian Cup in all above sports",
    },
    # ── Mahalliy ─────────────────────────────────────────────────────────────
    {
        "level": "maxaliy", "order": 1,
        "title_uz": "O'zbekiston chempionati va kubiglari",
        "title_ru": "Чемпионат и Кубок Узбекистана",
        "title_en": "Uzbekistan Championship and Cup",
    },
    {
        "level": "maxaliy", "order": 2,
        "title_uz": "Mahalliy o'quv-yig'in mashg'ulotlari",
        "title_ru": "Местные учебно-тренировочные сборы",
        "title_en": "Local training camps and sessions",
    },
    {
        "level": "maxaliy", "order": 3,
        "title_uz": "Sport mutaxassislari amaliy dars mashg'ulotlari \"Dual ta'lim\"",
        "title_ru": "Практические занятия специалистов спорта \"Дуальное образование\"",
        "title_en": "Sports specialists practical classes \"Dual education\"",
    },
]


class Command(BaseCommand):
    help = "Velodrom sport majmuasi pasportini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Oldin mavjud ma'lumotlarni o'chiradi")

    def handle(self, *args, **options):
        if options['clear']:
            SportMajmua.objects.filter(slug='velodrom').delete()
            self.stdout.write(self.style.WARNING("Velodrom ma'lumotlari o'chirildi."))

        majmua, created = SportMajmua.objects.update_or_create(
            slug='velodrom',
            defaults=VELODROM,
        )
        action = "Yaratildi" if created else "Yangilandi"
        self.stdout.write(f"{action}: {majmua.name_uz}")

        for stat in STATS:
            SportMajmuaStat.objects.update_or_create(
                majmua=majmua, order=stat['order'],
                defaults=stat,
            )
        self.stdout.write(f"  + {len(STATS)} ta texnik ko'rsatkich")

        for st in SPORT_TYPES:
            SportMajmuaSportTuri.objects.update_or_create(
                majmua=majmua, order=st['order'],
                defaults=st,
            )
        self.stdout.write(f"  + {len(SPORT_TYPES)} ta sport turi")

        for ev in EVENTS:
            SportMajmuaTadbir.objects.update_or_create(
                majmua=majmua, level=ev['level'], order=ev['order'],
                defaults=ev,
            )
        self.stdout.write(f"  + {len(EVENTS)} ta tadbir")

        self.stdout.write(self.style.SUCCESS("Velodrom pasporti muvaffaqiyatli saqlandi."))
