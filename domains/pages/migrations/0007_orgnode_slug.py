from django.db import migrations, models
from django.utils.text import slugify


def assign_slugs(apps, schema_editor):
    OrgNode = apps.get_model('pages', 'OrgNode')
    used = set()
    for node in OrgNode.objects.all().order_by('order'):
        base = slugify(node.name_uz) or f'node-{str(node.id)[:8]}'
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
            field=models.SlugField(blank=True, max_length=220, verbose_name='Slug'),
        ),
        migrations.RunPython(assign_slugs, remove_slugs),
        migrations.AlterField(
            model_name='orgnode',
            name='slug',
            field=models.SlugField(blank=True, max_length=220, unique=True, verbose_name='Slug'),
        ),
    ]
