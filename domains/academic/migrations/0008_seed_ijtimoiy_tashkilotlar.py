from django.db import migrations


IJTIMOIY_TASHKILOTLAR = [
    {
        'type': 'kafedra',
        'slug': 'xotin-qizlar-qomitasi',
        'name_uz': "Xotin-qizlar qo'mitasi",
        'name_ru': 'Комитет женщин',
        'name_en': "Women's Committee",
        'description_uz': (
            "Akademiyaning Xotin-qizlar qo'mitasi ayol xodimlar va talabalarning "
            "ijtimoiy himoyasi, madaniy-ma'rifiy faoliyati hamda kasb-kor rivojlanishini "
            "qo'llab-quvvatlash maqsadida faoliyat yuritadi."
        ),
        'description_ru': (
            "Комитет женщин Академии осуществляет деятельность в целях социальной защиты "
            "женщин-сотрудников и студенток, поддержки культурно-просветительской деятельности "
            "и профессионального развития."
        ),
        'description_en': (
            "The Women's Committee of the Academy operates to support the social protection "
            "of female employees and students, cultural and educational activities, "
            "and professional development."
        ),
        'order': 10,
        'is_active': True,
    },
    {
        'type': 'kafedra',
        'slug': 'yoshlar-ittifoqi',
        'name_uz': "Yoshlar ittifoqi",
        'name_ru': 'Союз молодёжи',
        'name_en': "Youth Union",
        'description_uz': (
            "Akademiyaning Yoshlar ittifoqi talaba yoshlarning ijtimoiy faolligini oshirish, "
            "sport va madaniy-ommaviy tadbirlarni tashkil etish, hamda yoshlarning "
            "vatanparvarlik ruhini shakllantirish yo'lida faoliyat olib boradi."
        ),
        'description_ru': (
            "Союз молодёжи Академии ведёт работу по повышению социальной активности "
            "студентов, организации спортивных и культурно-массовых мероприятий, "
            "а также формированию патриотического духа молодёжи."
        ),
        'description_en': (
            "The Youth Union of the Academy works to increase the social activity of students, "
            "organize sports and cultural events, and foster a spirit of patriotism among youth."
        ),
        'order': 11,
        'is_active': True,
    },
    {
        'type': 'kafedra',
        'slug': 'kasaba-uyushmasi',
        'name_uz': "Kasaba uyushmasi",
        'name_ru': 'Профсоюз',
        'name_en': "Trade Union",
        'description_uz': (
            "Akademiyaning Kasaba uyushmasi xodimlar va talabalarning mehnat huquqlari, "
            "ijtimoiy kafolatlari va dam olish sharoitlarini himoya qilish maqsadida "
            "faoliyat yuritadi."
        ),
        'description_ru': (
            "Профсоюз Академии осуществляет деятельность по защите трудовых прав, "
            "социальных гарантий и условий отдыха сотрудников и студентов."
        ),
        'description_en': (
            "The Trade Union of the Academy operates to protect the labor rights, "
            "social guarantees, and recreational conditions of employees and students."
        ),
        'order': 12,
        'is_active': True,
    },
]


def seed(apps, schema_editor):
    FakultetKafedra = apps.get_model('academic', 'FakultetKafedra')
    for data in IJTIMOIY_TASHKILOTLAR:
        FakultetKafedra.objects.update_or_create(
            slug=data['slug'],
            defaults={k: v for k, v in data.items() if k != 'slug'},
        )


def unseed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0007_seed_academy_stats_detail'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
