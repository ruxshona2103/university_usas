from django.db import migrations


FAKULTETLAR = [
    {
        'type': 'fakultet',
        'slug': 'sport-va-parasport-turlari-fakulteti',
        'name_uz': 'Sport va parasport turlari fakulteti',
        'name_ru': 'Факультет видов спорта и параспорта',
        'name_en': 'Faculty of Sports and Para-Sports',
        'order': 1,
    },
    {
        'type': 'kafedra',
        'slug': 'yakkakurash-va-suv-sport-turlari-kafedrasi',
        'name_uz': 'Yakkakurash va suv sport turlari kafedrasi',
        'name_ru': 'Кафедра единоборств и водных видов спорта',
        'name_en': 'Department of Wrestling and Aquatic Sports',
        'description_uz': (
            "O'zbekiston Respublikasi Prezidentining 2024-yil 28-maydagi PQ-197-son qarori bilan "
            "O'zbekiston davlat sport akademiyasi tashkil qilindi. Akademiyaning \"Yakkakurash va suv sport turlari\" "
            "kafedrasida 2025-yil 2-sentabrdan boshlab quyidagi sport turlari kafedra tarkibiga kiritildi.\n"
            "Kafedra professor-o'qituvchilari tomonidan o'quv qo'llanmalar va monografiyalar chop etilgan."
        ),
        'decree_info': "PQ-197-son, 2024-yil 28-may",
        'sport_types_uz': (
            "Dzyudo\nTaekvondo WT\nBoks\nEshkak eshish\nYengil atletika\n"
            "O'g'ir atletika\nYunon-rim kurash\nErkin kurash\nSuzish\n"
            "Velosport\nGimnastika\nKomondan otish\nQilichbozlik\nO'q otish"
        ),
        'bachelor_subjects_uz': (
            "Tayanch sport turlarini o'rgatish metodikasi (Suzish)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Sport va harakatli o'yinlar)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Yengil atletika)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Gimnastika)\n"
            "Taekvondo nazariyasi va uslubiyati\n"
            "Dzyudo nazariyasi va uslubiyati\n"
            "Boks nazariyasi va uslubiyati\n"
            "Eshkak eshish nazariyasi va uslubiyati\n"
            "Yengil atletika nazariyasi va uslubiyati\n"
            "O'g'ir atletika nazariyasi va uslubiyati\n"
            "Yunon-rim kurash nazariyasi va uslubiyati\n"
            "Erkin kurash nazariyasi va uslubiyati\n"
            "Suzish nazariyasi va uslubiyati\n"
            "Velosport nazariyasi va uslubiyati\n"
            "Gimnastika nazariyasi va uslubiyati\n"
            "Komondan otish nazariyasi va uslubiyati\n"
            "Qilichbozlik nazariyasi va uslubiyati\n"
            "O'q otish nazariyasi va uslubiyati"
        ),
        'master_subjects_uz': (
            "Sportda ilmiy tadqiqotlar\n"
            "Sportda saralash, modellashtirish va bashorat qilish\n"
            "Taekvondoda sportchilarni tayyorlashning ilmiy-uslubiy asoslari\n"
            "Boksda sportchilarni tayyorlashning ilmiy-uslubiy asoslari\n"
            "Dzyudoda sportchilarni tayyorlashning ilmiy-uslubiy asoslari\n"
            "Eshkak eshishda sportchilarni tayyorlashning ilmiy-uslubiy asoslari"
        ),
        'order': 2,
        'publications': [
            {
                'title_uz': "Yuqori malakali Dzyudochilarning ko'p yillik tayyorgarlik tizimini takomillashtirishning ilmiy-nazariy asoslari",
                'author': 'S.E. Qodirov',
                'pub_type': 'monograf',
                'order': 1,
            },
            {
                'title_uz': "Taekvondo nazariyasi va uslubiyati",
                'author': 'A.A. Nuritdinov',
                'pub_type': 'qollanma',
                'order': 2,
            },
            {
                'title_uz': "Yunon-rim kurashchilarda maxsus kuch tayyorgarligini takomillashtirish metodikasi",
                'author': 'J.A. Kubitdinov',
                'pub_type': 'monograf',
                'order': 3,
            },
        ],
    },
    {
        'type': 'kafedra',
        'slug': 'parasport-va-umumkasbiy-fanlar-kafedrasi',
        'name_uz': 'Parasport va umumkasbiy fanlar kafedrasi',
        'name_ru': 'Кафедра параспорта и общепрофессиональных дисциплин',
        'name_en': 'Department of Para-Sports and General Professional Subjects',
        'order': 3,
    },
]

KAFEDRA_STAFF_CATEGORY = {
    'slug': 'yakkakurash-kafedra-staff',
    'title_uz': 'Yakkakurash va suv sport turlari kafedrasi',
    'title_ru': 'Кафедра единоборств и водных видов спорта',
    'title_en': 'Wrestling and Aquatic Sports Department',
    'order': 50,
}

KAFEDRA_STAFF = [
    {
        'full_name_uz': 'Qodirov Sirojiddin Erkinboyevich',
        'title_uz': 'Kafedra mudiri',
        'position_uz': 'p.f.b.f.d. (PhD), professor',
        'email': 'qodirov.sirojiddin@list.ru',
        'is_head': True,
        'order': 1,
    },
    {
        'full_name_uz': "Nuritdinov Abrorjon Ahrorjon O'g'li",
        'title_uz': 'Dotsent',
        'position_uz': "XTSU 3-Dan qora belbog' sohibi",
        'email': 'abror.nuritdinov.1994@gmail.com',
        'is_head': False,
        'order': 2,
    },
    {
        'full_name_uz': 'Kubitdinov Jamshed Abduraxmonovich',
        'title_uz': 'Dotsent',
        'position_uz': 'p.f.b.f.d. (PhD)',
        'email': 'jamshedkubitdinov@gmail.com',
        'is_head': False,
        'order': 3,
    },
    {
        'full_name_uz': "Toirov Fazliddin Raximjon O'g'li",
        'title_uz': 'Dotsent',
        'position_uz': "Yengil atletika bo'yicha sport ustasi",
        'email': 'fazliddintoirov89@gmail.com',
        'is_head': False,
        'order': 4,
    },
    {
        'full_name_uz': "Suleymanov Muhammad Amin Erkin O'g'li",
        'title_uz': 'Dotsent',
        'position_uz': 'p.f.b.f.d. (PhD)',
        'email': 'sulejmanovmuhic@gmail.com',
        'is_head': False,
        'order': 5,
    },
]


def seed(apps, schema_editor):
    FakultetKafedra   = apps.get_model('academic', 'FakultetKafedra')
    KafedraPublication = apps.get_model('academic', 'KafedraPublication')
    PersonCategory    = apps.get_model('students', 'PersonCategory')
    Person            = apps.get_model('students', 'Person')

    for data in FAKULTETLAR:
        pubs = data.pop('publications', [])
        obj, _ = FakultetKafedra.objects.update_or_create(
            slug=data['slug'],
            defaults={k: v for k, v in data.items() if k != 'slug'},
        )
        obj.is_active = True
        obj.save()

        for p in pubs:
            KafedraPublication.objects.get_or_create(
                kafedra=obj,
                title_uz=p['title_uz'],
                defaults={
                    'author':   p['author'],
                    'pub_type': p['pub_type'],
                    'order':    p['order'],
                },
            )

    # Kafedra xodimlari
    cat, _ = PersonCategory.objects.get_or_create(
        slug=KAFEDRA_STAFF_CATEGORY['slug'],
        defaults={
            'title_uz': KAFEDRA_STAFF_CATEGORY['title_uz'],
            'title_ru': KAFEDRA_STAFF_CATEGORY['title_ru'],
            'title_en': KAFEDRA_STAFF_CATEGORY['title_en'],
            'order':    KAFEDRA_STAFF_CATEGORY['order'],
        },
    )
    for s in KAFEDRA_STAFF:
        Person.objects.get_or_create(
            category=cat,
            full_name_uz=s['full_name_uz'],
            defaults={
                'title_uz':    s['title_uz'],
                'position_uz': s['position_uz'],
                'email':       s['email'],
                'is_head':     s['is_head'],
                'order':       s['order'],
                'is_active':   True,
            },
        )


def unseed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_extend_fakultet_kafedra_and_publication'),
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
