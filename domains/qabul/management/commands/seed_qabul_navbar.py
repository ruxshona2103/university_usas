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
        'order': 1,
        'items': [
            {'slug': 'admission-news',       'title_uz': 'Yangiliklar',               'title_ru': 'Новости',                    'title_en': 'News',                  'order': 1},
            {'slug': 'admission-commission', 'title_uz': 'Qabul komissiya tarkibi',   'title_ru': 'Состав комиссии',            'title_en': 'Commission members',    'order': 2},
            {'slug': 'admission-regulations','title_uz': "Me'yoriy hujjatlar",         'title_ru': 'Нормативные документы',      'title_en': 'Regulations',           'order': 3},
            {'slug': 'admission-days',       'title_uz': 'Qabul kunlari',             'title_ru': 'Дни приёма',                 'title_en': 'Admission days',        'order': 4},
            {'slug': 'call-center',          'title_uz': 'Call-center',               'title_ru': 'Call-center',                'title_en': 'Call-center',           'order': 5},
        ],
    },
    {
        'slug': 'bakalavr',
        'title_uz': 'Bakalavr',
        'title_ru': 'Бакалавриат',
        'title_en': 'Bachelor',
        'order': 2,
        'items': [
            {'slug': 'applicant-guide',       'title_uz': "Abituriyentlar uchun qo'llanma",       'title_ru': 'Руководство для абитуриентов',   'title_en': "Applicant's guide",        'order': 1},
            {'slug': 'recommended-applicants','title_uz': 'Tavsiyanomaga ega abituriyentlar',      'title_ru': 'Абитуриенты с рекомендацией',    'title_en': 'Recommended applicants',   'order': 2},
            {'slug': 'personal-documents',    'title_uz': "Shaxsiy yig'ma jild hujjatlari",        'title_ru': 'Личное дело (документы)',         'title_en': 'Personal documents',       'order': 3},
            {'slug': 'admission-privileges',  'title_uz': 'Imtiyozlar',                            'title_ru': 'Льготы',                         'title_en': 'Privileges',               'order': 4},
            {'slug': 'passing-scores',        'title_uz': "O'tish ballari",                         'title_ru': 'Проходные баллы',                'title_en': 'Passing scores',           'order': 5},
            {'slug': 'test-subjects',         'title_uz': 'Test-sinovlari fanlari',                'title_ru': 'Предметы тест-экзаменов',         'title_en': 'Test subjects',            'order': 6},
            {'slug': 'transfer',              'title_uz': "O'qishni ko'chirish",                    'title_ru': 'Перевод',                        'title_en': 'Transfer',                 'order': 7},
            {'slug': 'visually-impaired',     'title_uz': "Ko'zi ojiz abituriyentlar uchun",        'title_ru': 'Для слабовидящих',               'title_en': 'Visually impaired',        'order': 8},
            {'slug': 'college-graduates',     'title_uz': 'Texnikum bitiruvchilari',               'title_ru': 'Выпускники техникумов',           'title_en': 'College graduates',        'order': 9},
            {'slug': 'second-degree',         'title_uz': "Ikkinchi oliy ta'lim",                   'title_ru': 'Второе высшее образование',       'title_en': 'Second degree',            'order': 10},
            {'slug': 'admission-contracts',   'title_uz': 'Shartnomalar',                          'title_ru': 'Договоры',                       'title_en': 'Contracts',                'order': 11},
            {'slug': 'increased-contract',    'title_uz': "Oshirilgan to'lov-shartnomasi",          'title_ru': 'Повышенный договор оплаты',       'title_en': 'Increased contract',       'order': 12},
            {'slug': 'admission-contract-prices','title_uz': 'Kontrakt narxlari',                  'title_ru': 'Стоимость контракта',             'title_en': 'Contract prices',          'order': 13},
            {'slug': 'bachelor-results',      'title_uz': 'Bakalavr natijalari',                   'title_ru': 'Результаты бакалавриата',         'title_en': 'Bachelor results',         'order': 14},
            {'slug': 'exam-schedule',         'title_uz': 'Kasbiy imtihonlar jadvali',             'title_ru': 'Расписание профессиональных экзаменов', 'title_en': 'Exam schedule',     'order': 15},
        ],
    },
    {
        'slug': 'magistratura',
        'title_uz': 'Magistratura',
        'title_ru': 'Магистратура',
        'title_en': "Master's",
        'order': 3,
        'items': [
            {'slug': 'masters-admission-plan', 'title_uz': 'Qabul rejasi',              'title_ru': 'План приёма',                 'title_en': 'Admission plan',      'order': 1},
            {'slug': 'masters-documents',      'title_uz': 'Hujjat topshirish',         'title_ru': 'Подача документов',           'title_en': 'Document submission', 'order': 2},
            {'slug': 'personal-documents-m',   'title_uz': "Hujjatlar to'plami",         'title_ru': 'Пакет документов',            'title_en': 'Documents package',   'order': 3},
            {'slug': 'masters-results',        'title_uz': 'Magistratura natijalari',   'title_ru': 'Результаты магистратуры',     'title_en': 'Masters results',     'order': 4},
        ],
    },
    {
        'slug': 'xorijiy-talabalar',
        'title_uz': 'Xorijiy talabalar',
        'title_ru': 'Иностранные студенты',
        'title_en': 'Foreign Students',
        'order': 4,
        'items': [
            {'slug': 'foreign-students-apply', 'title_uz': 'Ariza yuborish',                       'title_ru': 'Подать заявку',                        'title_en': 'Apply',                           'order': 1},
            {'slug': 'foreign-bachelor',        'title_uz': "Bakalavr ta'lim yo'nalishlari",        'title_ru': 'Направления бакалавриата',             'title_en': 'Bachelor programs',               'order': 2},
            {'slug': 'foreign-masters',         'title_uz': "Magistratura ta'lim yo'nalishlari",    'title_ru': 'Направления магистратуры',             'title_en': 'Masters programs',                'order': 3},
            {'slug': 'foreign-contracts',       'title_uz': 'Shartnomalar',                        'title_ru': 'Договоры',                             'title_en': 'Contracts',                       'order': 4},
            {'slug': 'increased-contract-f',    'title_uz': "Oshirilgan to'lov-shartnomasi",        'title_ru': 'Повышенный договор',                   'title_en': 'Increased contract',              'order': 5},
            {'slug': 'foreign-contract-prices', 'title_uz': 'Kontrakt narxlari',                   'title_ru': 'Стоимость контракта',                  'title_en': 'Contract prices',                 'order': 6},
        ],
    },
    {
        'slug': 'talabalar-turar-joyi',
        'title_uz': 'Talabalar turar joyi',
        'title_ru': 'Общежитие',
        'title_en': 'Student Dormitory',
        'order': 5,
        'items': [
            {'slug': 'dormitory', 'title_uz': "Talabalar uchun yotoqxona ijara to'lovlari", 'title_ru': 'Аренда общежития для студентов', 'title_en': 'Dormitory rental fees', 'order': 1},
        ],
    },
]


class Command(BaseCommand):
    help = "Qabul navbar seed"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

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
            for item in items:
                QabulNavbarItem.objects.update_or_create(
                    navbar=navbar,
                    slug=item['slug'],
                    defaults=item,
                )
            self.stdout.write(self.style.SUCCESS(
                f"[{'+'if created else '~'}] {navbar.title_uz} ({navbar.items.count()} item)"
            ))
