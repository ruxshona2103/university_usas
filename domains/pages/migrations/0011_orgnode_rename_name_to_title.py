from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_rekvizit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orgnode',
            old_name='name_uz',
            new_name='title_uz',
        ),
        migrations.RenameField(
            model_name='orgnode',
            old_name='name_ru',
            new_name='title_ru',
        ),
        migrations.RenameField(
            model_name='orgnode',
            old_name='name_en',
            new_name='title_en',
        ),
    ]
