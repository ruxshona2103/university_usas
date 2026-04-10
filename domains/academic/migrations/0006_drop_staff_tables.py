"""
Staff va StaffContent modellari o'chiriladi.
Barcha xodimlar endi students.Person orqali boshqariladi.
"""
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_remove_staff_navbar_items'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(name='StaffContent'),
        migrations.DeleteModel(name='Staff'),
    ]
