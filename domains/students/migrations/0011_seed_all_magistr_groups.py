from django.db import migrations

GROUPS = [
    {
        'specialty_code': '71010201',
        'specialty_name_uz': "Sport faoliyati (dzyudo)",
        'education_lang': 'uz',
        'year': '2025-2026',
        'order': 2,
        'students': [
            {
                'order': 1,
                'student_name': "Hamroyev Jasurbek Musurmonovich",
                'dissertation_topic_uz': "Dzyudochilarni kuchli-tezkor sifatlarini rivojlantirishda innovatsion usullardan foydalanish",
                'supervisor_name': "Olimov Muxsin Sotiboldiyevich",
                'supervisor_info_uz': "p.f.d (DsC), professor",
            },
            {
                'order': 2,
                'student_name': "Aliyeva Dildora Baxtiyorovna",
                'dissertation_topic_uz': "Yosh dzyudochilarni ruhiy-irodaviy tayyorlash metodikasi",
                'supervisor_name': "Atajanov San'a Farhatovich",
                'supervisor_info_uz': "dotsent",
            },
        ],
    },
    {
        'specialty_code': '71010201',
        'specialty_name_uz': "Sport faoliyati (taekvondo WTF)",
        'education_lang': 'uz',
        'year': '2025-2026',
        'order': 3,
        'students': [
            {
                'order': 1,
                'student_name': "Yusupov Sherzod Abdullayevich",
                'dissertation_topic_uz': "Taekvondo WTF bo'yicha musobaqaga tayyorlashda texnik-taktik tayyorgarlikni takomillashtirish",
                'supervisor_name': "Olimov Muxsin Sotiboldiyevich",
                'supervisor_info_uz': "p.f.d (DsC), professor",
            },
        ],
    },
    {
        'specialty_code': '71010201',
        'specialty_name_uz': "Sport faoliyati (boks)",
        'education_lang': 'uz',
        'year': '2025-2026',
        'order': 4,
        'students': [
            {
                'order': 1,
                'student_name': "Nazarov Dilshod Erkinovich",
                'dissertation_topic_uz': "Bokschilarda zarbalar texnikasini takomillashtirish metodikasi",
                'supervisor_name': "Atajanov San'a Farhatovich",
                'supervisor_info_uz': "dotsent",
            },
        ],
    },
    {
        'specialty_code': '71010201',
        'specialty_name_uz': "Sport faoliyati (eshkak eshish)",
        'education_lang': 'uz',
        'year': '2025-2026',
        'order': 5,
        'students': [
            {
                'order': 1,
                'student_name': "Toshmatov Ulugbek Nematjonovich",
                'dissertation_topic_uz': "Eshkak eshish sportida chidamlilikni rivojlantirish metodikasi",
                'supervisor_name': "Olimov Muxsin Sotiboldiyevich",
                'supervisor_info_uz': "p.f.d (DsC), professor",
            },
        ],
    },
    {
        'specialty_code': '70410801',
        'specialty_name_uz': "Menejment",
        'education_lang': 'uz',
        'year': '2025-2026',
        'order': 6,
        'students': [
            {
                'order': 1,
                'student_name': "Rahimov Bobur Alixonovich",
                'dissertation_topic_uz': "Sport tashkilotlarida menejmentni takomillashtirish yo'llari",
                'supervisor_name': "Xolmatov Ilhom Abdullayevich",
                'supervisor_info_uz': "i.f.n, dotsent",
            },
            {
                'order': 2,
                'student_name': "Karimova Nilufar Sobirovna",
                'dissertation_topic_uz': "Jismoniy tarbiya va sport sohasida kadrlar boshqaruvini optimallashtirish",
                'supervisor_name': "Xolmatov Ilhom Abdullayevich",
                'supervisor_info_uz': "i.f.n, dotsent",
            },
            {
                'order': 3,
                'student_name': "Qodirov Firdavs Baxtiyorovich",
                'dissertation_topic_uz': "Sport muassasalarida moliyaviy resurslarni boshqarish samaradorligi",
                'supervisor_name': "Xolmatov Ilhom Abdullayevich",
                'supervisor_info_uz': "i.f.n, dotsent",
            },
            {
                'order': 4,
                'student_name': "Normatova Zulfiya Hamidovna",
                'dissertation_topic_uz': "Sport sohasida xizmat ko'rsatish sifatini boshqarish",
                'supervisor_name': "Xolmatov Ilhom Abdullayevich",
                'supervisor_info_uz': "i.f.n, dotsent",
            },
            {
                'order': 5,
                'student_name': "Mirzayev Jasur Toxirovich",
                'dissertation_topic_uz': "Olimpiya zahirasini tayyorlash tizimida boshqaruv samaradorligi",
                'supervisor_name': "Xolmatov Ilhom Abdullayevich",
                'supervisor_info_uz': "i.f.n, dotsent",
            },
        ],
    },
    {
        'specialty_code': '70411201',
        'specialty_name_uz': "Marketing",
        'education_lang': 'uz',
        'year': '2025-2026',
        'order': 7,
        'students': [
            {
                'order': 1,
                'student_name': "Ergasheva Mohira Sherzodovna",
                'dissertation_topic_uz': "Sport sohasida marketing strategiyalarini ishlab chiqish va tadbiq etish",
                'supervisor_name': "Xolmatov Ilhom Abdullayevich",
                'supervisor_info_uz': "i.f.n, dotsent",
            },
        ],
    },
    {
        'specialty_code': '70310301',
        'specialty_name_uz': "Psixologiya",
        'education_lang': 'uz',
        'year': '2025-2026',
        'order': 8,
        'students': [
            {
                'order': 1,
                'student_name': "Tursunova Kamola Baxtiyorovna",
                'dissertation_topic_uz': "Sportchilarda ruhiy chidamlilikni shakllantirish psixologik mexanizmlari",
                'supervisor_name': "Sobirova Laylo Baxramovna",
                'supervisor_info_uz': "p.f.d (DsC), dotsent",
            },
            {
                'order': 2,
                'student_name': "Xasanov Sardor Muzaffarovich",
                'dissertation_topic_uz': "Yuqori mahoratli sportchilarning motivatsion sohasi xususiyatlari",
                'supervisor_name': "Sobirova Laylo Baxramovna",
                'supervisor_info_uz': "p.f.d (DsC), dotsent",
            },
            {
                'order': 3,
                'student_name': "Begmatova Dilnoza Anvarovna",
                'dissertation_topic_uz': "Bolalar va o'smirlar sportida psixologik yordam ko'rsatish tizimi",
                'supervisor_name': "Sobirova Laylo Baxramovna",
                'supervisor_info_uz': "p.f.d (DsC), dotsent",
            },
            {
                'order': 4,
                'student_name': "Umarov Zafar Qodiraliyevich",
                'dissertation_topic_uz': "Sport jamoalarida psixologik iqlimni optimallashtirishning amaliy usullari",
                'supervisor_name': "Sobirova Laylo Baxramovna",
                'supervisor_info_uz': "p.f.d (DsC), dotsent",
            },
        ],
    },
]


def seed(apps, schema_editor):
    MagistrGroup   = apps.get_model('students', 'MagistrGroup')
    MagistrStudent = apps.get_model('students', 'MagistrStudent')

    for g in GROUPS:
        students = g['students']
        group, _ = MagistrGroup.objects.get_or_create(
            specialty_code=g['specialty_code'],
            specialty_name_uz=g['specialty_name_uz'],
            year=g['year'],
            defaults=dict(
                education_lang=g['education_lang'],
                order=g['order'],
                is_active=True,
            ),
        )
        for s in students:
            MagistrStudent.objects.get_or_create(
                group=group,
                student_name=s['student_name'],
                defaults=dict(
                    order=s['order'],
                    dissertation_topic_uz=s['dissertation_topic_uz'],
                    supervisor_name=s['supervisor_name'],
                    supervisor_info_uz=s['supervisor_info_uz'],
                ),
            )


def unseed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0010_seed_parasport_magistr'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
