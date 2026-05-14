import uuid
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models
import domains.pages.models.homepage_haqida


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0029_savoljavobcategory_savoljavob'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageHaqida',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description_uz', models.TextField(blank=True, verbose_name='Tavsif (Uz)')),
                ('description_ru', models.TextField(blank=True, verbose_name='Tavsif (Ru)')),
                ('description_en', models.TextField(blank=True, verbose_name='Tavsif (En)')),
                ('feature_1_title_uz', models.CharField(blank=True, max_length=300, verbose_name='1-xususiyat sarlavhasi (Uz)')),
                ('feature_1_title_ru', models.CharField(blank=True, max_length=300, verbose_name='1-xususiyat sarlavhasi (Ru)')),
                ('feature_1_title_en', models.CharField(blank=True, max_length=300, verbose_name='1-xususiyat sarlavhasi (En)')),
                ('feature_1_desc_uz', models.TextField(blank=True, verbose_name='1-xususiyat tavsifi (Uz)')),
                ('feature_1_desc_ru', models.TextField(blank=True, verbose_name='1-xususiyat tavsifi (Ru)')),
                ('feature_1_desc_en', models.TextField(blank=True, verbose_name='1-xususiyat tavsifi (En)')),
                ('feature_2_title_uz', models.CharField(blank=True, max_length=300, verbose_name='2-xususiyat sarlavhasi (Uz)')),
                ('feature_2_title_ru', models.CharField(blank=True, max_length=300, verbose_name='2-xususiyat sarlavhasi (Ru)')),
                ('feature_2_title_en', models.CharField(blank=True, max_length=300, verbose_name='2-xususiyat sarlavhasi (En)')),
                ('feature_2_desc_uz', models.TextField(blank=True, verbose_name='2-xususiyat tavsifi (Uz)')),
                ('feature_2_desc_ru', models.TextField(blank=True, verbose_name='2-xususiyat tavsifi (Ru)')),
                ('feature_2_desc_en', models.TextField(blank=True, verbose_name='2-xususiyat tavsifi (En)')),
            ],
            options={
                'verbose_name': 'Asosiy sahifa — Haqida bloki',
                'verbose_name_plural': 'Asosiy sahifa — Haqida bloki',
                'db_table': 'pages_homepage_haqida',
            },
        ),
        migrations.CreateModel(
            name='HomepageHaqidaRasm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=domains.pages.models.homepage_haqida.homepage_haqida_rasm_upload, verbose_name='Rasm')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faolmi?')),
                ('haqida', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='rasmlar',
                    to='pages.homepagehaqida',
                    verbose_name='Haqida bloki',
                )),
            ],
            options={
                'verbose_name': 'Carousel rasmi',
                'verbose_name_plural': 'Carousel rasmlari',
                'db_table': 'pages_homepage_haqida_rasm',
                'ordering': ['order'],
            },
        ),
    ]
