"""
python manage.py seed_tashkiliy_tuzilma
python manage.py seed_tashkiliy_tuzilma --clear
"""
from django.core.management.base import BaseCommand

from domains.academic.models import TashkiliyTuzilmaItem


ITEMS = [
    {
        "slug": "sport-ilmiy-tadqiqotlar-instituti",
        "text_uz": "Jismoniy tarbiya va sport ilmiy tadqiqotlar instituti",
        "text_ru": "Научно-исследовательский институт физической культуры и спорта",
        "text_en": "Research Institute of Physical Culture and Sports",
        "order": 1,
        "is_active": True,
    },
    {
        "slug": "qayta-tayyorlash-va-malakani-oshirish-instituti",
        "text_uz": "Jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish instituti hamda uning Nukus, Samarqand va Farg'ona filiallari",
        "text_ru": "Институт переподготовки и повышения квалификации специалистов по физической культуре и спорту и его филиалы в Нукусе, Самарканде и Фергане",
        "text_en": "Institute for Retraining and Advanced Training of Physical Culture and Sports Specialists and its branches in Nukus, Samarkand and Fergana",
        "order": 2,
        "is_active": True,
    },
    {
        "slug": "ozbekiston-tarixi-va-xorijiy-tillar-markazi",
        "text_uz": "O'zbekiston tarixi va xorijiy tillarni o'qitish markazi",
        "text_ru": "Центр преподавания истории Узбекистана и иностранных языков",
        "text_en": "Centre for Teaching History of Uzbekistan and Foreign Languages",
        "order": 3,
        "is_active": True,
    },
    {
        "slug": "davlat-sport-tibbiyoti-markazi",
        "text_uz": "Davlat sport tibbiyoti ilmiy amaliy markazi",
        "text_ru": "Государственный научно-практический центр спортивной медицины",
        "text_en": "State Scientific and Practical Centre of Sports Medicine",
        "order": 4,
        "is_active": True,
    },
]


class Command(BaseCommand):
    help = "Tashkiliy tuzilma uchun 4 ta asosiy blokni seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Avval eski yozuvlarni o'chiradi")

    def handle(self, *args, **options):
        if options["clear"]:
            n = TashkiliyTuzilmaItem.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        created = 0
        updated = 0
        for item in ITEMS:
            obj, is_new = TashkiliyTuzilmaItem.objects.update_or_create(
                slug=item["slug"],
                defaults=item,
            )
            if is_new:
                created += 1
            else:
                updated += 1
            self.stdout.write(f"  [{'+' if is_new else '~'}] {obj.slug}")

        self.stdout.write(self.style.SUCCESS(f"Natija: {created} yangi, {updated} yangilandi"))
