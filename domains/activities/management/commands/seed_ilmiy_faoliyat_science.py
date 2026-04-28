"""
python manage.py seed_ilmiy_faoliyat_science

Ilmiy faoliyat (fan) uchun:
  - 1 ta root IlmiyFaoliyatCategory  (slug="ilmiy-faoliyat")
  - 4 ta child  IlmiyFaoliyatCategory (kartochkalar)
  - Har bir kartochkada namunali IlmiyFaoliyat itemlar
"""

import uuid

from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

ROOT = {
    "id":       "b2c3d4e5-0002-0002-0002-000000000002",
    "slug":     "ilmiy-faoliyat",
    "title_uz": "Ilmiy faoliyat",
    "title_ru": "Научная деятельность",
    "title_en": "Scientific Activity",
    "order":    2,
}

SUBCATEGORIES = [
    {
        "id":             "b2c3d4e5-0002-0002-0002-000000000021",
        "slug":           "ilmiy-loyihalar",
        "title_uz":       "Ilmiy loyihalar",
        "title_ru":       "Научные проекты",
        "title_en":       "Scientific Projects",
        "description_uz": "Amalga oshirilayotgan va rejalashtirilgan ilmiy loyihalar.",
        "description_ru": "Реализуемые и планируемые научные проекты.",
        "description_en": "Ongoing and planned scientific projects.",
        "icon":           "flask-conical",
        "order":          1,
        "items": [
            {
                "title_uz": "Sport biomexanikasi bo'yicha ilmiy loyiha",
                "title_ru": "Научный проект по спортивной биомеханике",
                "title_en": "Scientific Project on Sports Biomechanics",
                "description_uz": "Atletlar harakatini tahlil qilish bo'yicha tadqiqot loyihasi.",
                "order": 1,
            },
            {
                "title_uz": "Jismoniy tarbiya samaradorligini o'rganish",
                "title_ru": "Исследование эффективности физического воспитания",
                "title_en": "Research on Physical Education Effectiveness",
                "description_uz": "Yangi usullar orqali jismoniy tarbiya samaradorligini baholash.",
                "order": 2,
            },
            {
                "title_uz": "Sport psixologiyasi tadqiqoti",
                "title_ru": "Исследование спортивной психологии",
                "title_en": "Sports Psychology Research",
                "description_uz": "Sportchilar ruhiy holatini baholash va takomillashtirish usullari.",
                "order": 3,
            },
            {
                "title_uz": "Ovqatlanish va sport natijalari aloqasi",
                "title_ru": "Связь питания и спортивных результатов",
                "title_en": "Nutrition and Sports Performance Correlation",
                "description_uz": "Sportchi ovqatlanishi va sport natijalari o'rtasidagi bog'liqlik tadqiqoti.",
                "order": 4,
            },
        ],
    },
    {
        "id":             "b2c3d4e5-0002-0002-0002-000000000022",
        "slug":           "doktorantura",
        "title_uz":       "Doktorantura",
        "title_ru":       "Докторантура",
        "title_en":       "Doctoral Studies",
        "description_uz": "Doktorantura bo'yicha yo'riqnomalar va ma'lumotlar.",
        "description_ru": "Руководства и информация по докторантуре.",
        "description_en": "Guidance and information on doctoral studies.",
        "icon":           "graduation-cap",
        "order":          2,
        "items": [
            {
                "title_uz": "DSc doktoranturaga qabul qilish tartibi",
                "title_ru": "Порядок приёма в докторантуру DSc",
                "title_en": "DSc Doctoral Admission Procedure",
                "description_uz": "Doktoranturaga qabul qilish shartlari va hujjatlar ro'yxati.",
                "order": 1,
            },
            {
                "title_uz": "PhD doktorantura yo'nalishlari",
                "title_ru": "Направления докторантуры PhD",
                "title_en": "PhD Doctoral Directions",
                "description_uz": "Akademiyadagi barcha PhD yo'nalishlari va mutaxassisliklar.",
                "order": 2,
            },
            {
                "title_uz": "Dissertatsiya yozish bo'yicha qo'llanma",
                "title_ru": "Руководство по написанию диссертации",
                "title_en": "Dissertation Writing Guide",
                "description_uz": "Dissertatsiya tayyorlash bosqichlari va talablar.",
                "order": 3,
            },
            {
                "title_uz": "Ilmiy rahbar tanlash mezonlari",
                "title_ru": "Критерии выбора научного руководителя",
                "title_en": "Scientific Supervisor Selection Criteria",
                "description_uz": "Ilmiy rahbar tanlashda e'tiborga olish kerak bo'lgan mezonlar.",
                "order": 4,
            },
        ],
    },
    {
        "id":             "b2c3d4e5-0002-0002-0002-000000000023",
        "slug":           "ilmiy-konferensiyalar",
        "title_uz":       "Ilmiy konferensiyalar",
        "title_ru":       "Научные конференции",
        "title_en":       "Scientific Conferences",
        "description_uz": "Konferensiyalar, tezislar va ilmiy tadbirlar.",
        "description_ru": "Конференции, тезисы и научные мероприятия.",
        "description_en": "Conferences, theses and scientific events.",
        "icon":           "calendar-days",
        "order":          3,
        "items": [
            {
                "title_uz": "Xalqaro sport fanlari konferensiyasi 2025",
                "title_ru": "Международная конференция по спортивным наукам 2025",
                "title_en": "International Sports Sciences Conference 2025",
                "description_uz": "2025-yil may oyida bo'lib o'tadigan xalqaro ilmiy konferensiya.",
                "order": 1,
            },
            {
                "title_uz": "Respublika yoshlar ilmiy anjumani",
                "title_ru": "Республиканский молодёжный научный форум",
                "title_en": "Republican Youth Scientific Forum",
                "description_uz": "Yosh olimlar va doktorantlar uchun ilmiy anjuman.",
                "order": 2,
            },
            {
                "title_uz": "Jismoniy tarbiya innovatsiyalari simpozium",
                "title_ru": "Симпозиум по инновациям в физическом воспитании",
                "title_en": "Physical Education Innovations Symposium",
                "description_uz": "Zamonaviy jismoniy tarbiya uslubiyatini muhokama qilish platformasi.",
                "order": 3,
            },
        ],
    },
    {
        "id":             "b2c3d4e5-0002-0002-0002-000000000024",
        "slug":           "ilmiy-ishlar-va-innovatsiyalar",
        "title_uz":       "Ilmiy ishlar va innovatsiyalar",
        "title_ru":       "Научные работы и инновации",
        "title_en":       "Scientific Works and Innovations",
        "description_uz": "Tadqiqot natijalari va innovatsion loyihalar.",
        "description_ru": "Результаты исследований и инновационные проекты.",
        "description_en": "Research results and innovative projects.",
        "icon":           "lightbulb",
        "order":          4,
        "items": [
            {
                "title_uz": "Akademiya professor-o'qituvchilari ilmiy ishlari to'plami",
                "title_ru": "Сборник научных работ профессоров и преподавателей академии",
                "title_en": "Academy Faculty Scientific Works Collection",
                "description_uz": "2024-2025 yillardagi ilmiy maqolalar va tadqiqot natijalari.",
                "order": 1,
            },
            {
                "title_uz": "Sport texnologiyalari innovatsiyasi",
                "title_ru": "Инновации в спортивных технологиях",
                "title_en": "Sports Technology Innovation",
                "description_uz": "Zamonaviy sport texnologiyalari va ularni ta'limga tatbiq etish.",
                "order": 2,
            },
            {
                "title_uz": "Raqamli sport tahlili platformasi",
                "title_ru": "Платформа цифрового спортивного анализа",
                "title_en": "Digital Sports Analysis Platform",
                "description_uz": "Sportchilar ma'lumotlarini raqamli tahlil qilish tizimi.",
                "order": 3,
            },
            {
                "title_uz": "Patent va intellektual mulk ro'yxati",
                "title_ru": "Список патентов и интеллектуальной собственности",
                "title_en": "Patent and Intellectual Property List",
                "description_uz": "Akademiya olimlari tomonidan olingan patentlar ro'yxati.",
                "order": 4,
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Ilmiy faoliyat (fan) kategoriyalari va namunali itemlarni DB ga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help="Avval ilmiy-faoliyat slug bo'yicha mavjud categorylarni o'chiradi",
        )

    def handle(self, *args, **options):
        if options['clear']:
            IlmiyFaoliyatCategory.objects.filter(slug=ROOT['slug']).delete()
            self.stdout.write(self.style.WARNING("Mavjud ilmiy-faoliyat ma'lumotlari o'chirildi."))

        root, created = IlmiyFaoliyatCategory.objects.update_or_create(
            slug=ROOT['slug'],
            defaults={
                'id':       uuid.UUID(ROOT['id']),
                'title_uz': ROOT['title_uz'],
                'title_ru': ROOT['title_ru'],
                'title_en': ROOT['title_en'],
                'parent':   None,
                'order':    ROOT['order'],
            },
        )
        action = 'Yaratildi' if created else 'Yangilandi'
        self.stdout.write(f"[{action}] Root: {root.title_uz}")

        for sub_data in SUBCATEGORIES:
            sub, s_created = IlmiyFaoliyatCategory.objects.update_or_create(
                slug=sub_data['slug'],
                defaults={
                    'id':             uuid.UUID(sub_data['id']),
                    'title_uz':       sub_data['title_uz'],
                    'title_ru':       sub_data['title_ru'],
                    'title_en':       sub_data['title_en'],
                    'description_uz': sub_data['description_uz'],
                    'description_ru': sub_data['description_ru'],
                    'description_en': sub_data['description_en'],
                    'icon':           sub_data['icon'],
                    'parent':         root,
                    'order':          sub_data['order'],
                },
            )
            s_action = 'Yaratildi' if s_created else 'Yangilandi'
            self.stdout.write(f"  [{s_action}] Sub: {sub.title_uz}")

            for item_data in sub_data.get('items', []):
                item, i_created = IlmiyFaoliyat.objects.update_or_create(
                    category=sub,
                    order=item_data['order'],
                    defaults={
                        'title_uz':       item_data['title_uz'],
                        'title_ru':       item_data['title_ru'],
                        'title_en':       item_data['title_en'],
                        'description_uz': item_data.get('description_uz', ''),
                        'is_active':      True,
                    },
                )
                i_action = 'Yaratildi' if i_created else 'Yangilandi'
                self.stdout.write(f"    [{i_action}] Item: {item.title_uz}")

        self.stdout.write(self.style.SUCCESS("\nIlmiy faoliyat ma'lumotlari muvaffaqiyatli qo'shildi!"))
