from django.db import migrations, models
from django.utils.text import slugify


# NavbarSubItem da bor sluglar — name_uz → slug
NAVBAR_SLUG_MAP = {
    "Akademiya kengashi":                                          "academy-council",
    "Talabalar turar joyi":                                        "dormitory",
    "Sport va parasport turlari fakulteti":                        "faculties",
    "Xalqaro hamkorlik bo'limi":                                   "international-dept",
    "Iqtidorli talabalarning ilmiy tadqiqot faoliyatini tashkil etish sektori": "gifted-students",
    "Rektor":                                                      "rectorate",
    "Markazlar":                                                   "centers",
}


def assign_slugs(apps, schema_editor):
    OrgNode = apps.get_model('pages', 'OrgNode')
    used = set()

    for node in OrgNode.objects.all().order_by('order'):
        # NavbarSubItem da mos slug bormi?
        slug = NAVBAR_SLUG_MAP.get(node.name_uz)

        if not slug or slug in used:
            # Avtomatik slug
            base = slugify(node.name_uz) or f'node-{node.id}'
            slug = base
            n = 1
            while slug in used:
                slug = f'{base}-{n}'
                n += 1

        node.slug = slug
        node.save(update_fields=['slug'])
        used.add(slug)


def remove_slugs(apps, schema_editor):
    OrgNode = apps.get_model('pages', 'OrgNode')
    OrgNode.objects.all().update(slug='')


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_seed_org_structure'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgnode',
            name='slug',
            field=models.SlugField(blank=True, max_length=220, unique=False, verbose_name='Slug'),
        ),
        migrations.RunPython(assign_slugs, remove_slugs),
        migrations.AlterField(
            model_name='orgnode',
            name='slug',
            field=models.SlugField(max_length=220, unique=True, verbose_name='Slug'),
        ),
    ]
