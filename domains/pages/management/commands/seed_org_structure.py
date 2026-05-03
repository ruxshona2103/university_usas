"""
python manage.py seed_org_structure
"""
from django.core.management.base import BaseCommand
from domains.pages.models import OrgNode, OrgSection

SECTIONS = [
    ('rahbariyat',              "Kuzatuv kengashi",                        "Akademiya boshqaruv organlari va rahbariyat tarkibi.",      1),
    ('yoshlar-manaviyat',       "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar", "Talabalar hayoti, tarbiya va ijtimoiy qo'llab-quvvatlash.", 2),
    ('talim-bloki',             "O'quv ishlari bo'yicha",                  "O'quv jarayoni, metodika va ta'lim texnologiyalari.",       3),
    ('ilmiy-xalqaro',           "Ilmiy ishlar va innovatsiyalar",           "Ilmiy tadqiqotlar, innovatsiya va hamkorlik.",              4),
    ('akademiya-tashkilotlar',  "Akademiya huzuridagi tashkilotlar",        "Akademiya tizimiga kiruvchi institut va markazlar.",        5),
    ('markaz-bolimlar',         "Markaz va bo'limlar",                      "Ma'muriy, moliyaviy va xo'jalik xizmatlari.",              6),
]

# (key, parent_key, node_type, slug,
#  section_slug, section_order,
#  title_uz, title_ru, title_en,
#  description_uz,
#  is_starred, is_double_starred, is_highlighted, order)

NODES = [

    # ══════════════════════════════════════════════════════════════
    # 1. KUZATUV KENGASHI
    # ══════════════════════════════════════════════════════════════
    (
        'akademiya_kengash', None, 'governing', 'akademiya-kengashi',
        'rahbariyat', 1,
        "Akademiya kengashi", "Академический совет", "Academic Council",
        "Oliy boshqaruv organi va asosiy qarorlar.",
        False, False, False, 1,
    ),
    (
        'xalq_mash', None, 'other', 'xalqaro-maslahatchi',
        'rahbariyat', 2,
        "Xalqaro maslahatchi", "Международный советник", "International Adviser",
        "Xalqaro hamkorlik va tajriba almashuv bo'yicha maslahatlar.",
        False, False, False, 2,
    ),
    (
        'rektor', None, 'rector', 'rektor',
        'rahbariyat', 3,
        "Rektor", "Ректор", "Rector",
        "Akademiya faoliyatiga umumiy rahbarlik.",
        False, False, False, 3,
    ),
    (
        'rektor_yord', None, 'prorektor', 'rektor-yordamchisi',
        'rahbariyat', 4,
        "Rektor yordamchisi", "Помощник ректора", "Rector's Assistant",
        "Rektor faoliyatini tashkiliy qo'llab-quvvatlash.",
        False, False, False, 4,
    ),

    # ══════════════════════════════════════════════════════════════
    # 2. YOSHLAR MASALALARI VA MA'NAVIY-MA'RIFIY ISHLAR
    # ══════════════════════════════════════════════════════════════
    (
        'yoshlar_bolim', None, 'department', 'yoshlar-bilan-ishlash-bolimi',
        'yoshlar-manaviyat', 1,
        "Yoshlar bilan ishlash bo'limi",
        "Отдел работы с молодёжью",
        "Department of Youth Work",
        "Yoshlar tadbirlari, loyihalar va tashabbuslar.",
        False, False, False, 1,
    ),
    (
        'turar_joy', None, 'department', 'talabalar-turar-joyi',
        'yoshlar-manaviyat', 2,
        "Talabalar turar joyi", "Общежитие студентов", "Student Dormitory",
        "Yotoqxona va talabalarning yashash sharoitlari.",
        False, False, False, 2,
    ),
    (
        'psixolog', None, 'other', 'psixolog',
        'yoshlar-manaviyat', 3,
        "Psixolog", "Психолог", "Psychologist",
        "Psixologik maslahat va qo'llab-quvvatlash.",
        False, False, False, 3,
    ),
    (
        'sport_klubi', None, 'other', 'sport-klubi',
        'yoshlar-manaviyat', 4,
        "Sport klubi", "Спортивный клуб", "Sports Club",
        "Sport tadbirlari, musobaqalar va klub hayoti.",
        False, False, False, 4,
    ),

    # ══════════════════════════════════════════════════════════════
    # 3. O'QUV ISHLARI BO'YICHA
    # ══════════════════════════════════════════════════════════════
    (
        'oquv_uslub', None, 'department', 'oquv-uslubiy-bolim',
        'talim-bloki', 1,
        "O'quv-uslubiy bo'lim",
        "Учебно-методический отдел",
        "Academic-Methodological Department",
        "Dasturlar, metodik ta'minot va o'quv hujjatlari.",
        False, False, False, 1,
    ),
    (
        'raqamli', None, 'department', 'raqamli-talim-texnologiyalari-markazi',
        'talim-bloki', 2,
        "Raqamli ta'lim texnologiyalari markazi",
        "Центр цифровых образовательных технологий",
        "Centre for Digital Educational Technologies",
        "Raqamli platformalar, LMS va ta'lim IT yechimlari.",
        False, False, False, 2,
    ),
    (
        'sport_parasport', None, 'department', 'sport-va-parasport-turlari',
        'talim-bloki', 3,
        "Sport va parasport turlari",
        "Виды спорта и параспорта",
        "Sports and Para-Sports",
        "Sport va parasport ta'lim yo'nalishlari.",
        False, False, False, 3,
    ),

    # ══════════════════════════════════════════════════════════════
    # 4. ILMIY ISHLAR VA INNOVATSIYALAR
    # ══════════════════════════════════════════════════════════════
    (
        'ilmiy_tadq', None, 'department', 'ilmiy-tadqiqotlar',
        'ilmiy-xalqaro', 1,
        "Ilmiy tadqiqotlar",
        "Научные исследования",
        "Scientific Research",
        "Ilmiy loyihalar, grantlar va nashrlar.",
        False, False, False, 1,
    ),
    (
        'xalq_hamkor', None, 'department', 'xalqaro-hamkorlik',
        'ilmiy-xalqaro', 2,
        "Xalqaro hamkorlik",
        "Международное сотрудничество",
        "International Cooperation",
        "Xalqaro aloqalar, hamkorlar va akademik mobillik.",
        False, False, False, 2,
    ),
    (
        'iqtidor', None, 'department', 'iqtidorli-talabalar-ilmiy-faoliyati',
        'ilmiy-xalqaro', 3,
        "Iqtidorli talabalarning ilmiy faoliyati",
        "Научная деятельность одарённых студентов",
        "Research Activity of Talented Students",
        "Talabalar ilmiy ishlari va startap tashabbuslari.",
        False, False, False, 3,
    ),

    # ══════════════════════════════════════════════════════════════
    # 5. AKADEMIYA HUZURIDAGI TASHKILOTLAR
    # ══════════════════════════════════════════════════════════════
    (
        'malaka_inst', None, 'institute', 'malaka-oshirish-instituti',
        'akademiya-tashkilotlar', 1,
        "Jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish instituti",
        "Институт переподготовки и повышения квалификации специалистов по физической культуре и спорту",
        "Institute for Retraining and Advanced Training of Physical Culture and Sports Specialists",
        "Nukus, Samarqand va Farg'ona filiallari bilan.",
        False, False, False, 1,
    ),
    (
        'jt_inst', None, 'institute', 'jismoniy-tarbiya-ilmiy-instituti',
        'akademiya-tashkilotlar', 2,
        "Jismoniy tarbiya va sport ilmiy-tadqiqot instituti",
        "Научно-исследовательский институт физической культуры и спорта",
        "Research Institute of Physical Culture and Sports",
        "Sport fanlari bo'yicha ilmiy tadqiqotlar.",
        False, False, False, 2,
    ),
    (
        'sport_markaz', None, 'institute', 'davlat-sport-ilmiy-amaliy-markazi',
        'akademiya-tashkilotlar', 3,
        "Davlat sport ilmiy-amaliy markazi",
        "Государственный научно-практический центр спорта",
        "State Sports Scientific and Practical Centre",
        "Sport tibbiyoti va ilmiy-amaliy xizmatlar.",
        False, False, False, 3,
    ),
    (
        'tarix_markaz', None, 'institute', 'ozbekiston-tarixi-xorijiy-tillar-markazi',
        'akademiya-tashkilotlar', 4,
        "O'zbekiston tarixi va xorijiy tillarni o'qitish markazi",
        "Центр преподавания истории Узбекистана и иностранных языков",
        "Centre for Teaching History of Uzbekistan and Foreign Languages",
        "Tarix va xorijiy tillar bo'yicha ta'lim.",
        False, False, False, 4,
    ),
    (
        'kutubxona', None, 'institute', 'axborot-kutubxona-markazi',
        'akademiya-tashkilotlar', 5,
        "Axborot-kutubxona markazi",
        "Информационно-библиотечный центр",
        "Information and Library Centre",
        "Kutubxona, elektron resurslar va o'quv adabiyotlar.",
        False, False, False, 5,
    ),

    # ══════════════════════════════════════════════════════════════
    # 6. MARKAZ VA BO'LIMLAR (13 ta)
    # ══════════════════════════════════════════════════════════════
    (
        'reja_moliya', None, 'department', 'reja-moliya-sektori',
        'markaz-bolimlar', 1,
        "Reja-moliya sektori", "Планово-финансовый сектор", "Planning and Finance Sector",
        "Budjet rejalashtirish va moliyaviy boshqaruv.",
        False, False, False, 1,
    ),
    (
        'buxgalteriya', None, 'department', 'buxgalteriya',
        'markaz-bolimlar', 2,
        "Buxgalteriya", "Бухгалтерия", "Accounting Department",
        "Hisob-kitob, moliyaviy hisobot va to'lovlar.",
        False, False, False, 2,
    ),
    (
        'kadrlar', None, 'department', 'kadrlar-bolimi',
        'markaz-bolimlar', 3,
        "Kadrlar bo'limi", "Отдел кадров", "Human Resources Department",
        "Kadrlar ishlari va mehnat munosabatlari.",
        False, False, False, 3,
    ),
    (
        'yuriskonsult', None, 'other', 'yuriskonsult',
        'markaz-bolimlar', 4,
        "Yuriskonsult", "Юрисконсульт", "Legal Counsel",
        "Huquqiy maslahat va hujjatlar ekspertizasi.",
        False, False, False, 4,
    ),
    (
        'devxona', None, 'department', 'devxona-va-arxiv',
        'markaz-bolimlar', 5,
        "Devxona va arxiv", "Канцелярия и архив", "Office and Archive",
        "Hujjatlar aylanishi va arxiv yuritish.",
        False, False, False, 5,
    ),
    (
        'xavfsizlik', None, 'department', 'xavfsizlik-mudofaa-bolimi',
        'markaz-bolimlar', 6,
        "Xavfsizlik va mudofaa bo'limi",
        "Отдел безопасности и гражданской обороны",
        "Security and Civil Defence Department",
        "Xavfsizlik tartibi va favqulodda holatlarga tayyorgarlik.",
        False, False, False, 6,
    ),
    (
        'at_bolim', None, 'department', 'axborot-texnologiyalari-bolimi',
        'markaz-bolimlar', 7,
        "Axborot texnologiyalari bo'limi",
        "Отдел информационных технологий",
        "Information Technologies Department",
        "Kompyuter va tarmoq infratuzilmasi, kiberxavfsizlik.",
        False, False, False, 7,
    ),
    (
        'moddiy_tex', None, 'department', 'moddiy-texnik-taminot-bolimi',
        'markaz-bolimlar', 8,
        "Moddiy-texnik ta'minot bo'limi",
        "Отдел материально-технического обеспечения",
        "Material and Technical Supply Department",
        "Xarid jarayonlari va ombor xo'jaligi.",
        False, False, False, 8,
    ),
    (
        'xojalik', None, 'department', 'xojalik-bolimi',
        'markaz-bolimlar', 9,
        "Xo'jalik bo'limi", "Хозяйственный отдел", "Facilities Department",
        "Binolar texnik xizmati va kommunal ta'minot.",
        False, False, False, 9,
    ),
    (
        'press', None, 'other', 'press-xizmat',
        'markaz-bolimlar', 10,
        "Press-xizmat", "Пресс-служба", "Press Service",
        "OAV bilan ishlash va rasmiy axborot siyosati.",
        False, False, False, 10,
    ),
    (
        'ichki_nazorat', None, 'department', 'ichki-nazorat-bolimi',
        'markaz-bolimlar', 11,
        "Ichki nazorat bo'limi",
        "Отдел внутреннего контроля",
        "Internal Control Department",
        "Audit, moliyaviy intizom va qonun talablariga rioya.",
        False, False, False, 11,
    ),
    (
        'sifat_nazorat', None, 'department', 'talim-sifatini-nazorat-bolimi',
        'markaz-bolimlar', 12,
        "Ta'lim sifatini nazorat qilish bo'limi",
        "Отдел контроля качества образования",
        "Educational Quality Control Department",
        "Ta'lim sifati, monitoring va akkreditatsiya.",
        False, False, False, 12,
    ),
    (
        'sport_inshoot', None, 'department', 'sport-inshootlari-bolimi',
        'markaz-bolimlar', 13,
        "Sport inshootlari bo'limi",
        "Отдел спортивных сооружений",
        "Sports Facilities Department",
        "Stadion, sport zallari, basseyn va boshqa obyektlar.",
        False, False, False, 13,
    ),
]


class Command(BaseCommand):
    help = "Tashkiliy tuzilmani seed qiladi (eski ma'lumotlar o'chiriladi)"

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
            self.stdout.write(f"  [+] {title_uz[:60]}")

        self.stdout.write(self.style.SUCCESS(f"\nJami: {len(NODES)} ta tugun yaratildi."))
