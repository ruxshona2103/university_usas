"""
python manage.py seed_sport_section_data

Sport faoliyat sahifasi uchun:
  - 3 ta statistika kartochkasi (15+, 500+, 50+)
  - 6 ta sport yo'nalishi (Kurash, Suzish, Sikl, Parasport, Atletika, Gimnastika)
  - 8 ta yillik tadbir
"""

import uuid
from django.core.management.base import BaseCommand
from domains.activities.models import SportStat, SportYonalish, SportTadbir

STATS = [
    {
        "id":       "e7f1e675-5992-4804-bd8d-7f89b51d4d1d",
        "value":    15,
        "suffix":   "+",
        "color":    "blue",
        "title_uz": "Sport turlari bo'yicha seksiyalar",
        "title_ru": "Секции по видам спорта",
        "title_en": "Sections by sports types",
        "order":    1,
    },
    {
        "id":       "d5182a24-bf96-4102-bfa0-7cc9d38ecddb",
        "value":    500,
        "suffix":   "+",
        "color":    "green",
        "title_uz": "Faol talabalar sportchilar",
        "title_ru": "Активных студентов-спортсменов",
        "title_en": "Active student athletes",
        "order":    2,
    },
    {
        "id":       "3835a391-7488-4c45-b069-ae7e74aedace",
        "value":    50,
        "suffix":   "+",
        "color":    "orange",
        "title_uz": "Yillik musobaqalar va tadbirlar",
        "title_ru": "Ежегодных соревнований и мероприятий",
        "title_en": "Annual competitions and events",
        "order":    3,
    },
]

YONALISHLAR = [
    {
        "id":             "94558685-021e-4275-8e4d-abd909f207e2",
        "icon":           "🥊",
        "title_uz":       "Kurash va jang san'atlari",
        "title_ru":       "Борьба и боевые искусства",
        "title_en":       "Wrestling and Martial Arts",
        "description_uz": "Erkin kurash, judo, boks, taekvondo",
        "description_ru": "Вольная борьба, дзюдо, бокс, тхэквондо",
        "description_en": "Freestyle wrestling, judo, boxing, taekwondo",
        "order":          1,
    },
    {
        "id":             "1aefb129-82c8-428d-905f-b17e512e5686",
        "icon":           "🤽",
        "title_uz":       "Suv sport turlari",
        "title_ru":       "Водные виды спорта",
        "title_en":       "Water Sports",
        "description_uz": "Suzish, eshkak eshish, kanoye",
        "description_ru": "Плавание, гребля, каноэ",
        "description_en": "Swimming, rowing, canoeing",
        "order":          2,
    },
    {
        "id":             "351b63a9-3591-43a9-a668-0ff7d18f32d3",
        "icon":           "🚴",
        "title_uz":       "Sikl sport turlari",
        "title_ru":       "Циклические виды спорта",
        "title_en":       "Cycling Sports",
        "description_uz": "Velosport, triathlon",
        "description_ru": "Велоспорт, триатлон",
        "description_en": "Cycling, triathlon",
        "order":          3,
    },
    {
        "id":             "f60e6a9b-1558-4cea-9562-dc1c97c62c22",
        "icon":           "♿",
        "title_uz":       "Parasport",
        "title_ru":       "Параспорт",
        "title_en":       "Para Sports",
        "description_uz": "Adaptiv sport turlari, paralimpiya",
        "description_ru": "Адаптивные виды спорта, паралимпиада",
        "description_en": "Adaptive sports, paralympics",
        "order":          4,
    },
    {
        "id":             "b33db90f-6c10-4739-977a-339a0886aaa3",
        "icon":           "🏃",
        "title_uz":       "Atletika",
        "title_ru":       "Лёгкая атлетика",
        "title_en":       "Athletics",
        "description_uz": "Yugurish, sakrash, uloqtirish",
        "description_ru": "Бег, прыжки, метание",
        "description_en": "Running, jumping, throwing",
        "order":          5,
    },
    {
        "id":             "1110f106-f661-4890-969c-e92169ddda16",
        "icon":           "🤸",
        "title_uz":       "Gimnastika",
        "title_ru":       "Гимнастика",
        "title_en":       "Gymnastics",
        "description_uz": "Badiiy va sport gimnastikasi",
        "description_ru": "Художественная и спортивная гимнастика",
        "description_en": "Rhythmic and artistic gymnastics",
        "order":          6,
    },
]

TADBIRLAR = [
    {
        "id":             "2e151d81-f3e6-41e3-83ab-211d83e65be4",
        "title_uz":       "Akademiya ichki chempionati",
        "title_ru":       "Внутренний чемпионат академии",
        "title_en":       "Academy Internal Championship",
        "description_uz": "Barcha sport turlari bo'yicha akademiya ichki chempionati. Talabalar, o'qituvchilar va xodimlar ishtirok etadi.",
        "description_ru": "Внутренний чемпионат академии по всем видам спорта. Участвуют студенты, преподаватели и сотрудники.",
        "description_en": "Academy internal championship in all sports. Students, teachers and staff participate.",
        "location_uz":    "Akademiya sport zali",
        "location_ru":    "Спортивный зал академии",
        "location_en":    "Academy sports hall",
        "event_date":     "2025-03-15",
        "order":          1,
    },
    {
        "id":             "b35891c8-ff50-4e0f-b73d-6e8774b7ad78",
        "title_uz":       "Universitetlararo sport festivali",
        "title_ru":       "Межуниверситетский спортивный фестиваль",
        "title_en":       "Inter-University Sports Festival",
        "description_uz": "O'zbekiston universitetlari o'rtasidagi sport festivali. 20 dan ortiq universitet ishtirok etadi.",
        "description_ru": "Спортивный фестиваль среди университетов Узбекистана. Участвуют более 20 университетов.",
        "description_en": "Sports festival among universities of Uzbekistan. More than 20 universities participate.",
        "location_uz":    "Toshkent shahar sport majmuasi",
        "location_ru":    "Спортивный комплекс города Ташкента",
        "location_en":    "Tashkent city sports complex",
        "event_date":     "2025-04-20",
        "order":          2,
    },
    {
        "id":             "f4786808-c8f0-465d-b42d-eb281ba07260",
        "title_uz":       "Respublika talabalar olimpiadasi",
        "title_ru":       "Республиканская студенческая олимпиада",
        "title_en":       "Republican Student Olympics",
        "description_uz": "Respublika miqyosidagi talabalar sport olimpiadasi. Eng yaxshi sportchilar milliy terma jamoaga tanlanadi.",
        "description_ru": "Республиканская студенческая спортивная олимпиада. Лучшие спортсмены отбираются в национальную сборную.",
        "description_en": "Republican student sports Olympics. Best athletes are selected for the national team.",
        "location_uz":    "Milliy olimpiya qo'mitasi sport majmuasi",
        "location_ru":    "Спортивный комплекс Национального олимпийского комитета",
        "location_en":    "National Olympic Committee sports complex",
        "event_date":     "2025-05-10",
        "order":          3,
    },
    {
        "id":             "2719d004-d956-4fcc-981a-62cc36b29167",
        "title_uz":       "Xalqaro kurash turniri",
        "title_ru":       "Международный турнир по борьбе",
        "title_en":       "International Wrestling Tournament",
        "description_uz": "Akademiya tashkil etuvchi xalqaro kurash turniri. 15 davlatdan sportchilar ishtirok etadi.",
        "description_ru": "Международный турнир по борьбе, организуемый академией. Участвуют спортсмены из 15 стран.",
        "description_en": "International wrestling tournament organized by the academy. Athletes from 15 countries participate.",
        "location_uz":    "Akademiya sport arenasi",
        "location_ru":    "Спортивная арена академии",
        "location_en":    "Academy sports arena",
        "event_date":     "2025-06-05",
        "order":          4,
    },
    {
        "id":             "aa110001-0001-0001-0001-000000000051",
        "title_uz":       "Yozgi sport lageri",
        "title_ru":       "Летний спортивный лагерь",
        "title_en":       "Summer Sports Camp",
        "description_uz": "Talabalar uchun yozgi sport lageri — trenirovka va dam olish birgalikda.",
        "description_ru": "Летний спортивный лагерь для студентов — тренировки и отдых вместе.",
        "description_en": "Summer sports camp for students — training and recreation together.",
        "location_uz":    "Chorvoq dam olish maskani",
        "location_ru":    "Зона отдыха Чарвак",
        "location_en":    "Charvak resort",
        "event_date":     "2025-07-01",
        "order":          5,
    },
    {
        "id":             "aa110001-0001-0001-0001-000000000052",
        "title_uz":       "Suzish bo'yicha ochiq musobaqa",
        "title_ru":       "Открытые соревнования по плаванию",
        "title_en":       "Open Swimming Competition",
        "description_uz": "Barcha yoshdagi talabalar ishtirok etishi mumkin bo'lgan ochiq suzish musobaqasi.",
        "description_ru": "Открытые соревнования по плаванию для студентов всех возрастов.",
        "description_en": "Open swimming competition for students of all ages.",
        "location_uz":    "Akademiya suzish havzasi",
        "location_ru":    "Бассейн академии",
        "location_en":    "Academy swimming pool",
        "event_date":     "2025-09-20",
        "order":          6,
    },
    {
        "id":             "aa110001-0001-0001-0001-000000000053",
        "title_uz":       "Futbol kubogi musobaqasi",
        "title_ru":       "Кубковые соревнования по футболу",
        "title_en":       "Football Cup Competition",
        "description_uz": "Akademiya futbol kubogi — fakultetlar o'rtasidagi to'liq turnir jadvali.",
        "description_ru": "Кубок академии по футболу — полный турнирный график между факультетами.",
        "description_en": "Academy football cup — full tournament schedule between faculties.",
        "location_uz":    "Akademiya futbol maydoni",
        "location_ru":    "Футбольное поле академии",
        "location_en":    "Academy football field",
        "event_date":     "2025-10-15",
        "order":          7,
    },
    {
        "id":             "aa110001-0001-0001-0001-000000000054",
        "title_uz":       "Yil yakunlash sport kechasi",
        "title_ru":       "Спортивный вечер подведения итогов года",
        "title_en":       "Year-End Sports Gala",
        "description_uz": "Yilning eng yaxshi sportchilari va murabbiylarini taqdirlash marosimi.",
        "description_ru": "Церемония награждения лучших спортсменов и тренеров года.",
        "description_en": "Award ceremony for the best athletes and coaches of the year.",
        "location_uz":    "Akademiya aktyorlik zali",
        "location_ru":    "Актовый зал академии",
        "location_en":    "Academy auditorium",
        "event_date":     "2025-12-20",
        "order":          8,
    },
]


class Command(BaseCommand):
    help = "Sport faoliyat sahifasi: statistika, yo'nalishlar va tadbirlarni DB ga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Mavjud barcha Sport* datalarni o'chiradi")

    def handle(self, *args, **options):
        if options['clear']:
            SportStat.objects.all().delete()
            SportYonalish.objects.all().delete()
            SportTadbir.objects.all().delete()
            self.stdout.write(self.style.WARNING("Mavjud sport bo'lim ma'lumotlari o'chirildi."))

        self.stdout.write("\n--- STATISTIKA ---")
        for d in STATS:
            obj, created = SportStat.objects.update_or_create(
                id=uuid.UUID(d['id']),
                defaults={k: v for k, v in d.items() if k != 'id'},
            )
            self.stdout.write(f"  [{'Yaratildi' if created else 'Yangilandi'}] {obj.value}{obj.suffix} — {obj.title_uz}")

        self.stdout.write("\n--- YO'NALISHLAR ---")
        for d in YONALISHLAR:
            obj, created = SportYonalish.objects.update_or_create(
                id=uuid.UUID(d['id']),
                defaults={k: v for k, v in d.items() if k != 'id'},
            )
            self.stdout.write(f"  [{'Yaratildi' if created else 'Yangilandi'}] {obj.title_uz}")

        self.stdout.write("\n--- TADBIRLAR ---")
        for d in TADBIRLAR:
            obj, created = SportTadbir.objects.update_or_create(
                id=uuid.UUID(d['id']),
                defaults={k: v for k, v in d.items() if k != 'id'},
            )
            self.stdout.write(f"  [{'Yaratildi' if created else 'Yangilandi'}] {obj.event_date} — {obj.title_uz}")

        self.stdout.write(self.style.SUCCESS(
            f"\nJami: {len(STATS)} stat | {len(YONALISHLAR)} yo'nalish | {len(TADBIRLAR)} tadbir!"
        ))
