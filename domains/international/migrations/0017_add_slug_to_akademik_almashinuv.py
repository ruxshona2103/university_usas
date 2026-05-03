from django.db import migrations, models, connection
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    conn = schema_editor.connection
    with conn.cursor() as cursor:
        cursor.execute('SELECT id, title_uz FROM international_akademik_almashinuv ORDER BY "order", id')
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
            cursor.execute(
                'UPDATE international_akademik_almashinuv SET slug = %s WHERE id = %s',
                [slug, pk],
            )


def add_slug_column(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == 'postgresql':
        schema_editor.execute("""
            ALTER TABLE international_akademik_almashinuv
            ADD COLUMN IF NOT EXISTS slug varchar(450) NOT NULL DEFAULT '';
        """)
    else:
        # SQLite: tekshirib qo'shamiz
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(international_akademik_almashinuv)")
            cols = [row[1] for row in cursor.fetchall()]
        if 'slug' not in cols:
            schema_editor.execute("""
                ALTER TABLE international_akademik_almashinuv
                ADD COLUMN slug varchar(450) NOT NULL DEFAULT '';
            """)


def add_unique_index(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == 'postgresql':
        schema_editor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_indexes
                    WHERE tablename = 'international_akademik_almashinuv'
                    AND indexname = 'intl_almashinuv_slug_uniq'
                ) THEN
                    ALTER TABLE international_akademik_almashinuv
                    ADD CONSTRAINT intl_almashinuv_slug_uniq UNIQUE (slug);
                END IF;
            END$$;
        """)
    else:
        schema_editor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS intl_almashinuv_slug_uniq
            ON international_akademik_almashinuv (slug);
        """)


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0016_add_slug_to_international_post'),
    ]

    operations = [
        migrations.RunPython(add_slug_column, migrations.RunPython.noop),
        migrations.RunPython(generate_slugs, migrations.RunPython.noop),
        migrations.RunPython(add_unique_index, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='akademikalmashinuv',
                    name='slug',
                    field=models.SlugField(blank=True, max_length=450, unique=True, verbose_name='Slug'),
                ),
            ],
            database_operations=[],
        ),
    ]
