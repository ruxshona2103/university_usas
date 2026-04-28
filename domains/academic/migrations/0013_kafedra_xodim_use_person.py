from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0012_add_kafedra_rasm'),
        ('students', '0001_initial'),
    ]

    operations = [
        # Eski ma'lumotlarni tozalash (qaytadan seed qilinadi)
        migrations.RunSQL("DELETE FROM academic_kafedra_xodim;", migrations.RunSQL.noop),

        # Eski fieldlarni olib tashlash
        migrations.RemoveField(model_name='kafedraxodim', name='full_name'),
        migrations.RemoveField(model_name='kafedraxodim', name='position_uz'),
        migrations.RemoveField(model_name='kafedraxodim', name='position_ru'),
        migrations.RemoveField(model_name='kafedraxodim', name='position_en'),
        migrations.RemoveField(model_name='kafedraxodim', name='email'),
        migrations.RemoveField(model_name='kafedraxodim', name='photo'),
        migrations.RemoveField(model_name='kafedraxodim', name='is_active'),

        # Person FK qo'shish
        migrations.AddField(
            model_name='kafedraxodim',
            name='person',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='kafedra_links',
                to='students.person',
                verbose_name='Shaxs',
            ),
        ),

        # unique_together
        migrations.AlterUniqueTogether(
            name='kafedraxodim',
            unique_together={('kafedra', 'person')},
        ),
    ]
