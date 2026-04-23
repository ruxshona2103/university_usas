from django.db import migrations


REDIRECT_URL_MAP = {
    # Faoliyat — kategoriya slug bo'yicha filtrlanadi
    'faoliyat-sport':     '/api/activities/faoliyat/?category=sport-faoliyat',
    'faoliyat-ilmiy':     '/api/activities/faoliyat/?category=ilmiy-faoliyat',
    'faoliyat-oquv':      '/api/activities/faoliyat/?category=oquv-faoliyat',
    'faoliyat-manaviy':   '/api/activities/faoliyat/?category=manaviy-faoliyat',
    'faoliyat-moliyaviy': '/api/activities/faoliyat/?category=moliyaviy-faoliyat',

    # Yangiliklar
    'ax-news': '/api/news/',
    'st-news':  '/api/news/',
}


def fix_redirect_urls(apps, schema_editor):
    NavbarSubItem = apps.get_model('pages', 'NavbarSubItem')
    for slug, api_url in REDIRECT_URL_MAP.items():
        NavbarSubItem.objects.filter(slug=slug).update(redirect_url=api_url)


def reverse_redirect_urls(apps, schema_editor):
    NavbarSubItem = apps.get_model('pages', 'NavbarSubItem')
    old_urls = {
        'faoliyat-sport':     '/faoliyat/sport',
        'faoliyat-ilmiy':     '/faoliyat/ilmiy',
        'faoliyat-oquv':      '/faoliyat/oquv',
        'faoliyat-manaviy':   '/faoliyat/manaviy',
        'faoliyat-moliyaviy': '/faoliyat/moliyaviy',
        'ax-news': '/news',
        'st-news':  '/news',
    }
    for slug, old_url in old_urls.items():
        NavbarSubItem.objects.filter(slug=slug).update(redirect_url=old_url)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_redirect_urls, reverse_code=reverse_redirect_urls),
    ]
