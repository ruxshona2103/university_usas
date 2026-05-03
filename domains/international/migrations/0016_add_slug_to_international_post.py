from django.db import migrations, models
from django.utils.text import slugify


def generate_slugs(apps, schema_editor):
    InternationalPost = apps.get_model('international', 'InternationalPost')
    seen = set()
    for post in InternationalPost.objects.all().order_by('date', 'id'):
        base = slugify(post.title_uz, allow_unicode=True) or str(post.id)
        slug = base
        n = 1
        while slug in seen:
            slug = f'{base}-{n}'
            n += 1
        seen.add(slug)
        post.slug = slug
        post.save(update_fields=['slug'])


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
                ALTER TABLE international_post ADD CONSTRAINT international_post_slug_key UNIQUE (slug);
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
