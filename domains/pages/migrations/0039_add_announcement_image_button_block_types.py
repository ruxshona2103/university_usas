from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0038_alter_markaz_description_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentblock',
            name='block_type',
            field=models.CharField(
                choices=[
                    ('hero', 'Hero banner'),
                    ('rich-text', 'Matn (HTML)'),
                    ('stats', 'Statistikalar'),
                    ('gallery', 'Galereya'),
                    ('quote', 'Iqtibos'),
                    ('table', 'Jadval'),
                    ('timeline', "Vaqt chizig'i"),
                    ('announcement', "E'lon / Xabarnoma"),
                    ('image', 'Rasm (katta)'),
                    ('button-link', 'Tugma + Havola'),
                ],
                default='rich-text',
                max_length=20,
                verbose_name='Blok turi',
            ),
        ),
    ]
