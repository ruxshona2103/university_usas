from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0020_internationalpost_image_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='internationaldeptconfig',
            name='head_working_hours_uz',
            field=models.CharField(blank=True, max_length=200, verbose_name="Qabul kunlari (Uz)"),
        ),
        migrations.AddField(
            model_name='internationaldeptconfig',
            name='head_working_hours_ru',
            field=models.CharField(blank=True, max_length=200, verbose_name="Qabul kunlari (Ru)"),
        ),
        migrations.AddField(
            model_name='internationaldeptconfig',
            name='head_working_hours_en',
            field=models.CharField(blank=True, max_length=200, verbose_name="Qabul kunlari (En)"),
        ),
        migrations.RunSQL(
            sql="UPDATE international_dept_config SET head_working_hours_uz = head_working_hours WHERE head_working_hours IS NOT NULL AND head_working_hours != '';",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RemoveField(
            model_name='internationaldeptconfig',
            name='head_working_hours',
        ),
    ]
