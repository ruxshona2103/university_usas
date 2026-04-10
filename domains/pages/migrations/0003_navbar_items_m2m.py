from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_contentblock_block_type_contentblock_json_data_and_more'),
    ]

    operations = [
        # ContentBlock: navbar_item FK → navbar_items M2M
        migrations.RemoveIndex(
            model_name='contentblock',
            name='pages_conte_navbar__9c6f14_idx',
        ),
        migrations.RemoveField(
            model_name='contentblock',
            name='navbar_item',
        ),
        migrations.AddField(
            model_name='contentblock',
            name='navbar_items',
            field=models.ManyToManyField(
                blank=True,
                related_name='contentblock_items',
                to='pages.navbarsubitem',
                verbose_name='Navbar sahifalari',
            ),
        ),
        migrations.AddIndex(
            model_name='contentblock',
            index=models.Index(fields=['is_active', 'order'], name='pages_conte_is_acti_m2m_idx'),
        ),

        # LinkBlock: navbar_item FK → navbar_items M2M
        migrations.RemoveIndex(
            model_name='linkblock',
            name='pages_link__navbar__6111c1_idx',
        ),
        migrations.RemoveField(
            model_name='linkblock',
            name='navbar_item',
        ),
        migrations.AddField(
            model_name='linkblock',
            name='navbar_items',
            field=models.ManyToManyField(
                blank=True,
                related_name='linkblock_items',
                to='pages.navbarsubitem',
                verbose_name='Navbar sahifalari',
            ),
        ),
        migrations.AddIndex(
            model_name='linkblock',
            index=models.Index(fields=['is_active', 'order'], name='pages_linkb_is_acti_m2m_idx'),
        ),
    ]
