from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0004_staff_navbar_items_m2m'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='navbar_items',
        ),
    ]
