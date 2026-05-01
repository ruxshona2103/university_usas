from django.core.management.base import BaseCommand
from domains.pages.models import ContactLocation

DATA = [
    {
        'order': 1,
        'title_uz': 'Bosh ofis',
        'title_ru': 'Главный офис',
        'title_en': 'Main Office',
        'address_uz': "Toshkent sh, Yashnobod, Yangi O'zbekiston ko'chasi, Olimpiya shaharchasi. O'zbekiston davlat sport akademiyasi",
        'address_ru': 'г. Ташкент, Яшнободский район, улица Новый Узбекистан, Олимпийский городок. Государственная академия спорта Узбекистана',
        'address_en': 'Tashkent city, Yashnobod district, New Uzbekistan street, Olympic village. Uzbekistan State Sports Academy',
        'phone': '+998777317972',
        'email': 'info@usas.uz',
        'is_active': True,
    },
    {
        'order': 2,
        'title_uz': 'Qabul komissiyasi',
        'title_ru': 'Приёмная комиссия',
        'title_en': 'Admissions Committee',
        'address_uz': "Toshkent sh, Yashnobod, Yangi O'zbekiston ko'chasi, Olimpiya shaharchasi. O'zbekiston davlat sport akademiyasi",
        'address_ru': 'г. Ташкент, Яшнободский район, улица Новый Узбекистан, Олимпийский городок. Государственная академия спорта Узбекистана',
        'address_en': 'Tashkent city, Yashnobod district, New Uzbekistan street, Olympic village. Uzbekistan State Sports Academy',
        'phone': '+998777317972',
        'email': 'info@usas.uz',
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = "Aloqa joylari (Bosh ofis, Qabul komissiyasi) ma'lumotlarini yuklaydi"

    def handle(self, *args, **options):
        for d in DATA:
            obj, created = ContactLocation.objects.update_or_create(
                title_uz=d['title_uz'],
                defaults=d,
            )
            action = 'yaratildi' if created else 'yangilandi'
            self.stdout.write(self.style.SUCCESS(f"  {obj.order}. {obj.title_uz} — {action}"))

        self.stdout.write(self.style.SUCCESS(f"\nJami: {len(DATA)} ta aloqa joyi"))
