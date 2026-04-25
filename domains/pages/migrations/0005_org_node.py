import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_about_social'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgNode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('node_type', models.CharField(
                    choices=[
                        ('governing',  'Boshqaruv organi'),
                        ('rector',     'Rektor'),
                        ('prorektor',  'Prorektor / Yordamchi'),
                        ('department', "Bo'lim / Sektor"),
                        ('institute',  'Institut / Markaz'),
                        ('kafedra',    'Kafedra'),
                        ('other',      'Boshqa'),
                    ],
                    default='department',
                    max_length=20,
                    verbose_name='Tur',
                )),
                ('name_uz', models.CharField(max_length=400, verbose_name='Nomi (Uz)')),
                ('name_ru', models.CharField(blank=True, max_length=400, verbose_name='Nomi (Ru)')),
                ('name_en', models.CharField(blank=True, max_length=400, verbose_name='Nomi (En)')),
                ('is_starred',        models.BooleanField(default=False, verbose_name='* (bir yulduz)')),
                ('is_double_starred', models.BooleanField(default=False, verbose_name='** (ikki yulduz)')),
                ('is_highlighted',    models.BooleanField(default=False, verbose_name='Ajratilgan (qizil ramka)')),
                ('is_active',         models.BooleanField(default=True,  verbose_name='Faolmi?')),
                ('order',             models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('parent', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='children',
                    to='pages.orgnode',
                    verbose_name='Yuqori daraja',
                )),
            ],
            options={
                'verbose_name':        'Tashkiliy tugun',
                'verbose_name_plural': 'Tashkiliy tuzilma',
                'db_table':            'pages_org_node',
                'ordering':            ['order', 'name_uz'],
            },
        ),
    ]
