from django.db import migrations, models
from django.utils.text import slugify


def generate_reyting_slugs(apps, schema_editor):
    conn = schema_editor.connection
    with conn.cursor() as cursor:
        cursor.execute('SELECT id, title_uz FROM international_xalqaro_reyting_bolim ORDER BY bolim_type, "order", id')
        rows = cursor.fetchall()
    seen = set()
    updates = []
    for pk, title_uz in rows:
        base = slugify(title_uz or '', allow_unicode=True) or str(pk)
        slug = base
        n = 1
        while slug in seen:
            slug = f'{base}-{n}'
            n += 1
        seen.add(slug)
        updates.append((slug, str(pk)))
    with conn.cursor() as cursor:
        for slug, pk in updates:
            cursor.execute('UPDATE international_xalqaro_reyting_bolim SET slug = %s WHERE id = %s', [slug, pk])


def generate_professor_slugs(apps, schema_editor):
    conn = schema_editor.connection
    with conn.cursor() as cursor:
        cursor.execute('SELECT id, full_name FROM international_xorijlik_professor ORDER BY "order", id')
        rows = cursor.fetchall()
    seen = set()
    updates = []
    for pk, full_name in rows:
        base = slugify(full_name or '', allow_unicode=True) or str(pk)
        slug = base
        n = 1
        while slug in seen:
            slug = f'{base}-{n}'
            n += 1
        seen.add(slug)
        updates.append((slug, str(pk)))
    with conn.cursor() as cursor:
        for slug, pk in updates:
            cursor.execute('UPDATE international_xorijlik_professor SET slug = %s WHERE id = %s', [slug, pk])


def add_columns(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == 'postgresql':
        schema_editor.execute("ALTER TABLE international_xalqaro_reyting_bolim ADD COLUMN IF NOT EXISTS slug varchar(450) NOT NULL DEFAULT '';")
        schema_editor.execute("ALTER TABLE international_xorijlik_professor ADD COLUMN IF NOT EXISTS slug varchar(350) NOT NULL DEFAULT '';")
    else:
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(international_xalqaro_reyting_bolim)")
            if 'slug' not in [r[1] for r in cursor.fetchall()]:
                schema_editor.execute("ALTER TABLE international_xalqaro_reyting_bolim ADD COLUMN slug varchar(450) NOT NULL DEFAULT '';")
            cursor.execute("PRAGMA table_info(international_xorijlik_professor)")
            if 'slug' not in [r[1] for r in cursor.fetchall()]:
                schema_editor.execute("ALTER TABLE international_xorijlik_professor ADD COLUMN slug varchar(350) NOT NULL DEFAULT '';")


def add_unique_indexes(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == 'postgresql':
        schema_editor.execute("""
            DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE tablename='international_xalqaro_reyting_bolim' AND indexname='intl_reyting_bolim_slug_uniq') THEN
                    ALTER TABLE international_xalqaro_reyting_bolim ADD CONSTRAINT intl_reyting_bolim_slug_uniq UNIQUE (slug);
                END IF;
            END$$;
        """)
        schema_editor.execute("""
            DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_indexes WHERE tablename='international_xorijlik_professor' AND indexname='intl_xorijlik_professor_slug_uniq') THEN
                    ALTER TABLE international_xorijlik_professor ADD CONSTRAINT intl_xorijlik_professor_slug_uniq UNIQUE (slug);
                END IF;
            END$$;
        """)
    else:
        schema_editor.execute("CREATE UNIQUE INDEX IF NOT EXISTS intl_reyting_bolim_slug_uniq ON international_xalqaro_reyting_bolim (slug);")
        schema_editor.execute("CREATE UNIQUE INDEX IF NOT EXISTS intl_xorijlik_professor_slug_uniq ON international_xorijlik_professor (slug);")


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0017_add_slug_to_akademik_almashinuv'),
    ]

    operations = [
        migrations.RunPython(add_columns, migrations.RunPython.noop),
        migrations.RunPython(generate_reyting_slugs, migrations.RunPython.noop),
        migrations.RunPython(generate_professor_slugs, migrations.RunPython.noop),
        migrations.RunPython(add_unique_indexes, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='xalqaroreytingbolim',
                    name='slug',
                    field=models.SlugField(blank=True, max_length=450, unique=True, verbose_name='Slug'),
                ),
                migrations.AddField(
                    model_name='xorijlikprofessor',
                    name='slug',
                    field=models.SlugField(blank=True, max_length=350, unique=True, verbose_name='Slug'),
                ),
            ],
            database_operations=[],
        ),
    ]
