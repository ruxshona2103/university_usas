from django.db import migrations
from django.utils.text import slugify


def forward(apps, schema_editor):
    db = schema_editor.connection
    vendor = db.vendor  # 'postgresql' | 'sqlite3'

    # ── 1. slug column qo'shamiz ──────────────────────────────────────────────
    with db.cursor() as c:
        if vendor == 'postgresql':
            c.execute(
                "ALTER TABLE pages_org_node "
                "ADD COLUMN IF NOT EXISTS slug varchar(220) NOT NULL DEFAULT ''"
            )
        else:
            c.execute("PRAGMA table_info(pages_org_node)")
            cols = [row[1] for row in c.fetchall()]
            if 'slug' not in cols:
                c.execute(
                    "ALTER TABLE pages_org_node "
                    "ADD COLUMN slug varchar(220) NOT NULL DEFAULT ''"
                )

    # ── 2. Slug qiymatlarini to'ldiramiz ──────────────────────────────────────
    with db.cursor() as c:
        c.execute('SELECT id, name_uz FROM pages_org_node ORDER BY "order"')
        rows = c.fetchall()

    used = set()
    updates = []
    for node_id, name_uz in rows:
        base = slugify(name_uz or '') or f'node-{str(node_id)[:8]}'
        slug, n = base, 1
        while slug in used:
            slug = f'{base}-{n}'
            n += 1
        used.add(slug)
        updates.append((slug, node_id))

    if updates:
        with db.cursor() as c:
            for slug, node_id in updates:
                c.execute(
                    "UPDATE pages_org_node SET slug = %s WHERE id = %s",
                    [slug, node_id],
                )

    # ── 3. Unique index va LIKE index (idempotent) ────────────────────────────
    with db.cursor() as c:
        if vendor == 'postgresql':
            c.execute("DROP INDEX IF EXISTS pages_org_node_slug_c1545551_like")
            c.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS pages_org_node_slug_uniq "
                "ON pages_org_node (slug)"
            )
            c.execute(
                "CREATE INDEX IF NOT EXISTS pages_org_node_slug_c1545551_like "
                "ON pages_org_node (slug varchar_pattern_ops)"
            )
        else:
            c.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS pages_org_node_slug_uniq "
                "ON pages_org_node (slug)"
            )


def backward(apps, schema_editor):
    db = schema_editor.connection
    with db.cursor() as c:
        if db.vendor == 'postgresql':
            c.execute("DROP INDEX IF EXISTS pages_org_node_slug_uniq")
            c.execute("DROP INDEX IF EXISTS pages_org_node_slug_c1545551_like")
            c.execute("ALTER TABLE pages_org_node DROP COLUMN IF EXISTS slug")
        else:
            c.execute("DROP INDEX IF EXISTS pages_org_node_slug_uniq")


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_seed_org_structure'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
