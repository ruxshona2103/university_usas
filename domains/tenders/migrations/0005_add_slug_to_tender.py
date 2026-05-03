from django.db import migrations, models


def add_slugs(apps, schema_editor):
    vendor = schema_editor.connection.vendor
    if vendor == 'postgresql':
        schema_editor.execute("""
            UPDATE tenders_announcement
            SET slug = LOWER(REGEXP_REPLACE(
                REGEXP_REPLACE(title_uz, '[^\\w\\s-]', '', 'g'),
                '\\s+', '-', 'g'
            ))
            WHERE slug = '' OR slug IS NULL
        """)
        schema_editor.execute("""
            WITH duplicates AS (
                SELECT id,
                       slug,
                       ROW_NUMBER() OVER (PARTITION BY slug ORDER BY id) AS rn
                FROM tenders_announcement
                WHERE slug != ''
            )
            UPDATE tenders_announcement
            SET slug = d.slug || '-' || (d.rn - 1)::text
            FROM duplicates d
            WHERE tenders_announcement.id = d.id AND d.rn > 1
        """)
    else:
        from django.apps import apps as django_apps
        import re
        model = django_apps.get_model('tenders', 'TenderAnnouncement')
        for obj in model.objects.filter(slug=''):
            base = re.sub(r'\s+', '-', re.sub(r'[^\w\s-]', '', (obj.title_uz or '').lower())).strip('-') or str(obj.pk)
            slug = base
            n = 1
            while model.objects.filter(slug=slug).exclude(pk=obj.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            model.objects.filter(pk=obj.pk).update(slug=slug)


class Migration(migrations.Migration):

    dependencies = [
        ('tenders', '0004_add_announcement_type'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="ALTER TABLE tenders_announcement ADD COLUMN IF NOT EXISTS slug VARCHAR(550) NOT NULL DEFAULT ''",
                    reverse_sql="ALTER TABLE tenders_announcement DROP COLUMN IF EXISTS slug",
                ),
                migrations.RunPython(add_slugs, migrations.RunPython.noop),
                migrations.RunSQL(
                    sql="CREATE UNIQUE INDEX IF NOT EXISTS tenders_announcement_slug_uniq ON tenders_announcement (slug)",
                    reverse_sql="DROP INDEX IF EXISTS tenders_announcement_slug_uniq",
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name='tenderannouncement',
                    name='slug',
                    field=models.SlugField(blank=True, max_length=550, unique=True, verbose_name='Slug'),
                ),
            ],
        ),
    ]
