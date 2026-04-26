from django.db import migrations


NODES = [
    # (temp_key, parent_key, node_type, name_uz, is_starred, is_double_starred, is_highlighted, order)
    ('kuzatuv',      None,          'governing',  "Kuzatuv kengashi",                                                                                   False, False, False, 0),
    ('rektor',       'kuzatuv',     'rector',     "Rektor",                                                                                              False, False, False, 0),

    # Akademiya kengashi (chap tomon)
    ('ak_kengash',   'rektor',      'governing',  "Akademiya kengashi",                                                                                  False, False, False, 1),
    ('birinchi_pro', 'ak_kengash',  'prorektor',  "Yoshlar masalalari va ma'naviy-ma'rifiy ishlar bo'yicha birinchi prorektor",                           False, False, False, 1),
    ('yoshlar_bolim','birinchi_pro','department',  "Yoshlar bilan ishlash, ma'naviyat va ma'rifat bo'limi",                                               False, False, False, 1),
    ('turar_joy',    'birinchi_pro','department',  "Talabalar turar joyi",                                                                                False, False, False, 2),
    ('psixolog',     'birinchi_pro','other',       "Psixolog",                                                                                            False, False, False, 3),
    ('sport_klubi',  'birinchi_pro','other',       "Sport klubi",                                                                                         False, True,  False, 4),

    # Xalqaro maslahatchi
    ('xalq_mash',    'rektor',      'other',       "Xalqaro maslahatchi",                                                                                 False, False, False, 2),
    ('oquv_pro',     'xalq_mash',   'prorektor',   "O'quv ishlari bo'yicha prorektor",                                                                    False, False, False, 1),
    ('oquv_uslub',   'oquv_pro',    'department',  "O'quv-uslubiy bo'lim",                                                                                False, False, False, 1),
    ('raqamli',      'oquv_pro',    'department',  "Raqamli ta'lim texnologiyalari markazi",                                                              False, False, False, 2),
    ('parasport_fak','oquv_pro',    'department',  "Sport va parasport turlari fakulteti",                                                                 False, False, False, 3),

    # Ilmiy ishlar prorektor
    ('ilmiy_pro',    'rektor',      'prorektor',   "Ilmiy ishlar va innovatsiyalar bo'yicha prorektor",                                                    False, False, False, 3),
    ('ilmiy_sektor', 'ilmiy_pro',   'department',  "Ilmiy tadqiqotlar, innovatsiyalar va ilmiy-pedagogik kadrlar tayyorlash sektori",                      False, False, False, 1),
    ('xalq_hamkor',  'ilmiy_pro',   'department',  "Xalqaro hamkorlik bo'limi",                                                                           False, False, False, 2),
    ('iqtidor',      'ilmiy_pro',   'department',  "Iqtidorli talabalarning ilmiy tadqiqot faoliyatini tashkil etish sektori",                             False, False, False, 3),

    # Rektorga bevosita bo'ysunuvchi institutlar
    ('malaka_inst',  'rektor',      'institute',   "Jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish instituti hamda uning Nukus, Samarqand va Farg'ona filiallari", True, False, False, 4),
    ('jt_inst',      'rektor',      'institute',   "Jismoniy tarbiya va sport ilmiy-tadqiqotlar instituti",                                                True, False, True,  5),
    ('tibbiyot',     'rektor',      'institute',   "Davlat sport tibbiyoti ilmiy amaliy markazi",                                                          True, False, False, 6),
    ('tarix_markaz', 'rektor',      'institute',   "O'zbekiston tarixi va xorijiy tillarni o'qitish markazi",                                              False, False, False, 7),
    ('kutubxona',    'rektor',      'institute',   "Axborot kutubxona markazi",                                                                            False, False, False, 8),

    # Reja-moliya sektori
    ('reja_moliya',  'rektor',      'department',  "Reja-moliya sektori",                                                                                  False, False, False, 9),
    ('buxgalteriya', 'reja_moliya', 'department',  "Buxgalteriya",                                                                                         False, False, False, 1),
    ('fuqaro_mehnat','reja_moliya', 'department',  "Fuqaro va mehnat muhofazasi bo'limi",                                                                   False, False, False, 2),
    ('texnik_vosita','reja_moliya', 'department',  "O'qitishning texnik vositalari bo'limi",                                                                False, False, False, 3),
    ('bosh_muh',     'reja_moliya', 'other',       "Bosh muhandis",                                                                                         False, False, False, 4),
    ('marketing',    'reja_moliya', 'department',  "Marketing va talabalar amaliyoti bo'limi",                                                              False, False, False, 5),

    # Rektor yordamchisi
    ('rektor_yord',  'rektor',      'prorektor',   "Rektor yordamchisi",                                                                                    False, False, False, 10),
    ('talim_nazorat','rektor_yord', 'department',  "Ta'lim sifatini nazorat qilish bo'limi",                                                                False, False, False, 1),
    ('murojaat',     'rektor_yord', 'department',  "Jismoniy va yuridik shaxslarning murojaatlari bilan ishlash, nazorat va monitoring sektori",             False, False, False, 2),
    ('komplaens',    'rektor_yord', 'department',  "Korrupsiyaga qarshi kurashish \"Komplaens-nazorat\" tizimini boshqarish bo'limi",                        False, False, False, 3),
    ('matbuot',      'rektor_yord', 'other',       "Matbuot kotibi",                                                                                         False, False, False, 4),
    ('xodimlar',     'rektor_yord', 'department',  "Xodimlar bo'limi",                                                                                       False, False, False, 5),
    ('devonxona',    'rektor_yord', 'department',  "Devonxona va arxiv",                                                                                      False, False, False, 6),
    ('yuriskonsult', 'rektor_yord', 'other',       "Yuriskonsult",                                                                                            False, False, False, 7),
    ('birinchi_bolim','rektor_yord','department',  "Birinchi bo'lim",                                                                                         False, False, False, 8),

    # Kafedralar
    ('kaf_yakka',    'rektor',      'kafedra',     "Yakkakurash va suv sporti turlari kafedrasi",                                                             False, False, False, 11),
    ('kaf_jamoaviy', 'rektor',      'kafedra',     "Sportning jamoaviy, texnik va murakkab turlari kafedrasi",                                                False, False, False, 12),
    ('kaf_parasport','rektor',      'kafedra',     "Parasport turlari kafedrasi",                                                                             False, False, False, 13),
    ('kaf_ijtimoiy', 'rektor',      'kafedra',     "Ijtimoiy-gumanitar, tibbiy-biologik fanlar kafedrasi",                                                    False, False, False, 14),
]


def seed(apps, schema_editor):
    OrgNode = apps.get_model('pages', 'OrgNode')
    if OrgNode.objects.exists():
        return
    created = {}
    for key, parent_key, node_type, name_uz, is_starred, is_double_starred, is_highlighted, order in NODES:
        parent = created.get(parent_key) if parent_key else None
        obj = OrgNode.objects.create(
            node_type=node_type,
            name_uz=name_uz,
            is_starred=is_starred,
            is_double_starred=is_double_starred,
            is_highlighted=is_highlighted,
            order=order,
            parent=parent,
        )
        created[key] = obj


def unseed(apps, schema_editor):
    OrgNode = apps.get_model('pages', 'OrgNode')
    OrgNode.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_org_node'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
