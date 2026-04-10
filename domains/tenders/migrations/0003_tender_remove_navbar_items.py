from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0002_tender_navbar_items_m2m'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tenderannouncement',
            name='navbar_items',
        ),
    ]
