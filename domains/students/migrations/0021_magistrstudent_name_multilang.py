from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0020_person_add_degree'),
    ]

    operations = [
        # Rename existing column to _uz variant
        migrations.RenameField(
            model_name='magistrstudent',
            old_name='student_name',
            new_name='student_name_uz',
        ),
        migrations.AlterField(
            model_name='magistrstudent',
            name='student_name_uz',
            field=models.CharField(max_length=300, verbose_name="Talabaning F.I.Sh. (Uz)"),
        ),
        migrations.AddField(
            model_name='magistrstudent',
            name='student_name_ru',
            field=models.CharField(blank=True, max_length=300, verbose_name="Talabaning F.I.Sh. (Ru)"),
        ),
        migrations.AddField(
            model_name='magistrstudent',
            name='student_name_en',
            field=models.CharField(blank=True, max_length=300, verbose_name="Talabaning F.I.Sh. (En)"),
        ),
    ]
