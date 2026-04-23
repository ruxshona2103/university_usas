from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0002_alter_academystat_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademyDetailPage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('resource_center_uz', models.TextField(blank=True, null=True, verbose_name='Axborot-resurs markazi (Uz)')),
                ('resource_center_ru', models.TextField(blank=True, null=True, verbose_name='Axborot-resurs markazi (Ru)')),
                ('resource_center_en', models.TextField(blank=True, null=True, verbose_name='Axborot-resurs markazi (En)')),
                ('edu_direction_count', models.CharField(blank=True, default='', max_length=50, verbose_name="Ta'lim yo'nalishlari")),
                ('sport_type_count', models.CharField(blank=True, default='', max_length=50, verbose_name='Sport turlari')),
                ('masters_count', models.CharField(blank=True, default='', max_length=50, verbose_name='Magistratura mutaxassisliklari')),
                ('auditorium_count', models.CharField(blank=True, default='', max_length=50, verbose_name="O'quv auditoriyalari")),
                ('detail_uz', models.TextField(blank=True, null=True, verbose_name="Batafsil ma'lumotlar (Uz)")),
                ('detail_ru', models.TextField(blank=True, null=True, verbose_name="Batafsil ma'lumotlar (Ru)")),
                ('detail_en', models.TextField(blank=True, null=True, verbose_name="Batafsil ma'lumotlar (En)")),
            ],
            options={
                'verbose_name': 'Akademiya raqamlarda — batafsil',
                'verbose_name_plural': 'Akademiya raqamlarda — batafsil',
                'db_table': 'academic_detail_page',
            },
        ),
    ]
