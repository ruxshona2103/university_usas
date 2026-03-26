import datetime
from django.db import migrations


def convert_date_to_datetime(apps, schema_editor):
    for model_name in ['News', 'Event', 'Blog']:
        Model = apps.get_model('news', model_name)
        for obj in Model.objects.all():
            if obj.date and isinstance(obj.date, datetime.date) and not isinstance(obj.date, datetime.datetime):
                obj.date = datetime.datetime(obj.date.year, obj.date.month, obj.date.day, 0, 0, 0)
                obj.save(update_fields=['date'])


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_date_to_datetimefield'),
    ]

    operations = [
        migrations.RunPython(convert_date_to_datetime, migrations.RunPython.noop),
    ]
