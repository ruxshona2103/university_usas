from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0005_alter_ilmiyfaoliyat_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ilmiyfaoliyat',
            name='title_uz',
            field=models.CharField(default='', max_length=500, verbose_name='Sarlavha (Uz)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ilmiyfaoliyat',
            name='title_ru',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sarlavha (Ru)'),
        ),
        migrations.AddField(
            model_name='ilmiyfaoliyat',
            name='title_en',
            field=models.CharField(blank=True, max_length=500, verbose_name='Sarlavha (En)'),
        ),
    ]
