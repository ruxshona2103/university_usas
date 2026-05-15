import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0031_navbarsubitem_subtitle'),
    ]

    operations = [
        migrations.CreateModel(
            name='KampusXizmati',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
                ('icon_class', models.CharField(blank=True, max_length=100, verbose_name='Icon nomi (lucide)')),
                ('title_uz', models.CharField(max_length=200, verbose_name='Sarlavha (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=200, verbose_name='Sarlavha (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=200, verbose_name='Sarlavha (En)')),
                ('link', models.CharField(blank=True, max_length=300, verbose_name='Havola (relative yoki URL)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faolmi?')),
            ],
            options={
                'verbose_name': 'Kampus xizmati',
                'verbose_name_plural': 'Kampus xizmatlari',
                'db_table': 'pages_kampus_xizmati',
                'ordering': ['order'],
            },
        ),
    ]
