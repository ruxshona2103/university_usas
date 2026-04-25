import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_herovideo_poster_image_alter_partner_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutSocial',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('title_uz', models.CharField(max_length=500, verbose_name='Sarlavha (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=500, verbose_name='Sarlavha (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=500, verbose_name='Sarlavha (En)')),
            ],
            options={
                'verbose_name': 'Axborot xizmati haqida',
                'verbose_name_plural': 'Axborot xizmati haqida',
                'db_table': 'pages_about_social',
            },
        ),
        migrations.CreateModel(
            name='AboutSocialSection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('key', models.CharField(help_text="API javobida ishlatiladi, masalan: section_5, section_6", max_length=50, verbose_name='Kalit')),
                ('title_uz', models.CharField(max_length=300, verbose_name='Sarlavha (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=300, verbose_name='Sarlavha (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=300, verbose_name='Sarlavha (En)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('about_social', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sections',
                    to='pages.aboutsocial',
                    verbose_name='Axborot xizmati',
                )),
            ],
            options={
                'verbose_name': "Bo'lim",
                'verbose_name_plural': "Bo'limlar",
                'db_table': 'pages_about_social_section',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='AboutSocialSectionItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('text_uz', models.TextField(verbose_name='Matn (Uz)')),
                ('text_ru', models.TextField(blank=True, verbose_name='Matn (Ru)')),
                ('text_en', models.TextField(blank=True, verbose_name='Matn (En)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('section', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items',
                    to='pages.aboutsocialsection',
                    verbose_name="Bo'lim",
                )),
            ],
            options={
                'verbose_name': 'Element',
                'verbose_name_plural': 'Elementlar',
                'db_table': 'pages_about_social_section_item',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='AboutSocialExtraTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('text_uz', models.CharField(max_length=300, verbose_name='Matn (Uz)')),
                ('text_ru', models.CharField(blank=True, max_length=300, verbose_name='Matn (Ru)')),
                ('text_en', models.CharField(blank=True, max_length=300, verbose_name='Matn (En)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('about_social', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='extra_tasks',
                    to='pages.aboutsocial',
                    verbose_name='Axborot xizmati',
                )),
            ],
            options={
                'verbose_name': "Qo'shimcha vazifa",
                'verbose_name_plural': "Qo'shimcha vazifalar",
                'db_table': 'pages_about_social_extra_task',
                'ordering': ['order'],
            },
        ),
    ]
