"""
python manage.py seed_events          # yaratadi (slug bo'yicha idempotent)
python manage.py seed_events --clear  # barcha eventlarni o'chirib qaytadan yozadi
"""
from datetime import datetime, timezone as dt_timezone
from django.core.management.base import BaseCommand
from domains.news.models import Event

_UTC = dt_timezone.utc

EVENTS = [
    {
        "slug": "magistratura-talabalari-uchun-trening-2025",
        "date": datetime(2025, 10, 29, 14, 0, 0, tzinfo=_UTC),
        "start_time": datetime(2025, 10, 29, 14, 0, 0, tzinfo=_UTC),
        "title_uz": "Magistratura talabalari uchun trening",
        "title_ru": "Тренинг для магистрантов",
        "title_en": "Training for Master's Students",
        "tavsif_uz": "«Konstruktiv hamkorlik va samarali jamoani shakllantirish» mavzusida interaktiv trening",
        "tavsif_ru": "Интерактивный тренинг «Конструктивное сотрудничество и формирование эффективной команды»",
        "tavsif_en": "Interactive training on \"Constructive Cooperation and Building an Effective Team\"",
        "description_uz": """Hurmatli magistrantlar!

Sizlarni "Konstruktiv hamkorlik va samarali jamoani shakllantirish" mavzusida tashkil etilayotgan treningga taklif qilamiz.

TRENING DAVOMIDA QUYIDAGI MAVZULAR YORITILADI:

• Jamoada samarali muloqot asoslari
• Hamkorlikni kuchaytirish yo'llari
• Konfliktlarni boshqarish
• Jamoa ruhini ko'tarish texnikalari
• Amaliy mashg'ulotlar va jamoaviy o'yinlar

Trening interaktiv shaklda bo'lib, sizga real hayotiy vaziyatlarda qanday ishlashni o'rgatadi. Trening tajribali trener tomonidan olib boriladi.

O'z vaqtida kelishingiz so'raladi. Treningda ishtirok etib, o'z jamoaviy ko'nikmalaringizni yanada mustahkamlab oling!""",
        "description_ru": """Уважаемые магистранты!

Приглашаем вас на тренинг по теме «Конструктивное сотрудничество и формирование эффективной команды».

В ХОДЕ ТРЕНИНГА БУДУТ РАССМОТРЕНЫ СЛЕДУЮЩИЕ ТЕМЫ:

• Основы эффективного общения в команде
• Пути укрепления сотрудничества
• Управление конфликтами
• Техники повышения командного духа
• Практические занятия и командные игры

Тренинг проходит в интерактивной форме и научит вас работать в реальных жизненных ситуациях. Тренинг проводится опытным тренером.

Просим прийти вовремя. Участвуя в тренинге, укрепите свои командные навыки!""",
        "description_en": """Dear master's students!

We invite you to a training on the topic "Constructive Cooperation and Building an Effective Team".

TOPICS TO BE COVERED:

• Fundamentals of effective team communication
• Ways to strengthen cooperation
• Conflict management
• Team spirit building techniques
• Practical exercises and team games

The training is interactive and will teach you how to work in real-life situations. The training will be conducted by an experienced trainer.

Please arrive on time. Join the training and strengthen your teamwork skills!""",
        "location_uz": "Olimpiya shaharchasi, O'ZDSA binosi, 1-qavat, 147-xona",
        "location_ru": "Олимпийская деревня, здание ГОСФКА, 1 этаж, кабинет 147",
        "location_en": "Olympic Village, USAS building, 1st floor, room 147",
        "article_type": "event",
        "is_published": True,
    },
]


class Command(BaseCommand):
    help = "Eventlarni seed qiladi (slug bo'yicha idempotent)"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = Event.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta event"))

        created = updated = 0
        for data in EVENTS:
            slug = data.pop('slug')
            obj, is_new = Event.objects.update_or_create(slug=slug, defaults=data)
            data['slug'] = slug  # restore for next run
            if is_new:
                created += 1
                self.stdout.write(f"  [+] {obj.title_uz}")
            else:
                updated += 1
                self.stdout.write(f"  [~] {obj.title_uz}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created} yangi, {updated} yangilandi."
        ))
