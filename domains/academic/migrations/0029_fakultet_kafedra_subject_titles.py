from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0028_fakultet_kafedra_goals_functions'),
    ]

    operations = [
        migrations.AddField(
            model_name='fakultetkafedra',
            name='sport_types_title_uz',
            field=models.CharField(blank=True, help_text="Bo'sh qoldirilsa standart matn ishlatiladi", max_length=200, verbose_name='Sport turlari — sarlavha (Uz)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='sport_types_title_ru',
            field=models.CharField(blank=True, max_length=200, verbose_name='Sport turlari — sarlavha (Ru)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='sport_types_title_en',
            field=models.CharField(blank=True, max_length=200, verbose_name='Sport turlari — sarlavha (En)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='bachelor_subjects_title_uz',
            field=models.CharField(blank=True, help_text="Bo'sh qoldirilsa standart matn ishlatiladi", max_length=200, verbose_name='Bakalavr — sarlavha (Uz)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='bachelor_subjects_title_ru',
            field=models.CharField(blank=True, max_length=200, verbose_name='Bakalavr — sarlavha (Ru)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='bachelor_subjects_title_en',
            field=models.CharField(blank=True, max_length=200, verbose_name='Bakalavr — sarlavha (En)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='master_subjects_title_uz',
            field=models.CharField(blank=True, help_text="Bo'sh qoldirilsa standart matn ishlatiladi", max_length=200, verbose_name='Magistratura — sarlavha (Uz)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='master_subjects_title_ru',
            field=models.CharField(blank=True, max_length=200, verbose_name='Magistratura — sarlavha (Ru)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='master_subjects_title_en',
            field=models.CharField(blank=True, max_length=200, verbose_name='Magistratura — sarlavha (En)'),
        ),
    ]
