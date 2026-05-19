"""
python manage.py seed_sport_natija_kalendar

Sport natijalari (10.05.2026 holati) va 2026-yil sport kalendari:
  - 1-bosqich: 98 talaba (yig'ma qator)
  - 2-bosqich: 17 talaba (yig'ma qator)
  - Magistratura: 20 talaba (yig'ma qator)
  - Para sport: 33 talaba (yig'ma qator)
  - SportKalendar 2026: 24 sport turi
"""

import uuid
from django.core.management.base import BaseCommand
from domains.activities.models import SportNatija, SportKalendar


# ── Sport natijalari (10.05.2026) ─────────────────────────────────────────────
ALL_NATIJA = [
    {
        "id": "bb000001-0001-0001-0001-000000000001",
        "bosqich": "1",
        "sport_turi_uz": "1-bosqich (jami)",
        "sport_turi_ru": "1-й курс (итого)",
        "sport_turi_en": "Year 1 (total)",
        "talabalar_soni": 98,
        "jahon_chempionati_1": 0,  "jahon_chempionati_2": 0,  "jahon_chempionati_3": 2,
        "jahon_kubogi_1":      1,  "jahon_kubogi_2":      0,  "jahon_kubogi_3":      0,
        "para_osiyo_1":        0,  "para_osiyo_2":        0,  "para_osiyo_3":        0,
        "osiyo_chempionati_1": 1,  "osiyo_chempionati_2": 4,  "osiyo_chempionati_3": 2,
        "osiyo_kubogi_1":      0,  "osiyo_kubogi_2":      2,  "osiyo_kubogi_3":      1,
        "xalqaro_turnir_1":    1,  "xalqaro_turnir_2":    7,  "xalqaro_turnir_3":    4,
        "prezident_1":         0,  "prezident_2":         0,  "prezident_3":         0,
        "ozb_chempionati_1":  41,  "ozb_chempionati_2":  20,  "ozb_chempionati_3":  18,
        "ozb_kubogi_1":       19,  "ozb_kubogi_2":       11,  "ozb_kubogi_3":        7,
        "order": 1,
    },
    {
        "id": "bb000002-0001-0001-0001-000000000001",
        "bosqich": "2",
        "sport_turi_uz": "2-bosqich (jami)",
        "sport_turi_ru": "2-й курс (итого)",
        "sport_turi_en": "Year 2 (total)",
        "talabalar_soni": 17,
        "jahon_chempionati_1": 0,  "jahon_chempionati_2": 0,  "jahon_chempionati_3": 0,
        "jahon_kubogi_1":      0,  "jahon_kubogi_2":      0,  "jahon_kubogi_3":      0,
        "para_osiyo_1":        0,  "para_osiyo_2":        0,  "para_osiyo_3":        0,
        "osiyo_chempionati_1": 0,  "osiyo_chempionati_2": 0,  "osiyo_chempionati_3": 0,
        "osiyo_kubogi_1":      0,  "osiyo_kubogi_2":      0,  "osiyo_kubogi_3":      0,
        "xalqaro_turnir_1":    0,  "xalqaro_turnir_2":    0,  "xalqaro_turnir_3":    0,
        "prezident_1":         0,  "prezident_2":         0,  "prezident_3":         0,
        "ozb_chempionati_1":   2,  "ozb_chempionati_2":   6,  "ozb_chempionati_3":   6,
        "ozb_kubogi_1":        2,  "ozb_kubogi_2":        0,  "ozb_kubogi_3":        2,
        "order": 1,
    },
    {
        "id": "bb000003-0001-0001-0001-000000000001",
        "bosqich": "magistr",
        "sport_turi_uz": "Magistratura (jami)",
        "sport_turi_ru": "Магистратура (итого)",
        "sport_turi_en": "Master's (total)",
        "talabalar_soni": 20,
        "jahon_chempionati_1": 0,  "jahon_chempionati_2": 0,  "jahon_chempionati_3": 0,
        "jahon_kubogi_1":      0,  "jahon_kubogi_2":      1,  "jahon_kubogi_3":      0,
        "para_osiyo_1":        0,  "para_osiyo_2":        0,  "para_osiyo_3":        0,
        "osiyo_chempionati_1": 1,  "osiyo_chempionati_2": 1,  "osiyo_chempionati_3": 0,
        "osiyo_kubogi_1":      0,  "osiyo_kubogi_2":      0,  "osiyo_kubogi_3":      0,
        "xalqaro_turnir_1":    0,  "xalqaro_turnir_2":    0,  "xalqaro_turnir_3":    0,
        "prezident_1":         0,  "prezident_2":         0,  "prezident_3":         0,
        "ozb_chempionati_1":   1,  "ozb_chempionati_2":   0,  "ozb_chempionati_3":   0,
        "ozb_kubogi_1":        0,  "ozb_kubogi_2":        0,  "ozb_kubogi_3":        0,
        "order": 1,
    },
    {
        "id": "bb000004-0001-0001-0001-000000000001",
        "bosqich": "para",
        "sport_turi_uz": "Para sport (jami)",
        "sport_turi_ru": "Пара спорт (итого)",
        "sport_turi_en": "Para Sports (total)",
        "talabalar_soni": 33,
        "jahon_chempionati_1": 0,  "jahon_chempionati_2": 0,  "jahon_chempionati_3": 0,
        "jahon_kubogi_1":      0,  "jahon_kubogi_2":      0,  "jahon_kubogi_3":      0,
        "para_osiyo_1":        0,  "para_osiyo_2":        0,  "para_osiyo_3":        0,
        "osiyo_chempionati_1": 0,  "osiyo_chempionati_2": 0,  "osiyo_chempionati_3": 0,
        "osiyo_kubogi_1":      0,  "osiyo_kubogi_2":      0,  "osiyo_kubogi_3":      0,
        "xalqaro_turnir_1":    1,  "xalqaro_turnir_2":    1,  "xalqaro_turnir_3":    0,
        "prezident_1":         0,  "prezident_2":         0,  "prezident_3":         0,
        "ozb_chempionati_1":   0,  "ozb_chempionati_2":   0,  "ozb_chempionati_3":   0,
        "ozb_kubogi_1":        0,  "ozb_kubogi_2":        0,  "ozb_kubogi_3":        0,
        "order": 1,
    },
]

# ── Sport kalendari 2026 ──────────────────────────────────────────────────────
KALENDAR_2026 = [
    {
        "id": "cc000001-0001-0001-0001-000000000001",
        "yil": 2026,
        "sport_turi_uz": "Boks",
        "sport_turi_ru": "Бокс",
        "sport_turi_en": "Boxing",
        "jahon_chempionati": 1, "jahon_kubogi": 1,
        "yoshlar_olimpiya": 1, "osiyo_oyinlari": 1, "osiyo_chempionati": 2,
        "xalqaro_turnir": 3, "prezident_olimpiyada": 1,
        "order": 1,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000002",
        "yil": 2026,
        "sport_turi_uz": "Dzyudo",
        "sport_turi_ru": "Дзюдо",
        "sport_turi_en": "Judo",
        "jahon_chempionati": 2, "osiyo_oyinlari": 3,
        "osiyo_chempionati": 2, "xalqaro_turnir": 1, "ozb_chempionati": 1,
        "order": 2,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000003",
        "yil": 2026,
        "sport_turi_uz": "Yengil atletika",
        "sport_turi_ru": "Лёгкая атлетика",
        "sport_turi_en": "Athletics",
        "jahon_chempionati": 1, "yoshlar_olimpiya": 1,
        "osiyo_oyinlari": 1, "osiyo_chempionati": 3, "xalqaro_turnir": 1,
        "ozb_chempionati": 2, "ozb_kubogi": 1, "prezident_olimpiyada": 1,
        "order": 3,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000004",
        "yil": 2026,
        "sport_turi_uz": "Og'ir atletika",
        "sport_turi_ru": "Тяжёлая атлетика",
        "sport_turi_en": "Weightlifting",
        "jahon_chempionati": 2, "osiyo_chempionati": 2,
        "ozb_chempionati": 1, "ozb_kubogi": 1,
        "order": 4,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000005",
        "yil": 2026,
        "sport_turi_uz": "Yunon-rum kurashi",
        "sport_turi_ru": "Греко-римская борьба",
        "sport_turi_en": "Greco-Roman Wrestling",
        "jahon_chempionati": 2, "osiyo_chempionati": 3,
        "xalqaro_turnir": 1, "ozb_chempionati": 1, "ozb_kubogi": 1, "prezident_olimpiyada": 1,
        "order": 5,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000006",
        "yil": 2026,
        "sport_turi_uz": "Erkin kurash",
        "sport_turi_ru": "Вольная борьба",
        "sport_turi_en": "Freestyle Wrestling",
        "jahon_chempionati": 2, "osiyo_chempionati": 3,
        "xalqaro_turnir": 1, "ozb_chempionati": 1, "ozb_kubogi": 1, "prezident_olimpiyada": 1,
        "order": 6,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000007",
        "yil": 2026,
        "sport_turi_uz": "Taekvondo WT",
        "sport_turi_ru": "Тхэквондо WT",
        "sport_turi_en": "Taekwondo WT",
        "jahon_chempionati": 1, "osiyo_oyinlari": 1, "osiyo_chempionati": 2,
        "ozb_chempionati": 1, "prezident_olimpiyada": 1,
        "order": 7,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000008",
        "yil": 2026,
        "sport_turi_uz": "Suzish",
        "sport_turi_ru": "Плавание",
        "sport_turi_en": "Swimming",
        "jahon_chempionati": 2, "osiyo_oyinlari": 1, "osiyo_chempionati": 1,
        "ozb_chempionati": 2, "ozb_kubogi": 3, "prezident_olimpiyada": 1,
        "order": 8,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000009",
        "yil": 2026,
        "sport_turi_uz": "Baydarka va kanoe",
        "sport_turi_ru": "Байдарки и каноэ",
        "sport_turi_en": "Canoe/Kayak",
        "jahon_chempionati": 1, "osiyo_chempionati": 2,
        "xalqaro_turnir": 1, "ozb_chempionati": 1,
        "order": 9,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000010",
        "yil": 2026,
        "sport_turi_uz": "Velosport",
        "sport_turi_ru": "Велоспорт",
        "sport_turi_en": "Cycling",
        "jahon_chempionati": 3, "jahon_kubogi": 6,
        "ozb_chempionati": 3, "ozb_kubogi": 1,
        "order": 10,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000011",
        "yil": 2026,
        "sport_turi_uz": "Gimnastika",
        "sport_turi_ru": "Гимнастика",
        "sport_turi_en": "Gymnastics",
        "jahon_chempionati": 2, "jahon_kubogi": 1, "osiyo_kubogi": 2,
        "xalqaro_turnir": 2, "ozb_chempionati": 4,
        "order": 11,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000012",
        "yil": 2026,
        "sport_turi_uz": "Qilichbozlik",
        "sport_turi_ru": "Фехтование",
        "sport_turi_en": "Fencing",
        "jahon_chempionati": 2, "jahon_kubogi": 2,
        "osiyo_oyinlari": 1, "osiyo_chempionati": 2,
        "xalqaro_turnir": 1, "ozb_chempionati": 1, "prezident_olimpiyada": 1,
        "order": 12,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000013",
        "yil": 2026,
        "sport_turi_uz": "Kamondan otish",
        "sport_turi_ru": "Стрельба из лука",
        "sport_turi_en": "Archery",
        "jahon_kubogi": 5, "osiyo_chempionati": 1,
        "xalqaro_turnir": 2, "ozb_chempionati": 2,
        "order": 13,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000014",
        "yil": 2026,
        "sport_turi_uz": "O'q otish",
        "sport_turi_ru": "Стрельба",
        "sport_turi_en": "Shooting",
        "jahon_chempionati": 1, "ozb_chempionati": 1, "ozb_kubogi": 1,
        "order": 14,
    },
    # ── Para sport turlari ───────────────────────────────────────────────────
    {
        "id": "cc000001-0001-0001-0001-000000000015",
        "yil": 2026,
        "sport_turi_uz": "Para Suzish",
        "sport_turi_ru": "Пара Плавание",
        "sport_turi_en": "Para Swimming",
        "jahon_seriyasi": 2, "osiyo_oyinlari": 1,
        "ozb_chempionati": 2, "ozb_kubogi": 2, "prezident_olimpiyada": 1,
        "order": 15,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000016",
        "yil": 2026,
        "sport_turi_uz": "Para Qilichbozlik",
        "sport_turi_ru": "Пара Фехтование",
        "sport_turi_en": "Para Fencing",
        "jahon_chempionati": 1, "osiyo_oyinlari": 1,
        "xalqaro_turnir": 1, "ozb_chempionati": 1, "ozb_kubogi": 1,
        "order": 16,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000017",
        "yil": 2026,
        "sport_turi_uz": "Para Velosport",
        "sport_turi_ru": "Пара Велоспорт",
        "sport_turi_en": "Para Cycling",
        "jahon_chempionati": 2, "xalqaro_turnir": 2,
        "ozb_chempionati": 1, "ozb_kubogi": 2, "prezident_olimpiyada": 1,
        "order": 17,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000018",
        "yil": 2026,
        "sport_turi_uz": "Para Kamondan otish",
        "sport_turi_ru": "Пара Стрельба из лука",
        "sport_turi_en": "Para Archery",
        "jahon_chempionati": 1, "osiyo_oyinlari": 1,
        "xalqaro_turnir": 1, "ozb_chempionati": 1, "ozb_kubogi": 2,
        "order": 18,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000019",
        "yil": 2026,
        "sport_turi_uz": "Para Yengil atletika",
        "sport_turi_ru": "Пара Лёгкая атлетика",
        "sport_turi_en": "Para Athletics",
        "jahon_chempionati": 1, "osiyo_oyinlari": 1,
        "xalqaro_turnir": 7, "ozb_chempionati": 1, "ozb_kubogi": 1, "prezident_olimpiyada": 1,
        "order": 19,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000020",
        "yil": 2026,
        "sport_turi_uz": "Para Taekvondo WT",
        "sport_turi_ru": "Пара Тхэквондо WT",
        "sport_turi_en": "Para Taekwondo WT",
        "jahon_seriyasi": 1, "osiyo_oyinlari": 1, "osiyo_chempionati": 1,
        "xalqaro_turnir": 6, "ozb_chempionati": 1, "prezident_olimpiyada": 1,
        "order": 20,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000021",
        "yil": 2026,
        "sport_turi_uz": "Para Kanoe",
        "sport_turi_ru": "Пара Каноэ",
        "sport_turi_en": "Para Canoe",
        "jahon_chempionati": 1, "osiyo_oyinlari": 1,
        "xalqaro_turnir": 1, "ozb_chempionati": 1, "ozb_kubogi": 1,
        "order": 21,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000022",
        "yil": 2026,
        "sport_turi_uz": "Para Dzyudo",
        "sport_turi_ru": "Пара Дзюдо",
        "sport_turi_en": "Para Judo",
        "jahon_chempionati": 1, "osiyo_oyinlari": 1,
        "xalqaro_turnir": 2, "ozb_chempionati": 1, "ozb_kubogi": 1,
        "order": 22,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000023",
        "yil": 2026,
        "sport_turi_uz": "Para Paurlifting",
        "sport_turi_ru": "Пара Пауэрлифтинг",
        "sport_turi_en": "Para Powerlifting",
        "jahon_chempionati": 1, "osiyo_oyinlari": 1,
        "xalqaro_turnir": 1, "ozb_chempionati": 2, "ozb_kubogi": 2, "prezident_olimpiyada": 1,
        "order": 23,
    },
    {
        "id": "cc000001-0001-0001-0001-000000000024",
        "yil": 2026,
        "sport_turi_uz": "Para Baydarka",
        "sport_turi_ru": "Пара Байдарка",
        "sport_turi_en": "Para Kayak",
        "jahon_chempionati": 2, "xalqaro_turnir": 1,
        "ozb_chempionati": 1, "ozb_kubogi": 1, "prezident_olimpiyada": 1,
        "order": 24,
    },
]

NATIJA_FIELD_DEFAULTS = {
    "talabalar_soni": 0,
    "jahon_chempionati_1": 0, "jahon_chempionati_2": 0, "jahon_chempionati_3": 0,
    "jahon_kubogi_1": 0, "jahon_kubogi_2": 0, "jahon_kubogi_3": 0,
    "para_osiyo_1": 0, "para_osiyo_2": 0, "para_osiyo_3": 0,
    "osiyo_chempionati_1": 0, "osiyo_chempionati_2": 0, "osiyo_chempionati_3": 0,
    "osiyo_kubogi_1": 0, "osiyo_kubogi_2": 0, "osiyo_kubogi_3": 0,
    "xalqaro_turnir_1": 0, "xalqaro_turnir_2": 0, "xalqaro_turnir_3": 0,
    "prezident_1": 0, "prezident_2": 0, "prezident_3": 0,
    "ozb_chempionati_1": 0, "ozb_chempionati_2": 0, "ozb_chempionati_3": 0,
    "ozb_kubogi_1": 0, "ozb_kubogi_2": 0, "ozb_kubogi_3": 0,
}

KALENDAR_FIELD_DEFAULTS = {
    "jahon_chempionati": 0, "jahon_seriyasi": 0, "jahon_kubogi": 0,
    "yoshlar_olimpiya": 0, "osiyo_oyinlari": 0, "osiyo_chempionati": 0,
    "osiyo_kubogi": 0, "xalqaro_turnir": 0,
    "ozb_chempionati": 0, "ozb_kubogi": 0, "prezident_olimpiyada": 0,
}


class Command(BaseCommand):
    help = "Sport natijalari (10.05.2026) va 2026-yil sport kalendarini DB ga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true',
                            help="Mavjud SportNatija va SportKalendar datalarni o'chiradi")

    def handle(self, *args, **options):
        if options['clear']:
            SportNatija.objects.all().delete()
            SportKalendar.objects.all().delete()
            self.stdout.write(self.style.WARNING("Mavjud natija va kalendar ma'lumotlari o'chirildi."))

        self.stdout.write("\n--- SPORT NATIJALARI (10.05.2026) ---")
        for d in ALL_NATIJA:
            defaults = {**NATIJA_FIELD_DEFAULTS}
            defaults.update({k: v for k, v in d.items() if k not in ('id', 'bosqich')})
            obj, created = SportNatija.objects.update_or_create(
                id=uuid.UUID(d['id']),
                defaults={'bosqich': d['bosqich'], **defaults},
            )
            self.stdout.write(
                f"  [{'Yaratildi' if created else 'Yangilandi'}] "
                f"{obj.get_bosqich_display()} — {obj.sport_turi_uz} (jami={obj.jami})"
            )

        self.stdout.write("\n--- SPORT KALENDARI 2026 ---")
        for d in KALENDAR_2026:
            defaults = {**KALENDAR_FIELD_DEFAULTS}
            defaults.update({k: v for k, v in d.items() if k not in ('id', 'yil')})
            obj, created = SportKalendar.objects.update_or_create(
                id=uuid.UUID(d['id']),
                defaults={'yil': d['yil'], **defaults},
            )
            self.stdout.write(
                f"  [{'Yaratildi' if created else 'Yangilandi'}] "
                f"{obj.yil} — {obj.sport_turi_uz} (jami={obj.jami})"
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nJami: {len(ALL_NATIJA)} natija qatori | {len(KALENDAR_2026)} kalendar qatori!"
        ))
