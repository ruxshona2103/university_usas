"""
Seed command: Navbar + Academic tuzilmasini yaratish va bog'lash.

Ishlatish:
    python manage.py seed_navbar_academic            # dry-run (preview)
    python manage.py seed_navbar_academic --apply    # DB ga yozadi

Idempotent: slug bo'yicha get_or_create, ikkinchi marta xavfsiz ishlatish mumkin.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from domains.pages.models import NavbarCategory, NavbarSubItem
from domains.academic.models import OrganizationUnit
from domains.academic.models.unit import UnitType


# ──────────────────────────────────────────────────────────────────────────────
# Navbar + Academic tuzilmasi
# academic_unit = None  →  faqat navbar sahifa (academic unit bog'lanmaydi)
# academic_unit = {...} →  OrganizationUnit ham yaratiladi va bog'lanadi
# ──────────────────────────────────────────────────────────────────────────────

STRUCTURE = [
    {
        'slug': 'universitet',
        'name_uz': 'Universitet',
        'name_ru': 'Университет',
        'name_en': 'University',
        'order': 1,
        'items': [
            {
                'slug': 'akademiya-tarixi',
                'name_uz': 'Akademiya tarixi',
                'name_ru': 'История академии',
                'name_en': 'Academy history',
                'order': 1,
                'academic_unit': None,  # academic unit bog'lanmaydi — faqat static matn
            },
            {
                'slug': 'tuzilma',
                'name_uz': 'Tuzilma',
                'name_ru': 'Структура',
                'name_en': 'Structure',
                'order': 2,
                'academic_unit': None,  # org-chart sahifasi — bitta unitga emas, daraxts
            },
            {
                'slug': 'rektorat',
                'name_uz': 'Rektorat',
                'name_ru': 'Ректорат',
                'name_en': 'Rectorate',
                'order': 3,
                'academic_unit': {
                    'title_uz': 'Rektorat',
                    'title_ru': 'Ректорат',
                    'title_en': 'Rectorate',
                    'unit_type': UnitType.RECTOR,
                    'is_featured': True,
                    'has_own_page': True,
                    'order': 3,
                },
            },
            {
                'slug': 'universitet-kengashi',
                'name_uz': 'Universitet kengashi',
                'name_ru': 'Совет университета',
                'name_en': 'University council',
                'order': 4,
                'academic_unit': {
                    'title_uz': 'Universitet kengashi',
                    'title_ru': 'Совет университета',
                    'title_en': 'University council',
                    'unit_type': UnitType.COUNCIL,
                    'has_own_page': True,
                    'order': 1,
                },
            },
            {
                'slug': 'kuzatuv-kengashi',
                'name_uz': 'Kuzatuv kengashi',
                'name_ru': 'Наблюдательный совет',
                'name_en': 'Supervisory board',
                'order': 5,
                'academic_unit': {
                    'title_uz': 'Kuzatuv kengashi',
                    'title_ru': 'Наблюдательный совет',
                    'title_en': 'Supervisory board',
                    'unit_type': UnitType.SUPERVISORY,
                    'has_own_page': True,
                    'order': 2,
                },
            },
            {
                'slug': 'fakultetlar',
                'name_uz': 'Fakultetlar',
                'name_ru': 'Факультеты',
                'name_en': 'Faculties',
                'order': 6,
                'academic_unit': None,  # ro'yxat sahifasi — filter: type=faculty
            },
            {
                'slug': 'kafedralar',
                'name_uz': 'Kafedralar',
                'name_ru': 'Кафедры',
                'name_en': 'Departments',
                'order': 7,
                'academic_unit': None,  # ro'yxat sahifasi — filter: type=department
            },
            {
                'slug': 'markazlar',
                'name_uz': 'Markazlar',
                'name_ru': 'Центры',
                'name_en': 'Centers',
                'order': 8,
                'academic_unit': None,  # ro'yxat sahifasi — filter: type=center
            },
            {
                'slug': 'binolar',
                'name_uz': "O'quv binolari",
                'name_ru': 'Учебные корпуса',
                'name_en': 'Buildings',
                'order': 9,
                'academic_unit': None,
            },
            {
                'slug': 'rekvizitlar',
                'name_uz': 'Rekvizitlar',
                'name_ru': 'Реквизиты',
                'name_en': 'Requisites',
                'order': 10,
                'academic_unit': None,
            },
        ],
    },
    {
        'slug': 'faoliyat',
        'name_uz': 'Faoliyat',
        'name_ru': 'Деятельность',
        'name_en': 'Activities',
        'order': 2,
        'items': [
            {'slug': 'ilmiy-faoliyat',     'name_uz': 'Ilmiy faoliyat',             'name_ru': 'Научная деятельность',      'name_en': 'Scientific activity',   'order': 1, 'academic_unit': None},
            {'slug': 'madaniy-hayot',       'name_uz': 'Madaniy hayot',              'name_ru': 'Культурная жизнь',           'name_en': 'Cultural life',          'order': 2, 'academic_unit': None},
            {'slug': 'moliyaviy-faoliyat',  'name_uz': 'Moliyaviy faoliyat',         'name_ru': 'Финансовая деятельность',    'name_en': 'Financial activity',     'order': 3, 'academic_unit': None},
            {'slug': 'kontrakt-narxlari',   'name_uz': "To'lov-kontrakt narxlari",   'name_ru': 'Стоимость обучения',         'name_en': 'Tuition fees',           'order': 4, 'academic_unit': None},
            {'slug': 'ochiq-malumotlar',    'name_uz': "Ochiq ma'lumotlar",           'name_ru': 'Открытые данные',            'name_en': 'Open data',              'order': 5, 'academic_unit': None},
        ],
    },
    {
        'slug': 'xalqaro-aloqalar',
        'name_uz': 'Xalqaro aloqalar',
        'name_ru': 'Международные связи',
        'name_en': 'International relations',
        'order': 3,
        'items': [
            {'slug': 'xalqaro-hamkorlar',       'name_uz': 'Xalqaro hamkor tashkilotlar',       'name_ru': 'Международные партнёры',          'name_en': 'International partners',        'order': 1,  'academic_unit': None},
            {'slug': 'malaka-oshirish',          'name_uz': "Xorijda malaka oshirish va ta'lim", 'name_ru': 'Повышение квалификации за рубежом','name_en': 'Professional development abroad','order': 2,  'academic_unit': None},
            {'slug': 'xalqaro-bolim-elonlari',   'name_uz': "Xalqaro bo'lim e'lonlari",          'name_ru': 'Объявления международного отдела', 'name_en': 'International dept. news',       'order': 3,  'academic_unit': None},
            {'slug': 'biz-haqimizda',            'name_uz': 'Xorijliklar "Biz haqimizda"',       'name_ru': 'Иностранцы о нас',                'name_en': 'Foreigners about us',            'order': 4,  'academic_unit': None},
            {'slug': 'xorijlik-professorlar',    'name_uz': "Xorijlik professor-o'qituvchilar",  'name_ru': 'Иностранные профессора',          'name_en': 'Foreign professors',             'order': 5,  'academic_unit': None},
            {'slug': 'jalb-etilgan-sarmoyalar',  'name_uz': 'Jalb etilgan sarmoyalar va grantlar','name_ru': 'Привлечённые инвестиции и гранты','name_en': 'Investments and grants',         'order': 6,  'academic_unit': None},
            {'slug': 'amaldagi-loyihalar',       'name_uz': 'Amaldagi loyihalar',                'name_ru': 'Текущие проекты',                 'name_en': 'Ongoing projects',               'order': 7,  'academic_unit': None},
            {'slug': 'erasmus-grantlar',         'name_uz': 'Erasmus+ Grantlar',                 'name_ru': 'Гранты Erasmus+',                 'name_en': 'Erasmus+ Grants',                'order': 8,  'academic_unit': None},
            {'slug': 'study-in-uzbekistan',      'name_uz': 'Study in Uzbekistan',               'name_ru': 'Study in Uzbekistan',             'name_en': 'Study in Uzbekistan',            'order': 9,  'academic_unit': None},
            {'slug': 'sdg',                      'name_uz': 'SDG',                               'name_ru': 'ЦУР',                             'name_en': 'SDG',                            'order': 10, 'academic_unit': None},
        ],
    },
    {
        'slug': 'talabalarga',
        'name_uz': 'Talabalarga',
        'name_ru': 'Студентам',
        'name_en': 'For students',
        'order': 4,
        'items': [
            {'slug': 'bakalavr',          'name_uz': 'Bakalavr',               'name_ru': 'Бакалавриат',         'name_en': 'Bachelor',           'order': 1, 'academic_unit': None},
            {'slug': 'magistratura',      'name_uz': 'Magistratura',           'name_ru': 'Магистратура',        'name_en': 'Master',             'order': 2, 'academic_unit': None},
            {'slug': 'dars-jadvali',      'name_uz': 'Dars jadvali',           'name_ru': 'Расписание занятий',  'name_en': 'Class schedule',     'order': 3, 'academic_unit': None},
            {'slug': 'akademik-mobillik', 'name_uz': 'Akademik mobillik',      'name_ru': 'Академическая мобильность','name_en': 'Academic mobility','order': 4, 'academic_unit': None},
            {'slug': 'psixolog',          'name_uz': 'Psixolog',               'name_ru': 'Психолог',            'name_en': 'Psychologist',       'order': 5, 'academic_unit': None},
        ],
    },
    {
        'slug': 'axborot-xizmati',
        'name_uz': 'Axborot xizmati',
        'name_ru': 'Пресс-служба',
        'name_en': 'Press service',
        'order': 5,
        'items': [
            {'slug': 'yangiliklar',    'name_uz': 'Yangiliklar',      'name_ru': 'Новости',         'name_en': 'News',          'order': 1, 'academic_unit': None},
            {'slug': 'elonlar',        'name_uz': "E'lonlar",         'name_ru': 'Объявления',      'name_en': 'Announcements', 'order': 2, 'academic_unit': None},
            {'slug': 'tadbirlar',      'name_uz': 'Tadbirlar',        'name_ru': 'Мероприятия',     'name_en': 'Events',        'order': 3, 'academic_unit': None},
            {'slug': 'fotogalereya',   'name_uz': 'Fotogalereya',     'name_ru': 'Фотогалерея',     'name_en': 'Photo gallery', 'order': 4, 'academic_unit': None},
            {'slug': 'videogalereya',  'name_uz': 'Videogalereya',    'name_ru': 'Видеогалерея',    'name_en': 'Video gallery', 'order': 5, 'academic_unit': None},
        ],
    },
    {
        'slug': 'qabul',
        'name_uz': 'Qabul',
        'name_ru': 'Приёмная комиссия',
        'name_en': 'Admissions',
        'order': 6,
        'items': [
            {'slug': 'bakalavr-qabul',    'name_uz': "Bakalavr qabul",          'name_ru': 'Приём на бакалавриат',    'name_en': 'Bachelor admissions',  'order': 1, 'academic_unit': None},
            {'slug': 'magistr-qabul',     'name_uz': "Magistratura qabul",      'name_ru': 'Приём в магистратуру',   'name_en': 'Master admissions',    'order': 2, 'academic_unit': None},
            {'slug': 'xorijiy-talabalar', 'name_uz': "Xorijiy talabalar",       'name_ru': 'Иностранные студенты',   'name_en': 'Foreign students',     'order': 3, 'academic_unit': None},
            {'slug': 'otish-ballari',     'name_uz': "O'tish ballari",           'name_ru': 'Проходные баллы',        'name_en': 'Passing scores',       'order': 4, 'academic_unit': None},
            {'slug': 'qabul-hujjatlari',  'name_uz': "Qabul hujjatlari",        'name_ru': 'Документы для поступления','name_en': 'Admission documents', 'order': 5, 'academic_unit': None},
        ],
    },
    {
        'slug': 'rektorga-murojaat',
        'name_uz': 'Rektorga murojaat',
        'name_ru': 'Обращение к ректору',
        'name_en': 'Appeal to rector',
        'order': 7,
        'direct_url': '/murojaat/',  # to'g'ridan sahifa, sub-item yo'q
        'items': [],
    },
    {
        'slug': 'kelajakka-qadam',
        'name_uz': '"Kelajakka qadam" markazi',
        'name_ru': 'Центр "Шаг в будущее"',
        'name_en': '"Step to the Future" center',
        'order': 8,
        'items': [
            {'slug': 'markaz-haqida',  'name_uz': 'Markaz haqida',    'name_ru': 'О центре',        'name_en': 'About center', 'order': 1, 'academic_unit': None},
            {'slug': 'markaz-elonlar', 'name_uz': "Markaz e'lonlari", 'name_ru': 'Объявления центра','name_en': 'Center news',  'order': 2, 'academic_unit': None},
        ],
    },
]


class Command(BaseCommand):
    help = (
        "Navbar va Academic tuzilmasini seed qilish va bog'lash (Variant A).\n"
        "  --apply         DB ga yozadi (default: dry-run)\n"
        "  --reset-units   STRUCTURE da academic_unit bor bo'lgan sluglar uchun\n"
        "                  noto'g'ri bog'langan unitlarni tozalab, qayta yaratadi"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply',
            action='store_true',
            help='DB ga yozadi. Usiz faqat preview.',
        )
        parser.add_argument(
            '--reset-units',
            action='store_true',
            help='Academic unitlarni tozalab qayta yaratadi (noto\'g\'ri bog\'lanishlarni tuzatadi).',
        )

    def handle(self, *args, **options):
        apply       = options['apply']
        reset_units = options['reset_units']
        mode        = 'APPLY' if apply else 'DRY-RUN'

        self.stdout.write(self.style.MIGRATE_HEADING(f'\n=== SEED MODE: {mode} ===\n'))

        nav_created = nav_updated = 0
        item_created = item_updated = 0
        unit_created = unit_updated = unit_deleted = 0

        # STRUCTURE da academic_unit belgilangan sluglar
        academic_slugs = {
            item_data['slug']
            for cat_data in STRUCTURE
            for item_data in cat_data.get('items', [])
            if item_data.get('academic_unit')
        }

        # --reset-units: noto'g'ri bog'langan unitlarni o'chirish
        if reset_units and apply:
            self.stdout.write(self.style.WARNING('\n-- reset-units: noto\'g\'ri unitlar tozalanmoqda --'))
            wrong = OrganizationUnit.objects.filter(
                navbar_item__slug__in=academic_slugs
            ).exclude(
                # slug va navbar slug mos bo'lmaganlar
                slug__in=academic_slugs
            )
            # Shuningdek, academic_slugs dan tashqaridagi noto'g'ri linklar
            wrong2 = OrganizationUnit.objects.filter(navbar_item__isnull=False).exclude(
                navbar_item__slug__in=academic_slugs
            )
            for u in list(wrong) + list(wrong2):
                self.stdout.write(self.style.WARNING(
                    f'  DEL unit={u.title_uz!r} slug={u.slug!r} navbar={u.navbar_item.slug if u.navbar_item else None}'
                ))
            count, _ = (list(wrong) and OrganizationUnit.objects.filter(
                pk__in=[u.pk for u in wrong]
            ).delete()) or (0, {})
            count2, _ = OrganizationUnit.objects.filter(
                pk__in=[u.pk for u in wrong2]
            ).delete()
            unit_deleted = (count or 0) + (count2 or 0)

        for cat_data in STRUCTURE:
            # .get() ishlatamiz — STRUCTURE ni mutate qilmaymiz
            items      = cat_data.get('items', [])
            direct_url = cat_data.get('direct_url', '')

            self.stdout.write(self.style.MIGRATE_LABEL(
                f"\nNavbar category: [{cat_data['slug']}] {cat_data['name_uz']}"
            ))

            if apply:
                with transaction.atomic():
                    cat, created = NavbarCategory.objects.update_or_create(
                        slug=cat_data['slug'],
                        defaults={
                            'name_uz':    cat_data['name_uz'],
                            'name_ru':    cat_data.get('name_ru', ''),
                            'name_en':    cat_data.get('name_en', ''),
                            'order':      cat_data['order'],
                            'is_active':  True,
                            'direct_url': direct_url,
                        }
                    )
                nav_created += created
                nav_updated += not created
                label = '✔ CREATED' if created else '~ updated'
                self.stdout.write(self.style.SUCCESS(f'  {label} category') if created else f'  {label} category')
            else:
                self.stdout.write(f'  → would create/update category')
                cat = None

            for item_data in items:
                # .get() — dict ni o'zgartirmaymiz
                au_data = item_data.get('academic_unit')

                self.stdout.write(
                    f"    NavbarSubItem: [{item_data['slug']}] {item_data['name_uz']}"
                    + (' + OrganizationUnit' if au_data else '')
                )

                if not apply:
                    if au_data:
                        self.stdout.write(f'      → would create/update OrganizationUnit (slug={item_data["slug"]})')
                    continue

                with transaction.atomic():
                    item, created = NavbarSubItem.objects.update_or_create(
                        slug=item_data['slug'],
                        defaults={
                            'category':  cat,
                            'name_uz':   item_data['name_uz'],
                            'name_ru':   item_data.get('name_ru', ''),
                            'name_en':   item_data.get('name_en', ''),
                            'order':     item_data['order'],
                            'page_type': NavbarSubItem.PageType.STATIC,
                            'is_active': True,
                        }
                    )
                item_created += created
                item_updated += not created
                if created:
                    self.stdout.write(self.style.SUCCESS('      ✔ CREATED navbar item'))

                if not au_data:
                    continue

                # Academic unit: FAQAT navbar_item bo'yicha qidirish (slug bo'yicha emas!)
                # Bu noto'g'ri unit topib olishni oldini oladi.
                with transaction.atomic():
                    existing = OrganizationUnit.objects.filter(navbar_item=item).first()
                    if existing:
                        OrganizationUnit.objects.filter(pk=existing.pk).update(
                            slug=item.slug,
                            title_uz=au_data['title_uz'],
                            title_ru=au_data.get('title_ru', ''),
                            title_en=au_data.get('title_en', ''),
                            unit_type=au_data['unit_type'],
                            has_own_page=au_data.get('has_own_page', True),
                            is_featured=au_data.get('is_featured', False),
                            order=au_data.get('order', 0),
                        )
                        unit_updated += 1
                        self.stdout.write(f'      ~ updated OrganizationUnit (slug={item.slug})')
                    else:
                        OrganizationUnit.objects.create(
                            navbar_item=item,
                            slug=item.slug,
                            title_uz=au_data['title_uz'],
                            title_ru=au_data.get('title_ru', ''),
                            title_en=au_data.get('title_en', ''),
                            unit_type=au_data['unit_type'],
                            has_own_page=au_data.get('has_own_page', True),
                            is_featured=au_data.get('is_featured', False),
                            order=au_data.get('order', 0),
                            is_active=True,
                        )
                        unit_created += 1
                        self.stdout.write(self.style.SUCCESS(
                            f'      ✔ CREATED OrganizationUnit slug={item.slug}'
                        ))

        self.stdout.write(self.style.MIGRATE_HEADING('\n=== NATIJA ==='))
        self.stdout.write(
            f'NavbarCategory:    created={nav_created}, updated={nav_updated}\n'
            f'NavbarSubItem:     created={item_created}, updated={item_updated}\n'
            f'OrganizationUnit:  created={unit_created}, updated={unit_updated}'
            + (f', deleted(reset)={unit_deleted}' if reset_units else '')
        )
        if not apply:
            self.stdout.write(self.style.WARNING('\nDry-run tugadi. --apply bilan ishlatib DB ga yozing.'))
