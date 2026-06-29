from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0027_kafedra_xodim_lavozim_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='fakultetkafedra',
            name='goals_uz',
            field=models.TextField(blank=True, verbose_name='Maqsad va vazifalari (Uz)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='goals_ru',
            field=models.TextField(blank=True, verbose_name='Maqsad va vazifalari (Ru)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='goals_en',
            field=models.TextField(blank=True, verbose_name='Maqsad va vazifalari (En)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='functions_uz',
            field=models.TextField(blank=True, verbose_name='Funksiyalari (Uz)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='functions_ru',
            field=models.TextField(blank=True, verbose_name='Funksiyalari (Ru)'),
        ),
        migrations.AddField(
            model_name='fakultetkafedra',
            name='functions_en',
            field=models.TextField(blank=True, verbose_name='Funksiyalari (En)'),
        ),
    ]
