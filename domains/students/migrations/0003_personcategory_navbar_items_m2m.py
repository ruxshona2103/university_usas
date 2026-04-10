from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_personcontent_tags_m2m'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personcategory',
            name='navbar_item',
        ),
        migrations.AddField(
            model_name='personcategory',
            name='navbar_items',
            field=models.ManyToManyField(
                blank=True,
                related_name='person_category_items',
                to='pages.navbarsubitem',
                verbose_name='Navbar sahifalari',
            ),
        ),
    ]
