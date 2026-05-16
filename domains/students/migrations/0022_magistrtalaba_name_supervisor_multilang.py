from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0021_magistrstudent_name_multilang'),
    ]

    operations = [
        # full_name → full_name_uz
        migrations.RenameField(
            model_name='magistrtalaba',
            old_name='full_name',
            new_name='full_name_uz',
        ),
        migrations.AlterField(
            model_name='magistrtalaba',
            name='full_name_uz',
            field=models.CharField(blank=True, max_length=300, verbose_name='F.I.Sh. (Uz)'),
        ),
        migrations.AddField(
            model_name='magistrtalaba',
            name='full_name_ru',
            field=models.CharField(blank=True, max_length=300, verbose_name='F.I.Sh. (Ru)'),
        ),
        migrations.AddField(
            model_name='magistrtalaba',
            name='full_name_en',
            field=models.CharField(blank=True, max_length=300, verbose_name='F.I.Sh. (En)'),
        ),
        # supervisor_name → supervisor_name_uz
        migrations.RenameField(
            model_name='magistrtalaba',
            old_name='supervisor_name',
            new_name='supervisor_name_uz',
        ),
        migrations.AlterField(
            model_name='magistrtalaba',
            name='supervisor_name_uz',
            field=models.CharField(blank=True, max_length=300, verbose_name='Ilmiy rahbar F.I.Sh. (Uz)'),
        ),
        migrations.AddField(
            model_name='magistrtalaba',
            name='supervisor_name_ru',
            field=models.CharField(blank=True, max_length=300, verbose_name='Ilmiy rahbar F.I.Sh. (Ru)'),
        ),
        migrations.AddField(
            model_name='magistrtalaba',
            name='supervisor_name_en',
            field=models.CharField(blank=True, max_length=300, verbose_name='Ilmiy rahbar F.I.Sh. (En)'),
        ),
    ]
