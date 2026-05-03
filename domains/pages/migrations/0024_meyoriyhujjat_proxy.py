from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0023_orgnode_image_ru_en'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeyoriyHujjat',
            fields=[],
            options={
                'verbose_name': "Me'yoriy hujjat",
                'verbose_name_plural': "Me'yoriy hujjatlar",
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('pages.linkblock',),
        ),
    ]
