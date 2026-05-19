from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0020_ilmiy_anjuman'),
    ]

    operations = [
        # Remove old fields
        migrations.RemoveField(model_name='sportnatija', name='mdh_1'),
        migrations.RemoveField(model_name='sportnatija', name='mdh_2'),
        migrations.RemoveField(model_name='sportnatija', name='mdh_3'),
        migrations.RemoveField(model_name='sportnatija', name='osiyo_yoshlar_1'),
        migrations.RemoveField(model_name='sportnatija', name='osiyo_yoshlar_2'),
        migrations.RemoveField(model_name='sportnatija', name='osiyo_yoshlar_3'),
        # Add new fields
        migrations.AddField(
            model_name='sportnatija',
            name='jahon_kubogi_1',
            field=models.PositiveIntegerField(default=0, verbose_name="Jahon kubogi — 1-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='jahon_kubogi_2',
            field=models.PositiveIntegerField(default=0, verbose_name="Jahon kubogi — 2-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='jahon_kubogi_3',
            field=models.PositiveIntegerField(default=0, verbose_name="Jahon kubogi — 3-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='prezident_1',
            field=models.PositiveIntegerField(default=0, verbose_name="Prezident olimpiyadasi — 1-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='prezident_2',
            field=models.PositiveIntegerField(default=0, verbose_name="Prezident olimpiyadasi — 2-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='prezident_3',
            field=models.PositiveIntegerField(default=0, verbose_name="Prezident olimpiyadasi — 3-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='ozb_chempionati_1',
            field=models.PositiveIntegerField(default=0, verbose_name="O'zbekiston chempionati — 1-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='ozb_chempionati_2',
            field=models.PositiveIntegerField(default=0, verbose_name="O'zbekiston chempionati — 2-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='ozb_chempionati_3',
            field=models.PositiveIntegerField(default=0, verbose_name="O'zbekiston chempionati — 3-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='ozb_kubogi_1',
            field=models.PositiveIntegerField(default=0, verbose_name="O'zbekiston kubogi — 1-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='ozb_kubogi_2',
            field=models.PositiveIntegerField(default=0, verbose_name="O'zbekiston kubogi — 2-o'rin"),
        ),
        migrations.AddField(
            model_name='sportnatija',
            name='ozb_kubogi_3',
            field=models.PositiveIntegerField(default=0, verbose_name="O'zbekiston kubogi — 3-o'rin"),
        ),
    ]
