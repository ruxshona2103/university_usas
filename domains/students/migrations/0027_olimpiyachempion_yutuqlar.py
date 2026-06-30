from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0026_alter_psixologsection_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='olimpiyachempion',
            name='yutuqlar_uz',
            field=models.TextField(blank=True, verbose_name="Sovrinli o'rinlar (UZ)"),
        ),
        migrations.AddField(
            model_name='olimpiyachempion',
            name='yutuqlar_ru',
            field=models.TextField(blank=True, verbose_name="Sovrinli o'rinlar (RU)"),
        ),
        migrations.AddField(
            model_name='olimpiyachempion',
            name='yutuqlar_en',
            field=models.TextField(blank=True, verbose_name="Sovrinli o'rinlar (EN)"),
        ),
    ]
