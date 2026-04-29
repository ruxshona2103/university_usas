from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0018_interaktiv_xizmat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Markaz',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
                ('name_uz', models.CharField(max_length=300, verbose_name='Nomi (Uz)')),
                ('name_ru', models.CharField(blank=True, max_length=300, verbose_name='Nomi (Ru)')),
                ('name_en', models.CharField(blank=True, max_length=300, verbose_name='Nomi (En)')),
                ('description_uz', models.TextField(blank=True, verbose_name='Tavsif (Uz)')),
                ('description_ru', models.TextField(blank=True, verbose_name='Tavsif (Ru)')),
                ('description_en', models.TextField(blank=True, verbose_name='Tavsif (En)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='pages/markazlar/', verbose_name='Rasm')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faolmi?')),
            ],
            options={
                'verbose_name': "Markaz / Bo'lim",
                'verbose_name_plural': "Markazlar / Bo'limlar",
                'db_table': 'pages_markaz',
                'ordering': ['order', 'name_uz'],
            },
        ),
        migrations.CreateModel(
            name='MarkazSubBolim',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('markaz', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='sub_bolimlar',
                    to='pages.markaz',
                    verbose_name='Markaz',
                )),
                ('name_uz', models.CharField(max_length=300, verbose_name='Nomi (Uz)')),
                ('name_ru', models.CharField(blank=True, max_length=300, verbose_name='Nomi (Ru)')),
                ('name_en', models.CharField(blank=True, max_length=300, verbose_name='Nomi (En)')),
                ('description_uz', models.TextField(blank=True, verbose_name='Tavsif (Uz)')),
                ('description_ru', models.TextField(blank=True, verbose_name='Tavsif (Ru)')),
                ('description_en', models.TextField(blank=True, verbose_name='Tavsif (En)')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
            ],
            options={
                'verbose_name': "Sub-bo'lim",
                'verbose_name_plural': "Sub-bo'limlar",
                'db_table': 'pages_markaz_sub_bolim',
                'ordering': ['order', 'name_uz'],
            },
        ),
    ]
