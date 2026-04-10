"""
Migration: Person modeli birlashtirish.
- PersonCategory: navbar_items M2M olib tashlanadi
- Person: xodimlar uchun nullable fieldlar qo'shiladi
- PersonImage: yangi jadval
"""
import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_personcategory_navbar_items_m2m'),
        ('pages', '0001_initial'),
    ]

    operations = [

        # ── 1. PersonCategory: navbar_items olib tashlanadi ───────────────────

        migrations.RemoveField(
            model_name='personcategory',
            name='navbar_items',
        ),

        # ── 2. Person: xodimlar uchun nullable fieldlar ───────────────────────

        migrations.AddField(
            model_name='person',
            name='title_uz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Lavozim (Uz)'),
        ),
        migrations.AddField(
            model_name='person',
            name='title_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Lavozim (Ru)'),
        ),
        migrations.AddField(
            model_name='person',
            name='title_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Lavozim (En)'),
        ),
        migrations.AddField(
            model_name='person',
            name='position_uz',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ilmiy unvon (Uz)'),
        ),
        migrations.AddField(
            model_name='person',
            name='position_ru',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ilmiy unvon (Ru)'),
        ),
        migrations.AddField(
            model_name='person',
            name='position_en',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ilmiy unvon (En)'),
        ),
        migrations.AddField(
            model_name='person',
            name='phone',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Telefon'),
        ),
        migrations.AddField(
            model_name='person',
            name='fax',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Faks'),
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='person',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Manzil'),
        ),
        migrations.AddField(
            model_name='person',
            name='reception',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Qabul vaqti'),
        ),
        migrations.AddField(
            model_name='person',
            name='is_head',
            field=models.BooleanField(default=False, verbose_name="Bo'lim boshlig'i"),
        ),

        # ── 3. PersonImage: yangi jadval ──────────────────────────────────────

        migrations.CreateModel(
            name='PersonImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Yangilangan vaqt')),
                ('image', models.ImageField(upload_to='persons/gallery/%Y/%m/', verbose_name='Rasm')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Tartib')),
                ('person', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='images',
                    to='students.person',
                    verbose_name='Shaxs',
                )),
            ],
            options={
                'verbose_name': 'Shaxs rasmi',
                'verbose_name_plural': 'Shaxs rasmlari',
                'db_table': 'students_person_image',
                'ordering': ['order'],
            },
        ),
    ]
