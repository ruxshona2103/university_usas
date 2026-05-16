import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0035_kampusxizmati_add_image'),
        ('students', '0020_person_add_degree'),
    ]

    operations = [
        # Markaz — maqsad va vazifalari
        migrations.AddField(
            model_name='markaz',
            name='goals_uz',
            field=models.TextField(blank=True, verbose_name='Maqsad va vazifalari (Uz)'),
        ),
        migrations.AddField(
            model_name='markaz',
            name='goals_ru',
            field=models.TextField(blank=True, verbose_name='Maqsad va vazifalari (Ru)'),
        ),
        migrations.AddField(
            model_name='markaz',
            name='goals_en',
            field=models.TextField(blank=True, verbose_name='Maqsad va vazifalari (En)'),
        ),
        # Markaz — funksiyalari
        migrations.AddField(
            model_name='markaz',
            name='functions_uz',
            field=models.TextField(blank=True, verbose_name='Funksiyalari (Uz)'),
        ),
        migrations.AddField(
            model_name='markaz',
            name='functions_ru',
            field=models.TextField(blank=True, verbose_name='Funksiyalari (Ru)'),
        ),
        migrations.AddField(
            model_name='markaz',
            name='functions_en',
            field=models.TextField(blank=True, verbose_name='Funksiyalari (En)'),
        ),
        # MarkazXodim — yangi model
        migrations.CreateModel(
            name='MarkazXodim',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('markaz', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='xodimlar',
                    to='pages.markaz',
                    verbose_name="Markaz / Bo'lim",
                )),
                ('person', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='markaz_xodim_set',
                    to='students.person',
                    verbose_name='Xodim',
                )),
            ],
            options={
                'verbose_name': 'Markaz xodimi',
                'verbose_name_plural': 'Markaz xodimlari',
                'db_table': 'pages_markaz_xodim',
                'ordering': ['order'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='markazxodim',
            unique_together={('markaz', 'person')},
        ),
    ]
