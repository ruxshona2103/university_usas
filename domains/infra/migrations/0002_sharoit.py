import domains.infra.models.sharoit
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infra', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sharoit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
                ('category', models.CharField(
                    choices=[('sport', 'Zamonaviy sport inshootlar'), ('talim', "Ta'lim uchun sharoitlar")],
                    db_index=True, default='talim', max_length=10, verbose_name="Bo'lim",
                )),
                ('title_uz', models.CharField(max_length=300, verbose_name='Nomi (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=300, verbose_name='Nomi (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=300, verbose_name='Nomi (En)')),
                ('description_uz', models.TextField(blank=True, verbose_name='Tavsif (Uz)')),
                ('description_ru', models.TextField(blank=True, verbose_name='Tavsif (Ru)')),
                ('description_en', models.TextField(blank=True, verbose_name='Tavsif (En)')),
                ('image', models.ImageField(blank=True, null=True, upload_to=domains.infra.models.sharoit.sharoit_image_upload, verbose_name='Rasm')),
                ('icon', models.CharField(blank=True, max_length=100, verbose_name='Icon (CSS class yoki emoji)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faolmi?')),
            ],
            options={
                'verbose_name': 'Sharoit va imkoniyat',
                'verbose_name_plural': 'Sharoit va imkoniyatlar',
                'db_table': 'infra_sharoit',
                'ordering': ['category', 'order'],
            },
        ),
    ]
