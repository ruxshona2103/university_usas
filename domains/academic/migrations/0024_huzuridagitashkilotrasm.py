import domains.academic.models.huzuridagi_tashkilot
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0023_huzuridagitashkilot_image_en_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HuzuridagiTashkilotRasm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=domains.academic.models.huzuridagi_tashkilot.tashkilot_rasm_upload, verbose_name='Rasm')),
                ('caption_uz', models.CharField(blank=True, max_length=300, verbose_name='Izoh (Uz)')),
                ('caption_ru', models.CharField(blank=True, max_length=300, verbose_name='Izoh (Ru)')),
                ('caption_en', models.CharField(blank=True, max_length=300, verbose_name='Izoh (En)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('tashkilot', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='rasmlar',
                    to='academic.huzuridagitashkilot',
                    verbose_name='Tashkilot',
                )),
            ],
            options={
                'verbose_name': 'Tashkilot rasmi',
                'verbose_name_plural': 'Tashkilot rasmlari',
                'db_table': 'academic_huzuridagi_tashkilot_rasm',
                'ordering': ['order'],
            },
        ),
    ]
