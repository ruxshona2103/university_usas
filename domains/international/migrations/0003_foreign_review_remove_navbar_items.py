from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0002_foreign_review_navbar_items_m2m'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foreignprofessorreview',
            name='navbar_items',
        ),
    ]
