from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0003_staffcontent_tags_m2m'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='staff',
            name='academic_st_navbar__fe0da6_idx',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='navbar_item',
        ),
        migrations.AddField(
            model_name='staff',
            name='navbar_items',
            field=models.ManyToManyField(
                blank=True,
                related_name='staff_items',
                to='pages.navbarsubitem',
                verbose_name='Navbar sahifalari',
            ),
        ),
    ]
