from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='personcontent',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='personcontent',
            name='tag',
        ),
        migrations.AddField(
            model_name='personcontent',
            name='tags',
            field=models.ManyToManyField(
                blank=True,
                related_name='person_contents',
                to='common.tag',
                verbose_name='Taglar',
            ),
        ),
    ]
