import domains.academic.models.huzuridagi_tashkilot
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0015_add_dean_vice_dean_mudiri_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='HuzuridagiTashkilot',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
                ('name_uz', models.CharField(max_length=400, verbose_name='Nomi (Uz)')),
                ('name_ru', models.CharField(blank=True, max_length=400, verbose_name='Nomi (Ru)')),
                ('name_en', models.CharField(blank=True, max_length=400, verbose_name='Nomi (En)')),
                ('description_uz', models.TextField(blank=True, verbose_name='Tavsif (Uz)')),
                ('description_ru', models.TextField(blank=True, verbose_name='Tavsif (Ru)')),
                ('description_en', models.TextField(blank=True, verbose_name='Tavsif (En)')),
                ('image', models.ImageField(blank=True, null=True, upload_to=domains.academic.models.huzuridagi_tashkilot.tashkilot_image_upload, verbose_name='Rasm')),
                ('website', models.URLField(blank=True, verbose_name='Veb-sayt')),
                ('phone', models.CharField(blank=True, max_length=50, verbose_name='Telefon')),
                ('email', models.CharField(blank=True, max_length=200, verbose_name='Email')),
                ('address_uz', models.CharField(blank=True, max_length=400, verbose_name='Manzil (Uz)')),
                ('address_ru', models.CharField(blank=True, max_length=400, verbose_name='Manzil (Ru)')),
                ('address_en', models.CharField(blank=True, max_length=400, verbose_name='Manzil (En)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faolmi?')),
            ],
            options={
                'verbose_name': 'Huzuridagi tashkilot',
                'verbose_name_plural': 'Akademiya huzuridagi tashkilotlar',
                'db_table': 'academic_huzuridagi_tashkilot',
                'ordering': ['order'],
            },
        ),
    ]
