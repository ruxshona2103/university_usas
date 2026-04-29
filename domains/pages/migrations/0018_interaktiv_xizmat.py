import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_add_about_academy_image_gallery'),
    ]

    operations = [
        migrations.CreateModel(
            name='InteraktivXizmat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
                ('icon_class', models.CharField(blank=True, max_length=100, verbose_name='Icon (CSS class yoki SVG nomi)')),
                ('title_uz', models.CharField(max_length=200, verbose_name='Nomi (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=200, verbose_name='Nomi (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=200, verbose_name='Nomi (En)')),
                ('description_uz', models.TextField(blank=True, verbose_name='Tavsif (Uz)')),
                ('description_ru', models.TextField(blank=True, verbose_name='Tavsif (Ru)')),
                ('description_en', models.TextField(blank=True, verbose_name='Tavsif (En)')),
                ('link', models.URLField(blank=True, verbose_name='Havola (URL)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faolmi?')),
            ],
            options={
                'verbose_name': 'Interaktiv xizmat',
                'verbose_name_plural': 'Interaktiv xizmatlar',
                'db_table': 'pages_interaktiv_xizmat',
                'ordering': ['order'],
            },
        ),
    ]
