"""
python manage.py seed_navbar

TZ bo'yicha barcha NavbarCategory va NavbarSubItem larni yaratadi.
Idempotent: slug bo'yicha get_or_create — qayta ishlasa dublikat yaratmaydi.
"""
from django.core.management.base import BaseCommand

from domains.pages.models import NavbarCategory, NavbarSubItem


# ──────────────────────────────────────────────────────────────────────────────
# TZ bo'yicha to'liq navbar tuzilmasi
# slug — frontend JSON id/slug bilan mos keladi → /api/pages/{slug}/
# ──────────────────────────────────────────────────────────────────────────────
NAVBAR_DATA = [
    # ═══════════════════════════════════════════════════════════════
    # 1. AKADEMIYA
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Akademiya',
        'name_ru': 'Академия',
        'name_en': 'Academy',
        'slug': 'akademiya',
        'order': 1,
        'items': [
            {'name_uz': 'Akademiya haqida',                  'name_ru': 'Об академии',               'name_en': 'About Academy',                'slug': 'about-academy',              'order': 1},
            {'name_uz': 'Akademiya raqamlarda',              'name_ru': 'Академия в цифрах',          'name_en': 'Academy in Numbers',           'slug': 'academy-in-numbers',         'order': 2},
            {'name_uz': 'Akademiya tarixi',                  'name_ru': 'История академии',           'name_en': 'Academy History',              'slug': 'academy-history',            'order': 3},
            {'name_uz': 'Rektorat',                          'name_ru': 'Ректорат',                   'name_en': 'Rectorate',                    'slug': 'rectorate',                  'order': 4},
            {'name_uz': 'Tuzilma',                           'name_ru': 'Структура',                  'name_en': 'Structure',                    'slug': 'academy-structure',          'order': 5},
            {'name_uz': 'Rekvizitlar',                       'name_ru': 'Реквизиты',                  'name_en': 'Details',                      'slug': 'academy-details',            'order': 6},
            {'name_uz': "Me'yoriy hujjatlar",                'name_ru': 'Нормативные документы',      'name_en': 'Regulations',                  'slug': 'academy-regulations',        'order': 7},
            {'name_uz': "O'quv binolari",                    'name_ru': 'Учебные здания',             'name_en': 'Academy Buildings',            'slug': 'academy-buildings',          'order': 8},
            {'name_uz': 'Akademiya kengashi',                'name_ru': 'Совет академии',             'name_en': 'Academy Council',              'slug': 'academy-council',            'order': 9},
            {'name_uz': 'Akademiya huzuridagi tashkilotlar', 'name_ru': 'Организации при академии',   'name_en': 'Organizations',                'slug': 'organizations',              'order': 10},
            {'name_uz': 'Fakultetlar',                       'name_ru': 'Факультеты',                 'name_en': 'Faculties',                    'slug': 'faculties',                  'order': 11},
            {'name_uz': 'Institutlar',                       'name_ru': 'Институты',                  'name_en': 'Institutes',                   'slug': 'institutes',                 'order': 12},
            {'name_uz': 'Jamoat tashkilotlari',              'name_ru': 'Общественные организации',   'name_en': 'Public Organizations',         'slug': 'public-organizations',       'order': 13},
            {'name_uz': 'Markazlar',                         'name_ru': 'Центры',                     'name_en': 'Centers',                      'slug': 'centers',                    'order': 14},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 2. FAOLIYAT
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Faoliyat',
        'name_ru': 'Деятельность',
        'name_en': 'Activity',
        'slug': 'faoliyat',
        'order': 2,
        'items': [
            # Sport
            {'name_uz': 'Sport faoliyati',                   'name_ru': 'Спортивная деятельность',    'name_en': 'Sports Activity',              'slug': 'sport-activity',             'order': 1},
            # Ilmiy
            {'name_uz': 'Ilmiy loyihalar',                   'name_ru': 'Научные проекты',            'name_en': 'Scientific Projects',          'slug': 'scientific-projects',        'order': 2},
            {'name_uz': 'Doktorantura',                      'name_ru': 'Докторантура',               'name_en': 'Doctoral Studies',             'slug': 'doctoral-studies',           'order': 3},
            {'name_uz': 'Avtoreferatlar',                    'name_ru': 'Авторефераты',               'name_en': 'Abstracts',                    'slug': 'autoreferat',                'order': 4},
            {'name_uz': 'Ilmiy konferensiyalar',             'name_ru': 'Научные конференции',        'name_en': 'Scientific Conferences',       'slug': 'scientific-conferences',     'order': 5},
            {'name_uz': 'Ilmiy ishlar va innovatsiyalar',    'name_ru': 'Научные работы',             'name_en': 'Scientific Works',             'slug': 'scientific-works',           'order': 6},
            # O'quv
            {'name_uz': 'Bakalavriat',                       'name_ru': 'Бакалавриат',               'name_en': 'Bachelor',                     'slug': 'bachelor',                   'order': 7},
            {'name_uz': 'Magistratura',                      'name_ru': 'Магистратура',              'name_en': 'Masters',                      'slug': 'masters',                    'order': 8},
            {"name_uz": "O'quv adabiyotlari",                'name_ru': 'Учебная литература',         'name_en': 'Educational Literature',       'slug': 'educational-literature',     'order': 9},
            {'name_uz': 'Yangi adabiyotlar',                 'name_ru': 'Новая литература',           'name_en': 'New Books',                    'slug': 'new-books',                  'order': 10},
            # Ma'naviy
            {"name_uz": "Ma'naviyat rukni",                  'name_ru': 'Духовность',                 'name_en': 'Spiritual Corner',             'slug': 'spiritual-corner',           'order': 11},
            # Moliyaviy
            {"name_uz": "To'lov-kontrakt narxlari",          'name_ru': 'Стоимость контракта',        'name_en': 'Contract Prices',              'slug': 'contract-prices',            'order': 12},
            {'name_uz': 'Avtomototransport vositalari',      'name_ru': 'Автотранспорт',              'name_en': 'Auto Transport',               'slug': 'auto-transport',             'order': 13},
            # Ekologiya
            {'name_uz': "Yashil Akademiya loyihasi",         'name_ru': 'Зелёная Академия',           'name_en': 'Green Academy',                'slug': 'green-academy',              'order': 14},
            {'name_uz': 'Ekofaol talabalar',                 'name_ru': 'Экоактивные студенты',       'name_en': 'Eco-Active Students',          'slug': 'eco-active-students',        'order': 15},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 3. XALQARO ALOQALAR
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Xalqaro aloqalar',
        'name_ru': 'Международные связи',
        'name_en': 'International Relations',
        'slug': 'xalqaro-aloqalar',
        'order': 3,
        'items': [
            {'name_uz': 'Xalqaro hamkor tashkilotlar',       'name_ru': 'Международные партнёры',     'name_en': 'International Partners',       'slug': 'international-partners',     'order': 1},
            {"name_uz": 'Xorijda malaka oshirish va ta\'lim','name_ru': 'Обучение за рубежом',        'name_en': 'Abroad Training',              'slug': 'abroad-training',            'order': 2},
            {"name_uz": "Xalqaro bo'lim e'lonlari",          'name_ru': 'Объявления',                 'name_en': 'International Announcements',  'slug': 'international-announcements','order': 3},
            {'name_uz': 'Akademik almashinuv',               'name_ru': 'Академическая мобильность',  'name_en': 'Academic Mobility',            'slug': 'academic-mobility',          'order': 4},
            {'name_uz': 'Xorijliklar "Biz haqimizda"',       'name_ru': 'Иностранцы о нас',          'name_en': 'About Us (Foreigners)',         'slug': 'about-us-foreigners',        'order': 5},
            {"name_uz": "Xorijlik professor-o'qituvchilar",  'name_ru': 'Иностранные профессора',     'name_en': 'Foreign Professors',           'slug': 'foreign-professors',         'order': 6},
            {'name_uz': 'Xalqaro reyting',                   'name_ru': 'Международный рейтинг',      'name_en': 'International Rating',         'slug': 'international-rating',       'order': 7},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 4. TALABALARGA
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Talabalarga',
        'name_ru': 'Студентам',
        'name_en': 'Students',
        'slug': 'talabalarga',
        'order': 4,
        'items': [
            {'name_uz': 'Talabalarga imtiyozlar',            'name_ru': 'Льготы студентам',           'name_en': 'Student Privileges',           'slug': 'student-privileges',         'order': 1},
            # Bakalavriat
            {"name_uz": "Yo'riqnoma (Bakalavr)",             'name_ru': 'Руководство (Бакалавр)',     'name_en': 'Bachelor Guide',               'slug': 'bachelor-guide',             'order': 2},
            {'name_uz': 'Bakalavr baholash tizimi',          'name_ru': 'Система оценивания',         'name_en': 'Grading System',               'slug': 'grading-system',             'order': 3},
            {'name_uz': 'GPA va Kredit talablari',           'name_ru': 'GPA и кредиты',              'name_en': 'GPA & Credit',                 'slug': 'gpa-credit',                 'order': 4},
            {'name_uz': 'Dars jadvali',                      'name_ru': 'Расписание занятий',         'name_en': 'Class Schedule',               'slug': 'class-schedule',             'order': 5},
            {'name_uz': 'Stipendiyalar',                     'name_ru': 'Стипендии',                  'name_en': 'Scholarships',                 'slug': 'scholarships',               'order': 6},
            {'name_uz': 'Yakuniy nazorat',                   'name_ru': 'Итоговый контроль',          'name_en': 'Final Control',                'slug': 'final-control',              'order': 7},
            {'name_uz': 'Yakuniy nazorat savollari',         'name_ru': 'Вопросы итогового контроля', 'name_en': 'Final Control Questions',      'slug': 'final-control-questions',    'order': 8},
            {"name_uz": "Fanlar o'quv qo'llanmasi",          'name_ru': 'Учебные пособия',            'name_en': 'Course Manual',                'slug': 'course-manual',              'order': 9},
            {'name_uz': 'Iqtidorli talabalar',               'name_ru': 'Одарённые студенты',         'name_en': 'Gifted Students',              'slug': 'gifted-students',            'order': 10},
            # Magistratura
            {'name_uz': 'Magistratura stipendiyalari',       'name_ru': 'Стипендии магистратуры',     'name_en': 'Masters Scholarships',         'slug': 'masters-scholarships',       'order': 11},
            {'name_uz': 'Magistrlik dissertatsiyasi himoyasi','name_ru': 'Защита диссертации',        'name_en': 'Masters Defense',              'slug': 'masters-defense',            'order': 12},
            {'name_uz': 'Magistrlik dissertatsiya mavzulari','name_ru': 'Темы диссертаций',           'name_en': 'Masters Topics',               'slug': 'masters-topics',             'order': 13},
            {'name_uz': 'Magistratura baholash tizimi',      'name_ru': 'Оценивание магистратуры',    'name_en': 'Masters Grading',              'slug': 'masters-grading',            'order': 14},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 5. AXBOROT XIZMATI
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Axborot xizmati',
        'name_ru': 'Пресс-служба',
        'name_en': 'Information Service',
        'slug': 'axborot-xizmati',
        'order': 5,
        'items': [
            {'name_uz': 'Yangiliklar',                       'name_ru': 'Новости',                    'name_en': 'News',                         'slug': 'news',                       'order': 1},
            {'name_uz': 'Rektor tadbirlari va nutqlari',     'name_ru': 'Мероприятия ректора',        'name_en': 'Rector Activities',            'slug': 'rector-activities',          'order': 2},
            {'name_uz': 'Brifinglar',                        'name_ru': 'Брифинги',                   'name_en': 'Briefings',                    'slug': 'briefings',                  'order': 3},
            {'name_uz': 'Tanlovlar',                         'name_ru': 'Конкурсы',                   'name_en': 'Contests',                     'slug': 'contests',                   'order': 4},
            {'name_uz': 'Matbuot xizmati',                   'name_ru': 'Пресс-служба',               'name_en': 'Press Service',                'slug': 'press-service',              'order': 5},
            {'name_uz': 'Savol-javob',                       'name_ru': 'Вопросы и ответы',           'name_en': 'FAQ',                          'slug': 'faq',                        'order': 6},
            {'name_uz': 'Fotogalereya',                      'name_ru': 'Фотогалерея',                'name_en': 'Photo Gallery',                'slug': 'photo-gallery',              'order': 7},
            {'name_uz': 'Videogalereya',                     'name_ru': 'Видеогалерея',               'name_en': 'Video Gallery',                'slug': 'video-gallery',              'order': 8},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 6. QABUL
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Qabul',
        'name_ru': 'Приёмная комиссия',
        'name_en': 'Admissions',
        'slug': 'qabul',
        'order': 6,
        'items': [
            # Komissiya
            {'name_uz': 'Qabul yangiliklari',                'name_ru': 'Новости приёма',             'name_en': 'Admission News',               'slug': 'admission-news',             'order': 1},
            {'name_uz': 'Qabul komissiya tarkibi',           'name_ru': 'Состав комиссии',            'name_en': 'Commission Members',           'slug': 'admission-commission',       'order': 2},
            {"name_uz": "Me'yoriy hujjatlar (Qabul)",        'name_ru': 'Нормативные документы',      'name_en': 'Admission Regulations',        'slug': 'admission-regulations',      'order': 3},
            {'name_uz': 'Qabul kunlari',                     'name_ru': 'Дни приёма',                 'name_en': 'Admission Days',               'slug': 'admission-days',             'order': 4},
            {'name_uz': 'Call-center',                       'name_ru': 'Call-центр',                 'name_en': 'Call Center',                  'slug': 'call-center',                'order': 5},
            # Bakalavriat
            {'name_uz': 'Abituriyentlar uchun qo\'llanma',   'name_ru': 'Руководство абитуриента',    'name_en': 'Applicant Guide',              'slug': 'applicant-guide',            'order': 6},
            {'name_uz': 'Tavsiyanomaga ega abituriyentlar',  'name_ru': 'Рекомендованные абитуриенты','name_en': 'Recommended Applicants',       'slug': 'recommended-applicants',     'order': 7},
            {'name_uz': "Shaxsiy yig'ma jild hujjatlari",   'name_ru': 'Личное дело',                'name_en': 'Personal Documents',           'slug': 'personal-documents',         'order': 8},
            {'name_uz': 'Imtiyozlar',                        'name_ru': 'Льготы',                     'name_en': 'Privileges',                   'slug': 'admission-privileges',       'order': 9},
            {'name_uz': "O'tish ballari",                    'name_ru': 'Проходные баллы',            'name_en': 'Passing Scores',               'slug': 'passing-scores',             'order': 10},
            {'name_uz': 'Test-sinovlari fanlari',            'name_ru': 'Предметы теста',             'name_en': 'Test Subjects',                'slug': 'test-subjects',              'order': 11},
            {"name_uz": "O'qishni ko'chirish",               'name_ru': 'Перевод',                    'name_en': 'Transfer',                     'slug': 'transfer',                   'order': 12},
            {"name_uz": "Ko'zi ojiz abituriyentlar uchun",   'name_ru': 'Для слабовидящих',           'name_en': 'Visually Impaired',            'slug': 'visually-impaired',          'order': 13},
            {'name_uz': 'Texnikum bitiruvchilari',           'name_ru': 'Выпускники техникума',       'name_en': 'College Graduates',            'slug': 'college-graduates',          'order': 14},
            {"name_uz": "Ikkinchi oliy ta'lim",              'name_ru': 'Второе высшее',              'name_en': 'Second Degree',                'slug': 'second-degree',              'order': 15},
            {'name_uz': 'Shartnomalar',                      'name_ru': 'Договоры',                   'name_en': 'Contracts',                    'slug': 'admission-contracts',        'order': 16},
            {'name_uz': "Oshirilgan to'lov-shartnomasi",     'name_ru': 'Повышенный контракт',        'name_en': 'Increased Contract',           'slug': 'increased-contract',         'order': 17},
            {'name_uz': 'Kontrakt narxlari (Qabul)',         'name_ru': 'Стоимость контракта',        'name_en': 'Contract Prices (Admission)',   'slug': 'admission-contract-prices',  'order': 18},
            {'name_uz': 'Bakalavr natijalari',               'name_ru': 'Результаты бакалавриата',    'name_en': 'Bachelor Results',             'slug': 'bachelor-results',           'order': 19},
            {'name_uz': 'Kasbiy imtihonlar jadvali',         'name_ru': 'Расписание экзаменов',       'name_en': 'Exam Schedule',                'slug': 'exam-schedule',              'order': 20},
            # Magistratura
            {'name_uz': 'Magistratura qabul rejasi',         'name_ru': 'План приёма магистратуры',   'name_en': 'Masters Admission Plan',       'slug': 'masters-admission-plan',     'order': 21},
            {'name_uz': "Magistratura hujjat topshirish",    'name_ru': 'Подача документов',          'name_en': 'Masters Documents',            'slug': 'masters-documents',          'order': 22},
            {'name_uz': 'Magistratura natijalari',           'name_ru': 'Результаты магистратуры',    'name_en': 'Masters Results',              'slug': 'masters-results',            'order': 23},
            # Xorijiy talabalar
            {'name_uz': 'Xorijiy talabalar uchun ariza',     'name_ru': 'Заявка иностранных студентов','name_en': 'Foreign Students Application', 'slug': 'foreign-students-apply',     'order': 24},
            {'name_uz': 'Xorijiy talabalar — Bakalavr',      'name_ru': 'Бакалавр для иностранцев',  'name_en': 'Foreign — Bachelor',           'slug': 'foreign-bachelor',           'order': 25},
            {'name_uz': 'Xorijiy talabalar — Magistratura',  'name_ru': 'Магистратура для иностранцев','name_en': 'Foreign — Masters',           'slug': 'foreign-masters',            'order': 26},
            # Turar joy
            {'name_uz': 'Talabalar turar joyi',              'name_ru': 'Общежитие',                  'name_en': 'Dormitory',                    'slug': 'dormitory',                  'order': 27},
            {"name_uz": "Qo'shma ta'lim dasturlari",         'name_ru': 'Совместные программы',       'name_en': 'Joint Programs',               'slug': 'joint-programs',             'order': 28},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 7. REKTORGA MUROJAAT
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Rektorga murojaat',
        'name_ru': 'Обращение к ректору',
        'name_en': 'Rector Appeal',
        'slug': 'rektorga-murojaat',
        'order': 7,
        'items': [
            {'name_uz': 'Rektorga murojaat',                 'name_ru': 'Обращение к ректору',        'name_en': 'Rector Appeal',                'slug': 'rector-appeal',              'order': 1},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 8. FAXRLARIMIZ
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Faxrlarimiz',
        'name_ru': 'Наша гордость',
        'name_en': 'Our Pride',
        'slug': 'faxrlarimiz',
        'order': 8,
        'items': [
            {'name_uz': 'Bitiruvchilarimiz',                 'name_ru': 'Выпускники',                 'name_en': 'Graduates',                    'slug': 'graduates',                  'order': 1},
            {'name_uz': 'Faxrli ustozlarimiz',               'name_ru': 'Почётные учителя',           'name_en': 'Honorary Teachers',            'slug': 'honorary-teachers',          'order': 2},
            {"name_uz": "Ilg'or olimlarimiz",                'name_ru': 'Выдающиеся учёные',          'name_en': 'Distinguished Scientists',     'slug': 'distinguished-scientists',   'order': 3},
            {"name_uz": "O'ZDSA yulduzlari",                 'name_ru': 'Звёзды УЗГСА',               'name_en': 'OZDSA Stars',                  'slug': 'ozdsa-stars',                'order': 4},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 9. ALOQA
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Aloqa',
        'name_ru': 'Контакты',
        'name_en': 'Contact',
        'slug': 'aloqa',
        'order': 9,
        'items': [
            {'name_uz': 'Aloqa',                             'name_ru': 'Контакты',                   'name_en': 'Contact',                      'slug': 'contact',                    'order': 1},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 10. VIRTUAL SAYOHAT
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Virtual sayohat',
        'name_ru': 'Виртуальный тур',
        'name_en': 'Virtual Tour',
        'slug': 'virtual-sayohat',
        'order': 10,
        'items': [
            {'name_uz': 'Virtual sayohat',                   'name_ru': 'Виртуальный тур',            'name_en': 'Virtual Tour',                 'slug': 'virtual-tour',               'order': 1},
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # 11. REYTING (qo'shimcha)
    # ═══════════════════════════════════════════════════════════════
    {
        'name_uz': 'Reyting',
        'name_ru': 'Рейтинг',
        'name_en': 'Rating',
        'slug': 'reyting',
        'order': 11,
        'items': [
            {'name_uz': 'Milliy reyting',                    'name_ru': 'Национальный рейтинг',       'name_en': 'National Rating',              'slug': 'national-rating',            'order': 1},
            {'name_uz': 'Xalqaro reyting',                   'name_ru': 'Международный рейтинг',      'name_en': 'International Rating',         'slug': 'international-rating-page',  'order': 2},
        ],
    },
]


class Command(BaseCommand):
    help = "TZ bo'yicha NavbarCategory va NavbarSubItem larni seed qiladi (idempotent)"

    def handle(self, *args, **options):
        created_cats  = 0
        updated_cats  = 0
        created_items = 0
        updated_items = 0

        for cat_data in NAVBAR_DATA:
            items = cat_data.pop('items', [])

            cat, created = NavbarCategory.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name_uz': cat_data['name_uz'],
                    'name_ru': cat_data.get('name_ru', ''),
                    'name_en': cat_data.get('name_en', ''),
                    'order':   cat_data['order'],
                    'is_active': True,
                },
            )
            if created:
                created_cats += 1
                self.stdout.write(self.style.SUCCESS(f"  + Kategoriya: {cat.name_uz}"))
            else:
                updated_cats += 1

            for item_data in items:
                item, icreated = NavbarSubItem.objects.update_or_create(
                    slug=item_data['slug'],
                    defaults={
                        'category':    cat,
                        'name_uz':     item_data['name_uz'],
                        'name_ru':     item_data.get('name_ru', ''),
                        'name_en':     item_data.get('name_en', ''),
                        'order':       item_data['order'],
                        'page_type':   'static',
                        'is_active':   True,
                    },
                )
                if icreated:
                    created_items += 1
                    self.stdout.write(f"      + {item.slug}")
                else:
                    updated_items += 1

            # items ni qaytarib qo'yamiz (agar keyingi ishlatilsa)
            cat_data['items'] = items

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created_cats} kategoriya yaratildi, {updated_cats} yangilandi | "
            f"{created_items} sahifa yaratildi, {updated_items} yangilandi"
        ))
