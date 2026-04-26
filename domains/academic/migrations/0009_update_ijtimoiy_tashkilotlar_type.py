from django.db import migrations

TASHKILOT_SLUGS = [
    'xotin-qizlar-qomitasi',
    'yoshlar-ittifoqi',
    'kasaba-uyushmasi',
]


def update_type(apps, schema_editor):
    FakultetKafedra = apps.get_model('academic', 'FakultetKafedra')
    FakultetKafedra.objects.filter(slug__in=TASHKILOT_SLUGS).update(type='tashkilot')


def revert_type(apps, schema_editor):
    FakultetKafedra = apps.get_model('academic', 'FakultetKafedra')
    FakultetKafedra.objects.filter(slug__in=TASHKILOT_SLUGS).update(type='kafedra')


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0008_seed_ijtimoiy_tashkilotlar'),
    ]

    operations = [
        migrations.RunPython(update_type, revert_type),
    ]
