"""
python manage.py seed_rekvizit
"""
from django.core.management.base import BaseCommand

from domains.pages.models import Rekvizit


DATA = {
    "org_name_uz": "O'zbekiston Davlat Sport Akademiyasi",
    "org_name_ru": "Государственная спортивная академия Узбекистана",
    "org_name_en": "Uzbekistan State Sports Academy",
    "org_short_name": "O'ZDSA",
    "email_1": "info@usas.uz",
    "email_2": "akademiyasport@exat.uz",
    "phone_1": "+99877737971",
    "phone_2": "+998777317972",
    "postal_code": "111709",
    "address_uz": (
        "111709, Toshkent shahri, Yashnobod tumani, Yangi O'zbekiston ko'chasi, "
        "Olimpiya shaharchasi. O'zbekiston davlat sport akademiyasi"
    ),
    "address_ru": (
        "111709, г. Ташкент, Яшнободский район, улица Янги Узбекистан, "
        "Олимпийский городок. Государственная спортивная академия Узбекистана"
    ),
    "address_en": (
        "111709, Tashkent city, Yashnobod district, Yangi O'zbekiston street, "
        "Olympic Village. Uzbekistan State Sports Academy"
    ),
}


class Command(BaseCommand):
    help = "Tashkilot rekvizitlarini seed qiladi"

    def handle(self, *args, **options):
        obj, created = Rekvizit.objects.update_or_create(
            pk=Rekvizit.SINGLETON_PK,
            defaults=DATA,
        )
        action = "Yaratildi" if created else "Yangilandi"
        self.stdout.write(self.style.SUCCESS(
            f"{action}: {obj.org_short_name} rekvizitlari saqlandi."
        ))
