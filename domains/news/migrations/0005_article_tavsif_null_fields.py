from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_add_likes_comments'),
    ]

    operations = [
        # tavsif fieldlari qo'shish
        migrations.AddField(
            model_name='article',
            name='tavsif_uz',
            field=models.TextField(blank=True, null=True, verbose_name='Tavsif (Uz)'),
        ),
        migrations.AddField(
            model_name='article',
            name='tavsif_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Tavsif (Ru)'),
        ),
        migrations.AddField(
            model_name='article',
            name='tavsif_en',
            field=models.TextField(blank=True, null=True, verbose_name='Tavsif (En)'),
        ),
        # title fieldlariga null=True qo'shish
        migrations.AlterField(
            model_name='article',
            name='title_uz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Sarlavha (Uz)'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Sarlavha (Ru)'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Sarlavha (En)'),
        ),
        # description fieldlariga null=True qo'shish
        migrations.AlterField(
            model_name='article',
            name='description_uz',
            field=models.TextField(blank=True, null=True, verbose_name='Batafsil (Uz)'),
        ),
        migrations.AlterField(
            model_name='article',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Batafsil (Ru)'),
        ),
        migrations.AlterField(
            model_name='article',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Batafsil (En)'),
        ),
    ]
