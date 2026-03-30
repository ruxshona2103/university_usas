from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_staff_navbar_item'),
        ('pages', '0007_staff_navbar_item'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrganizationUnit',
        ),
    ]
