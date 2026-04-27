from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_orgnode_rename_name_to_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgSection',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title_uz', models.CharField(max_length=200, verbose_name='Sarlavha (Uz)')),
                ('title_ru', models.CharField(blank=True, max_length=200, verbose_name='Sarlavha (Ru)')),
                ('title_en', models.CharField(blank=True, max_length=200, verbose_name='Sarlavha (En)')),
                ('description_uz', models.CharField(blank=True, max_length=500, verbose_name='Tavsif (Uz)')),
                ('description_ru', models.CharField(blank=True, max_length=500, verbose_name='Tavsif (Ru)')),
                ('description_en', models.CharField(blank=True, max_length=500, verbose_name='Tavsif (En)')),
                ('slug', models.SlugField(max_length=120, unique=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': "Tuzilma bo'limi",
                'verbose_name_plural': "Tuzilma bo'limlari",
                'db_table': 'pages_org_section',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='orgnode',
            name='description_uz',
            field=models.CharField(blank=True, max_length=500, verbose_name='Tavsif (Uz)'),
        ),
        migrations.AddField(
            model_name='orgnode',
            name='description_ru',
            field=models.CharField(blank=True, max_length=500, verbose_name='Tavsif (Ru)'),
        ),
        migrations.AddField(
            model_name='orgnode',
            name='description_en',
            field=models.CharField(blank=True, max_length=500, verbose_name='Tavsif (En)'),
        ),
        migrations.AddField(
            model_name='orgnode',
            name='section',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='nodes',
                to='pages.orgsection',
                verbose_name="Bo'lim (sektsiya)",
            ),
        ),
        migrations.AddField(
            model_name='orgnode',
            name='section_order',
            field=models.PositiveIntegerField(default=0, verbose_name="Bo'limdagi tartib"),
        ),
    ]
