from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0019_alter_olimpiyachempion_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='degree_uz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ilmiy daraja (Uz)'),
        ),
        migrations.AddField(
            model_name='person',
            name='degree_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ilmiy daraja (Ru)'),
        ),
        migrations.AddField(
            model_name='person',
            name='degree_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ilmiy daraja (En)'),
        ),
    ]
