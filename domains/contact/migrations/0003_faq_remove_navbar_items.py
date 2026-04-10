from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_faq_navbar_items_m2m'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='navbar_items',
        ),
    ]
