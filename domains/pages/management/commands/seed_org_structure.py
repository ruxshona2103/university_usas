"""
python manage.py seed_org_structure          # to'liq qayta yozadi (clear + seed)
"""
from django.core.management.base import BaseCommand
from domains.pages.models import OrgNode


# ── Tuzilma ma'lumotlari ──────────────────────────────────────────────────────
# (key, parent_key, node_type, name_uz, name_ru, name_en,
#  is_starred, is_double_starred, is_highlighted, order)

NODES = [
    # ═══════════════════════════════════════════════════════════════
    # 0 — KUZATUV KENGASHI (ildiz)
    # ═══════════════════════════════════════════════════════════════
    (
        'kuzatuv', None, 'governing',
        "Kuzatuv kengashi",
        "Наблюдательный совет",
        "Supervisory Board",
        False, False, False, 0,
    ),

    # ═══════════════════════════════════════════════════════════════
    # 1 — AKADEMIYA KENGASHI (kuzatuv ostida, chap ustun)
    # ═══════════════════════════════════════════════════════════════
    (
        'ak_kengash', 'kuzatuv', 'governing',
        "Akademiya kengashi",
        "Академический совет",
        "Academic Council",
        False, False, False, 1,
    ),
    (
        'birinchi_pro', 'ak_kengash', 'prorektor',
        "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektor",
        "Первый проректор по вопросам молодёжи и духовно-просветительской работе",
        "First Vice-Rector for Youth Affairs and Spiritual-Educational Work",
        False, False, False, 1,
    ),
    (
        'yoshlar_bolim', 'birinchi_pro', 'department',
        "Yoshlar bilan ishlash, ma'naviyat va ma'rifat bo'limi",
        "Отдел работы с молодёжью, духовности и просвещения",
        "Department of Youth Work, Spirituality and Enlightenment",
        False, False, False, 1,
    ),
    (
        'turar_joy', 'birinchi_pro', 'department',
        "Talabalar turar joyi",
        "Общежитие студентов",
        "Student Dormitory",
        False, False, False, 2,
    ),
    (
        'psixolog', 'birinchi_pro', 'other',
        "Psixolog",
        "Психолог",
        "Psychologist",
        False, False, False, 3,
    ),
    (
        'sport_klubi', 'birinchi_pro', 'other',
        "Sport klubi",
        "Спортивный клуб",
        "Sports Club",
        False, True, False, 4,
    ),

    # ═══════════════════════════════════════════════════════════════
    # 2 — XALQARO MASLAHATCHI (kuzatuv ostida, 2-ustun)
    # ═══════════════════════════════════════════════════════════════
    (
        'xalq_mash', 'kuzatuv', 'other',
        "Xalqaro maslahatchi",
        "Международный советник",
        "International Adviser",
        False, False, False, 2,
    ),
    (
        'oquv_pro', 'xalq_mash', 'prorektor',
        "O'quv ishlari bo'yicha prorektor",
        "Проректор по учебной работе",
        "Vice-Rector for Academic Affairs",
        False, False, False, 1,
    ),
    (
        'oquv_uslub', 'oquv_pro', 'department',
        "O'quv-uslubiy bo'lim",
        "Учебно-методический отдел",
        "Academic-Methodological Department",
        False, False, False, 1,
    ),
    (
        'raqamli', 'oquv_pro', 'department',
        "Raqamli ta'lim texnologiyalari markazi",
        "Центр цифровых образовательных технологий",
        "Centre for Digital Educational Technologies",
        False, False, False, 2,
    ),
    (
        'parasport_fak', 'oquv_pro', 'department',
        "Sport va parasport turlari fakulteti",
        "Факультет видов спорта и параспорта",
        "Faculty of Sports and Para-Sports",
        False, False, False, 3,
    ),

    # ═══════════════════════════════════════════════════════════════
    # 3 — REKTOR (kuzatuv ostida, markaz)
    # ═══════════════════════════════════════════════════════════════
    (
        'rektor', 'kuzatuv', 'rector',
        "Rektor",
        "Ректор",
        "Rector",
        False, False, False, 3,
    ),

    # 3.1 — Ilmiy ishlar prorektor
    (
        'ilmiy_pro', 'rektor', 'prorektor',
        "Ilmiy ishlar va innovatsiyalar bo'yicha prorektor",
        "Проректор по научным вопросам и инновациям",
        "Vice-Rector for Research and Innovation",
        False, False, False, 1,
    ),
    (
        'ilmiy_sektor', 'ilmiy_pro', 'department',
        "Ilmiy tadqiqotlar, innovatsiyalar va ilmiy-pedagogik kadrlar tayyorlash sektori",
        "Сектор научных исследований, инноваций и подготовки научно-педагогических кадров",
        "Sector for Research, Innovation and Scientific-Pedagogical Staff Training",
        False, False, False, 1,
    ),
    (
        'xalq_hamkor', 'ilmiy_pro', 'department',
        "Xalqaro hamkorlik bo'limi",
        "Отдел международного сотрудничества",
        "Department of International Cooperation",
        False, False, False, 2,
    ),
    (
        'iqtidor', 'ilmiy_pro', 'department',
        "Iqtidorli talabalarning ilmiy tadqiqot faoliyatini tashkil etish sektori",
        "Сектор организации научно-исследовательской деятельности одарённых студентов",
        "Sector for Organising Research Activities of Talented Students",
        False, False, True, 3,
    ),

    # 3.2 — Institutlar (bevosita rektorga bo'ysunuvchi)
    (
        'malaka_inst', 'rektor', 'institute',
        "Jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish instituti hamda uning Nukus, Samarqand va Farg'ona filiallari",
        "Институт переподготовки и повышения квалификации специалистов по физической культуре и спорту и его филиалы в Нукусе, Самарканде и Фергане",
        "Institute for Retraining and Professional Development of Physical Culture and Sports Specialists and its branches in Nukus, Samarkand and Fergana",
        True, False, False, 2,
    ),
    (
        'jt_inst', 'rektor', 'institute',
        "Jismoniy tarbiya va sport ilmiy-tadqiqotlar instituti",
        "Научно-исследовательский институт физической культуры и спорта",
        "Research Institute of Physical Culture and Sports",
        True, False, False, 3,
    ),
    (
        'tibbiyot', 'rektor', 'institute',
        "Davlat sport tibbiyoti ilmiy amaliy markazi",
        "Государственный научно-практический центр спортивной медицины",
        "State Scientific and Practical Centre of Sports Medicine",
        True, False, False, 4,
    ),
    (
        'tarix_markaz', 'rektor', 'institute',
        "O'zbekiston tarixi va xorijiy tillarni o'qitish markazi",
        "Центр изучения истории Узбекистана и иностранных языков",
        "Centre for Uzbekistan History and Foreign Language Teaching",
        False, False, False, 5,
    ),
    (
        'kutubxona', 'rektor', 'institute',
        "Axborot kutubxona markazi",
        "Информационно-библиотечный центр",
        "Information and Library Centre",
        False, False, False, 6,
    ),

    # 3.3 — Reja-moliya sektori (rektorga bo'ysunuvchi)
    (
        'reja_moliya', 'rektor', 'department',
        "Reja-moliya sektori",
        "Планово-финансовый сектор",
        "Planning and Finance Sector",
        False, False, False, 7,
    ),
    (
        'buxgalteriya', 'reja_moliya', 'department',
        "Buxgalteriya",
        "Бухгалтерия",
        "Accounting Department",
        False, False, False, 1,
    ),
    (
        'fuqaro_mehnat', 'reja_moliya', 'department',
        "Fuqaro va mehnat muhofazasi bo'limi",
        "Отдел гражданской и трудовой защиты",
        "Department of Civil and Labour Protection",
        False, False, False, 2,
    ),
    (
        'texnik_vosita', 'reja_moliya', 'department',
        "O'qitishning texnik vositalari bo'limi",
        "Отдел технических средств обучения",
        "Department of Technical Teaching Aids",
        False, False, False, 3,
    ),
    (
        'bosh_muh', 'reja_moliya', 'other',
        "Bosh muhandis",
        "Главный инженер",
        "Chief Engineer",
        False, False, False, 4,
    ),
    (
        'marketing', 'reja_moliya', 'department',
        "Marketing va talabalar amaliyoti bo'limi",
        "Отдел маркетинга и студенческой практики",
        "Department of Marketing and Student Internship",
        False, False, True, 5,
    ),

    # ═══════════════════════════════════════════════════════════════
    # 4 — REKTOR YORDAMCHISI (rektor ostida, o'ng ustun)
    # ═══════════════════════════════════════════════════════════════
    (
        'rektor_yord', 'rektor', 'prorektor',
        "Rektor yordamchisi",
        "Помощник ректора",
        "Rector's Assistant",
        False, False, False, 8,
    ),
    (
        'talim_nazorat', 'rektor_yord', 'department',
        "Ta'lim sifatini nazorat qilish bo'limi",
        "Отдел контроля качества образования",
        "Department of Educational Quality Control",
        False, False, False, 1,
    ),
    (
        'murojaat', 'rektor_yord', 'department',
        "Jismoniy va yuridik shaxslarning murojaatlari bilan ishlash, nazorat va monitoring sektori",
        "Сектор работы с обращениями физических и юридических лиц, контроля и мониторинга",
        "Sector for Handling Appeals of Individuals and Legal Entities, Control and Monitoring",
        False, False, False, 2,
    ),
    (
        'komplaens', 'rektor_yord', 'department',
        "Korrupsiyaga qarshi kurashish \"Komplaens-nazorat\" tizimini boshqarish bo'limi",
        "Отдел управления системой противодействия коррупции \"Комплаенс-контроль\"",
        "Department for Managing the Anti-Corruption Compliance Control System",
        False, False, False, 3,
    ),
    (
        'matbuot', 'rektor_yord', 'other',
        "Matbuot kotibi",
        "Пресс-секретарь",
        "Press Secretary",
        False, False, False, 4,
    ),
    (
        'xodimlar', 'rektor_yord', 'department',
        "Xodimlar bo'limi",
        "Отдел кадров",
        "Human Resources Department",
        False, False, False, 5,
    ),
    (
        'devonxona', 'rektor_yord', 'department',
        "Devonxona va arxiv",
        "Канцелярия и архив",
        "Office and Archive",
        False, False, False, 6,
    ),
    (
        'yuriskonsult', 'rektor_yord', 'other',
        "Yuriskonsult",
        "Юрисконсульт",
        "Legal Adviser",
        False, False, False, 7,
    ),
    (
        'birinchi_bolim', 'rektor_yord', 'department',
        "Birinchi bo'lim",
        "Первый отдел",
        "First Department",
        False, False, False, 8,
    ),

    # ═══════════════════════════════════════════════════════════════
    # 5 — KAFEDRALAR (rektor ostida, pastki qator)
    # ═══════════════════════════════════════════════════════════════
    (
        'kaf_yakka', 'rektor', 'kafedra',
        "Yakkakurash va suv sporti turlari kafedrasi",
        "Кафедра видов единоборств и водного спорта",
        "Department of Individual Combat and Aquatic Sports",
        False, False, False, 11,
    ),
    (
        'kaf_jamoaviy', 'rektor', 'kafedra',
        "Sportning jamoaviy, texnik va murakkab turlari kafedrasi",
        "Кафедра командных, технических и сложнокоординационных видов спорта",
        "Department of Team, Technical and Complex Sports",
        False, False, False, 12,
    ),
    (
        'kaf_parasport', 'rektor', 'kafedra',
        "Parasport turlari kafedrasi",
        "Кафедра видов параспорта",
        "Department of Para-Sports",
        False, False, False, 13,
    ),
    (
        'kaf_ijtimoiy', 'rektor', 'kafedra',
        "Ijtimoiy-gumanitar, tibbiy-biologik fanlar kafedrasi",
        "Кафедра социально-гуманитарных, медико-биологических дисциплин",
        "Department of Social-Humanitarian and Medical-Biological Sciences",
        False, False, False, 14,
    ),
]


class Command(BaseCommand):
    help = "Tashkiliy tuzilmani rasmga muvofiq qayta seed qiladi"

    def handle(self, *args, **options):
        deleted, _ = OrgNode.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"{deleted} ta eski tugun o'chirildi."))

        created_map = {}
        for row in NODES:
            (key, parent_key, node_type, title_uz, title_ru, title_en,
             is_starred, is_double_starred, is_highlighted, order) = row

            parent = created_map.get(parent_key) if parent_key else None
            node = OrgNode.objects.create(
                node_type         = node_type,
                title_uz          = title_uz,
                title_ru          = title_ru,
                title_en          = title_en,
                is_starred        = is_starred,
                is_double_starred = is_double_starred,
                is_highlighted    = is_highlighted,
                order             = order,
                parent            = parent,
            )
            created_map[key] = node

        self.stdout.write(self.style.SUCCESS(
            f"{len(NODES)} ta tugun muvaffaqiyatli yaratildi."
        ))
        self.stdout.write("  Tuzilma:")
        self.stdout.write("  KUZATUV KENGASHI")
        self.stdout.write("  +-- Akademiya kengashi -> Birinchi prorektor")
        self.stdout.write("  +-- Xalqaro maslahatchi -> O'quv prorektor")
        self.stdout.write("  +-- REKTOR -> Ilmiy pro / Institutlar / Reja-moliya / Rektor yordamchisi / Kafedralar")
