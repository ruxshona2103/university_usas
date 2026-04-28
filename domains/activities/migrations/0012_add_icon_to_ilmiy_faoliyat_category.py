from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0011_file_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='ilmiyfaoliyatcategory',
            name='icon',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Icon nomi'),
        ),
    ]
