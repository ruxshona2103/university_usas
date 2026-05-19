import domains.international.models.national_rating
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0023_nationalrating_nationalratingimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nationalratingimage',
            old_name='image',
            new_name='image_uz',
        ),
        migrations.AddField(
            model_name='nationalratingimage',
            name='image_ru',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=domains.international.models.national_rating.national_rating_image_upload,
                verbose_name='Rasm (Ru)',
            ),
        ),
        migrations.AddField(
            model_name='nationalratingimage',
            name='image_en',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=domains.international.models.national_rating.national_rating_image_upload,
                verbose_name='Rasm (En)',
            ),
        ),
    ]
