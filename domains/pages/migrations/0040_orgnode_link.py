from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0039_add_announcement_image_button_block_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgnode',
            name='link',
            field=models.CharField(
                blank=True,
                help_text="Bosilganda ochiladigan manzil, masalan: /page/markazlar/buxgalteriya yoki /page/rectorate. Bo'sh qoldirilsa — nomi mos keladigan markaz sahifasiga avtomatik ulanadi.",
                max_length=500,
                verbose_name='Havola (batafsil sahifa)',
            ),
        ),
    ]
