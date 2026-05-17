from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0024_huzuridagitashkilotrasm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='huzuridagitashkilot',
            name='org_type',
            field=models.CharField(
                choices=[
                    ('akademiya', 'Akademiya huzuridagi'),
                    ('jamoat', 'Jamoat tashkiloti'),
                    ('kengash', 'Akademiya kengashi'),
                ],
                default='akademiya',
                max_length=20,
                verbose_name='Tashkilot turi',
            ),
        ),
    ]
