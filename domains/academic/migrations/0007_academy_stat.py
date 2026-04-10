import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0006_drop_staff_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademyStat',
            fields=[
                ('id',         models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True,     verbose_name='Yangilangan vaqt')),

                ('label_uz', models.CharField(max_length=300, verbose_name='Yorliq (Uz)')),
                ('label_ru', models.CharField(max_length=300, blank=True, verbose_name='Yorliq (Ru)')),
                ('label_en', models.CharField(max_length=300, blank=True, verbose_name='Yorliq (En)')),

                ('value_uz', models.CharField(max_length=300, verbose_name='Qiymat (Uz)')),
                ('value_ru', models.CharField(max_length=300, blank=True, verbose_name='Qiymat (Ru)')),
                ('value_en', models.CharField(max_length=300, blank=True, verbose_name='Qiymat (En)')),

                ('order',     models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faolmi?')),
            ],
            options={
                'verbose_name':        'Akademiya raqamda',
                'verbose_name_plural': 'Akademiya raqamlarda',
                'db_table':  'academic_academy_stat',
                'ordering':  ['order', 'created_at'],
            },
        ),
    ]
