import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0024_alter_magistrtalaba_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='PsixologXizmat',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title_uz', models.CharField(max_length=300, verbose_name='Sarlavha (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=300, verbose_name='Sarlavha (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=300, verbose_name='Sarlavha (En)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
            ],
            options={
                'verbose_name': 'Psixolog xizmati',
                'verbose_name_plural': 'Psixolog xizmatlari',
                'db_table': 'students_psixolog_xizmat',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='PsixologSection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title_uz', models.CharField(max_length=200, verbose_name='Sarlavha (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=200, verbose_name='Sarlavha (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=200, verbose_name='Sarlavha (En)')),
                ('content_uz', models.TextField(verbose_name='Matn (Uz)')),
                ('content_ru', models.TextField(blank=True, verbose_name='Matn (Ru)')),
                ('content_en', models.TextField(blank=True, verbose_name='Matn (En)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
            ],
            options={
                'verbose_name': "Psixolog bo'limi",
                'verbose_name_plural': "Psixolog bo'limlari",
                'db_table': 'students_psixolog_section',
                'ordering': ['order'],
            },
        ),
    ]
