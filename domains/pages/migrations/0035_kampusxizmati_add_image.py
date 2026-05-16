from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0034_aboutacademy_image_en_aboutacademy_image_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kampusxizmati',
            name='image',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to='kampus_xizmati/',
                verbose_name="Rasm (icon o'rniga)",
            ),
        ),
    ]
