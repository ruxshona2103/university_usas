"""
python manage.py seed_navbar

TZ bo'yicha barcha NavbarCategory, NavbarSubItem va kontent ma'lumotlarini yaratadi.
Idempotent: slug / unique key bo'yicha get_or_create — qayta ishlasa dublikat yaratmaydi.
"""
from django.core.management.base import BaseCommand

from domains.pages.models import (
    NavbarCategory, NavbarSubItem,
    ContactConfig, PresidentQuote, SocialLink,
    Partner, HeroVideo, ContentBlock, LinkBlock,
)
from domains.academic.models import Staff, StaffContent
from domains.news.models import News, Event, Blog, InformationContent
from domains.students.models import PersonCategory, Person
from domains.international.models import ForeignProfessorReview
from domains.contact.models import FAQ
from domains.tenders.models import TenderAnnouncement
from common.models import Tag


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


def page(slug):
    """NavbarSubItem ni slug bo'yicha qaytaradi yoki None"""
    try:
        return NavbarSubItem.objects.get(slug=slug)
    except NavbarSubItem.DoesNotExist:
        return None


class Command(BaseCommand):
    help = "NavbarCategory, NavbarSubItem va barcha kontent ma'lumotlarini seed qiladi (idempotent)"

    def handle(self, *args, **options):
        self._seed_navbar()
        self._seed_site_config()
        self._seed_tags()
        self._seed_hero_video()
        self._seed_partners()
        self._seed_staff()
        self._seed_content_blocks()
        self._seed_information_content()
        self._seed_news()
        self._seed_faq()
        self._seed_foreign_professors()
        self._seed_honored_people()
        self._seed_tenders()
        self.stdout.write(self.style.SUCCESS('\n✓ Barcha seed ma\'lumotlar muvaffaqiyatli qo\'shildi!'))

    # ──────────────────────────────────────────────────────────────────────────
    # 1. NAVBAR
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_navbar(self):
        self.stdout.write('\n── Navbar ...')
        created_cats = updated_cats = created_items = updated_items = 0

        for cat_data in NAVBAR_DATA:
            items = cat_data.pop('items', [])
            cat, created = NavbarCategory.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name_uz':   cat_data['name_uz'],
                    'name_ru':   cat_data.get('name_ru', ''),
                    'name_en':   cat_data.get('name_en', ''),
                    'order':     cat_data['order'],
                    'is_active': True,
                },
            )
            if created:
                created_cats += 1
            else:
                updated_cats += 1

            for item_data in items:
                _, icreated = NavbarSubItem.objects.update_or_create(
                    slug=item_data['slug'],
                    defaults={
                        'category': cat,
                        'name_uz':  item_data['name_uz'],
                        'name_ru':  item_data.get('name_ru', ''),
                        'name_en':  item_data.get('name_en', ''),
                        'order':    item_data['order'],
                        'page_type': 'static',
                        'is_active': True,
                    },
                )
                if icreated:
                    created_items += 1
                else:
                    updated_items += 1
            cat_data['items'] = items

        self.stdout.write(self.style.SUCCESS(
            f"   {created_cats} kategoriya, {created_items} sahifa yaratildi"
        ))

    # ──────────────────────────────────────────────────────────────────────────
    # 2. SAYT SOZLAMALARI
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_site_config(self):
        self.stdout.write('\n── Sayt sozlamalari ...')

        ContactConfig.objects.update_or_create(
            pk=ContactConfig.objects.first().pk if ContactConfig.objects.exists() else None,
            defaults={} if ContactConfig.objects.exists() else {
                'email':      'info@usas.uz',
                'phone':      '+998 71 244-70-00',
                'address_uz': "Toshkent sh., Yunusobod tumani, Yusupov ko'chasi 2-uy",
                'address_ru': 'г. Ташкент, Юнусабадский р-н, ул. Юсупова, д. 2',
                'address_en': '2 Yusupov Street, Yunusabad district, Tashkent',
            },
        )
        if not ContactConfig.objects.exists():
            ContactConfig.objects.create(
                email='info@usas.uz',
                phone='+998 71 244-70-00',
                address_uz="Toshkent sh., Yunusobod tumani, Yusupov ko'chasi 2-uy",
                address_ru='г. Ташкент, Юнусабадский р-н, ул. Юсупова, д. 2',
                address_en='2 Yusupov Street, Yunusabad district, Tashkent',
            )

        PresidentQuote.objects.get_or_create(
            author="Sh.M. Mirziyoyev, O'zbekiston Respublikasi Prezidenti",
            defaults={
                'quote_uz': (
                    "Sport — bu nafaqat sog'lom turmush tarzi, balki milliy ruh, iroda va g'alabaga intilishning timsoli. "
                    "Biz yosh avlodni jismoniy jihatdan barkamol, ma'nan yetuk inson qilib tarbiyalashimiz kerak."
                ),
                'quote_ru': (
                    "Спорт — это не просто здоровый образ жизни, это символ национального духа, воли и стремления к победе. "
                    "Мы должны воспитывать молодое поколение физически совершенным и духовно зрелым."
                ),
                'quote_en': (
                    "Sport is not only a healthy lifestyle, but also a symbol of national spirit, will and aspiration for victory. "
                    "We must raise the young generation to be physically perfect and spiritually mature."
                ),
                'is_active': True,
            },
        )

        for platform, url in [
            ('telegram',  'https://t.me/usas_uz'),
            ('instagram', 'https://instagram.com/usas_uz'),
            ('facebook',  'https://facebook.com/usas.uz'),
            ('youtube',   'https://youtube.com/@usas_uz'),
        ]:
            SocialLink.objects.update_or_create(
                platform=platform,
                defaults={'url': url, 'is_active': True},
            )

        self.stdout.write(self.style.SUCCESS('   OK'))

    # ──────────────────────────────────────────────────────────────────────────
    # 3. TEGLAR (Staff tab uchun)
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_tags(self):
        self.stdout.write('\n── Teglar ...')
        tags = [
            ('tarjimai-hol',     "Tarjimai hol",       'Биография',     'Biography'),
            ('ilmiy-faoliyat',   "Ilmiy faoliyat",     'Научная деятельность', 'Scientific Activity'),
            ('qabul-soatlari',   "Qabul soatlari",     'Часы приёма',   'Reception Hours'),
            ('nashrlar',         "Nashrlar",            'Публикации',    'Publications'),
            ('loyihalar',        "Loyihalar",           'Проекты',       'Projects'),
        ]
        for slug, uz, ru, en in tags:
            Tag.objects.update_or_create(
                slug=slug,
                defaults={'name_uz': uz, 'name_ru': ru, 'name_en': en},
            )
        self.stdout.write(self.style.SUCCESS(f'   {len(tags)} teg'))

    # ──────────────────────────────────────────────────────────────────────────
    # 4. HERO VIDEO
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_hero_video(self):
        self.stdout.write('\n── Hero video ...')
        HeroVideo.objects.get_or_create(
            title="O'ZDSA — Kelajak sport yulduzlari",
            defaults={
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'is_active': True,
            },
        )
        self.stdout.write(self.style.SUCCESS('   OK'))

    # ──────────────────────────────────────────────────────────────────────────
    # 5. HAMKORLAR
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_partners(self):
        self.stdout.write('\n── Hamkorlar ...')
        partners = [
            ("Xalqaro Olimpiya Qo'mitasi",           "Международный олимпийский комитет",    "International Olympic Committee",    'https://olympics.com',          1),
            ("O'zbekiston Milliy Olimpiya Qo'mitasi", "НОК Узбекистана",                      "NOC of Uzbekistan",                  'https://olympic.uz',            2),
            ("WADA — Jahon Antidoping Agentligi",    "ВАДА",                                 "World Anti-Doping Agency",           'https://wada-ama.org',          3),
            ("O'zbekiston Jismoniy Tarbiya va Sport vazirligi", "Министерство спорта РУз",    "Ministry of Sports of Uzbekistan",   'https://minsport.uz',           4),
            ("Osiyo Olimpiya Kengashi",               "Олимпийский совет Азии",               "Olympic Council of Asia",            'https://ocasia.org',            5),
            ("SportAccord",                          "СпортАккорд",                          "SportAccord",                        'https://sportaccord.com',       6),
        ]
        for uz, ru, en, url, order in partners:
            Partner.objects.get_or_create(
                title_uz=uz,
                defaults={'title_ru': ru, 'title_en': en, 'url': url, 'order': order, 'is_active': True},
            )
        self.stdout.write(self.style.SUCCESS(f'   {len(partners)} hamkor'))

    # ──────────────────────────────────────────────────────────────────────────
    # 6. XODIMLAR (Staff)
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_staff(self):
        self.stdout.write('\n── Xodimlar ...')
        tag_bio = Tag.objects.filter(slug='tarjimai-hol').first()
        tag_sci = Tag.objects.filter(slug='ilmiy-faoliyat').first()
        tag_rec = Tag.objects.filter(slug='qabul-soatlari').first()

        rectorate_page = page('rectorate')
        faculties_page  = page('faculties')
        council_page    = page('academy-council')

        staff_data = [
            # slug, navbar_slug, role, is_head, full_name, title_uz, title_ru, title_en,
            # position_uz, position_ru, position_en, phone, email, address_uz, reception, order
            {
                'navbar':    'rectorate',
                'role':      'rector',
                'is_head':   True,
                'full_name': 'Abdullayev Jasur Qodirovich',
                'title_uz':  'Sport fanlari doktori, professor',
                'title_ru':  'Доктор спортивных наук, профессор',
                'title_en':  'Doctor of Sports Sciences, Professor',
                'pos_uz':    'Rektor',
                'pos_ru':    'Ректор',
                'pos_en':    'Rector',
                'phone':     '+998 71 244-70-01',
                'email':     'rector@usas.uz',
                'address_uz':"Toshkent sh., Yunusobod tumani, Yusupov ko'chasi 2-uy, 101-xona",
                'reception': "Seshanba va Payshanba: 14:00–17:00",
                'desc_uz':   (
                    "<p>Abdullayev Jasur Qodirovich — O'zbekiston Davlat Sport Akademiyasining rektori, "
                    "sport fanlari doktori, professor. 1998-yilda NUU da tahsil olgan, keyinchalik Germaniya va "
                    "Yaponiyada malaka oshirgan. 20 yildan ortiq pedagogik va ilmiy faoliyat tajribasiga ega.</p>"
                    "<p>20 dan ortiq ilmiy maqola va 3 ta monografiya muallifi. O'zbekiston sport federatsiyalari "
                    "qoshida ilmiy-uslubiy kengash a'zosi.</p>"
                ),
                'desc_ru':   (
                    "<p>Абдуллаев Джасур Кодирович — ректор Узбекского государственного академии спорта, "
                    "доктор спортивных наук, профессор. Имеет более 20 лет педагогического и научного опыта.</p>"
                ),
                'desc_en':   (
                    "<p>Abdullayev Jasur Qodirovich — Rector of the Uzbekistan State Sports Academy, "
                    "Doctor of Sports Sciences, Professor with over 20 years of experience.</p>"
                ),
                'order': 1,
            },
            {
                'navbar':    'rectorate',
                'role':      'prorector',
                'is_head':   False,
                'full_name': "Karimov Sherzod Il'homovich",
                'title_uz':  'Pedagogika fanlari nomzodi, dotsent',
                'title_ru':  'Кандидат педагогических наук, доцент',
                'title_en':  'PhD in Pedagogy, Associate Professor',
                'pos_uz':    "Ta'lim ishlari bo'yicha prorektor",
                'pos_ru':    'Проректор по учебной работе',
                'pos_en':    'Vice-Rector for Academic Affairs',
                'phone':     '+998 71 244-70-02',
                'email':     'prorector.edu@usas.uz',
                'address_uz':"102-xona",
                'reception': "Dushanba va Chorshanba: 10:00–13:00",
                'desc_uz':   "<p>Ta'lim va o'quv jarayonlarini boshqarish bo'yicha 15 yillik tajribaga ega mutaxassis.</p>",
                'desc_ru':   "<p>Специалист с 15-летним опытом управления образовательными процессами.</p>",
                'desc_en':   "<p>Specialist with 15 years of experience in managing educational processes.</p>",
                'order': 2,
            },
            {
                'navbar':    'rectorate',
                'role':      'prorector',
                'is_head':   False,
                'full_name': 'Nazarov Bobur Akbarovich',
                'title_uz':  'Biologiya fanlari doktori, professor',
                'title_ru':  'Доктор биологических наук, профессор',
                'title_en':  'Doctor of Biological Sciences, Professor',
                'pos_uz':    "Ilmiy ishlar va innovatsiyalar bo'yicha prorektor",
                'pos_ru':    'Проректор по науке и инновациям',
                'pos_en':    'Vice-Rector for Research and Innovations',
                'phone':     '+998 71 244-70-03',
                'email':     'prorector.science@usas.uz',
                'address_uz':"103-xona",
                'reception': "Seshanba va Payshanba: 10:00–12:00",
                'desc_uz':   "<p>Sport biologiyasi va fiziologiyasi sohasida 18 yillik ilmiy tajribaga ega.</p>",
                'desc_ru':   "<p>18 лет научного опыта в области спортивной биологии и физиологии.</p>",
                'desc_en':   "<p>18 years of scientific experience in sports biology and physiology.</p>",
                'order': 3,
            },
            {
                'navbar':    'rectorate',
                'role':      'prorector',
                'is_head':   False,
                'full_name': 'Yusupov Temur Ulug\'bekovich',
                'title_uz':  'Pedagogika fanlari nomzodi',
                'title_ru':  'Кандидат педагогических наук',
                'title_en':  'PhD in Pedagogy',
                'pos_uz':    "Xalqaro aloqalar bo'yicha prorektor",
                'pos_ru':    'Проректор по международным связям',
                'pos_en':    'Vice-Rector for International Relations',
                'phone':     '+998 71 244-70-04',
                'email':     'prorector.int@usas.uz',
                'address_uz':"104-xona",
                'reception': "Dushanba, Chorshanba va Juma: 14:00–16:00",
                'desc_uz':   "<p>Xalqaro sport tashkilotlari bilan hamkorlikni rivojlantirish bo'yicha mutaxassis.</p>",
                'desc_ru':   "<p>Специалист по развитию сотрудничества с международными спортивными организациями.</p>",
                'desc_en':   "<p>Specialist in developing cooperation with international sports organizations.</p>",
                'order': 4,
            },
            {
                'navbar':    'rectorate',
                'role':      'prorector',
                'is_head':   False,
                'full_name': 'Xolmatov Dilshod Rahimovich',
                'title_uz':  'Psixologiya fanlari nomzodi',
                'title_ru':  'Кандидат психологических наук',
                'title_en':  'PhD in Psychology',
                'pos_uz':    "Ma'naviy-tarbiyaviy ishlar bo'yicha prorektor",
                'pos_ru':    'Проректор по воспитательной работе',
                'pos_en':    'Vice-Rector for Student Affairs',
                'phone':     '+998 71 244-70-05',
                'email':     'prorector.student@usas.uz',
                'address_uz':"105-xona",
                'reception': "Har kuni: 9:00–12:00",
                'desc_uz':   "<p>Talabalar o'rtasida ma'naviyat va sport ruhiyatini shakllantirish bo'yicha tajribali mutaxassis.</p>",
                'desc_ru':   "<p>Опытный специалист по формированию духовности и спортивного духа среди студентов.</p>",
                'desc_en':   "<p>Experienced specialist in fostering spirituality and sports spirit among students.</p>",
                'order': 5,
            },
            # Dekanlar
            {
                'navbar':    'faculties',
                'role':      'dean',
                'is_head':   False,
                'full_name': 'Toshmatov Alisher Hamidovich',
                'title_uz':  'Sport fanlari nomzodi, dotsent',
                'title_ru':  'Кандидат спортивных наук, доцент',
                'title_en':  'PhD in Sports Sciences, Associate Professor',
                'pos_uz':    "Jismoniy tarbiya va sport fakulteti dekani",
                'pos_ru':    'Декан факультета физической культуры и спорта',
                'pos_en':    'Dean of Faculty of Physical Education and Sports',
                'phone':     '+998 71 244-71-01',
                'email':     'dean.sport@usas.uz',
                'address_uz':"201-xona",
                'reception': "Chorshanba: 14:00–17:00",
                'desc_uz':   "<p>Jismoniy tarbiya metodikasi va sport pedagogikasi bo'yicha mutaxassis.</p>",
                'desc_ru':   "<p>Специалист по методике физического воспитания и спортивной педагогике.</p>",
                'desc_en':   "<p>Specialist in physical education methodology and sports pedagogy.</p>",
                'order': 1,
            },
            {
                'navbar':    'faculties',
                'role':      'dean',
                'is_head':   False,
                'full_name': 'Rahimova Gulnora Utkurovna',
                'title_uz':  'Iqtisodiyot fanlari nomzodi, dotsent',
                'title_ru':  'Кандидат экономических наук, доцент',
                'title_en':  'PhD in Economics, Associate Professor',
                'pos_uz':    "Sport menejment va marketing fakulteti dekani",
                'pos_ru':    'Декан факультета спортивного менеджмента',
                'pos_en':    'Dean of Faculty of Sports Management',
                'phone':     '+998 71 244-71-02',
                'email':     'dean.management@usas.uz',
                'address_uz':"202-xona",
                'reception': "Seshanba va Payshanba: 10:00–12:00",
                'desc_uz':   "<p>Sport sanoati va menejmentida 12 yillik amaliy tajribaga ega.</p>",
                'desc_ru':   "<p>Имеет 12-летний практический опыт в спортивной индустрии и менеджменте.</p>",
                'desc_en':   "<p>Has 12 years of practical experience in sports industry and management.</p>",
                'order': 2,
            },
            {
                'navbar':    'faculties',
                'role':      'dean',
                'is_head':   False,
                'full_name': 'Mirzayev Nodir Baxromovich',
                'title_uz':  'Pedagogika fanlari nomzodi',
                'title_ru':  'Кандидат педагогических наук',
                'title_en':  'PhD in Pedagogy',
                'pos_uz':    "Trenerlik va sport murabbiyligi fakulteti dekani",
                'pos_ru':    'Декан тренерского факультета',
                'pos_en':    'Dean of Coaching Faculty',
                'phone':     '+998 71 244-71-03',
                'email':     'dean.coaching@usas.uz',
                'address_uz':"203-xona",
                'reception': "Dushanba va Juma: 9:00–12:00",
                'desc_uz':   "<p>Olimpiya darajasidagi sportchilarni tayyorlash metodikasi bo'yicha ixtisoslashgan.</p>",
                'desc_ru':   "<p>Специализируется на методике подготовки спортсменов олимпийского уровня.</p>",
                'desc_en':   "<p>Specializes in the methodology of training Olympic-level athletes.</p>",
                'order': 3,
            },
            {
                'navbar':    'faculties',
                'role':      'dean',
                'is_head':   False,
                'full_name': 'Xasanov Sardor Baxtiyorovich',
                'title_uz':  'Pedagogika fanlari doktori, professor',
                'title_ru':  'Доктор педагогических наук, профессор',
                'title_en':  'Doctor of Pedagogical Sciences, Professor',
                'pos_uz':    "Magistratura va doktorantura fakulteti dekani",
                'pos_ru':    'Декан факультета магистратуры и докторантуры',
                'pos_en':    'Dean of Graduate Studies Faculty',
                'phone':     '+998 71 244-71-04',
                'email':     'dean.graduate@usas.uz',
                'address_uz':"204-xona",
                'reception': "Chorshanba: 10:00–13:00",
                'desc_uz':   "<p>Oliy ta'lim pedagogikasi va ilmiy kadrlar tayyorlash sohasida yetakchi mutaxassis.</p>",
                'desc_ru':   "<p>Ведущий специалист в области педагогики высшей школы и подготовки научных кадров.</p>",
                'desc_en':   "<p>Leading expert in higher education pedagogy and academic staff training.</p>",
                'order': 4,
            },
            # Akademiya kengashi a'zolari
            {
                'navbar':    'academy-council',
                'role':      'council_member',
                'is_head':   False,
                'full_name': "Umarov Behruz Salimovich",
                'title_uz':  'Sport fanlari doktori, professor',
                'title_ru':  'Доктор спортивных наук, профессор',
                'title_en':  'Doctor of Sports Sciences, Professor',
                'pos_uz':    "Akademiya kengashi raisi o'rinbosari",
                'pos_ru':    'Заместитель председателя совета академии',
                'pos_en':    'Deputy Chairman of Academy Council',
                'phone':     '+998 71 244-72-01',
                'email':     'council@usas.uz',
                'address_uz':"110-xona",
                'reception': "Payshanba: 14:00–16:00",
                'desc_uz':   "<p>Sport fanlari bo'yicha 25 yillik ilmiy-pedagogik faoliyat tajribasiga ega.</p>",
                'desc_ru':   "<p>Имеет 25 лет научно-педагогической деятельности в области спортивных наук.</p>",
                'desc_en':   "<p>Has 25 years of scientific-pedagogical activity in sports sciences.</p>",
                'order': 1,
            },
            {
                'navbar':    'academy-council',
                'role':      'council_member',
                'is_head':   False,
                'full_name': "Qodirov Mansur Hamidullayevich",
                'title_uz':  'Tibbiyot fanlari doktori',
                'title_ru':  'Доктор медицинских наук',
                'title_en':  'Doctor of Medical Sciences',
                'pos_uz':    "Sport tibbiyoti kafedra mudiri",
                'pos_ru':    'Заведующий кафедрой спортивной медицины',
                'pos_en':    'Head of Sports Medicine Department',
                'phone':     '+998 71 244-72-02',
                'email':     'medicine@usas.uz',
                'address_uz':"111-xona",
                'reception': "Seshanba: 10:00–12:00",
                'desc_uz':   "<p>Sport tibbiyoti va sportchilar reabilitatsiyasi sohasida taniqli mutaxassis.</p>",
                'desc_ru':   "<p>Известный специалист в области спортивной медицины и реабилитации спортсменов.</p>",
                'desc_en':   "<p>Renowned specialist in sports medicine and athlete rehabilitation.</p>",
                'order': 2,
            },
            {
                'navbar':    'academy-council',
                'role':      'council_member',
                'is_head':   False,
                'full_name': "Ismoilova Maftuna Rasulovna",
                'title_uz':  'Psixologiya fanlari nomzodi, dotsent',
                'title_ru':  'Кандидат психологических наук, доцент',
                'title_en':  'PhD in Psychology, Associate Professor',
                'pos_uz':    "Sport psixologiyasi kafedrasi dotsenti",
                'pos_ru':    'Доцент кафедры спортивной психологии',
                'pos_en':    'Associate Professor of Sports Psychology Department',
                'phone':     '+998 71 244-72-03',
                'email':     'psychology@usas.uz',
                'address_uz':"112-xona",
                'reception': "Dushanba va Chorshanba: 14:00–16:00",
                'desc_uz':   "<p>Sportchilar psixologik tayyorgarligi va motivatsiyasi bo'yicha tadqiqotchi.</p>",
                'desc_ru':   "<p>Исследователь в области психологической подготовки и мотивации спортсменов.</p>",
                'desc_en':   "<p>Researcher in psychological preparation and motivation of athletes.</p>",
                'order': 3,
            },
        ]

        for d in staff_data:
            p = page(d['navbar'])
            if not p:
                continue
            staff_obj, created = Staff.objects.get_or_create(
                navbar_item=p,
                full_name=d['full_name'],
                defaults={
                    'role':         d['role'],
                    'is_head':      d['is_head'],
                    'title_uz':     d['title_uz'],
                    'title_ru':     d['title_ru'],
                    'title_en':     d['title_en'],
                    'position_uz':  d['pos_uz'],
                    'position_ru':  d['pos_ru'],
                    'position_en':  d['pos_en'],
                    'phone':        d['phone'],
                    'email':        d['email'],
                    'address':      d['address_uz'],
                    'reception':    d['reception'],
                    'description_uz': d['desc_uz'],
                    'description_ru': d['desc_ru'],
                    'description_en': d['desc_en'],
                    'order':        d['order'],
                    'is_active':    True,
                },
            )
            if created and tag_bio:
                StaffContent.objects.get_or_create(
                    staff=staff_obj,
                    tag=tag_bio,
                    defaults={'content_uz': d['desc_uz'], 'content_ru': d['desc_ru'], 'content_en': d['desc_en'], 'order': 1},
                )
            if created and tag_sci:
                StaffContent.objects.get_or_create(
                    staff=staff_obj,
                    tag=tag_sci,
                    defaults={
                        'content_uz': '<p>Ilmiy maqolalar va tadqiqotlar haqida ma\'lumot.</p>',
                        'content_ru': '<p>Информация о научных статьях и исследованиях.</p>',
                        'content_en': '<p>Information about scientific articles and research.</p>',
                        'order': 2,
                    },
                )
            if created and tag_rec:
                StaffContent.objects.get_or_create(
                    staff=staff_obj,
                    tag=tag_rec,
                    defaults={
                        'content_uz': f'<p><strong>Qabul kunlari:</strong> {d["reception"]}</p><p><strong>Manzil:</strong> {d["address_uz"]}</p>',
                        'content_ru': f'<p><strong>Часы приёма:</strong> {d["reception"]}</p>',
                        'content_en': f'<p><strong>Reception hours:</strong> {d["reception"]}</p>',
                        'order': 3,
                    },
                )

        self.stdout.write(self.style.SUCCESS(f'   {len(staff_data)} xodim'))

    # ──────────────────────────────────────────────────────────────────────────
    # 7. KONTENT BLOKLARI
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_content_blocks(self):
        self.stdout.write('\n── Kontent bloklari ...')
        count = 0

        blocks = [
            # ── ABOUT ACADEMY ──
            ('about-academy', 'hero', 1,
             "O'ZDSA haqida", "Об академии", "About the Academy",
             "<p>O'zbekiston Davlat Sport Akademiyasi (O'ZDSA) — mamlakatimizning yetakchi sport ta'lim muassasasi. "
             "1972-yilda tashkil etilgan akademiya bugun 5 000 dan ortiq talabani o'z bag'rida tarbiyalaydi.</p>",
             "<p>Узбекский государственный академия спорта (УЗГСА) — ведущее спортивное учебное заведение страны.</p>",
             "<p>Uzbekistan State Sports Academy is the country's leading sports educational institution founded in 1972.</p>",
             None),
            ('about-academy', 'rich-text', 2,
             "Akademiyaning missiyasi", "Миссия академии", "Academy Mission",
             "<h3>Missiyamiz</h3><p>Yuqori malakali sport mutaxassislarini — murabbiylari, pedagoglarini va sport menejerlarini tayyorlash.</p>"
             "<h3>Vazifalarimiz</h3><ul><li>Zamonaviy sport ta'limini rivojlantirish</li><li>Ilmiy-tadqiqot ishlarini kengaytirish</li>"
             "<li>Xalqaro hamkorlikni mustahkamlash</li><li>Sport infratuzilmasini yangilash</li></ul>",
             "<h3>Наша миссия</h3><p>Подготовка высококвалифицированных спортивных специалистов.</p>",
             "<h3>Our Mission</h3><p>Training highly qualified sports specialists — coaches, teachers and sports managers.</p>",
             None),

            # ── ACADEMY IN NUMBERS ──
            ('academy-in-numbers', 'stats', 1,
             "Akademiya raqamlarda", "Академия в цифрах", "Academy in Numbers",
             None, None, None,
             {"stats": [
                 {"value": 5247, "label_uz": "Talabalar",          "label_ru": "Студенты",         "label_en": "Students",          "suffix": "+"},
                 {"value": 412,  "label_uz": "O'qituvchilar",       "label_ru": "Преподаватели",     "label_en": "Teachers",          "suffix": ""},
                 {"value": 38,   "label_uz": "Ta'lim yo'nalishlari","label_ru": "Направлений",       "label_en": "Study Directions",  "suffix": ""},
                 {"value": 52,   "label_uz": "Xalqaro hamkorlar",   "label_ru": "Международных партнёров","label_en":"Int'l Partners","suffix": ""},
                 {"value": 1972, "label_uz": "Tashkil etilgan yil", "label_ru": "Год основания",    "label_en": "Year Founded",      "suffix": ""},
                 {"value": 180,  "label_uz": "Olimpiya medaliylari","label_ru": "Олимпийских медалей","label_en":"Olympic Medals",    "suffix": "+"},
             ]}),

            # ── ACADEMY HISTORY ──
            ('academy-history', 'hero', 1,
             "Akademiya tarixi", "История академии", "Academy History",
             "<p>O'ZDSA 50 yildan ortiq tarix davomida O'zbekiston sportigas munosib hissa qo'shib kelmoqda.</p>",
             "<p>УЗГСА вносит достойный вклад в спорт Узбекистана на протяжении более 50 лет.</p>",
             "<p>USAS has been contributing to Uzbekistan sports for over 50 years.</p>",
             None),
            ('academy-history', 'timeline', 2,
             "Akademiya tarixiy bosqichlari", "Исторические этапы", "Historical Milestones",
             None, None, None,
             {"events": [
                 {"date": "1972", "title_uz": "Akademiya tashkil etildi",    "title_ru": "Основание академии",       "title_en": "Academy Founded",
                  "desc_uz": "O'zbekiston Davlat Jismoniy Tarbiya Instituti sifatida tashkil topdi.",
                  "desc_ru": "Основан как Узбекский государственный институт физической культуры.",
                  "desc_en": "Founded as Uzbekistan State Institute of Physical Culture."},
                 {"date": "1991", "title_uz": "Mustaqillik davri",           "title_ru": "Период независимости",     "title_en": "Independence Era",
                  "desc_uz": "O'zbekiston mustaqilligidan so'ng yangi bosqichga ko'tarildi.",
                  "desc_ru": "После независимости Узбекистана перешёл на новый этап развития.",
                  "desc_en": "After Uzbekistan's independence, entered a new stage of development."},
                 {"date": "2001", "title_uz": "Akademiya maqomi berildi",    "title_ru": "Присвоен статус академии", "title_en": "Academy Status Granted",
                  "desc_uz": "Institut O'zbekiston Davlat Sport Akademiyasi nomini oldi.",
                  "desc_ru": "Институт получил статус академии.",
                  "desc_en": "The institute received academy status."},
                 {"date": "2010", "title_uz": "Zamonaviy infratuzilma",      "title_ru": "Современная инфраструктура","title_en": "Modern Infrastructure",
                  "desc_uz": "Yangi sport majmuasi va laboratoriyalar qurildi.",
                  "desc_ru": "Построен новый спортивный комплекс и лаборатории.",
                  "desc_en": "New sports complex and laboratories were built."},
                 {"date": "2017", "title_uz": "Xalqaro akkreditatsiya",      "title_ru": "Международная аккредитация","title_en": "International Accreditation",
                  "desc_uz": "Bir qator xalqaro sport tashkilotlari tomonidan akkreditatsiya olindi.",
                  "desc_ru": "Получена аккредитация ряда международных спортивных организаций.",
                  "desc_en": "Accreditation received from several international sports organizations."},
                 {"date": "2023", "title_uz": "Yangi rivojlanish bosqichi",  "title_ru": "Новый этап развития",      "title_en": "New Development Stage",
                  "desc_uz": "Raqamli ta'lim va sun'iy intellekt laboratoriyasi ochildi.",
                  "desc_ru": "Открыта лаборатория цифрового образования и ИИ.",
                  "desc_en": "Digital education and AI laboratory opened."},
             ]}),

            # ── FACULTIES ──
            ('faculties', 'hero', 1,
             "Fakultetlar", "Факультеты", "Faculties",
             "<p>O'ZDSA da 4 ta fakultet faoliyat yuritadi. Har bir fakultet o'z sohasida yuqori malakali mutaxassislar tayyorlaydi.</p>",
             "<p>В УЗГСА функционируют 4 факультета, каждый из которых готовит высококвалифицированных специалистов.</p>",
             "<p>USAS has 4 faculties, each training highly qualified specialists in their field.</p>",
             None),
            ('faculties', 'rich-text', 2,
             "Fakultetlar haqida", "О факультетах", "About Faculties",
             "<h3>1. Jismoniy tarbiya va sport fakulteti</h3><p>Jismoniy tarbiya o'qituvchilari va sport murabbiylari tayyorlanadi.</p>"
             "<h3>2. Sport menejment va marketing fakulteti</h3><p>Sport industriyasi uchun menejerlar va marketologlar tayyorlanadi.</p>"
             "<h3>3. Trenerlik va sport murabbiyligi fakulteti</h3><p>Olimpiya sport turlari bo'yicha professional murabbiylar tayyorlanadi.</p>"
             "<h3>4. Magistratura va doktorantura fakulteti</h3><p>Ilmiy-pedagogik kadrlar tayyorlanadi.</p>",
             "<h3>1. Факультет физического воспитания и спорта</h3><p>Готовятся учителя физкультуры и спортивные тренеры.</p>"
             "<h3>2. Факультет спортивного менеджмента</h3><p>Готовятся менеджеры и маркетологи для спортивной индустрии.</p>"
             "<h3>3. Тренерский факультет</h3><p>Готовятся профессиональные тренеры по олимпийским видам спорта.</p>"
             "<h3>4. Факультет магистратуры и докторантуры</h3><p>Готовятся научно-педагогические кадры.</p>",
             "<h3>1. Faculty of Physical Education and Sports</h3><p>Physical education teachers and sports coaches are trained.</p>"
             "<h3>2. Faculty of Sports Management</h3><p>Managers and marketers for the sports industry are trained.</p>"
             "<h3>3. Faculty of Coaching</h3><p>Professional coaches for Olympic sports are trained.</p>"
             "<h3>4. Faculty of Graduate Studies</h3><p>Scientific-pedagogical staff are trained.</p>",
             None),

            # ── INSTITUTES ──
            ('institutes', 'rich-text', 1,
             "Institutlar", "Институты", "Institutes",
             "<h3>1. Sport ilmi va texnologiyalari instituti</h3><p>Sport fani sohasida ilmiy-tadqiqot ishlarini olib boradi.</p>"
             "<h3>2. Olimpiya tayyorgarligi instituti</h3><p>Olimpiya o'yinlariga tayyorgarlik dasturlarini ishlab chiqadi.</p>"
             "<h3>3. Sport tibbiyoti va reabilitatsiya instituti</h3><p>Sportchilar salomatligini saqlash va davolash bo'yicha xizmat ko'rsatadi.</p>",
             "<h3>1. Институт спортивной науки и технологий</h3><p>Проводит научно-исследовательские работы в области спортивной науки.</p>"
             "<h3>2. Институт олимпийской подготовки</h3><p>Разрабатывает программы подготовки к Олимпийским играм.</p>"
             "<h3>3. Институт спортивной медицины и реабилитации</h3><p>Оказывает услуги по сохранению здоровья и лечению спортсменов.</p>",
             "<h3>1. Institute of Sports Science and Technology</h3><p>Conducts research in sports science.</p>"
             "<h3>2. Institute of Olympic Preparation</h3><p>Develops Olympic preparation programs.</p>"
             "<h3>3. Institute of Sports Medicine and Rehabilitation</h3><p>Provides services for athlete health maintenance and treatment.</p>",
             None),

            # ── SPORT ACTIVITY ──
            ('sport-activity', 'hero', 1,
             "Sport faoliyati", "Спортивная деятельность", "Sports Activity",
             "<p>O'ZDSA talabalar 60 dan ortiq sport turi bo'yicha mashg'ulot olib boradilar va xalqaro musobaqalarda qatnashadilar.</p>",
             "<p>Студенты УЗГСА занимаются более чем 60 видами спорта и участвуют в международных соревнованиях.</p>",
             "<p>USAS students train in over 60 sports disciplines and participate in international competitions.</p>",
             None),
            ('sport-activity', 'stats', 2,
             "Sport yutuqlar", "Спортивные достижения", "Sports Achievements",
             None, None, None,
             {"stats": [
                 {"value": 60,  "label_uz": "Sport turlari",       "label_ru": "Видов спорта",         "label_en": "Sports Disciplines",  "suffix": "+"},
                 {"value": 180, "label_uz": "Olimpiya medaliylari","label_ru": "Олимпийских медалей",   "label_en": "Olympic Medals",       "suffix": "+"},
                 {"value": 350, "label_uz": "Jahon chempionlari",  "label_ru": "Чемпионов мира",        "label_en": "World Champions",      "suffix": "+"},
                 {"value": 12,  "label_uz": "Sport zallari",       "label_ru": "Спортивных залов",      "label_en": "Sports Halls",         "suffix": ""},
             ]}),

            # ── DOCTORAL STUDIES ──
            ('doctoral-studies', 'hero', 1,
             "Doktorantura", "Докторантура", "Doctoral Studies",
             "<p>O'ZDSA doktorantura dasturlari orqali eng yuqori ilmiy darajaga ega kadrlar tayyorlanadi.</p>",
             "<p>Через программы докторантуры УЗГСА готовятся кадры с высшей научной степенью.</p>",
             "<p>Through USAS doctoral programs, the highest degree academic staff are trained.</p>",
             None),
            ('doctoral-studies', 'table', 2,
             "Doktorantura yo'nalishlari", "Направления докторантуры", "Doctoral Directions",
             None, None, None,
             {"headers_uz": ["Kod", "Yo'nalish nomi", "Muddati", "O'quv shakli"],
              "headers_ru": ["Код", "Название направления", "Срок", "Форма обучения"],
              "headers_en": ["Code", "Direction Name", "Duration", "Study Form"],
              "rows": [
                  ["5A110101", "Jismoniy tarbiya nazariyasi va metodikasi", "3 yil", "Kunduzgi"],
                  ["5A110102", "Sport pedagogikasi",                         "3 yil", "Kunduzgi"],
                  ["5A110103", "Olimpiya sport turlari",                     "3 yil", "Kunduzgi / Sirtqi"],
                  ["5A110104", "Sport psixologiyasi",                        "3 yil", "Kunduzgi"],
                  ["5A110105", "Sport biomexanikasi va fiziologiyasi",        "3 yil", "Kunduzgi"],
              ]}),

            # ── BACHELOR ──
            ('bachelor', 'hero', 1,
             "Bakalavriat", "Бакалавриат", "Bachelor's Program",
             "<p>O'ZDSA bakalavriat dasturlari bo'yicha 4 yillik ta'lim beriladi. 26 ta yo'nalish bo'yicha talabalar qabul qilinadi.</p>",
             "<p>В УЗГСА предоставляется 4-летнее образование по бакалавриату по 26 направлениям.</p>",
             "<p>USAS offers 4-year bachelor's programs in 26 directions.</p>",
             None),
            ('bachelor', 'stats', 2,
             "Bakalavriat statistikasi", "Статистика бакалавриата", "Bachelor Statistics",
             None, None, None,
             {"stats": [
                 {"value": 26,   "label_uz": "Ta'lim yo'nalishlari",  "label_ru": "Направлений", "label_en": "Directions",  "suffix": ""},
                 {"value": 3800, "label_uz": "Bakalavr talabalar",    "label_ru": "Студентов",   "label_en": "Students",    "suffix": "+"},
                 {"value": 4,    "label_uz": "O'qish muddati (yil)",  "label_ru": "Лет обучения","label_en": "Study years", "suffix": ""},
             ]}),

            # ── MASTERS ──
            ('masters', 'hero', 1,
             "Magistratura", "Магистратура", "Master's Program",
             "<p>O'ZDSA magistratura dasturlari bo'yicha 2 yillik ta'lim beriladi. Ilmiy va amaliy yo'nalishlar mavjud.</p>",
             "<p>В УЗГСА предоставляется 2-летнее образование по магистратуре.</p>",
             "<p>USAS offers 2-year master's programs with both scientific and practical tracks.</p>",
             None),
            ('masters', 'table', 2,
             "Magistratura yo'nalishlari", "Направления магистратуры", "Master's Directions",
             None, None, None,
             {"headers_uz": ["Yo'nalish", "Muddati", "Narxi"],
              "headers_ru": ["Направление", "Срок", "Стоимость"],
              "headers_en": ["Direction", "Duration", "Cost"],
              "rows": [
                  ["Sport pedagogikasi va psixologiyasi",     "2 yil", "14 000 000 so'm"],
                  ["Olimpiya sport murabbiyligi",             "2 yil", "14 000 000 so'm"],
                  ["Sport menejment",                        "2 yil", "16 000 000 so'm"],
                  ["Sport tibbiyoti",                        "2 yil", "18 000 000 so'm"],
                  ["Amaliy sport fanlari",                   "2 yil", "14 000 000 so'm"],
              ]}),

            # ── INTERNATIONAL PARTNERS ──
            ('international-partners', 'hero', 1,
             "Xalqaro hamkorlar", "Международные партнёры", "International Partners",
             "<p>O'ZDSA dunyo bo'ylab 52 dan ortiq nufuzli universitetlar va tashkilotlar bilan hamkorlik qiladi.</p>",
             "<p>УЗГСА сотрудничает с более чем 52 престижными университетами и организациями по всему миру.</p>",
             "<p>USAS cooperates with over 52 prestigious universities and organizations worldwide.</p>",
             None),
            ('international-partners', 'rich-text', 2,
             "Asosiy hamkorlar", "Основные партнёры", "Key Partners",
             "<h3>Yevropadagi hamkorlar</h3><ul><li>Germaniya Sport Universiteti (Köln)</li><li>Finlyandiya Jivaskyla Universiteti</li>"
             "<li>Polsha Gdansk Sport Akademiyasi</li></ul>"
             "<h3>Osiyodagi hamkorlar</h3><ul><li>Xitoy Beijing Sport Universiteti</li><li>Yaponiya Nippon Sport Instituti</li>"
             "<li>Janubiy Koreya Incheon Universiteti</li></ul>"
             "<h3>MDA davlatlari</h3><ul><li>Rossiya Sport Pedagogika Akademiyasi</li><li>Qozog'iston Sport va Turizm Akademiyasi</li></ul>",
             "<h3>Партнёры в Европе</h3><ul><li>Немецкий спортивный университет (Кёльн)</li></ul>"
             "<h3>Партнёры в Азии</h3><ul><li>Пекинский спортивный университет</li></ul>",
             "<h3>Partners in Europe</h3><ul><li>German Sport University Cologne</li></ul>"
             "<h3>Partners in Asia</h3><ul><li>Beijing Sport University</li></ul>",
             None),

            # ── ACADEMIC MOBILITY ──
            ('academic-mobility', 'hero', 1,
             "Akademik almashinuv", "Академическая мобильность", "Academic Mobility",
             "<p>Akademik almashinuv dasturlari orqali talabalar va o'qituvchilar xorijda tahsil olish va malaka oshirish imkoniyatiga ega.</p>",
             "<p>Через программы академической мобильности студенты и преподаватели могут учиться и повышать квалификацию за рубежом.</p>",
             "<p>Through academic mobility programs, students and teachers can study and improve their qualifications abroad.</p>",
             None),
            ('academic-mobility', 'rich-text', 2,
             "Dasturlar haqida", "О программах", "About Programs",
             "<h3>Erasmus+ dasturi</h3><p>Yevropa universitetlarida 1 semestr yoki 1 yil tahsil olish imkoniyati.</p>"
             "<h3>Fulbright dasturi</h3><p>AQSHda ilmiy tadqiqot va magistratura uchun grant.</p>"
             "<h3>Silk Road dasturi</h3><p>Osiyo va MDA mamlakatlari universitetlari bilan almashinuv.</p>",
             "<h3>Программа Erasmus+</h3><p>Возможность обучения в европейских университетах 1 семестр или 1 год.</p>",
             "<h3>Erasmus+ Program</h3><p>Opportunity to study at European universities for 1 semester or 1 year.</p>",
             None),

            # ── STUDENT PRIVILEGES ──
            ('student-privileges', 'rich-text', 1,
             "Talabalar imtiyozlari", "Льготы студентам", "Student Privileges",
             "<h3>Ijtimoiy imtiyozlar</h3><ul><li>Stipendiya va qo'shimcha to'lovlar</li><li>Preferansial narxlarda ovqatlanish</li>"
             "<li>Sport inventar va kiyim-kechak bilan ta'minlanish</li></ul>"
             "<h3>O'quv imtiyozlari</h3><ul><li>Bepul kutubxona va elektron resurslar</li><li>Ilmiy tadqiqotlarga davlat granti</li>"
             "<li>Xalqaro musobaqalarda qatnashish uchun moliyaviy qo'llab-quvvatlash</li></ul>",
             "<h3>Социальные льготы</h3><ul><li>Стипендии и дополнительные выплаты</li></ul>",
             "<h3>Social Privileges</h3><ul><li>Scholarships and additional payments</li></ul>",
             None),

            # ── SCHOLARSHIPS ──
            ('scholarships', 'hero', 1,
             "Stipendiyalar", "Стипендии", "Scholarships",
             "<p>O'ZDSA talabalar uchun davlat stipendiyasi va akademik natijalarga ko'ra qo'shimcha moddiy rag'batlantirishlar mavjud.</p>",
             "<p>В УЗГСА действуют государственные стипендии и дополнительные поощрения по академическим результатам.</p>",
             "<p>USAS has state scholarships and additional incentives based on academic results.</p>",
             None),
            ('scholarships', 'table', 2,
             "Stipendiya turlari", "Виды стипендий", "Scholarship Types",
             None, None, None,
             {"headers_uz": ["Tur", "Miqdori", "Shartlar"],
              "headers_ru": ["Вид", "Размер", "Условия"],
              "headers_en": ["Type", "Amount", "Conditions"],
              "rows": [
                  ["Davlat stipendiyasi",            "735 000 so'm/oy",    "GPA 3.0 dan yuqori"],
                  ["Prezident stipendiyasi",          "2 200 000 so'm/oy", "GPA 3.8 dan yuqori + ilmiy faoliyat"],
                  ["Sport ustamasi",                  "500 000 so'm/oy",   "Milliy terma jamoa a'zolari"],
                  ["O'zbekiston chempioni ustamasi",  "1 000 000 so'm/oy", "O'zbekiston chempionlari"],
                  ["Xalqaro medal ustamasi",          "2 000 000 so'm/oy", "Xalqaro musobaqalar g'oliblari"],
              ]}),

            # ── DORMITORY ──
            ('dormitory', 'hero', 1,
             "Talabalar turar joyi", "Общежитие", "Dormitory",
             "<p>O'ZDSA 2 000 o'rinli zamonaviy talabalar yotoqxonasiga ega. Barcha qulayliklar bilan jihozlangan.</p>",
             "<p>УЗГСА имеет современное общежитие на 2000 мест со всеми удобствами.</p>",
             "<p>USAS has a modern dormitory with 2000 places equipped with all amenities.</p>",
             None),
            ('dormitory', 'rich-text', 2,
             "Yotoqxona xizmatlari", "Услуги общежития", "Dormitory Services",
             "<h3>Imkoniyatlar</h3><ul><li>Ikkita yotoqxona binosi (A va B korpus)</li><li>Wi-Fi Internet</li>"
             "<li>Oshxona va kafe</li><li>Sport zali</li><li>O'qish xonasi</li><li>Tibbiy punkt</li></ul>"
             "<h3>Narxlar</h3><p>Bir o'rinlik xona: 400 000 so'm/oy<br>Ikki o'rinlik xona: 250 000 so'm/oy</p>",
             "<h3>Возможности</h3><ul><li>Два корпуса общежития</li><li>Wi-Fi интернет</li><li>Столовая</li></ul>",
             "<h3>Facilities</h3><ul><li>Two dormitory buildings</li><li>Wi-Fi Internet</li><li>Cafeteria</li></ul>",
             None),

            # ── CONTRACT PRICES ──
            ('contract-prices', 'table', 1,
             "To'lov-kontrakt narxlari", "Стоимость контракта", "Contract Prices",
             None, None, None,
             {"headers_uz": ["Yo'nalish", "Ta'lim shakli", "Narx (yillik)"],
              "headers_ru": ["Направление", "Форма обучения", "Цена (в год)"],
              "headers_en": ["Direction", "Study Form", "Price (annual)"],
              "rows": [
                  ["Jismoniy tarbiya",             "Kunduzgi",  "10 500 000 so'm"],
                  ["Sport murabbiyligi",           "Kunduzgi",  "10 500 000 so'm"],
                  ["Sport menejment",              "Kunduzgi",  "12 000 000 so'm"],
                  ["Sport jurnalistikasi",         "Kunduzgi",  "11 000 000 so'm"],
                  ["Magistratura (barcha tur.)",   "Kunduzgi",  "14 000 000 so'm"],
              ]}),

            # ── GREEN ACADEMY ──
            ('green-academy', 'hero', 1,
             "Yashil Akademiya loyihasi", "Проект Зелёная Академия", "Green Academy Project",
             "<p>O'ZDSA 2022-yildan boshlab «Yashil Akademiya» loyihasini amalga oshirmoqda — ekologik barqarorlik va yashil muhit.</p>",
             "<p>С 2022 года УЗГСА реализует проект «Зелёная Академия» — экологическая устойчивость и зелёная среда.</p>",
             "<p>Since 2022, USAS has been implementing the 'Green Academy' project — ecological sustainability and green environment.</p>",
             None),
            ('green-academy', 'stats', 2,
             "Yashil loyiha natijalari", "Результаты зелёного проекта", "Green Project Results",
             None, None, None,
             {"stats": [
                 {"value": 2000, "label_uz": "Ekilgan daraxtlar",  "label_ru": "Посаженных деревьев", "label_en": "Trees Planted",      "suffix": "+"},
                 {"value": 35,   "label_uz": "Ekoguruhlar",        "label_ru": "Экогрупп",            "label_en": "Eco Groups",         "suffix": ""},
                 {"value": 60,   "label_uz": "Qoplama foizi",      "label_ru": "% покрытия",          "label_en": "Coverage %",         "suffix": "%"},
             ]}),

            # ── SCIENTIFIC PROJECTS ──
            ('scientific-projects', 'hero', 1,
             "Ilmiy loyihalar", "Научные проекты", "Scientific Projects",
             "<p>O'ZDSA olimlari davlat va xalqaro grantlar bo'yicha 30 dan ortiq ilmiy loyihalarda ishtirok etmoqda.</p>",
             "<p>Учёные УЗГСА участвуют в более чем 30 научных проектах по государственным и международным грантам.</p>",
             "<p>USAS scientists participate in over 30 research projects under state and international grants.</p>",
             None),
            ('scientific-projects', 'stats', 2,
             "Ilmiy ko'rsatkichlar", "Научные показатели", "Scientific Indicators",
             None, None, None,
             {"stats": [
                 {"value": 30,  "label_uz": "Faol loyihalar",       "label_ru": "Активных проектов",  "label_en": "Active Projects",   "suffix": "+"},
                 {"value": 450, "label_uz": "Ilmiy maqolalar",       "label_ru": "Научных статей",     "label_en": "Scientific Papers", "suffix": "+"},
                 {"value": 15,  "label_uz": "Patentlar",             "label_ru": "Патентов",           "label_en": "Patents",           "suffix": ""},
             ]}),

            # ── NATIONAL RATING ──
            ('national-rating', 'stats', 1,
             "Milliy reyting", "Национальный рейтинг", "National Rating",
             None, None, None,
             {"stats": [
                 {"value": 1,   "label_uz": "Sport sohasida reyting","label_ru": "Рейтинг в спорте",   "label_en": "Sports Ranking",     "suffix": "-o'rin"},
                 {"value": 3,   "label_uz": "Umumiy reyting",        "label_ru": "Общий рейтинг",      "label_en": "Overall Ranking",    "suffix": "-o'rin"},
             ]}),
            ('national-rating', 'rich-text', 2,
             "Reyting haqida", "О рейтинге", "About Rating",
             "<p>O'ZDSA O'zbekiston oliy ta'lim muassasalari milliy reytingida birinchi o'rinda turadi (sport sohasida). "
             "Davlat ta'lim sifatini baholash agentligi (DTSB) tomonidan har yili o'tkaziladi.</p>",
             "<p>УЗГСА занимает первое место в национальном рейтинге вузов Узбекистана (в сфере спорта).</p>",
             "<p>USAS ranks first in the national rating of Uzbekistan's higher education institutions in the sports sector.</p>",
             None),

            # ── CENTERS ──
            ('centers', 'rich-text', 1,
             "Akademiya markazlari", "Центры академии", "Academy Centers",
             "<h3>1. Sport ilmi va texnologiyalari markazi</h3><p>Ilmiy tadqiqotlar va texnologik innovatsiyalar markazi.</p>"
             "<h3>2. Olimpiya tayyorgarligi markazi</h3><p>Olimpiya sportchilarini tayyorlash uchun maxsus markaz.</p>"
             "<h3>3. Sport psixologiyasi markazi</h3><p>Sportchilar psixologik tayyorgarligini ta'minlaydi.</p>"
             "<h3>4. Karyer rivojlantirish markazi</h3><p>Bitiruvchilar va talabalarga ish topishda yordam beradi.</p>"
             "<h3>5. Til o'rganish markazi</h3><p>Chet tillari va professional kommunikatsiya kurslari.</p>",
             "<h3>1. Центр спортивной науки и технологий</h3><p>Центр научных исследований и технологических инноваций.</p>",
             "<h3>1. Center of Sports Science and Technology</h3><p>Center for scientific research and technological innovations.</p>",
             None),
        ]

        for (slug, btype, order, tuz, tru, ten, duz, dru, den, jdata) in blocks:
            p = page(slug)
            if not p:
                continue
            obj, created = ContentBlock.objects.get_or_create(
                navbar_item=p,
                title_uz=tuz,
                defaults={
                    'block_type':      btype,
                    'title_ru':        tru or '',
                    'title_en':        ten or '',
                    'description_uz':  duz or '',
                    'description_ru':  dru or '',
                    'description_en':  den or '',
                    'json_data':       jdata,
                    'order':           order,
                    'is_active':       True,
                },
            )
            if created:
                count += 1

        # ── LINK BLOCKS (hujjatlar va foydali havolalar) ──
        link_blocks = [
            # (slug, block_type, title_uz, title_ru, title_en, link, order)
            ('academy-regulations', 'file-list', "Akademiya ustavi", "Устав академии", "Academy Charter",
             'https://usas.uz/docs/charter.pdf', 1),
            ('academy-regulations', 'file-list', "Ichki tartib qoidalari", "Внутренний регламент", "Internal Regulations",
             'https://usas.uz/docs/internal-rules.pdf', 2),
            ('academy-regulations', 'file-list', "O'quv jarayoni to'g'risidagi nizom", "Положение об учебном процессе", "Academic Process Regulation",
             'https://usas.uz/docs/academic-process.pdf', 3),
            ('admission-regulations', 'file-list', "Qabul to'g'risidagi nizom", "Положение о приёме", "Admission Regulation",
             'https://usas.uz/docs/admission.pdf', 1),
            ('admission-regulations', 'file-list', "Imtiyozlar ro'yxati", "Список льгот", "Privileges List",
             'https://usas.uz/docs/privileges.pdf', 2),
            ('educational-literature', 'file-list', "Jismoniy tarbiya nazariyasi va metodikasi", "Теория и методика физ. воспитания", "Theory and Methodology of PE",
             'https://usas.uz/docs/textbook1.pdf', 1),
            ('educational-literature', 'file-list', "Sport biologiyasi", "Спортивная биология", "Sports Biology",
             'https://usas.uz/docs/textbook2.pdf', 2),
            ('educational-literature', 'file-list', "Olimpiya harakati tarixi", "История олимпийского движения", "History of Olympic Movement",
             'https://usas.uz/docs/textbook3.pdf', 3),
            ('student-privileges', 'useful-links', "HEMIS tizimi", "Система HEMIS", "HEMIS System",
             'https://hemis.edu.uz', 1),
            ('student-privileges', 'useful-links', "Talaba shaxsiy kabineti", "Личный кабинет студента", "Student Personal Account",
             'https://my.usas.uz', 2),
            ('student-privileges', 'useful-links', "Elektron kutubxona", "Электронная библиотека", "Electronic Library",
             'https://lib.usas.uz', 3),
        ]
        for (slug, btype, tuz, tru, ten, link, order) in link_blocks:
            p = page(slug)
            if not p:
                continue
            obj, created = LinkBlock.objects.get_or_create(
                navbar_item=p,
                title_uz=tuz,
                defaults={
                    'block_type': btype,
                    'title_ru':   tru,
                    'title_en':   ten,
                    'link':       link,
                    'order':      order,
                    'is_active':  True,
                },
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'   {count} kontent blok'))

    # ──────────────────────────────────────────────────────────────────────────
    # 8. AXBOROT XIZMATI (InformationContent)
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_information_content(self):
        self.stdout.write('\n── Axborot xizmati ...')
        from django.utils.timezone import make_aware
        from datetime import datetime
        def dt(y, m, d): return make_aware(datetime(y, m, d))
        count = 0

        items = [
            # (slug, content_type, title_uz, title_ru, title_en, desc_uz, desc_ru, desc_en, date)
            ('rector-activities', 'rector',
             "Rektor Yaponiya Sport Universitetiga tashrif buyurdi",
             "Ректор посетил Японский спортивный университет",
             "Rector Visited Japan Sports University",
             "<p>O'ZDSA rektori Abdullayev J.Q. Yaponiya Sport Universiteti bilan hamkorlik memorandumini imzoladi.</p>",
             "<p>Ректор УЗГСА Абдуллаев Дж.К. подписал меморандум о сотрудничестве с Японским спортивным университетом.</p>",
             "<p>USAS Rector Abdullayev J.Q. signed a cooperation memorandum with Japan Sports University.</p>",
             dt(2026, 3, 15)),
            ('rector-activities', 'rector',
             "Rektor milliy terma jamoalar bosh murabbiyilari bilan uchrashdi",
             "Ректор встретился с главными тренерами национальных сборных",
             "Rector Met with Head Coaches of National Teams",
             "<p>Uchrashuvda zamonaviy sport ta'limi va kadrlar tayyorlash masalalari muhokama qilindi.</p>",
             "<p>На встрече обсуждались вопросы современного спортивного образования и подготовки кадров.</p>",
             "<p>The meeting discussed modern sports education and staff training issues.</p>",
             dt(2026, 3, 20)),
            ('rector-activities', 'rector',
             "O'ZDSA rektori Olimpiya qo'mitasi sessiyasida ishtirok etdi",
             "Ректор УЗГСА принял участие в сессии Олимпийского комитета",
             "USAS Rector Participated in Olympic Committee Session",
             "<p>Xalqaro Olimpiya Qo'mitasi yillik sessiyasida akademiyaning faoliyati yuzasidan ma'ruza qilindi.</p>",
             "<p>На ежегодной сессии Международного олимпийского комитета был сделан доклад о деятельности академии.</p>",
             "<p>A report was presented on the academy's activities at the IOC annual session.</p>",
             dt(2026, 2, 10)),

            # BRIEFINGS
            ('briefings', 'briefing',
             "2025-2026 o'quv yili natijalari bo'yicha brifing",
             "Брифинг по итогам 2025-2026 учебного года",
             "Briefing on 2025-2026 Academic Year Results",
             "<p>Akademiya rahbariyati o'quv yili natijalari, talabalar o'zlashtirishi va sport yutuqlari haqida ma'lumot berdi.</p>",
             "<p>Руководство академии рассказало об итогах учебного года, успеваемости студентов и спортивных достижениях.</p>",
             "<p>The academy administration provided information on academic year results, student performance and sports achievements.</p>",
             dt(2026, 3, 1)),
            ('briefings', 'briefing',
             "Xalqaro hamkorlik dasturlari bo'yicha brifing",
             "Брифинг по программам международного сотрудничества",
             "Briefing on International Cooperation Programs",
             "<p>2026-2027 yillarda talabalarga taqdim etiladigan xalqaro grant va almashinuv dasturlari tanishtrildi.</p>",
             "<p>Представлены международные гранты и программы обмена для студентов на 2026-2027 годы.</p>",
             "<p>International grants and exchange programs for students in 2026-2027 were presented.</p>",
             dt(2026, 2, 20)),

            # CONTESTS
            ('contests', 'contest',
             "«Eng yaxshi talaba-sportchi» tanloviga ariza qabul qilinmoqda",
             "Принимаются заявки на конкурс «Лучший студент-спортсмен»",
             "Applications Accepted for 'Best Student-Athlete' Contest",
             "<p>Har yilgi an'anaviy tanlov boshlanmoqda. Ariza topshirish muddati — 2026-yil 30-aprelgacha.</p>",
             "<p>Начинается ежегодный традиционный конкурс. Срок подачи заявок — до 30 апреля 2026 года.</p>",
             "<p>The annual traditional contest begins. Application deadline — April 30, 2026.</p>",
             dt(2026, 3, 10)),
            ('contests', 'contest',
             "«Ilmiy loyiha» tanlovi natijalari e'lon qilindi",
             "Объявлены результаты конкурса «Научный проект»",
             "'Research Project' Contest Results Announced",
             "<p>O'ZDSA yillik ilmiy loyiha tanlovida g'oliblar aniqlandi. 1-o'rin: Toshmatov A.H. (Sport biomexanikasi).</p>",
             "<p>Определены победители ежегодного конкурса научных проектов УЗГСА.</p>",
             "<p>Winners of the USAS annual research project contest have been determined.</p>",
             dt(2026, 3, 5)),

            # PRESS SERVICE
            ('press-service', 'press',
             "O'ZDSA Sport.uz gazetasiga intervyu berdi",
             "УЗГСА дало интервью газете Sport.uz",
             "USAS Gave Interview to Sport.uz Newspaper",
             "<p>Akademiya rektori O'zbekiston sport jurnali bilan suhbatda akademiyaning rivojlanish rejalarini bayon qildi.</p>",
             "<p>Ректор академии в интервью изданию рассказал о планах развития академии.</p>",
             "<p>The academy rector outlined development plans in an interview with the sports journal.</p>",
             dt(2026, 3, 25)),
            ('press-service', 'press',
             "Xalqaro sport nashrlari O'ZDSA haqida yozdi",
             "Международные спортивные издания написали об УЗГСА",
             "International Sports Publications Wrote About USAS",
             "<p>SportAccord va SportsGoal nashrlari O'ZDSA va O'zbekiston sport yutuqlari haqida maqola e'lon qildi.</p>",
             "<p>Издания SportAccord и SportsGoal опубликовали статью о УЗГСА и спортивных достижениях Узбекистана.</p>",
             "<p>SportAccord and SportsGoal publications published articles about USAS and Uzbekistan's sports achievements.</p>",
             dt(2026, 2, 28)),

            # PHOTO GALLERY
            ('photo-gallery', 'photo',
             "Bahor sport festivali fotolari",
             "Фотографии весеннего спортивного фестиваля",
             "Spring Sports Festival Photos",
             "<p>2026-yil 21-mart kuni o'tkazilgan bahor sport festivali suratlari.</p>",
             "<p>Фотографии весеннего спортивного фестиваля, проведённого 21 марта 2026 года.</p>",
             "<p>Photos from the Spring Sports Festival held on March 21, 2026.</p>",
             dt(2026, 3, 21)),
            ('photo-gallery', 'photo',
             "Xalqaro delegatsiya tashrifi fotolari",
             "Фото визита международной делегации",
             "International Delegation Visit Photos",
             "<p>Xalqaro Olimpiya Qo'mitasi delegatsiyasining O'ZDSA ga tashrifi fotosuratlari.</p>",
             "<p>Фотографии визита делегации Международного олимпийского комитета в УЗГСА.</p>",
             "<p>Photos of the IOC delegation visit to USAS.</p>",
             dt(2026, 3, 12)),

            # VIDEO GALLERY
            ('video-gallery', 'video',
             "O'ZDSA prezentatsion videosi",
             "Презентационное видео УЗГСА",
             "USAS Presentation Video",
             "<p>Akademiya infratuzilmasi, ta'lim jarayoni va sport yutuqlarini ko'rsatuvchi prezentatsion video.</p>",
             "<p>Презентационное видео, показывающее инфраструктуру академии, учебный процесс и спортивные достижения.</p>",
             "<p>Presentation video showcasing the academy's infrastructure, educational process and sports achievements.</p>",
             dt(2026, 1, 15)),
            ('video-gallery', 'video',
             "Olimpiya o'yinlariga tayyorgarlik jarayoni",
             "Процесс подготовки к Олимпийским играм",
             "Olympic Games Preparation Process",
             "<p>2028 Los-Anjeles Olimpiadasi uchun tayyorgarlik ko'rayotgan O'ZDSA talabalarining video mashg'ulotlari.</p>",
             "<p>Видео тренировок студентов УЗГСА, готовящихся к Олимпиаде 2028 в Лос-Анджелесе.</p>",
             "<p>Training videos of USAS students preparing for the 2028 Los Angeles Olympics.</p>",
             dt(2026, 2, 5)),
        ]

        for (slug, ctype, tuz, tru, ten, duz, dru, den, ev_date) in items:
            p = page(slug)
            if not p:
                continue
            obj, created = InformationContent.objects.get_or_create(
                navbar_item=p,
                title_uz=tuz,
                defaults={
                    'content_type':    ctype,
                    'title_ru':        tru,
                    'title_en':        ten,
                    'description_uz':  duz,
                    'description_ru':  dru,
                    'description_en':  den,
                    'date':            ev_date,
                    'is_published':    True,
                },
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'   {count} axborot yozuvi'))

    # ──────────────────────────────────────────────────────────────────────────
    # 9. YANGILIKLAR / TADBIRLAR / BLOG
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_news(self):
        self.stdout.write('\n── Yangiliklar, tadbirlar, blog ...')
        from django.utils.timezone import make_aware
        from datetime import datetime
        def dt(y, m, d): return make_aware(datetime(y, m, d))
        count = 0

        news_items = [
            ("O'ZDSA talabalari Osiyo chempionatida 5 ta medal qozondi",
             "Студенты УЗГСА завоевали 5 медалей на чемпионате Азии",
             "USAS Students Won 5 Medals at Asian Championship",
             "<p>O'ZDSA talabalaridan iborat O'zbekiston terma jamoasi Osiyo chempionatida 2 ta oltin, 1 ta kumush va 2 ta bronza medal qozondi.</p>"
             "<p>Gimnastika, kurash va yengil atletika bo'yicha medallar qo'lga kiritildi.</p>",
             "<p>Сборная Узбекистана из студентов УЗГСА завоевала 2 золотые, 1 серебряную и 2 бронзовые медали.</p>",
             "<p>Uzbekistan's national team of USAS students won 2 gold, 1 silver and 2 bronze medals at the Asian Championship.</p>",
             dt(2026, 3, 28)),
            ("Germaniya Sport Universiteti bilan hamkorlik memorandumi imzolandi",
             "Подписан меморандум о сотрудничестве с Немецким спортивным университетом",
             "Cooperation Memorandum Signed with German Sport University",
             "<p>O'ZDSA va Germaniyaning Köln shahridagi Sport Universiteti o'rtasida 5 yillik hamkorlik memorandumi imzolandi.</p>"
             "<p>Memorandum talabalar va o'qituvchilar almashinuvi, qo'shma ilmiy tadqiqotlar va malaka oshirishni nazarda tutadi.</p>",
             "<p>Подписан 5-летний меморандум о сотрудничестве между УЗГСА и Спортивным университетом Кёльна.</p>",
             "<p>A 5-year cooperation memorandum was signed between USAS and the German Sport University Cologne.</p>",
             dt(2026, 3, 22)),
            ("O'ZDSA da zamonaviy sport biomexanikasi laboratoriyasi ochildi",
             "В УЗГСА открылась современная лаборатория спортивной биомеханики",
             "Modern Sports Biomechanics Laboratory Opened at USAS",
             "<p>Akademiyada eng zamonaviy sport biomexanikasi laboratoriyasi ochildi. Laboratoriya xarid qilgan uskunalar Yaponiya va Germaniyadan keltirilgan.</p>"
             "<p>Yangi laboratoriya sportchilar texnikasini tahlil qilish va samaradorlikni oshirishda muhim rol o'ynaydi.</p>",
             "<p>Открылась современная лаборатория спортивной биомеханики. Оборудование было приобретено в Японии и Германии.</p>",
             "<p>A state-of-the-art sports biomechanics laboratory has opened. Equipment was sourced from Japan and Germany.</p>",
             dt(2026, 3, 10)),
            ("Prezident O'ZDSA bitiruvchilarini qabul qildi",
             "Президент принял выпускников УЗГСА",
             "President Received USAS Graduates",
             "<p>O'zbekiston Prezidenti Shavkat Mirziyoyev olimpiya va jahon chempionati g'oliblarini qabul qildi.</p>"
             "<p>Davlat rahbari sportchilarning yutuqlarini yuqori baholab, sport ta'limini yanada rivojlantirish vazifalarini belgilab berdi.</p>",
             "<p>Президент Шавкат Мирзиёев принял победителей Олимпийских игр и чемпионата мира — выпускников УЗГСА.</p>",
             "<p>President Shavkat Mirziyoyev received Olympic and world championship winners — USAS graduates.</p>",
             dt(2026, 2, 15)),
        ]
        for (tuz, tru, ten, duz, dru, den, ev_date) in news_items:
            obj, created = News.objects.get_or_create(
                title_uz=tuz,
                defaults={
                    'title_ru': tru, 'title_en': ten,
                    'description_uz': duz, 'description_ru': dru, 'description_en': den,
                    'date': ev_date, 'is_published': True,
                },
            )
            if created:
                count += 1

        events = [
            ("Yillik sport olympiadasi — 2026",
             "Ежегодная спортивная олимпиада — 2026",
             "Annual Sports Olympiad — 2026",
             "<p>O'ZDSA ichki yillik sport olympiadasi aprel oyida o'tkaziladi. Barcha kurs talabalari qatnasha oladi.</p>",
             "<p>Ежегодная внутренняя спортивная олимпиада УЗГСА проводится в апреле.</p>",
             "<p>The annual internal USAS Sports Olympiad is held in April. All students can participate.</p>",
             dt(2026, 4, 15), "O'ZDSA Sport majmuasi", "Спортивный комплекс УЗГСА", "USAS Sports Complex"),
            ("Xalqaro student sport konferensiyasi",
             "Международная студенческая спортивная конференция",
             "International Student Sports Conference",
             "<p>«Sport — sog'lom turmush tarzi» mavzusida xalqaro konferensiya. 15 mamlakatdan delegatlar qatnashadi.</p>",
             "<p>Международная конференция на тему «Спорт — здоровый образ жизни». Участники из 15 стран.</p>",
             "<p>International conference on 'Sports — Healthy Lifestyle'. Delegates from 15 countries.</p>",
             dt(2026, 5, 20), "O'ZDSA Konferensiya zali", "Конференц-зал УЗГСА", "USAS Conference Hall"),
            ("O'ZDSA ochiq eshiklar kuni",
             "День открытых дверей УЗГСА",
             "USAS Open Day",
             "<p>Barcha abituriyentlar va maktab o'quvchilari uchun ochiq eshiklar kuni. Akademiyaning barcha bo'limlari bilan tanishish mumkin.</p>",
             "<p>День открытых дверей для абитуриентов и школьников. Можно ознакомиться со всеми подразделениями академии.</p>",
             "<p>Open Day for all applicants and school students. All departments of the academy can be visited.</p>",
             dt(2026, 4, 20), "O'ZDSA, bosh bino", "УЗГСА, главный корпус", "USAS Main Building"),
        ]
        for (tuz, tru, ten, duz, dru, den, ev_date, luz, lru, len_) in events:
            obj, created = Event.objects.get_or_create(
                title_uz=tuz,
                defaults={
                    'title_ru': tru, 'title_en': ten,
                    'description_uz': duz, 'description_ru': dru, 'description_en': den,
                    'date': ev_date, 'location_uz': luz, 'location_ru': lru, 'location_en': len_,
                    'is_published': True,
                },
            )
            if created:
                count += 1

        blogs = [
            ("Zamonaviy sportchi: muvaffaqiyatning 5 ta siri",
             "Современный спортсмен: 5 секретов успеха",
             "Modern Athlete: 5 Secrets of Success",
             "<h3>1. Muntazam mashg'ulot</h3><p>Har kuni belgilangan jadval bo'yicha mashg'ulot — muvaffaqiyatning asosi.</p>"
             "<h3>2. To'g'ri ovqatlanish</h3><p>Sport dietologiyasi samaradorlikni 30% gacha oshirishi mumkin.</p>"
             "<h3>3. Psixologik tayyorgarlik</h3><p>Mental kuch jismoniy kuchdan kam emas.</p>"
             "<h3>4. Uyqu va tiklanish</h3><p>Kuniga 8-9 soat uyqu organizmni to'la tiklaydi.</p>"
             "<h3>5. Ilmiy yondashuv</h3><p>Zamonaviy texnologiyalardan foydalanish natijalarga sezilarli ta'sir ko'rsatadi.</p>",
             None, None,
             dt(2026, 3, 18)),
            ("Sport va ta'lim: uyg'unlik sirri",
             "Спорт и образование: секрет гармонии",
             "Sports and Education: The Secret of Harmony",
             "<p>Ko'p talabalar sport bilan ta'lim o'rtasidagi muvozanatni saqlash qiyin deb hisoblashadi. Lekin bu mumkin!</p>"
             "<h3>Vaqtni rejalashtirish</h3><p>Haftalik jadval tuzib, o'quv va mashg'ulot vaqtlarini aniq belgilang.</p>"
             "<h3>Prioritetlarni belgilash</h3><p>Imtihon davrida akademik yutuqlarni birinchi o'ringa qo'ying.</p>",
             None, None,
             dt(2026, 2, 25)),
        ]
        for (tuz, tru, ten, duz, dru, den, ev_date) in blogs:
            obj, created = Blog.objects.get_or_create(
                title_uz=tuz,
                defaults={
                    'title_ru': tru or '', 'title_en': ten or '',
                    'description_uz': duz, 'description_ru': dru or '', 'description_en': den or '',
                    'date': ev_date, 'is_published': True,
                },
            )
            if created:
                count += 1

        self.stdout.write(self.style.SUCCESS(f'   {count} yangilik/tadbir/blog'))

    # ──────────────────────────────────────────────────────────────────────────
    # 10. FAQ
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_faq(self):
        self.stdout.write('\n── FAQ ...')
        count = 0
        faqs = [
            ("O'ZDSA ga qabul qilish uchun qanday hujjatlar talab etiladi?",
             "Какие документы нужны для поступления в УЗГСА?",
             "What documents are required for admission to USAS?",
             "<p>Qabul uchun quyidagi hujjatlar talab etiladi: <ul><li>Pasport (original va nusxa)</li>"
             "<li>Attestat yoki diplom (original)</li><li>Sport razryadi yoki unvoni haqida guvohnoma</li>"
             "<li>Tibbiy ma'lumotnoma (086-shakl)</li><li>6 ta 3×4 formatdagi rasm</li></ul></p>",
             "<p>Для поступления требуются: паспорт, аттестат/диплом, справка о спортивном разряде, медицинская справка (форма 086), 6 фото 3×4.</p>",
             "<p>Required documents: passport, certificate/diploma, sports rank certificate, medical certificate (form 086), 6 photos 3×4.</p>"),
            ("O'ZDSA da qanday yo'nalishlar mavjud?",
             "Какие направления есть в УЗГСА?",
             "What directions are available at USAS?",
             "<p>O'ZDSA da 26 ta bakalavriat yo'nalishi mavjud, jumladan jismoniy tarbiya, sport murabbiyligi, sport menejment, "
             "sport tibbiyoti va boshqalar. To'liq ro'yxat qabul bo'limida mavjud.</p>",
             "<p>В УЗГСА есть 26 направлений бакалавриата: физическое воспитание, спортивный тренинг, спортивный менеджмент и другие.</p>",
             "<p>USAS has 26 bachelor's directions including physical education, sports coaching, sports management and others.</p>"),
            ("Yotoqxona bor bo'yicha xizmat ko'rsatiladi?",
             "Предоставляется ли общежитие?",
             "Is dormitory accommodation provided?",
             "<p>Ha, O'ZDSA 2 000 o'rinli yotoqxona bilan ta'minlangan. Shahar tashqarisidan kelgan va kamtamin oilalardan "
             "bo'lgan talabalarga birinchi navbatda joy beriladi. Narxi: 250 000 – 400 000 so'm/oy.</p>",
             "<p>Да, УЗГСА оснащён общежитием на 2000 мест. Цена: 250 000 – 400 000 сум/месяц.</p>",
             "<p>Yes, USAS has a dormitory with 2000 places. Price: 250,000 – 400,000 soums/month.</p>"),
            ("Stipendiya miqdori qancha?",
             "Каков размер стипендии?",
             "What is the scholarship amount?",
             "<p>Asosiy davlat stipendiyasi: <strong>735 000 so'm/oy</strong>. GPA 3.8 dan yuqori bo'lgan talabalarga "
             "Prezident stipendiyasi — <strong>2 200 000 so'm/oy</strong> to'lanadi. Milliy terma jamoa a'zolariga "
             "qo'shimcha sport ustamasi beriladi.</p>",
             "<p>Базовая государственная стипендия: 735 000 сум/месяц. Президентская стипендия: 2 200 000 сум/месяц.</p>",
             "<p>Basic state scholarship: 735,000 soums/month. Presidential scholarship: 2,200,000 soums/month.</p>"),
            ("Xorijiy talabalar uchun qabul tartibi qanday?",
             "Каков порядок приёма иностранных студентов?",
             "What is the admission procedure for foreign students?",
             "<p>Xorijiy talabalar online ariza orqali hujjat topshirishlari mumkin. Zarur hujjatlar: xalqaro pasport, "
             "ta'lim hujjatlari (notarial tasdiqlangan tarjima bilan), tibbiy sug'urta polisi va moliyaviy kafolat xati.</p>",
             "<p>Иностранные студенты могут подать документы онлайн. Необходимые документы: международный паспорт, "
             "документы об образовании (с нотариально заверенным переводом), медицинская страховка.</p>",
             "<p>Foreign students can apply online. Required documents: international passport, educational documents "
             "(with notarized translation), medical insurance policy and financial guarantee letter.</p>"),
            ("Akademik almashinuv dasturlarida qatnashish mumkinmi?",
             "Можно ли участвовать в программах академического обмена?",
             "Can I participate in academic exchange programs?",
             "<p>Ha, O'ZDSA 52 ta xalqaro universitetlar va tashkilotlar bilan hamkorlik qiladi. Talabalar Erasmus+, "
             "Fulbright va boshqa dasturlar orqali xorijda tahsil olishlari mumkin. Batafsil ma'lumot uchun xalqaro "
             "aloqalar bo'limiga murojaat qiling.</p>",
             "<p>Да, УЗГСА сотрудничает с 52 международными университетами. Студенты могут обучаться за рубежом через Erasmus+ и другие программы.</p>",
             "<p>Yes, USAS cooperates with 52 international universities. Students can study abroad through Erasmus+ and other programs.</p>"),
            ("Talabalar uchun qanday imtiyozlar mavjud?",
             "Какие льготы предусмотрены для студентов?",
             "What privileges are available for students?",
             "<p>O'ZDSA talabalar uchun: bepul sport inventar va forma, imtiyozli ovqatlanish, bepul elektron kutubxona, "
             "HEMIS tizimiga kirish, sport inshootlaridan bepul foydalanish, tibbiy xizmat va boshqa imtiyozlar mavjud.</p>",
             "<p>Для студентов УЗГСА: бесплатный спортивный инвентарь, льготное питание, бесплатная электронная библиотека и другие льготы.</p>",
             "<p>For USAS students: free sports equipment, subsidized meals, free electronic library, HEMIS access, free sports facilities and other privileges.</p>"),
            ("Kontrakt to'lovi qanday amalga oshiriladi?",
             "Как осуществляется оплата контракта?",
             "How is contract payment made?",
             "<p>Kontrakt to'lovi yillik yoki semestrlarga bo'lib to'lanishi mumkin. To'lov usullari: bank o'tkazmasi, "
             "kartadan to'lash yoki Payme/Click tizimidan foydalanish mumkin. Ijtimoiy himoyaga muhtoj talabalar uchun "
             "to'lovni kechiktirish imkoniyati mavjud.</p>",
             "<p>Оплата контракта может производиться годовой или поквартальной. Методы: банковский перевод, карта, Payme/Click.</p>",
             "<p>Contract payment can be made annually or by semester. Methods: bank transfer, card payment or Payme/Click.</p>"),
            ("Bitiruvchilar ish bilan ta'minlanishi qanday?",
             "Как обстоит дело с трудоустройством выпускников?",
             "How is graduate employment?",
             "<p>O'ZDSA bitiruvchilarining 85% dan ortig'i bitiruv yilida ishga joylashadi. Akademiyaning Karyer "
             "rivojlantirish markazi ish topishda yordam beradi. Asosiy ish o'rinlari: maktablar, sport klublari, "
             "milliy federatsiyalar va sport muassasalari.</p>",
             "<p>Более 85% выпускников УЗГСА трудоустраиваются в год окончания. Центр карьерного развития помогает в поиске работы.</p>",
             "<p>Over 85% of USAS graduates find employment in their graduation year. The Career Development Center helps with job placement.</p>"),
            ("O'ZDSA da sport infratuzilmasi haqida ma'lumot bering",
             "Расскажите об спортивной инфраструктуре УЗГСА",
             "Tell us about USAS sports infrastructure",
             "<p>O'ZDSA da mavjud sport inshootlari: <ul><li>3 ta universal sport zali</li><li>2 ta suzish havzasi</li>"
             "<li>Atletika maydoni (400 m yo'lakcha)</li><li>Kurash va martial arts zali</li>"
             "<li>Trenajor zali (500 m²)</li><li>Ochiq futbol maydoni va to'p o'yinlari maydoni</li></ul></p>",
             "<p>Спортивная инфраструктура УЗГСА: 3 универсальных зала, 2 бассейна, атлетический стадион, залы борьбы и тренажёрный зал.</p>",
             "<p>USAS sports infrastructure: 3 universal halls, 2 swimming pools, athletics stadium, wrestling halls and gym.</p>"),
        ]
        for (quz, qru, qen, auz, aru, aen) in faqs:
            obj, created = FAQ.objects.get_or_create(
                question_uz=quz,
                defaults={
                    'question_ru': qru, 'question_en': qen,
                    'answer_uz': auz, 'answer_ru': aru, 'answer_en': aen,
                    'is_answered': True, 'is_published': True,
                },
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'   {count} savol-javob'))

    # ──────────────────────────────────────────────────────────────────────────
    # 11. XORIJIY PROFESSORLAR
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_foreign_professors(self):
        self.stdout.write('\n── Xorijiy professorlar ...')
        count = 0
        p = page('foreign-professors')
        if not p:
            self.stdout.write('   foreign-professors sahifasi topilmadi')
            return

        professors = [
            ("Prof. Dr. Klaus Müller",
             "Sport fanlari professori, Köln Sport Universiteti",
             "Профессор спортивных наук, Спортивный университет Кёльна",
             "Professor of Sports Sciences, German Sport University Cologne",
             "Germaniya",
             "<p>«O'ZDSA bilan hamkorligimiz juda samarali bo'ldi. O'zbek sport fani jahon darajasida rivojlanmoqda. "
             "Talabalarga berilayotgan bilim va amaliy ko'nikmalar meni hayratda qoldiradi.»</p>",
             "<p>«Наше сотрудничество с УЗГСА оказалось очень продуктивным. Узбекская спортивная наука развивается на мировом уровне.»</p>",
             "<p>«Our cooperation with USAS has been very productive. Uzbek sports science is developing at the world level. "
             "The knowledge and practical skills given to students amaze me.»</p>",
             1),
            ("Prof. Dr. Li Wei",
             "Wushu va kurash sport fanlari doktori, Beijing Sport Universiteti",
             "Доктор спортивных наук, Пекинский спортивный университет",
             "Doctor of Sports Sciences, Beijing Sport University",
             "Xitoy",
             "<p>«O'ZDSA talabalarining sport texnikasi va intizomi ajoyib darajada. "
             "Akademiya infratuzilmasi ham, o'qitish sifati ham xalqaro standartlarga mos keladi.»</p>",
             "<p>«Спортивная техника и дисциплина студентов УЗГСА на отличном уровне. Инфраструктура и качество обучения соответствуют международным стандартам.»</p>",
             "<p>«The sports technique and discipline of USAS students is at an excellent level. "
             "The infrastructure and teaching quality meet international standards.»</p>",
             2),
            ("Dr. Sarah Johnson",
             "Sport psixologiyasi mutaxassisi, Ilinoys Universiteti (AQSH)",
             "Специалист по спортивной психологии, Университет Иллинойса (США)",
             "Sports Psychology Specialist, University of Illinois (USA)",
             "AQSH",
             "<p>«O'zbek sportchilarining ruhiy kuchi va g'alabaga intilishi meni ilhomlantiradi. "
             "O'ZDSA da psixologiya bo'limi g'oyat yaxshi rivojlangan va amaliyotga asoslangan.»</p>",
             "<p>«Психологическая сила и стремление к победе узбекских спортсменов меня вдохновляют. Кафедра психологии в УЗГСА хорошо развита и практикоориентирована.»</p>",
             "<p>«The mental strength and desire to win of Uzbek athletes inspires me. "
             "The psychology department at USAS is very well developed and practice-oriented.»</p>",
             3),
            ("Prof. Dr. Dmitriy Petrov",
             "Yengil atletika va olimpiya tayyorgarligi mutaxassisi, Moskva Sport Akademiyasi",
             "Специалист по лёгкой атлетике и олимпийской подготовке, Московская академия спорта",
             "Athletics and Olympic Preparation Specialist, Moscow Sports Academy",
             "Rossiya",
             "<p>«O'ZDSA bilan ko'p yillik hamkorlik mobaynida ko'plab iste'dodli sportchilarni tayyorlashga hissa qo'shdim. "
             "Akademiya murabbiylarning kasbiy mahorati juda yuqori darajada.»</p>",
             "<p>«За многолетнее сотрудничество с УЗГСА внёс вклад в подготовку многих талантливых спортсменов. Профессиональное мастерство тренеров академии на высоком уровне.»</p>",
             "<p>«During many years of cooperation with USAS, I have contributed to the preparation of many talented athletes. "
             "The professional skills of the academy's coaches are at a very high level.»</p>",
             4),
        ]
        for (name, pos_uz, pos_ru, pos_en, country, rev_uz, rev_ru, rev_en, order) in professors:
            obj, created = ForeignProfessorReview.objects.get_or_create(
                navbar_item=p,
                full_name=name,
                defaults={
                    'position_uz': pos_uz,
                    'position_ru': pos_ru,
                    'position_en': pos_en,
                    'country':     country,
                    'review_uz':   rev_uz,
                    'review_ru':   rev_ru,
                    'review_en':   rev_en,
                    'order':       order,
                    'is_active':   True,
                },
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'   {count} xorijiy professor'))

    # ──────────────────────────────────────────────────────────────────────────
    # 12. FAXRLARIMIZ (PersonCategory + Person)
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_honored_people(self):
        self.stdout.write('\n── Faxrlarimiz ...')
        count = 0

        categories = [
            ('graduates', [
                ("Xasanova Zulfiya Mansurovna",
                 "Jahon chempioni, kurash bo'yicha olimpiya bronza medali sohibi",
                 "Чемпион мира, бронзовый призёр Олимпийских игр по борьбе",
                 "World Champion, Olympic Bronze Medalist in Wrestling",
                 "<p>O'ZDSA ni 2010-yilda tamomlagan. Xalqaro musobaqalarda 45 ta medal qozongan. "
                 "Hozirda milliy terma jamoa murabbiyi sifatida faoliyat yuritadi.</p>",
                 1),
                ("Mirzayev Jasur Odilovich",
                 "Olimpiya o'yinlari kumush medali sohibi, boks bo'yicha",
                 "Серебряный призёр Олимпийских игр по боксу",
                 "Olympic Silver Medalist in Boxing",
                 "<p>O'ZDSA ni 2014-yilda tamomlagan. Jahon chempionatida 2 marotaba g'olib bo'lgan. "
                 "Xozirda xalqaro boks federatsiyasida texnik direktori.</p>",
                 2),
                ("Rahimova Feruza Aliyevna",
                 "Jahon chempioni, taekwondo bo'yicha",
                 "Чемпион мира по таэквондо",
                 "World Champion in Taekwondo",
                 "<p>O'ZDSA ni 2016-yilda tamomlagan. Osiyo o'yinlarida 3 marta oltin medal qozongan. "
                 "Hozirda O'zbekiston taekwondo federatsiyasi prezidenti.</p>",
                 3),
                ("Karimov Shamsiddin Baxtiyorovich",
                 "Olimpiya chempioni, erkin kurash bo'yicha",
                 "Олимпийский чемпион по вольной борьбе",
                 "Olympic Champion in Freestyle Wrestling",
                 "<p>O'ZDSA ni 2012-yilda tamomlagan. Olimpiya o'yinlarida oltin medal sohibi. "
                 "Davlat sport mukofoti laureati.</p>",
                 4),
            ]),
            ('honorary-teachers', [
                ("Sodiqov Hamid Raximovich",
                 "O'zbekiston xizmat ko'rsatgan sport ustasi, professor",
                 "Заслуженный мастер спорта Узбекистана, профессор",
                 "Honored Master of Sports of Uzbekistan, Professor",
                 "<p>50 yildan ortiq pedagogik faoliyat davomida 1000 dan ortiq sportchilarni tayyorlagan. "
                 "O'ZDSA ning faxriy professori. Sport pedagokikasi bo'yicha 10 ta darslik muallifi.</p>",
                 1),
                ("Tursunova Maftuna Kamoliddinovna",
                 "O'zbekiston xizmat ko'rsatgan o'qituvchisi, dotsent",
                 "Заслуженный учитель Узбекистана, доцент",
                 "Honored Teacher of Uzbekistan, Associate Professor",
                 "<p>35 yillik pedagogik faoliyat. Gimnastika va badiiy gimnastika bo'yicha mutaxassis. "
                 "Ko'plab xalqaro musobaqalar sovrindorlarini tayyorlagan.</p>",
                 2),
                ("Xoliqov Bahodir Sharipovich",
                 "O'zbekiston xizmat ko'rsatgan murabbiyi, sport fanlari doktori",
                 "Заслуженный тренер Узбекистана, доктор спортивных наук",
                 "Honored Coach of Uzbekistan, Doctor of Sports Sciences",
                 "<p>30 yildan ortiq trenerlik faoliyati. Olimpiya va jahon chempionlari tayyorlagan. "
                 "O'ZDSA trenerlik fakultetini tashkil etishda muhim rol o'ynagan.</p>",
                 3),
            ]),
            ('distinguished-scientists', [
                ("Nazarov Ilhom Abdullayevich",
                 "Sport fanlari doktori, professor, 200+ ilmiy maqola muallifi",
                 "Доктор спортивных наук, профессор, автор 200+ научных статей",
                 "Doctor of Sports Sciences, Professor, Author of 200+ Scientific Articles",
                 "<p>Sport biomexanikasi va fiziologiyasi sohasida taniqli olim. Scopus va WoS bazalarida 200 dan ortiq "
                 "maqolasi chop etilgan. Xalqaro sport fanlari jamiyatining a'zosi.</p>",
                 1),
                ("Qosimova Dilnoza Hamidovna",
                 "Tibbiyot fanlari doktori, sport tibbiyoti mutaxassisi",
                 "Доктор медицинских наук, специалист по спортивной медицине",
                 "Doctor of Medical Sciences, Sports Medicine Specialist",
                 "<p>Sport tibbiyoti va sportchilar reabilitatsiyasi bo'yicha fundamental tadqiqotlar olib borgan. "
                 "15 ta patentning muallifi. Xalqaro sport tibbiyoti konferensiyalari doimiy ishtirokchisi.</p>",
                 2),
                ("Ergashev Timur Saidovich",
                 "Pedagogika fanlari doktori, xalqaro ta'lim muassasalarida isbotlangan metodolog",
                 "Доктор педагогических наук, методолог международного уровня",
                 "Doctor of Pedagogical Sciences, International Level Methodologist",
                 "<p>Sport pedagogikasi metodologiyasi bo'yicha innovatsion yondashuvlar ishlab chiqqan. "
                 "Uning metodlari O'zbekiston va 5 ta xorijiy mamlakat sport maktablarida qo'llanilmoqda.</p>",
                 3),
            ]),
            ('ozdsa-stars', [
                ("Abduraxmonov Bekzod Mirzoevich",
                 "O'ZDSA talabasi, 2024 Osiyo o'yinlari oltin medali sohibi",
                 "Студент УЗГСА, золотой медалист Азиатских игр 2024",
                 "USAS Student, 2024 Asian Games Gold Medalist",
                 "<p>Kurash bo'yicha 2024 Osiyo o'yinlarida oltin medal qozongan O'ZDSA talabasi. "
                 "GPA ko'rsatkichi: 3.9. Sport va ta'limni muvaffaqiyatli uyg'unlashtirgan namunaviy talaba.</p>",
                 1),
                ("Yusupova Nozima Alixanovna",
                 "O'ZDSA talabasi, yengil atletika bo'yicha Osiyo rekordi egasi",
                 "Студентка УЗГСА, рекордсмен Азии по лёгкой атлетике",
                 "USAS Student, Asian Athletics Record Holder",
                 "<p>400 metr yugurish bo'yicha yangi Osiyo rekord o'rnatgan. Prezident stipendiyasi sohibasi. "
                 "2028 Olimpiya o'yinlari uchun asosiy nomzod.</p>",
                 2),
                ("Toshpulatov Sanjar Hamidovich",
                 "O'ZDSA talabasi va trenerlik kafedrasi aspiranti",
                 "Студент УЗГСА и аспирант кафедры тренерства",
                 "USAS Student and Graduate Student of Coaching Department",
                 "<p>Boks bo'yicha O'zbekiston chempioni. Bir vaqtda bakalavriat va aspiranturada tahsil olmoqda. "
                 "Ilmiy maqolalari xalqaro nashrlarda chop etilgan.</p>",
                 3),
            ]),
        ]

        for (nav_slug, persons) in categories:
            p = page(nav_slug)
            if not p:
                continue
            cat_titles = {
                'graduates':              ("Bitiruvchilarimiz",            "Выпускники",                   "Graduates"),
                'honorary-teachers':      ("Faxrli ustozlarimiz",          "Почётные учителя",             "Honorary Teachers"),
                'distinguished-scientists': ("Ilg'or olimlarimiz",         "Выдающиеся учёные",            "Distinguished Scientists"),
                'ozdsa-stars':            ("O'ZDSA yulduzlari",            "Звёзды УЗГСА",                 "OZDSA Stars"),
            }
            tuz, tru, ten = cat_titles[nav_slug]
            cat, _ = PersonCategory.objects.get_or_create(
                slug=nav_slug,
                defaults={'navbar_item': p, 'title_uz': tuz, 'title_ru': tru, 'title_en': ten, 'order': 1},
            )
            for (name_uz, pos_uz, pos_ru, pos_en, desc_uz, order) in persons:
                obj, created = Person.objects.get_or_create(
                    category=cat,
                    full_name_uz=name_uz,
                    defaults={
                        'full_name_ru':   name_uz,
                        'full_name_en':   name_uz,
                        'description_uz': pos_uz + ' ' + desc_uz,
                        'description_ru': pos_ru,
                        'description_en': pos_en,
                        'order':          order,
                        'is_active':      True,
                    },
                )
                if created:
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'   {count} faxrli shaxs'))

    # ──────────────────────────────────────────────────────────────────────────
    # 13. TENDERLAR
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_tenders(self):
        self.stdout.write('\n── Tenderlar ...')
        from django.utils.timezone import make_aware
        from datetime import datetime
        def dt(y, m, d): return make_aware(datetime(y, m, d))
        count = 0
        tenders = [
            ("Sport inventarlari va jihozlarini xarid qilish bo'yicha tender",
             "Тендер на закупку спортивного инвентаря и оборудования",
             "Tender for Procurement of Sports Equipment and Inventory",
             "<p>O'ZDSA 2026-2027 o'quv yili uchun sport inventarlari va jihozlarini xarid qilish bo'yicha ochiq tender e'lon qiladi.</p>"
             "<p>Talab qilinadigan jihozlar: og'ir atletika, kurash va gimnastika uchun.</p>",
             "<p>УЗГСА объявляет открытый тендер на закупку спортивного инвентаря и оборудования.</p>",
             "<p>USAS announces an open tender for the procurement of sports equipment and inventory.</p>",
             dt(2026, 4, 1),
             "Toshkent sh., Yunusobod tumani, Yusupov ko'chasi 2-uy",
             "tender@usas.uz", "+998 71 244-70-00"),
            ("O'quv binolarini ta'mirlash bo'yicha pudratchini tanlash",
             "Выбор подрядчика для ремонта учебных корпусов",
             "Selection of Contractor for Renovation of Academic Buildings",
             "<p>O'ZDSA B-korpus va A-korpusning qisman ta'mirlanishi uchun pudratchi tashkilotni tanlash bo'yicha tender e'lon qiladi.</p>"
             "<p>Ishlar 2026-yil iyun — iyul oylarida bajarilishi kerak.</p>",
             "<p>УЗГСА объявляет тендер на выбор подрядчика для частичного ремонта корпусов А и Б.</p>",
             "<p>USAS announces a tender for selecting a contractor for partial renovation of buildings A and B.</p>",
             dt(2026, 3, 25),
             "Toshkent sh., Yunusobod tumani, Yusupov ko'chasi 2-uy",
             "tender@usas.uz", "+998 71 244-70-00"),
        ]
        for (tuz, tru, ten, duz, dru, den, ev_date, addr, email, phone) in tenders:
            obj, created = TenderAnnouncement.objects.get_or_create(
                title_uz=tuz,
                defaults={
                    'title_ru': tru, 'title_en': ten,
                    'description_uz': duz, 'description_ru': dru, 'description_en': den,
                    'date': ev_date, 'address': addr, 'email': email, 'phone': phone,
                    'is_published': True,
                },
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'   {count} tender'))
