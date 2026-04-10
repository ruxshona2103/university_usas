from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0001_initial'),
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenderannouncement',
            name='navbar_items',
            field=models.ManyToManyField(
                blank=True,
                related_name='tender_items',
                to='pages.navbarsubitem',
                verbose_name='Navbar sahifalari',
            ),
        ),
    ]
