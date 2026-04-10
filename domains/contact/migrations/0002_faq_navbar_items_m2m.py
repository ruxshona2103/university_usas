from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='navbar_items',
            field=models.ManyToManyField(
                blank=True,
                related_name='faq_items',
                to='pages.navbarsubitem',
                verbose_name='Navbar sahifalari',
            ),
        ),
    ]
