from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0006_rector_appeal_sender_appeal_type_extra_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='qabulraqami',
            name='link',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Havola'),
        ),
    ]
