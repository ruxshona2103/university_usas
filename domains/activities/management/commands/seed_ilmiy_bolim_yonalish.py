"""
IlmiyYonalish modeliga 'ilmiy-bolim' slug bilan yozuv qo'shadi.
Frontend /page/ilmiy-yonalishlar/ilmiy-bolim URL uchun.

Mazmun: avvalgi IlmiyBolim (singleton) ma'lumotlarini IlmiyYonalishItem'larga
ko'chiradi.
"""
from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyYonalish, IlmiyYonalishItem


YONALISH = {
    "name_uz": "Ilmiy bo'lim",
    "name_ru": "Научный отдел",
    "name_en": "Scientific Department",
    "slug": "ilmiy-bolim",
    "order": 100,
}

# IlmiyBolim API'dagi yo'nalishlar — 5 ta vazifa
ITEMS = [
    {
        "name_uz": "Ilmiy loyihalar va grant dasturlarini rejalashtirish",
        "name_ru": "Планирование научных проектов и грантовых программ",
        "name_en": "Planning scientific projects and grant programs",
        "description_uz": "Ilmiy loyihalar va grant dasturlarini rejalashtirish hamda monitoring qilish, samaradorlikni baholash.",
        "description_ru": "Планирование и мониторинг научных проектов и грантовых программ, оценка эффективности.",
        "description_en": "Planning and monitoring scientific projects and grant programs, performance assessment.",
        "order": 1,
    },
    {
        "name_uz": "Nashr faoliyatini qo'llab-quvvatlash",
        "name_ru": "Поддержка публикационной деятельности",
        "name_en": "Support for publication activity",
        "description_uz": "Professor-o'qituvchilar va tadqiqotchilar nashr faoliyatini qo'llab-quvvatlash, xalqaro jurnallarda chop etishga ko'maklashish.",
        "description_ru": "Поддержка публикационной деятельности профессорско-преподавательского состава.",
        "description_en": "Supporting the publication activity of professors and researchers.",
        "order": 2,
    },
    {
        "name_uz": "Ilmiy konferensiya, seminar va forumlarni tashkil etish",
        "name_ru": "Организация научных конференций, семинаров и форумов",
        "name_en": "Organizing scientific conferences, seminars and forums",
        "description_uz": "Respublika va xalqaro miqyosdagi ilmiy tadbirlarni tashkil etish va ularda ishtirokni ta'minlash.",
        "description_ru": "Организация научных мероприятий республиканского и международного масштаба.",
        "description_en": "Organizing scientific events at national and international levels.",
        "order": 3,
    },
    {
        "name_uz": "Yosh olimlar va doktorantlar bilan tizimli ishlash",
        "name_ru": "Системная работа с молодыми учёными и докторантами",
        "name_en": "Systematic work with young scientists and doctoral students",
        "description_uz": "Yosh olimlar va doktorantlar bilan tizimli ishlash, ilmiy tadqiqotlar uchun shart-sharoit yaratish.",
        "description_ru": "Системная работа с молодыми учёными, создание условий для научных исследований.",
        "description_en": "Systematic work with young scientists, creating conditions for scientific research.",
        "order": 4,
    },
    {
        "name_uz": "Ilmiy natijalarni tijoratlashtirish",
        "name_ru": "Коммерциализация научных результатов",
        "name_en": "Commercialization of scientific results",
        "description_uz": "Ilmiy natijalarni tijoratlashtirish va innovatsiyalarni ommalashtirish, sanoat va sport bilan hamkorlik.",
        "description_ru": "Коммерциализация научных результатов и популяризация инноваций.",
        "description_en": "Commercializing scientific results and popularizing innovations.",
        "order": 5,
    },
]


class Command(BaseCommand):
    help = "IlmiyYonalish'ga 'ilmiy-bolim' slug bilan yozuv qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Avval o'chirib qayta yozish")

    def handle(self, *args, **options):
        clear = options.get("clear", False)

        # Parent
        yonalish, created = IlmiyYonalish.objects.update_or_create(
            slug=YONALISH["slug"],
            defaults={
                "name_uz": YONALISH["name_uz"],
                "name_ru": YONALISH["name_ru"],
                "name_en": YONALISH["name_en"],
                "order": YONALISH["order"],
                "is_active": True,
            },
        )
        self.stdout.write(self.style.SUCCESS(
            f"Yo'nalish: {yonalish.name_uz} ({'yaratildi' if created else 'yangilandi'})"
        ))

        if clear:
            yonalish.items.all().delete()
            self.stdout.write(self.style.WARNING("Eski items o'chirildi"))

        # Items
        for item in ITEMS:
            obj, created = IlmiyYonalishItem.objects.update_or_create(
                yonalish=yonalish,
                name_uz=item["name_uz"],
                defaults={
                    "name_ru": item["name_ru"],
                    "name_en": item["name_en"],
                    "description_uz": item["description_uz"],
                    "description_ru": item["description_ru"],
                    "description_en": item["description_en"],
                    "order": item["order"],
                    "is_active": True,
                },
            )
            self.stdout.write(self.style.SUCCESS(
                f"  Item: {obj.name_uz[:50]} ({'+' if created else '~'})"
            ))

        self.stdout.write(self.style.SUCCESS("\nSeed yakunlandi!"))
        self.stdout.write(
            f"URL: /page/ilmiy-yonalishlar/{yonalish.slug}\n"
            f"API: /api/ilmiy-yonalishlar/{yonalish.slug}/?lang=uz"
        )
