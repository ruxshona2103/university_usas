from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0002_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='staffcontent',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='staffcontent',
            name='tag',
        ),
        migrations.AddField(
            model_name='staffcontent',
            name='tags',
            field=models.ManyToManyField(
                blank=True,
                related_name='staff_contents',
                to='common.tag',
                verbose_name='Tablar (Taglar)',
            ),
        ),
    ]
