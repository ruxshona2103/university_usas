from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0022_add_contact_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgnode',
            name='image_ru',
            field=models.ImageField(blank=True, null=True, upload_to='org_nodes/', verbose_name='Rasm (Ru)'),
        ),
        migrations.AddField(
            model_name='orgnode',
            name='image_en',
            field=models.ImageField(blank=True, null=True, upload_to='org_nodes/', verbose_name='Rasm (En)'),
        ),
        migrations.AlterField(
            model_name='orgnode',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='org_nodes/', verbose_name='Rasm (Uz)'),
        ),
    ]
