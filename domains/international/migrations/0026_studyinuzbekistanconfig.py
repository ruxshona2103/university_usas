from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0025_alter_nationalratingimage_image_uz'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyInUzbekistanConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro_uz', models.TextField(blank=True, verbose_name='Kirish matni (Uz)', help_text='Sahifa bosh qismidagi matn. HTML qabul qiladi.')),
                ('intro_ru', models.TextField(blank=True, verbose_name='Kirish matni (Ru)')),
                ('intro_en', models.TextField(blank=True, verbose_name='Kirish matni (En)')),
                ('banner_image', models.FileField(blank=True, null=True, upload_to='study_in_uzbekistan/', verbose_name='Banner rasm')),
                ('banner_link', models.URLField(blank=True, max_length=500, verbose_name='Banner linki', help_text='Rasmni bosganda ochiladi')),
                ('banner_caption_uz', models.CharField(blank=True, max_length=300, verbose_name='Rasm taglik (Uz)')),
                ('banner_caption_ru', models.CharField(blank=True, max_length=300, verbose_name='Rasm taglik (Ru)')),
                ('banner_caption_en', models.CharField(blank=True, max_length=300, verbose_name='Rasm taglik (En)')),
                ('announcement_show', models.BooleanField(default=True, verbose_name="E'lonni ko'rsatish")),
                ('announcement_variant', models.CharField(
                    choices=[('warning', "Sariq (warning)"), ('info', "Ko'k (info)"), ('success', 'Yashil (success)')],
                    default='info', max_length=20, verbose_name="E'lon rangi",
                )),
                ('announcement_icon', models.CharField(blank=True, default='🔔', max_length=10, verbose_name="E'lon ikoni (emoji)")),
                ('announcement_title_uz', models.CharField(blank=True, max_length=300, verbose_name="E'lon sarlavhasi (Uz)")),
                ('announcement_title_ru', models.CharField(blank=True, max_length=300, verbose_name="E'lon sarlavhasi (Ru)")),
                ('announcement_title_en', models.CharField(blank=True, max_length=300, verbose_name="E'lon sarlavhasi (En)")),
                ('announcement_text_uz', models.TextField(blank=True, verbose_name="E'lon matni (Uz)")),
                ('announcement_text_ru', models.TextField(blank=True, verbose_name="E'lon matni (Ru)")),
                ('announcement_text_en', models.TextField(blank=True, verbose_name="E'lon matni (En)")),
                ('announcement_link', models.URLField(blank=True, max_length=500, verbose_name="E'lon linki")),
                ('announcement_link_text', models.CharField(blank=True, max_length=200, verbose_name='Link matni')),
                ('portal_url', models.URLField(blank=True, default='https://studyinuzbekistan.com', max_length=500, verbose_name='Portal URL (studyinuzbekistan.com)')),
                ('portal_button_uz', models.CharField(blank=True, default='Study in Uzbekistan', max_length=200, verbose_name='Tugma matni (Uz)')),
                ('portal_button_ru', models.CharField(blank=True, default='Study in Uzbekistan', max_length=200, verbose_name='Tugma matni (Ru)')),
                ('portal_button_en', models.CharField(blank=True, default='Study in Uzbekistan', max_length=200, verbose_name='Tugma matni (En)')),
            ],
            options={
                'verbose_name': 'Study in Uzbekistan sahifasi',
                'verbose_name_plural': 'Study in Uzbekistan sahifasi',
                'db_table': 'study_in_uzbekistan_config',
            },
        ),
    ]
