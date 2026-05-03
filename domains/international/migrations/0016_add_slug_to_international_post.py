from django.db import migrations, models
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    conn = schema_editor.connection
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, title_uz FROM international_post ORDER BY date, id")
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
                "UPDATE international_post SET slug = %s WHERE id = %s",
                [slug, pk],
            )


def add_slug_column(apps, schema_editor):
    schema_editor.execute("""
        ALTER TABLE international_post
        ADD COLUMN IF NOT EXISTS slug varchar(350) NOT NULL DEFAULT '';
    """)


def add_unique_index(apps, schema_editor):
    schema_editor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_indexes
                WHERE tablename = 'international_post'
                AND indexname = 'international_post_slug_key'
            ) THEN
                ALTER TABLE international_post
                ADD CONSTRAINT international_post_slug_key UNIQUE (slug);
            END IF;
        END$$;
    """)
    schema_editor.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_indexes
                WHERE tablename = 'international_post'
                AND indexname = 'international_post_slug_c2ce17b7_like'
            ) THEN
                CREATE INDEX international_post_slug_c2ce17b7_like
                ON international_post (slug varchar_pattern_ops);
            END IF;
        END$$;
    """)


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0015_xorijlikprofessor'),
    ]

    operations = [
        migrations.RunPython(add_slug_column, migrations.RunPython.noop),
        migrations.RunPython(generate_slugs, migrations.RunPython.noop),
        migrations.RunPython(add_unique_index, migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='internationalpost',
                    name='slug',
                    field=models.SlugField(blank=True, max_length=350, unique=True, verbose_name='Slug'),
                ),
            ],
            database_operations=[],
        ),
    ]
