"""
python manage.py seed_org_structure
"""
from django.core.management.base import BaseCommand
from domains.pages.models import OrgNode, OrgSection

SECTIONS = [
    ('rahbariyat',            "Rahbariyat",                          "Akademiya boshqaruv organlari va rahbariyat tarkibi.",       1),
    ('yoshlar-manaviyat',     "Yoshlar va ma'naviyat",               "Talabalar hayoti, tarbiya va ijtimoiy qo'llab-quvvatlash.",  2),
    ('talim-bloki',           "Ta'lim bloki",                        "O'quv jarayoni, metodika va ta'lim texnologiyalari.",        3),
    ('ilmiy-xalqaro',         "Ilmiy va xalqaro yo'nalish",          "Ilmiy tadqiqotlar, innovatsiya va hamkorlik.",               4),
    ('akademiya-tashkilotlar',"Akademiya huzuridagi tashkilotlar",   "Akademiya tizimiga kiruvchi institut va markazlar.",         5),
    ('moliya-xojalik',        "Moliyaviy-xo'jalik",                  "Reja-moliya, xavfsizlik va xo'jalik xizmatlari.",           6),
    ('nazorat-xizmatlar',     "Nazorat va xizmatlar",                "Sifat nazorati, murojaatlar va ma'muriy xizmatlar.",        7),
]

# (key, parent_key, node_type, slug,
#  section_slug, section_order,
#  title_uz, title_ru, title_en,
#  description_uz,
#  is_starred, is_double_starred, is_highlighted, order)

NODES = [

    # ══════════════════════════════════════════════════════════════
    # KUZATUV KENGASHI (root)
    # ══════════════════════════════════════════════════════════════
    (
        'kuzatuv', None, 'governing', 'kuzatuv-kengashi',
        'rahbariyat', 1,
        "Kuzatuv kengashi", "Наблюдательный совет", "Supervisory Board",
        "Strategik nazorat va muvofiqlashtirish organi.",
        False, False, False, 0,
    ),

    # ── Akademiya kengashi ──────────────────────────────────────
    (
        'ak_kengash', 'kuzatuv', 'governing', 'akademiya-kengashi',
        'rahbariyat', 2,
        "Akademiya kengashi", "Академический совет", "Academic Council",
        "Oliy boshqaruv organi va asosiy qarorlar.",
        False, False, False, 1,
    ),

    # ── Xalqaro maslahatchi ──────────────────────────────────────
    (
        'xalq_mash', 'kuzatuv', 'other', 'xalqaro-maslahatchi',
        'rahbariyat', 3,
        "Xalqaro maslahatchi", "Международный советник", "International Adviser",
        "Xalqaro hamkorlik va tajriba almashuv bo'yicha maslahatlar.",
        False, False, False, 2,
    ),

    # ── Rektor ──────────────────────────────────────────────────
    (
        'rektor', 'kuzatuv', 'rector', 'rektor',
        'rahbariyat', 4,
        "Rektor", "Ректор", "Rector",
        "Akademiya faoliyatiga umumiy rahbarlik.",
        False, False, False, 3,
    ),

    # ── Rektor yordamchisi ───────────────────────────────────────
    (
        'rektor_yord', 'kuzatuv', 'prorektor', 'rektor-yordamchisi',
        'rahbariyat', 5,
        "Rektor yordamchisi", "Помощник ректора", "Rector's Assistant",
        "Rektor faoliyatini tashkiliy qo'llab-quvvatlash.",
        False, False, False, 4,
    ),

    # ══════════════════════════════════════════════════════════════
    # YOSHLAR MASALALARI VA MA'NAVIY-MA'RIFIY ISHLAR
    # (Akademiya kengashi ostida)
    # ══════════════════════════════════════════════════════════════
    (
        'yoshlar_pro', 'ak_kengash', 'prorektor', 'yoshlar-manaviy-prorektor',
        'yoshlar-manaviyat', 1,
        "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha prorektor",
        "Проректор по вопросам молодёжи и духовно-просветительской работе",
        "Vice-Rector for Youth Affairs and Spiritual-Educational Work",
        "Yoshlar siyosati, tarbiya va ma'naviy-ma'rifiy ishlar.",
        False, False, False, 1,
    ),
    (
        'yoshlar_bolim', 'yoshlar_pro', 'department', 'yoshlar-bolimi',
        'yoshlar-manaviyat', 2,
        "Yoshlar bilan ishlash bo'limi",
        "Отдел работы с молодёжью",
        "Department of Youth Work",
        "Yoshlar tadbirlari, loyihalar va tashabbuslar.",
        False, False, False, 1,
    ),
    (
        'turar_joy', 'yoshlar_pro', 'department', 'talabalar-turar-joyi',
        'yoshlar-manaviyat', 3,
        "Talabalar turar joyi", "Общежитие студентов", "Student Dormitory",
        "Yotoqxona va talabalarning yashash sharoitlari.",
        False, False, False, 2,
    ),
    (
        'psixolog', 'yoshlar_pro', 'other', 'psixolog',
        'yoshlar-manaviyat', 4,
        "Psixolog", "Психолог", "Psychologist",
        "Psixologik maslahat va qo'llab-quvvatlash.",
        False, False, False, 3,
    ),
    (
        'sport_klubi', 'yoshlar_pro', 'other', 'sport-klubi',
        'yoshlar-manaviyat', 5,
        "Sport klubi", "Спортивный клуб", "Sports Club",
        "Sport tadbirlari, musobaqalar va klub hayoti.",
        False, False, False, 4,
    ),

    # ══════════════════════════════════════════════════════════════
    # O'QUV ISHLARI BO'YICHA
    # (Xalqaro maslahatchi ostida)
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
        "Raqamli ta'lim markazi",
        "Центр цифрового образования",
        "Digital Education Centre",
        "Raqamli platformalar, LMS va ta'lim IT yechimlari.",
        False, False, False, 2,
    ),
    (
        'parasport_fak', 'oquv_pro', 'department', 'sport-parasport',
        'talim-bloki', 4,
        "Sport va parasport", "Спорт и параспорт", "Sports and Para-Sports",
        "Sport va parasport ta'lim yo'nalishlari.",
        False, False, False, 3,
    ),

    # ══════════════════════════════════════════════════════════════
    # ILMIY ISHLAR VA INNOVATSIYALAR
    # (Rektor ostida)
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
        'ilmiy_tadq', 'ilmiy_pro', 'department', 'ilmiy-tadqiqotlar',
        'ilmiy-xalqaro', 2,
        "Ilmiy tadqiqotlar",
        "Научные исследования",
        "Scientific Research",
        "Ilmiy loyihalar, grantlar va nashrlar.",
        False, False, False, 1,
    ),
    (
        'xalq_hamkor', 'ilmiy_pro', 'department', 'xalqaro-hamkorlik',
        'ilmiy-xalqaro', 3,
        "Xalqaro hamkorlik",
        "Международное сотрудничество",
        "International Cooperation",
        "Xalqaro aloqalar, hamkorlar va akademik mobillik.",
        False, False, False, 2,
    ),
    (
        'iqtidor', 'ilmiy_pro', 'department', 'iqtidorli-talabalar-ilmiy-faoliyati',
        'ilmiy-xalqaro', 4,
        "Iqtidorli talabalarning ilmiy faoliyati",
        "Научная деятельность одарённых студентов",
        "Research Activity of Talented Students",
        "Talabalar ilmiy ishlari va startap tashabbuslari.",
        False, False, False, 3,
    ),

    # ══════════════════════════════════════════════════════════════
    # AKADEMIYA HUZURIDAGI TASHKILOTLAR
    # (Rektor ostida)
    # ══════════════════════════════════════════════════════════════
    (
        'malaka_inst', 'rektor', 'institute', 'malaka-oshirish-instituti',
        'akademiya-tashkilotlar', 1,
        "Jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash instituti",
        "Институт переподготовки и повышения квалификации специалистов по физической культуре и спорту",
        "Institute for Retraining and Advanced Training of Physical Culture and Sports Specialists",
        "Nukus, Samarqand va Farg'ona filiallari bilan.",
        True, False, False, 2,
    ),
    (
        'jt_inst', 'rektor', 'institute', 'jismoniy-tarbiya-ilmiy-instituti',
        'akademiya-tashkilotlar', 2,
        "Jismoniy tarbiya va sport ilmiy tadqiqotlar instituti",
        "Научно-исследовательский институт физической культуры и спорта",
        "Research Institute of Physical Culture and Sports",
        "Sport fanlari bo'yicha ilmiy tadqiqotlar.",
        True, False, False, 3,
    ),
    (
        'tibbiyot', 'rektor', 'institute', 'davlat-sport-tibbiyoti-markazi',
        'akademiya-tashkilotlar', 3,
        "Davlat sport tibbiyoti ilmiy-amaliy markazi",
        "Государственный научно-практический центр спортивной медицины",
        "State Scientific and Practical Centre of Sports Medicine",
        "Sport tibbiyoti va ilmiy-amaliy xizmatlar.",
        True, False, False, 4,
    ),
    (
        'tarix_markaz', 'rektor', 'institute', 'ozbekiston-tarixi-xorijiy-tillar-markazi',
        'akademiya-tashkilotlar', 4,
        "O'zbekiston tarixi va xorijiy tillarni o'qitish markazi",
        "Центр преподавания истории Узбекистана и иностранных языков",
        "Centre for Teaching History of Uzbekistan and Foreign Languages",
        "Tarix va xorijiy tillar bo'yicha ta'lim.",
        False, False, False, 5,
    ),
    (
        'kutubxona', 'rektor', 'institute', 'axborot-kutubxona-markazi',
        'akademiya-tashkilotlar', 5,
        "Axborot kutubxona markazi",
        "Информационно-библиотечный центр",
        "Information and Library Centre",
        "Kutubxona, elektron resurslar va o'quv adabiyotlar.",
        False, False, False, 6,
    ),

    # ══════════════════════════════════════════════════════════════
    # MARKAZ VA BO'LIMLAR (Rektor ostida — Reja-moliya sektori)
    # ══════════════════════════════════════════════════════════════
    (
        'reja_moliya', 'rektor', 'department', 'reja-moliya-sektori',
        'moliya-xojalik', 1,
        "Reja-moliya sektori", "Планово-финансовый сектор", "Planning and Finance Sector",
        "Budjet rejalashtirish va moliyaviy boshqaruv.",
        False, False, False, 7,
    ),
    (
        'buxgalteriya', 'reja_moliya', 'department', 'buxgalteriya',
        'moliya-xojalik', 2,
        "Buxgalteriya", "Бухгалтерия", "Accounting Department",
        "Hisob-kitob, moliyaviy hisobot va to'lovlar.",
        False, False, False, 1,
    ),
    (
        'fuqaro_mehnat', 'reja_moliya', 'department', 'fuqaro-mehnat-muhofazasi-bolimi',
        'moliya-xojalik', 3,
        "Fuqaro va mehnat muhofazasi bo'limi",
        "Отдел гражданской и трудовой защиты",
        "Department of Civil and Labour Protection",
        "Mehnat xavfsizligi va muhofaza qoidalari.",
        False, False, False, 2,
    ),
    (
        'texnik_vosita', 'reja_moliya', 'department', 'oquvning-texnik-vositalari-bolimi',
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
        "Bosh muhandis", "Главный инженер", "Chief Engineer",
        "Inshootlar, kommunal tizimlar va texnik nazorat.",
        False, False, False, 4,
    ),
    (
        'marketing', 'reja_moliya', 'department', 'marketing-talabalar-amaliyoti-bolimi',
        'moliya-xojalik', 6,
        "Marketing va talabalar amaliyoti bo'limi",
        "Отдел маркетинга и студенческой практики",
        "Department of Marketing and Student Internship",
        "Amaliyotlar, hamkor tashkilotlar va targ'ibot.",
        False, False, False, 5,
    ),

    # ══════════════════════════════════════════════════════════════
    # REKTOR YORDAMCHISI OSTIDAGI BO'LIMLAR
    # ══════════════════════════════════════════════════════════════
    (
        'talim_nazorat', 'rektor_yord', 'department', 'talim-sifatini-nazorat-bolimi',
        'nazorat-xizmatlar', 1,
        "Ta'lim sifatini nazorat qilish bo'limi",
        "Отдел контроля качества образования",
        "Department of Educational Quality Control",
        "Ta'lim sifati, monitoring va ichki nazorat.",
        False, False, False, 1,
    ),
    (
        'murojaat', 'rektor_yord', 'department', 'jismoniy-yuridik-shaxslar-murojaatlari',
        'nazorat-xizmatlar', 2,
        "Jismoniy va yuridik shaxslar murojaatlari bilan ishlash",
        "Работа с обращениями физических и юридических лиц",
        "Handling Appeals of Individuals and Legal Entities",
        "Murojaatlar, ijro intizomi va monitoring.",
        False, False, False, 2,
    ),
    (
        'komplaens', 'rektor_yord', 'department', 'korrupsiyaga-qarshi-kurashish-bolimi',
        'nazorat-xizmatlar', 3,
        "Korrupsiyaga qarshi kurashish bo'limi",
        "Отдел противодействия коррупции",
        "Anti-Corruption Department",
        "Shaffoflik, ichki nazorat va risklarni boshqarish.",
        False, False, False, 3,
    ),
    (
        'matbuot', 'rektor_yord', 'other', 'matbuot-kotibi',
        'nazorat-xizmatlar', 4,
        "Matbuot kotibi", "Пресс-секретарь", "Press Secretary",
        "OAV bilan ishlash va rasmiy axborot siyosati.",
        False, False, False, 4,
    ),
    (
        'xodimlar', 'rektor_yord', 'department', 'xodimlar-bolimi',
        'nazorat-xizmatlar', 5,
        "Xodimlar bo'limi", "Отдел кадров", "Human Resources Department",
        "Kadrlar ishlari va mehnat munosabatlari.",
        False, False, False, 5,
    ),
    (
        'devonxona', 'rektor_yord', 'department', 'devonxona-va-arxiv',
        'nazorat-xizmatlar', 6,
        "Devxonona va arxiv", "Канцелярия и архив", "Office and Archive",
        "Hujjatlar aylanishi va arxiv yuritish.",
        False, False, False, 6,
    ),
    (
        'yuridik', 'rektor_yord', 'other', 'yuridik-bolim',
        'nazorat-xizmatlar', 7,
        "Yuridik bo'lim", "Юридический отдел", "Legal Department",
        "Huquqiy maslahat va hujjatlar ekspertizasi.",
        False, False, False, 7,
    ),
    (
        'birinchi_bolim', 'rektor_yord', 'department', 'birinchi-bolim',
        'nazorat-xizmatlar', 8,
        "Birinchi bo'lim", "Первый отдел", "First Department",
        "Maxfiy ish yuritish va tartib-qoidalar.",
        False, False, False, 8,
    ),
]


class Command(BaseCommand):
    help = "Tashkiliy tuzilmani yangilangan sxemaga mos qayta seed qiladi"

    def handle(self, *args, **options):
        OrgNode.objects.all().delete()
        OrgSection.objects.all().delete()
        self.stdout.write(self.style.WARNING("Eski ma'lumotlar o'chirildi."))

        section_map = {}
        for slug, title_uz, description_uz, order in SECTIONS:
            sec = OrgSection.objects.create(
                slug=slug, title_uz=title_uz,
                description_uz=description_uz, order=order,
            )
            section_map[slug] = sec
        self.stdout.write(self.style.SUCCESS(f"{len(SECTIONS)} ta sektsiya yaratildi."))

        node_map = {}
        for row in NODES:
            (key, parent_key, node_type, slug,
             section_slug, section_order,
             title_uz, title_ru, title_en, description_uz,
             is_starred, is_double_starred, is_highlighted, order) = row

            node = OrgNode.objects.create(
                node_type=node_type, slug=slug,
                section=section_map.get(section_slug) if section_slug else None,
                section_order=section_order,
                title_uz=title_uz, title_ru=title_ru, title_en=title_en,
                description_uz=description_uz,
                is_starred=is_starred,
                is_double_starred=is_double_starred,
                is_highlighted=is_highlighted,
                order=order,
                parent=node_map.get(parent_key) if parent_key else None,
            )
            node_map[key] = node
            self.stdout.write(f"  [+] {title_uz[:60].encode('ascii','replace').decode()}")

        self.stdout.write(self.style.SUCCESS(f"\nJami: {len(NODES)} ta tugun yaratildi."))
