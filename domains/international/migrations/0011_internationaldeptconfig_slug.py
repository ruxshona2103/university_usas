from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0010_alter_internationalpost_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='internationaldeptconfig',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, verbose_name="Slug (URL)", help_text="Navbar sahifa slug'i, masalan: international-dept"),
        ),
        migrations.RunSQL(
            "UPDATE international_dept_config SET slug = 'international-dept' WHERE id = 1;",
            reverse_sql="UPDATE international_dept_config SET slug = '' WHERE id = 1;",
        ),
    ]
