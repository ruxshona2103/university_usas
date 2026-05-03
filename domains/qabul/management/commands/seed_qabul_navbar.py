"""
python manage.py seed_qabul_navbar
python manage.py seed_qabul_navbar --clear
"""
from django.core.management.base import BaseCommand
from domains.qabul.models import QabulNavbar, QabulNavbarItem

NAVBAR_DATA = [
    {
        'slug': 'qabul-komissiyasi',
        'title_uz': 'Qabul komissiyasi',
        'title_ru': 'Приёмная комиссия',
        'title_en': 'Admission Committee',
        'page_url': '/qabul/qabul-komissiyasi',
        'order': 1,
        'items': [
            {
                'slug': 'admission-news',
                'title_uz': 'Yangiliklar',
                'title_ru': 'Новости',
                'title_en': 'News',
                'page_url': '/qabul/qabul-komissiyasi/yangiliklar',
                'order': 1,
            },
            {
                'slug': 'admission-commission',
                'title_uz': 'Qabul komissiya tarkibi',
                'title_ru': 'Состав комиссии',
                'title_en': 'Commission members',
                'page_url': '/qabul/qabul-komissiyasi/tarkib',
                'order': 2,
            },
            {
                'slug': 'admission-regulations',
                'title_uz': "Me'yoriy hujjatlar",
                'title_ru': 'Нормативные документы',
                'title_en': 'Regulations',
                'page_url': '/qabul/qabul-komissiyasi/meyoriy-hujjatlar',
                'order': 3,
            },
            {
                'slug': 'admission-days',
                'title_uz': 'Qabul kunlari',
                'title_ru': 'Дни приёма',
                'title_en': 'Admission days',
                'page_url': '/qabul/qabul-komissiyasi/qabul-kunlari',
                'order': 4,
            },
            {
                'slug': 'call-center',
                'title_uz': 'Call-center',
                'title_ru': 'Call-center',
                'title_en': 'Call-center',
                'page_url': '/qabul/qabul-komissiyasi/call-center',
                'order': 5,
            },
        ],
    },
    {
        'slug': 'bakalavr',
        'title_uz': 'Bakalavr',
        'title_ru': 'Бакалавриат',
        'title_en': 'Bachelor',
        'page_url': '/qabul/bakalavr',
        'order': 2,
        'items': [
            {
                'slug': 'applicant-guide',
                'title_uz': "Abituriyentlar uchun qo'llanma",
                'title_ru': 'Руководство для абитуриентов',
                'title_en': "Applicant's guide",
                'page_url': '/qabul/bakalavr/qollanma',
                'order': 1,
            },
            {
                'slug': 'recommended-applicants',
                'title_uz': 'Tavsiyanomaga ega abituriyentlar',
                'title_ru': 'Абитуриенты с рекомендацией',
                'title_en': 'Recommended applicants',
                'page_url': '/qabul/bakalavr/tavsiyalar',
                'order': 2,
            },
            {
                'slug': 'personal-documents',
                'title_uz': "Shaxsiy yig'ma jild hujjatlari",
                'title_ru': 'Личное дело (документы)',
                'title_en': 'Personal documents',
                'page_url': '/qabul/bakalavr/hujjatlar',
                'order': 3,
            },
            {
                'slug': 'admission-privileges',
                'title_uz': 'Imtiyozlar',
                'title_ru': 'Льготы',
                'title_en': 'Privileges',
                'page_url': '/qabul/bakalavr/imtiyozlar',
                'order': 4,
            },
            {
                'slug': 'passing-scores',
                'title_uz': "O'tish ballari",
                'title_ru': 'Проходные баллы',
                'title_en': 'Passing scores',
                'page_url': '/qabul/bakalavr/otish-ballari',
                'order': 5,
            },
            {
                'slug': 'test-subjects',
                'title_uz': 'Test-sinovlari fanlari',
                'title_ru': 'Предметы тест-экзаменов',
                'title_en': 'Test subjects',
                'page_url': '/qabul/bakalavr/test-fanlar',
                'order': 6,
            },
            {
                'slug': 'transfer',
                'title_uz': "O'qishni ko'chirish",
                'title_ru': 'Перевод',
                'title_en': 'Transfer',
                'page_url': '/qabul/bakalavr/kochirish',
                'order': 7,
            },
            {
                'slug': 'visually-impaired',
                'title_uz': "Ko'zi ojiz abituriyentlar uchun",
                'title_ru': 'Для слабовидящих',
                'title_en': 'Visually impaired',
                'page_url': '/qabul/bakalavr/kozi-ojizlar',
                'order': 8,
            },
            {
                'slug': 'college-graduates',
                'title_uz': 'Texnikum bitiruvchilari',
                'title_ru': 'Выпускники техникумов',
                'title_en': 'College graduates',
                'page_url': '/qabul/bakalavr/texnikum',
                'order': 9,
            },
            {
                'slug': 'second-degree',
                'title_uz': "Ikkinchi oliy ta'lim",
                'title_ru': 'Второе высшее образование',
                'title_en': 'Second degree',
                'page_url': "/qabul/bakalavr/ikkinchi-oliy",
                'order': 10,
            },
            {
                'slug': 'admission-contracts',
                'title_uz': 'Shartnomalar',
                'title_ru': 'Договоры',
                'title_en': 'Contracts',
                'page_url': '/qabul/bakalavr/shartnomalar',
                'order': 11,
            },
            {
                'slug': 'increased-contract',
                'title_uz': "Oshirilgan to'lov-shartnomasi",
                'title_ru': 'Повышенный договор оплаты',
                'title_en': 'Increased contract',
                'page_url': "/qabul/bakalavr/oshirilgan-shartnoma",
                'order': 12,
            },
            {
                'slug': 'admission-contract-prices',
                'title_uz': 'Kontrakt narxlari',
                'title_ru': 'Стоимость контракта',
                'title_en': 'Contract prices',
                'page_url': '/qabul/bakalavr/kontrakt-narxlari',
                'order': 13,
            },
            {
                'slug': 'bachelor-results',
                'title_uz': 'Bakalavr natijalari',
                'title_ru': 'Результаты бакалавриата',
                'title_en': 'Bachelor results',
                'page_url': '/qabul/bakalavr/natijalar',
                'order': 14,
            },
            {
                'slug': 'exam-schedule',
                'title_uz': 'Kasbiy imtihonlar jadvali',
                'title_ru': 'Расписание профессиональных экзаменов',
                'title_en': 'Exam schedule',
                'page_url': '/qabul/bakalavr/imtihon-jadvali',
                'order': 15,
            },
        ],
    },
    {
        'slug': 'magistratura',
        'title_uz': 'Magistratura',
        'title_ru': 'Магистратура',
        'title_en': "Master's",
        'page_url': '/qabul/magistratura',
        'order': 3,
        'items': [
            {
                'slug': 'masters-admission-plan',
                'title_uz': 'Qabul rejasi',
                'title_ru': 'План приёма',
                'title_en': 'Admission plan',
                'page_url': '/qabul/magistratura/qabul-rejasi',
                'order': 1,
            },
            {
                'slug': 'masters-documents',
                'title_uz': 'Hujjat topshirish',
                'title_ru': 'Подача документов',
                'title_en': 'Document submission',
                'page_url': '/qabul/magistratura/hujjat-topshirish',
                'order': 2,
            },
            {
                'slug': 'personal-documents-m',
                'title_uz': "Hujjatlar to'plami",
                'title_ru': 'Пакет документов',
                'title_en': 'Documents package',
                'page_url': "/qabul/magistratura/hujjatlar-toplami",
                'order': 3,
            },
            {
                'slug': 'masters-results',
                'title_uz': 'Magistratura natijalari',
                'title_ru': 'Результаты магистратуры',
                'title_en': 'Masters results',
                'page_url': '/qabul/magistratura/natijalar',
                'order': 4,
            },
        ],
    },
    {
        'slug': 'xorijiy-talabalar',
        'title_uz': 'Xorijiy talabalar',
        'title_ru': 'Иностранные студенты',
        'title_en': 'Foreign Students',
        'page_url': '/qabul/xorijiy-talabalar',
        'order': 4,
        'items': [
            {
                'slug': 'foreign-students-apply',
                'title_uz': 'Ariza yuborish',
                'title_ru': 'Подать заявку',
                'title_en': 'Apply',
                'page_url': '/qabul/xorijiy-talabalar/ariza',
                'order': 1,
            },
            {
                'slug': 'foreign-bachelor',
                'title_uz': "Bakalavr ta'lim yo'nalishlari",
                'title_ru': 'Направления бакалавриата',
                'title_en': 'Bachelor programs',
                'page_url': "/qabul/xorijiy-talabalar/bakalavr-yunalishlari",
                'order': 2,
            },
            {
                'slug': 'foreign-masters',
                'title_uz': "Magistratura ta'lim yo'nalishlari",
                'title_ru': 'Направления магистратуры',
                'title_en': 'Masters programs',
                'page_url': "/qabul/xorijiy-talabalar/magistratura-yunalishlari",
                'order': 3,
            },
            {
                'slug': 'foreign-contracts',
                'title_uz': 'Shartnomalar',
                'title_ru': 'Договоры',
                'title_en': 'Contracts',
                'page_url': '/qabul/xorijiy-talabalar/shartnomalar',
                'order': 4,
            },
            {
                'slug': 'increased-contract-f',
                'title_uz': "Oshirilgan to'lov-shartnomasi",
                'title_ru': 'Повышенный договор',
                'title_en': 'Increased contract',
                'page_url': "/qabul/xorijiy-talabalar/oshirilgan-shartnoma",
                'order': 5,
            },
            {
                'slug': 'foreign-contract-prices',
                'title_uz': 'Kontrakt narxlari',
                'title_ru': 'Стоимость контракта',
                'title_en': 'Contract prices',
                'page_url': '/qabul/xorijiy-talabalar/kontrakt-narxlari',
                'order': 6,
            },
        ],
    },
    {
        'slug': 'talabalar-turar-joyi',
        'title_uz': 'Talabalar turar joyi',
        'title_ru': 'Общежитие',
        'title_en': 'Student Dormitory',
        'page_url': '/qabul/talabalar-turar-joyi',
        'order': 5,
        'items': [
            {
                'slug': 'dormitory',
                'title_uz': "Talabalar uchun yotoqxona ijara to'lovlari",
                'title_ru': 'Аренда общежития для студентов',
                'title_en': 'Dormitory rental fees',
                'page_url': "/qabul/talabalar-turar-joyi/ijara-tolovlari",
                'order': 1,
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Qabul navbar seed (page_url bilan)"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Barcha navbar ma'lumotlarini o'chirish")

    def handle(self, *args, **options):
        if options['clear']:
            QabulNavbar.objects.all().delete()
            self.stdout.write(self.style.WARNING("Qabul navbar o'chirildi"))

        for data in NAVBAR_DATA:
            items = data.pop('items', [])
            navbar, created = QabulNavbar.objects.update_or_create(
                slug=data['slug'],
                defaults=data,
            )
            for item_data in items:
                QabulNavbarItem.objects.update_or_create(
                    navbar=navbar,
                    slug=item_data['slug'],
                    defaults=item_data,
                )
            self.stdout.write(self.style.SUCCESS(
                f"[{'+'if created else '~'}] {navbar.title_uz} | {navbar.page_url} ({navbar.items.count()} item)"
            ))
