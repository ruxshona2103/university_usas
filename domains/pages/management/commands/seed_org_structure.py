"""
python manage.py seed_org_structure   # to'liq qayta yozadi
"""
from django.core.management.base import BaseCommand
from domains.pages.models import OrgNode, OrgSection


# ── Sektsiyalar ───────────────────────────────────────────────────────────────
# (slug, title_uz, description_uz, order)
SECTIONS = [
    ('rahbariyat',
     "Rahbariyat",
     "Akademiya boshqaruv organlari va rahbariyat tarkibi.",
     1),
    ('talim-bloki',
     "Ta'lim bloki",
     "O'quv jarayoni, metodika va ta'lim texnologiyalari.",
     2),
    ('ilmiy-xalqaro',
     "Ilmiy va xalqaro yo'nalish",
     "Ilmiy tadqiqotlar, innovatsiya va hamkorlik.",
     3),
    ('yoshlar-manaviyat',
     "Yoshlar va ma'naviyat",
     "Talabalar hayoti, tarbiya va ijtimoiy qo'llab-quvvatlash.",
     4),
    ('moliya-xojalik',
     "Moliyaviy-xo'jalik",
     "Reja-moliya, xavfsizlik va xo'jalik xizmatlari.",
     5),
    ('nazorat-xizmatlar',
     "Nazorat va xizmatlar",
     "Sifat nazorati, murojaatlar bilan ishlash va ma'muriy xizmatlar.",
     6),
    ('akademiya-tashkilotlar',
     "Akademiya huzuridagi tashkilotlar",
     "Akademiya tizimiga kiruvchi institut va markazlar.",
     7),
]

# ── Tugunlar ──────────────────────────────────────────────────────────────────
# (key, parent_key, node_type, slug,
#  section_slug, section_order,
#  title_uz, title_ru, title_en,
#  description_uz,
#  is_starred, is_double_starred, is_highlighted, order)
NODES = [
    # ══════════════════════════════════════════════════════════════
    # RAHBARIYAT sektsiyasi
    # ══════════════════════════════════════════════════════════════
    (
        'kuzatuv', None, 'governing', 'kuzatuv-kengashi',
        'rahbariyat', 1,
        "Kuzatuv kengashi",
        "Наблюдательный совет",
        "Supervisory Board",
        "Strategik nazorat va muvofiqlashtirish organi.",
        False, False, False, 0,
    ),
    (
        'ak_kengash', 'kuzatuv', 'governing', 'akademiya-kengashi',
        'rahbariyat', 2,
        "Akademiya kengashi",
        "Академический совет",
        "Academic Council",
        "Oliy boshqaruv organi va asosiy qarorlar.",
        False, False, False, 1,
    ),
    (
        'xalq_mash', 'kuzatuv', 'other', 'xalqaro-maslahatchi',
        'rahbariyat', 3,
        "Xalqaro maslahatchi",
        "Международный советник",
        "International Adviser",
        "Xalqaro hamkorlik va tajriba almashuv bo'yicha maslahatlar.",
        False, False, False, 2,
    ),
    (
        'rektor', 'kuzatuv', 'rector', 'rektor',
        'rahbariyat', 4,
        "Rektor",
        "Ректор",
        "Rector",
        "Akademiya faoliyatiga umumiy rahbarlik.",
        False, False, False, 3,
    ),
    (
        'rektor_yord', 'rektor', 'prorektor', 'rektor-yordamchisi',
        'rahbariyat', 5,
        "Rektor yordamchisi",
        "Помощник ректора",
        "Rector's Assistant",
        "Rektor faoliyatini tashkiliy qo'llab-quvvatlash.",
        False, False, False, 8,
    ),

    # ══════════════════════════════════════════════════════════════
    # TA'LIM BLOKI sektsiyasi
    # ══════════════════════════════════════════════════════════════
    (
        'oquv_pro', 'xalq_mash', 'prorektor', 'oquv-prorektor',
        'talim-bloki', 1,
        "O'quv ishlari bo'yicha prorektor",
        "Проректор по учебной работе",
        "Vice-Rector for Academic Affairs",
        "O'quv jarayonini boshqarish va muvofiqlashtirish.",
        False, False, False, 1,
    ),
    (
        'oquv_uslub', 'oquv_pro', 'department', 'oquv-uslubiy-bolim',
        'talim-bloki', 2,
        "O'quv-uslubiy bo'lim",
        "Учебно-методический отдел",
        "Academic-Methodological Department",
        "Dasturlar, metodik ta'minot va o'quv hujjatlari.",
        False, False, False, 1,
    ),
    (
        'raqamli', 'oquv_pro', 'department', 'raqamli-talim-markazi',
        'talim-bloki', 3,
        "Raqamli ta'lim texnologiyalari markazi",
        "Центр цифровых образовательных технологий",
        "Centre for Digital Educational Technologies",
        "Raqamli platformalar, LMS va ta'lim IT yechimlari.",
        False, False, False, 2,
    ),
    (
        'parasport_fak', 'oquv_pro', 'department', 'sport-parasport-fakulteti',
        'talim-bloki', 4,
        "Sport va parasport turlari fakulteti",
        "Факультет видов спорта и параспорта",
        "Faculty of Sports and Para-Sports",
        "Ta'lim yo'nalishlari, kafedralar va fakultet hayoti.",
        False, False, False, 3,
    ),
    (
        'kafedralar_group', 'rektor', 'kafedra', 'kafedralar',
        'talim-bloki', 5,
        "Kafedralar",
        "Кафедры",
        "Departments",
        "1) Yakkakurash va suv sporti; 2) Jamoaviy, texnik va murakkab; "
        "3) Parasport; 4) Ijtimoiy-gumanitar, tibbiy-biologik.",
        False, False, False, 10,
    ),

    # ══════════════════════════════════════════════════════════════
    # ILMIY VA XALQARO sektsiyasi
    # ══════════════════════════════════════════════════════════════
    (
        'ilmiy_pro', 'rektor', 'prorektor', 'ilmiy-prorektor',
        'ilmiy-xalqaro', 1,
        "Ilmiy ishlar va innovatsiyalar bo'yicha prorektor",
        "Проректор по научным вопросам и инновациям",
        "Vice-Rector for Research and Innovation",
        "Ilmiy faoliyat va innovatsiyalarni boshqarish.",
        False, False, False, 1,
    ),
    (
        'ilmiy_sektor', 'ilmiy_pro', 'department', 'ilmiy-tadqiqotlar-sektori',
        'ilmiy-xalqaro', 2,
        "Ilmiy tadqiqotlar, innovatsiyalar va ilmiy-pedagogik kadrlar tayyorlash sektori",
        "Сектор научных исследований, инноваций и подготовки научно-педагогических кадров",
        "Sector for Research, Innovation and Scientific-Pedagogical Staff Training",
        "Ilmiy loyihalar, grantlar va kadrlar salohiyati.",
        False, False, False, 1,
    ),
    (
        'xalq_hamkor', 'ilmiy_pro', 'department', 'xalqaro-hamkorlik',
        'ilmiy-xalqaro', 3,
        "Xalqaro hamkorlik bo'limi",
        "Отдел международного сотрудничества",
        "Department of International Cooperation",
        "Xalqaro aloqalar, hamkorlar va akademik mobillik.",
        False, False, False, 2,
    ),
    (
        'iqtidor', 'ilmiy_pro', 'department', 'iqtidorli-talabalar-sektori',
        'ilmiy-xalqaro', 4,
        "Iqtidorli talabalarning ilmiy tadqiqot faoliyatini tashkil etish sektori",
        "Сектор организации научно-исследовательской деятельности одарённых студентов",
        "Sector for Organising Research Activities of Talented Students",
        "Talabalar ilmiy ishlari va startap tashabbuslari.",
        False, False, True, 3,
    ),
    (
        'jt_inst', 'rektor', 'institute', 'jismoniy-tarbiya-ilmiy-instituti',
        'ilmiy-xalqaro', 5,
        "Jismoniy tarbiya va sport ilmiy-tadqiqotlar instituti",
        "Научно-исследовательский институт физической культуры и спорта",
        "Research Institute of Physical Culture and Sports",
        "Sport fanlari bo'yicha ilmiy tadqiqotlar va tahlil.",
        True, False, False, 3,
    ),

    # ══════════════════════════════════════════════════════════════
    # YOSHLAR VA MA'NAVIYAT sektsiyasi
    # ══════════════════════════════════════════════════════════════
    (
        'birinchi_pro', 'ak_kengash', 'prorektor', 'birinchi-prorektor',
        'yoshlar-manaviyat', 1,
        "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektor",
        "Первый проректор по вопросам молодёжи и духовно-просветительской работе",
        "First Vice-Rector for Youth Affairs and Spiritual-Educational Work",
        "Yoshlar siyosati, tarbiya va ma'naviy-ma'rifiy ishlar.",
        False, False, False, 1,
    ),
    (
        'yoshlar_bolim', 'birinchi_pro', 'department', 'yoshlar-bolimi',
        'yoshlar-manaviyat', 2,
        "Yoshlar bilan ishlash, ma'naviyat va ma'rifat bo'limi",
        "Отдел работы с молодёжью, духовности и просвещения",
        "Department of Youth Work, Spirituality and Enlightenment",
        "Tadbirlar, ma'naviy-ma'rifiy loyihalar va klublar.",
        False, False, False, 1,
    ),
    (
        'turar_joy', 'birinchi_pro', 'department', 'talabalar-turar-joyi',
        'yoshlar-manaviyat', 3,
        "Talabalar turar joyi",
        "Общежитие студентов",
        "Student Dormitory",
        "Yotoqxona va talabalarning yashash sharoitlari.",
        False, False, False, 2,
    ),
    (
        'psixolog', 'birinchi_pro', 'other', 'psixolog',
        'yoshlar-manaviyat', 4,
        "Psixolog",
        "Психолог",
        "Psychologist",
        "Psixologik maslahat va qo'llab-quvvatlash.",
        False, False, False, 3,
    ),
    (
        'sport_klubi', 'birinchi_pro', 'other', 'sport-klubi',
        'yoshlar-manaviyat', 5,
        "Sport klubi",
        "Спортивный клуб",
        "Sports Club",
        "Sport tadbirlari, musobaqalar va klub hayoti.",
        False, True, False, 4,
    ),

    # ══════════════════════════════════════════════════════════════
    # MOLIYAVIY-XO'JALIK sektsiyasi
    # ══════════════════════════════════════════════════════════════
    (
        'reja_moliya', 'rektor', 'department', 'reja-moliya-sektori',
        'moliya-xojalik', 1,
        "Reja-moliya sektori",
        "Планово-финансовый сектор",
        "Planning and Finance Sector",
        "Budjet rejalashtirish va moliyaviy boshqaruv.",
        False, False, False, 7,
    ),
    (
        'buxgalteriya', 'reja_moliya', 'department', 'buxgalteriya',
        'moliya-xojalik', 2,
        "Buxgalteriya",
        "Бухгалтерия",
        "Accounting Department",
        "Hisob-kitob, moliyaviy hisobot va to'lovlar.",
        False, False, False, 1,
    ),
    (
        'fuqaro_mehnat', 'reja_moliya', 'department', 'fuqaro-mehnat-muhofazasi',
        'moliya-xojalik', 3,
        "Fuqaro va mehnat muhofazasi bo'limi",
        "Отдел гражданской и трудовой защиты",
        "Department of Civil and Labour Protection",
        "Mehnat xavfsizligi va muhofaza qoidalari.",
        False, False, False, 2,
    ),
    (
        'texnik_vosita', 'reja_moliya', 'department', 'texnik-vositalar-bolimi',
        'moliya-xojalik', 4,
        "O'qitishning texnik vositalari bo'limi",
        "Отдел технических средств обучения",
        "Department of Technical Teaching Aids",
        "Audiovizual jihozlar va texnik ta'minot.",
        False, False, False, 3,
    ),
    (
        'bosh_muh', 'reja_moliya', 'other', 'bosh-muhandis',
        'moliya-xojalik', 5,
        "Bosh muhandis",
        "Главный инженер",
        "Chief Engineer",
        "Inshootlar, kommunal tizimlar va texnik nazorat.",
        False, False, False, 4,
    ),
    (
        'marketing', 'reja_moliya', 'department', 'marketing-amaliyot-bolimi',
        'moliya-xojalik', 6,
        "Marketing va talabalar amaliyoti bo'limi",
        "Отдел маркетинга и студенческой практики",
        "Department of Marketing and Student Internship",
        "Amaliyotlar, hamkor tashkilotlar va targ'ibot.",
        False, False, True, 5,
    ),

    # ══════════════════════════════════════════════════════════════
    # NAZORAT VA XIZMATLAR sektsiyasi
    # ══════════════════════════════════════════════════════════════
    (
        'talim_nazorat', 'rektor_yord', 'department', 'talim-sifati-nazorat',
        'nazorat-xizmatlar', 1,
        "Ta'lim sifatini nazorat qilish bo'limi",
        "Отдел контроля качества образования",
        "Department of Educational Quality Control",
        "Ta'lim sifati, monitoring va ichki nazorat.",
        False, False, False, 1,
    ),
    (
        'murojaat', 'rektor_yord', 'department', 'murojaatlar-sektori',
        'nazorat-xizmatlar', 2,
        "Jismoniy va yuridik shaxslarning murojaatlari bilan ishlash, nazorat va monitoring sektori",
        "Сектор работы с обращениями физических и юридических лиц, контроля и мониторинга",
        "Sector for Handling Appeals of Individuals and Legal Entities, Control and Monitoring",
        "Murojaatlar, ijro intizomi va monitoring.",
        False, False, False, 2,
    ),
    (
        'komplaens', 'rektor_yord', 'department', 'komplaens-nazorat',
        'nazorat-xizmatlar', 3,
        "Korrupsiyaga qarshi kurashish \"Komplaens-nazorat\" tizimini boshqarish bo'limi",
        "Отдел управления системой противодействия коррупции \"Комплаенс-контроль\"",
        "Department for Managing the Anti-Corruption Compliance Control System",
        "Shaffoflik, ichki nazorat va risklarni boshqarish.",
        False, False, False, 3,
    ),
    (
        'matbuot', 'rektor_yord', 'other', 'matbuot-kotibi',
        'nazorat-xizmatlar', 4,
        "Matbuot kotibi",
        "Пресс-секретарь",
        "Press Secretary",
        "OAV bilan ishlash va rasmiy axborot siyosati.",
        False, False, False, 4,
    ),
    (
        'xodimlar', 'rektor_yord', 'department', 'xodimlar-bolimi',
        'nazorat-xizmatlar', 5,
        "Xodimlar bo'limi",
        "Отдел кадров",
        "Human Resources Department",
        "Kadrlar ishlari va mehnat munosabatlari.",
        False, False, False, 5,
    ),
    (
        'devonxona', 'rektor_yord', 'department', 'devonxona-arxiv',
        'nazorat-xizmatlar', 6,
        "Devonxona va arxiv",
        "Канцелярия и архив",
        "Office and Archive",
        "Hujjatlar aylanishi va arxiv yuritish.",
        False, False, False, 6,
    ),
    (
        'yuriskonsult', 'rektor_yord', 'other', 'yuriskonsult',
        'nazorat-xizmatlar', 7,
        "Yuriskonsult",
        "Юрисконсульт",
        "Legal Adviser",
        "Huquqiy maslahat va hujjatlar ekspertizasi.",
        False, False, False, 7,
    ),
    (
        'birinchi_bolim', 'rektor_yord', 'department', 'birinchi-bolim',
        'nazorat-xizmatlar', 8,
        "Birinchi bo'lim",
        "Первый отдел",
        "First Department",
        "Maxfiy ish yuritish va tartib-qoidalar.",
        False, False, False, 8,
    ),

    # ══════════════════════════════════════════════════════════════
    # AKADEMIYA HUZURIDAGI TASHKILOTLAR sektsiyasi
    # ══════════════════════════════════════════════════════════════
    (
        'malaka_inst', 'rektor', 'institute', 'malaka-oshirish-instituti',
        'akademiya-tashkilotlar', 1,
        "Jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish instituti hamda uning Nukus, Samarqand va Farg'ona filiallari",
        "Институт переподготовки и повышения квалификации специалистов по физической культуре и спорту и его филиалы в Нукусе, Самарканде и Фергане",
        "Institute for Retraining and Professional Development of Physical Culture and Sports Specialists and its branches in Nukus, Samarkand and Fergana",
        "Nukus, Samarqand va Farg'ona filiallari bilan.",
        True, False, False, 2,
    ),
    (
        'tibbiyot', 'rektor', 'institute', 'sport-tibbiyoti-markazi',
        'akademiya-tashkilotlar', 2,
        "Davlat sport tibbiyoti ilmiy amaliy markazi",
        "Государственный научно-практический центр спортивной медицины",
        "State Scientific and Practical Centre of Sports Medicine",
        "Sport tibbiyoti va ilmiy-amaliy xizmatlar.",
        True, False, False, 4,
    ),
    (
        'tarix_markaz', 'rektor', 'institute', 'tarix-xorijiy-tillar-markazi',
        'akademiya-tashkilotlar', 3,
        "O'zbekiston tarixi va xorijiy tillarni o'qitish markazi",
        "Центр изучения истории Узбекистана и иностранных языков",
        "Centre for Uzbekistan History and Foreign Language Teaching",
        "Tarix va xorijiy tillar bo'yicha ta'lim.",
        False, False, False, 5,
    ),
    (
        'kutubxona', 'rektor', 'institute', 'axborot-kutubxona-markazi',
        'akademiya-tashkilotlar', 4,
        "Axborot kutubxona markazi",
        "Информационно-библиотечный центр",
        "Information and Library Centre",
        "Kutubxona, elektron resurslar va o'quv adabiyotlar.",
        False, False, False, 6,
    ),

    # ══════════════════════════════════════════════════════════════
    # Kafedralar (sektsiyasiz — tree uchun)
    # ══════════════════════════════════════════════════════════════
    (
        'kaf_yakka', 'kafedralar_group', 'kafedra', 'yakkakurash-suv-sporti-kafedrasi',
        None, 0,
        "Yakkakurash va suv sporti turlari kafedrasi",
        "Кафедра видов единоборств и водного спорта",
        "Department of Individual Combat and Aquatic Sports",
        "",
        False, False, False, 11,
    ),
    (
        'kaf_jamoaviy', 'kafedralar_group', 'kafedra', 'jamoaviy-texnik-sport-kafedrasi',
        None, 0,
        "Sportning jamoaviy, texnik va murakkab turlari kafedrasi",
        "Кафедра командных, технических и сложнокоординационных видов спорта",
        "Department of Team, Technical and Complex Sports",
        "",
        False, False, False, 12,
    ),
    (
        'kaf_parasport', 'kafedralar_group', 'kafedra', 'parasport-kafedrasi',
        None, 0,
        "Parasport turlari kafedrasi",
        "Кафедра видов параспорта",
        "Department of Para-Sports",
        "",
        False, False, False, 13,
    ),
    (
        'kaf_ijtimoiy', 'kafedralar_group', 'kafedra', 'ijtimoiy-gumanitar-kafedrasi',
        None, 0,
        "Ijtimoiy-gumanitar, tibbiy-biologik fanlar kafedrasi",
        "Кафедра социально-гуманитарных, медико-биологических дисциплин",
        "Department of Social-Humanitarian and Medical-Biological Sciences",
        "",
        False, False, False, 14,
    ),
]


class Command(BaseCommand):
    help = "Tashkiliy tuzilma sektsiyalari va tugunlarini qayta seed qiladi"

    def handle(self, *args, **options):
        # 1. Eski ma'lumotlarni o'chirish
        OrgNode.objects.all().delete()
        OrgSection.objects.all().delete()
        self.stdout.write(self.style.WARNING("Eski ma'lumotlar o'chirildi."))

        # 2. Sektsiyalarni yaratish
        section_map = {}
        for slug, title_uz, description_uz, order in SECTIONS:
            sec = OrgSection.objects.create(
                slug           = slug,
                title_uz       = title_uz,
                description_uz = description_uz,
                order          = order,
            )
            section_map[slug] = sec
        self.stdout.write(self.style.SUCCESS(f"{len(SECTIONS)} ta sektsiya yaratildi."))

        # 3. Tugunlarni yaratish
        node_map = {}
        for row in NODES:
            (key, parent_key, node_type, slug,
             section_slug, section_order,
             title_uz, title_ru, title_en,
             description_uz,
             is_starred, is_double_starred, is_highlighted, order) = row

            parent  = node_map.get(parent_key) if parent_key else None
            section = section_map.get(section_slug) if section_slug else None

            node = OrgNode.objects.create(
                node_type         = node_type,
                slug              = slug,
                section           = section,
                section_order     = section_order,
                title_uz          = title_uz,
                title_ru          = title_ru,
                title_en          = title_en,
                description_uz    = description_uz,
                is_starred        = is_starred,
                is_double_starred = is_double_starred,
                is_highlighted    = is_highlighted,
                order             = order,
                parent            = parent,
            )
            node_map[key] = node

        self.stdout.write(self.style.SUCCESS(
            f"{len(NODES)} ta tugun muvaffaqiyatli yaratildi."
        ))
