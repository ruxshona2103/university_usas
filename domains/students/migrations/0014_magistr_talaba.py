from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0013_stipendiya'),
    ]

    operations = [
        migrations.CreateModel(
            name='MagistrTalaba',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('person', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='magistr_talaba_entries',
                    to='students.person',
                    verbose_name='Shaxs (Person)',
                )),
                ('full_name', models.CharField(blank=True, max_length=300, verbose_name='F.I.Sh. (override)')),
                ('specialty_code', models.CharField(blank=True, max_length=50, verbose_name='Mutaxassislik kodi')),
                ('specialty_name_uz', models.CharField(blank=True, max_length=500, verbose_name='Mutaxassislik nomi (Uz)')),
                ('specialty_name_ru', models.CharField(blank=True, max_length=500, verbose_name='Mutaxassislik nomi (Ru)')),
                ('specialty_name_en', models.CharField(blank=True, max_length=500, verbose_name='Mutaxassislik nomi (En)')),
                ('dissertation_topic_uz', models.TextField(blank=True, verbose_name='Dissertatsiya mavzusi (Uz)')),
                ('dissertation_topic_ru', models.TextField(blank=True, verbose_name='Dissertatsiya mavzusi (Ru)')),
                ('dissertation_topic_en', models.TextField(blank=True, verbose_name='Dissertatsiya mavzusi (En)')),
                ('supervisor_name', models.CharField(blank=True, max_length=300, verbose_name='Ilmiy rahbar')),
                ('supervisor_info_uz', models.CharField(blank=True, max_length=300, verbose_name='Ilmiy daraja/unvon (Uz)')),
                ('supervisor_info_ru', models.CharField(blank=True, max_length=300, verbose_name='Ilmiy daraja/unvon (Ru)')),
                ('supervisor_info_en', models.CharField(blank=True, max_length=300, verbose_name='Ilmiy daraja/unvon (En)')),
                ('education_form_uz', models.CharField(blank=True, max_length=100, verbose_name="Ta'lim shakli (Uz)")),
                ('education_form_ru', models.CharField(blank=True, max_length=100, verbose_name="Ta'lim shakli (Ru)")),
                ('education_form_en', models.CharField(blank=True, max_length=100, verbose_name="Ta'lim shakli (En)")),
                ('year', models.CharField(blank=True, max_length=20, verbose_name="O'quv yili")),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faolmi?')),
            ],
            options={
                'verbose_name': 'Magistratura talabasi (yangi)',
                'verbose_name_plural': 'Magistratura talabalari (yangi)',
                'db_table': 'students_magistr_talaba',
                'ordering': ['year', 'order', 'full_name'],
            },
        ),
    ]
