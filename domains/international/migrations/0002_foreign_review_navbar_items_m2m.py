from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0001_initial'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='foreignprofessorreview',
            name='internation_navbar__7af7bf_idx',
        ),
        migrations.RemoveField(
            model_name='foreignprofessorreview',
            name='navbar_item',
        ),
        migrations.AddField(
            model_name='foreignprofessorreview',
            name='navbar_items',
            field=models.ManyToManyField(
                blank=True,
                related_name='foreign_review_items',
                to='pages.navbarsubitem',
                verbose_name='Navbar sahifalari',
            ),
        ),
    ]
