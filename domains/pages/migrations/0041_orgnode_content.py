from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0040_orgnode_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgnode',
            name='content_uz',
            field=models.TextField(blank=True, help_text="Havola bo'sh bo'lsa, tugun bosilganda shu matn o'z sahifasida ko'rsatiladi", verbose_name="Batafsil ma'lumot (Uz)"),
        ),
        migrations.AddField(
            model_name='orgnode',
            name='content_ru',
            field=models.TextField(blank=True, verbose_name="Batafsil ma'lumot (Ru)"),
        ),
        migrations.AddField(
            model_name='orgnode',
            name='content_en',
            field=models.TextField(blank=True, verbose_name="Batafsil ma'lumot (En)"),
        ),
    ]
