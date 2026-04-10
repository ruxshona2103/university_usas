from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_event_options_alter_news_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informationcontent',
            name='navbar_items',
        ),
    ]
