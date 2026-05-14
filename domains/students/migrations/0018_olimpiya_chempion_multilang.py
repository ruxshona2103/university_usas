from django.db import migrations, models


def copy_to_uz(apps, schema_editor):
    OlimpiyaChempion = apps.get_model('students', 'OlimpiyaChempion')
    for obj in OlimpiyaChempion.objects.all():
        changed = False
        if obj.full_name and not obj.full_name_uz:
            obj.full_name_uz = obj.full_name
            changed = True
        if obj.yonalish and not obj.yonalish_uz:
            obj.yonalish_uz = obj.yonalish
            changed = True
        if changed:
            obj.save(update_fields=['full_name_uz', 'yonalish_uz'])


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0017_remove_person_address_remove_person_reception_and_more'),
    ]

    operations = [
        # 1. Yangi ustunlar qo'shish
        migrations.AddField(
            model_name='olimpiyachempion',
            name='full_name_uz',
            field=models.CharField(blank=True, max_length=300, verbose_name="To'liq ismi (UZ)"),
        ),
        migrations.AddField(
            model_name='olimpiyachempion',
            name='full_name_ru',
            field=models.CharField(blank=True, max_length=300, verbose_name="To'liq ismi (RU)"),
        ),
        migrations.AddField(
            model_name='olimpiyachempion',
            name='full_name_en',
            field=models.CharField(blank=True, max_length=300, verbose_name="To'liq ismi (EN)"),
        ),
        migrations.AddField(
            model_name='olimpiyachempion',
            name='yonalish_uz',
            field=models.CharField(blank=True, max_length=300, verbose_name='Sport turi (UZ)'),
        ),
        migrations.AddField(
            model_name='olimpiyachempion',
            name='yonalish_ru',
            field=models.CharField(blank=True, max_length=300, verbose_name='Sport turi (RU)'),
        ),
        migrations.AddField(
            model_name='olimpiyachempion',
            name='yonalish_en',
            field=models.CharField(blank=True, max_length=300, verbose_name='Sport turi (EN)'),
        ),
        # 2. Mavjud ma'lumotlarni ko'chirish
        migrations.RunPython(copy_to_uz, migrations.RunPython.noop),
        # 3. Eski ustunlarni o'chirish
        migrations.RemoveField(
            model_name='olimpiyachempion',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='olimpiyachempion',
            name='yonalish',
        ),
        migrations.RemoveField(
            model_name='olimpiyachempion',
            name='guruh',
        ),
    ]
