"""
python manage.py seed_qabul
python manage.py seed_qabul --clear
"""
from django.core.management.base import BaseCommand
from domains.qabul.models import (
    QabulBolim, QabulBolimItem,
    QabulKomissiyaTarkibi,
    QabulKuni,
    CallCenter,
    QabulNarx,
    QabulHujjat,
)

BOLIMLAR = [
    {
        'slug': 'qabul-komissiyasi',
        'bolim_type': 'komissiya',
        'title_uz': 'Qabul komissiyasi',
        'title_ru': 'Приёмная комиссия',
        'title_en': 'Admission Committee',
        'description_uz': 'Qabul komissiyasi haqida ma\'lumot',
        'order': 1,
        'items': [],
    },
    {
        'slug': 'bakalavr',
        'bolim_type': 'bakalavr',
        'title_uz': 'Bakalavr',
        'title_ru': 'Бакалавриат',
        'title_en': 'Bachelor',
        'description_uz': 'Bakalavr ta\'lim yo\'nalishlariga qabul',
        'order': 2,
        'items': [
            {'item_type': 'text', 'title_uz': 'Abituriyentlar uchun qo\'llanma', 'order': 1},
            {'item_type': 'text', 'title_uz': 'Imtiyozlar', 'order': 2},
            {'item_type': 'text', 'title_uz': 'O\'tish ballari', 'order': 3},
            {'item_type': 'text', 'title_uz': 'Test-sinovlari fanlar', 'order': 4},
            {'item_type': 'text', 'title_uz': 'Shartnomalar', 'order': 5},
        ],
    },
    {
        'slug': 'magistratura',
        'bolim_type': 'magistratura',
        'title_uz': 'Magistratura',
        'title_ru': 'Магистратура',
        'title_en': 'Master\'s',
        'description_uz': 'Magistratura ta\'lim yo\'nalishlariga qabul',
        'order': 3,
        'items': [
            {'item_type': 'text', 'title_uz': 'Qabul rejasi', 'order': 1},
            {'item_type': 'text', 'title_uz': 'Hujjat topshirish', 'order': 2},
            {'item_type': 'text', 'title_uz': 'Hujjatlar to\'plami', 'order': 3},
            {'item_type': 'text', 'title_uz': 'Magistratura natijalari', 'order': 4},
        ],
    },
    {
        'slug': 'xorijiy-talabalar',
        'bolim_type': 'xorijiy',
        'title_uz': 'Xorijiy talabalar',
        'title_ru': 'Иностранные студенты',
        'title_en': 'Foreign Students',
        'description_uz': 'Xorijiy talabalar uchun qabul ma\'lumotlari',
        'order': 4,
        'items': [
            {'item_type': 'text', 'title_uz': 'Ariza yuborish', 'order': 1},
            {'item_type': 'text', 'title_uz': 'Bakalavr ta\'lim yo\'nalishlari', 'order': 2},
            {'item_type': 'text', 'title_uz': 'Magistratura ta\'lim yo\'nalishlari', 'order': 3},
            {'item_type': 'text', 'title_uz': 'Shartnomalar', 'order': 4},
            {'item_type': 'text', 'title_uz': 'Kontrakt narxlari', 'order': 5},
        ],
    },
    {
        'slug': 'talabalar-turar-joyi',
        'bolim_type': 'turar_joy',
        'title_uz': 'Talabalar turar joyi',
        'title_ru': 'Общежитие',
        'title_en': 'Student Dormitory',
        'description_uz': 'Talabalar uchun yotoqxona ijara to\'lovlari va ma\'lumotlari',
        'order': 5,
        'items': [
            {'item_type': 'text', 'title_uz': 'Yotoqxona ijara to\'lovlari', 'order': 1},
        ],
    },
]

CALL_CENTER = [
    {
        'phone': '+998 71 236 60 40',
        'label_uz': 'Qabul bo\'limi',
        'label_ru': 'Приёмная комиссия',
        'label_en': 'Admission Office',
        'working_hours_uz': 'Du-Ju: 09:00-18:00',
        'order': 1,
    },
]

QABUL_KUNLARI = [
    {
        'qabul_type': 'bakalavr',
        'title_uz': 'Hujjat qabul qilish',
        'title_ru': 'Приём документов',
        'title_en': 'Document Submission',
        'order': 1,
    },
    {
        'qabul_type': 'magistratura',
        'title_uz': 'Hujjat qabul qilish',
        'title_ru': 'Приём документов',
        'title_en': 'Document Submission',
        'order': 1,
    },
]

HUJJATLAR = [
    {'hujjat_type': 'bakalavr', 'title_uz': 'Pasport nusxasi', 'order': 1},
    {'hujjat_type': 'bakalavr', 'title_uz': 'Attestat (maktab tugallash)', 'order': 2},
    {'hujjat_type': 'bakalavr', 'title_uz': '3x4 fotosurat (6 dona)', 'order': 3},
    {'hujjat_type': 'magistratura', 'title_uz': 'Bakalavr diplomi nusxasi', 'order': 1},
    {'hujjat_type': 'magistratura', 'title_uz': 'Pasport nusxasi', 'order': 2},
    {'hujjat_type': 'xorijiy', 'title_uz': 'Passport copy', 'order': 1},
    {'hujjat_type': 'xorijiy', 'title_uz': 'Educational certificate', 'order': 2},
]


class Command(BaseCommand):
    help = "Qabul bo'limi uchun seed ma'lumotlar"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            QabulBolim.objects.all().delete()
            QabulKomissiyaTarkibi.objects.all().delete()
            QabulKuni.objects.all().delete()
            CallCenter.objects.all().delete()
            QabulNarx.objects.all().delete()
            QabulHujjat.objects.all().delete()
            self.stdout.write(self.style.WARNING("Barcha qabul ma'lumotlari o'chirildi"))

        for data in BOLIMLAR:
            items = data.pop('items', [])
            bolim, created = QabulBolim.objects.update_or_create(
                slug=data['slug'],
                defaults=data,
            )
            for item_data in items:
                QabulBolimItem.objects.get_or_create(
                    bolim=bolim,
                    title_uz=item_data['title_uz'],
                    defaults=item_data,
                )
            self.stdout.write(self.style.SUCCESS(f"[{'+'if created else '~'}] Bo'lim: {bolim.title_uz}"))

        for data in CALL_CENTER:
            obj, created = CallCenter.objects.update_or_create(
                phone=data['phone'],
                defaults=data,
            )
            self.stdout.write(self.style.SUCCESS(f"[{'+'if created else '~'}] CallCenter: {obj.phone}"))

        for data in QABUL_KUNLARI:
            obj, created = QabulKuni.objects.get_or_create(
                qabul_type=data['qabul_type'],
                title_uz=data['title_uz'],
                defaults=data,
            )
            self.stdout.write(self.style.SUCCESS(f"[{'+'if created else '~'}] Qabul kuni: {obj}"))

        for data in HUJJATLAR:
            obj, created = QabulHujjat.objects.get_or_create(
                hujjat_type=data['hujjat_type'],
                title_uz=data['title_uz'],
                defaults=data,
            )
            self.stdout.write(self.style.SUCCESS(f"[{'+'if created else '~'}] Hujjat: {obj.title_uz}"))
