from django.db import migrations

STUDENTS = [
    {
        'order': 1,
        'student_name': "Isoyeva Nigina O'tkirovna",
        'dissertation_topic_uz': "Jismoniy imkoniyati cheklangan talabalarni para yengil atletikaning uzunlikka sakrash turlariga o'rgatish",
        'supervisor_name': "Sobirova Laylo Baxramovna",
        'supervisor_info_uz': "p.f.d (DsC), dotsent",
    },
    {
        'order': 2,
        'student_name': "Asqarova Sabina Shavkat qizi",
        'dissertation_topic_uz': "Para dzyudochilarni sport musobaqalariga tayyorlash mexanizmlari",
        'supervisor_name': "Atajanov San'a Farhatovich",
        'supervisor_info_uz': "dotsent",
    },
    {
        'order': 3,
        'student_name': "Suyunova Gulshoda Odil qizi",
        'dissertation_topic_uz': "Malakali para dzyudochilarning funksional tayyorgarligini takomillashtirish metodikasi",
        'supervisor_name': "Sobirova Laylo Baxramovna",
        'supervisor_info_uz': "p.f.d (DsC), dotsent",
    },
    {
        'order': 4,
        'student_name': "Tagiyeva Muxlisa Botir qizi",
        'dissertation_topic_uz': "Para o'q otuvchilarni texnik-taktik tayyorgarligini takomillashtirish",
        'supervisor_name': "Sobirova Laylo Baxramovna",
        'supervisor_info_uz': "p.f.d (DsC), dotsent",
    },
    {
        'order': 5,
        'student_name': "Norpo'latov Eldorbek Erkinovich",
        'dissertation_topic_uz': "Paradzyudochilarni kuch sifatini rivojlantirishda maxsus trenajorlardan foydalanish",
        'supervisor_name': "Olimov Muxsin Sotiboldiyevich",
        'supervisor_info_uz': "p.f.d (DsC), professor",
    },
]


def seed(apps, schema_editor):
    MagistrGroup   = apps.get_model('students', 'MagistrGroup')
    MagistrStudent = apps.get_model('students', 'MagistrStudent')

    group, _ = MagistrGroup.objects.get_or_create(
        specialty_code='71010301',
        year='2025-2026',
        education_lang='uz',
        defaults=dict(
            specialty_name_uz="Adaptiv jismoniy tarbiya va sport",
            order=1,
            is_active=True,
        ),
    )

    for s in STUDENTS:
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
        ('students', '0009_magistrgroup_magistrstudent'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
