from django.db import migrations


# ── Frontend tomonidan ishlatiladigan barcha category slug'lar ────────────────
# RectorAppealSidebarCard  → category="rektorat"
# FaxrlarCategoryPage      → graduates / faxrli-ustozlar / ilgor-olimlarimiz / uzsa-yulduzlari

ROOT_CATEGORIES = [
    {
        'slug': 'rektorat',
        'title_uz': 'Rektorat',
        'title_ru': 'Ректорат',
        'title_en': 'Rectorate',
        'order': 1,
    },
    {
        'slug': 'faxrlarimiz',
        'title_uz': "Faxrlarimiz",
        'title_ru': 'Наша гордость',
        'title_en': 'Our Pride',
        'order': 2,
    },
]

# "faxrlarimiz" ning bolalari  (parent = faxrlarimiz)
CHILD_CATEGORIES = [
    {
        'slug': 'bitiruvchilar',
        'title_uz': 'Bitiruvchilar',
        'title_ru': 'Выпускники',
        'title_en': 'Graduates',
        'order': 1,
        'parent_slug': 'faxrlarimiz',
    },
    {
        'slug': 'faxrli-ustozlar',
        'title_uz': "Faxrli ustozlar",
        'title_ru': 'Почётные преподаватели',
        'title_en': 'Honorary Teachers',
        'order': 2,
        'parent_slug': 'faxrlarimiz',
    },
    {
        'slug': 'ilgor-olimlarimiz',
        'title_uz': "Ilg'or olimlarimiz",
        'title_ru': 'Ведущие учёные',
        'title_en': 'Distinguished Scientists',
        'order': 3,
        'parent_slug': 'faxrlarimiz',
    },
    {
        'slug': 'uzsa-yulduzlari',
        'title_uz': "UZSA yulduzlari",
        'title_ru': 'Звёзды UZSA',
        'title_en': 'UZSA Stars',
        'order': 4,
        'parent_slug': 'faxrlarimiz',
    },
]


def seed(apps, schema_editor):
    PersonCategory = apps.get_model('students', 'PersonCategory')

    # 1. Root kategoriyalar
    for cat in ROOT_CATEGORIES:
        PersonCategory.objects.get_or_create(
            slug=cat['slug'],
            defaults={
                'title_uz': cat['title_uz'],
                'title_ru': cat['title_ru'],
                'title_en': cat['title_en'],
                'order':    cat['order'],
            },
        )

    # 2. Bola kategoriyalar
    for cat in CHILD_CATEGORIES:
        parent = PersonCategory.objects.filter(slug=cat['parent_slug']).first()
        PersonCategory.objects.get_or_create(
            slug=cat['slug'],
            defaults={
                'title_uz': cat['title_uz'],
                'title_ru': cat['title_ru'],
                'title_en': cat['title_en'],
                'order':    cat['order'],
                'parent':   parent,
            },
        )


def unseed(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0022_magistrtalaba_name_supervisor_multilang'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
