from django.db import migrations, models


def move_digital_from_tasks(apps, schema_editor):
    """Mavjud 'RAQAMLI MA'LUMOTLAR' matnini `tasks`dan `digital_data`ga ko'chiradi."""
    Cfg = apps.get_model('international', 'InternationalDeptConfig')
    for cfg in Cfg.objects.all():
        changed = False
        for lang in ('uz', 'ru', 'en'):
            raw = getattr(cfg, f'tasks_{lang}') or ''
            lines = raw.splitlines()
            idx = next(
                (i for i, ln in enumerate(lines) if 'raqamli ma' in ln.lower()),
                None,
            )
            if idx is None:
                continue
            before = '\n'.join(lines[:idx]).strip()
            after = '\n'.join(lines[idx + 1:]).strip()
            setattr(cfg, f'tasks_{lang}', before)
            if after and not (getattr(cfg, f'digital_data_{lang}') or '').strip():
                setattr(cfg, f'digital_data_{lang}', after)
            changed = True
        if changed:
            cfg.save()


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0027_alter_studyinuzbekistanconfig_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='internationaldeptconfig',
            name='digital_data_uz',
            field=models.TextField(blank=True, help_text="Oddiy matn — sahifada «Bo'lim vazifalari» ostida alohida bo'lim bo'lib ko'rsatiladi", verbose_name="Raqamli ma'lumotlar (Uz)"),
        ),
        migrations.AddField(
            model_name='internationaldeptconfig',
            name='digital_data_ru',
            field=models.TextField(blank=True, verbose_name="Raqamli ma'lumotlar (Ru)"),
        ),
        migrations.AddField(
            model_name='internationaldeptconfig',
            name='digital_data_en',
            field=models.TextField(blank=True, verbose_name="Raqamli ma'lumotlar (En)"),
        ),
        migrations.RunPython(move_digital_from_tasks, migrations.RunPython.noop),
    ]
