"""
python manage.py seed_oquv_rejalari --dir "C:/Users/user/Desktop/OʻzDSA Oʻquv-faoliyat hujjatlari/Oʻquv rejalar"

O'quv rejalari → Bakalavr va Magistratura bo'limlariga PDF fayllarni qo'shadi.
Mavjud ma'lumotlarni o'chirmaydi.
"""

import os

from django.core.files import File
from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

# Papka nomi → (child slug suffix, uz title, ru title, en title, order)
BLOCKS = {
    "Bakalavr": {
        "slug_suffix": "bakalavriat",
        "title_uz": "Bakalavriat",
        "title_ru": "Бакалавриат",
        "title_en": "Bachelor",
        "order": 1,
        "labels": {
            "61010200 Sport faoliyati.pdf":   "61010200 — Sport faoliyati (Bakalavr)",
            "Parasport Bakalavr.pdf":         "Adaptiv jismoniy tarbiya — Parasport (Bakalavr)",
            "sport menejmenti Bakalavr.pdf":  "Sport menejmenti (Bakalavr)",
        },
    },
    "Magistratura": {
        "slug_suffix": "magistratura",
        "title_uz": "Magistratura",
        "title_ru": "Магистратура",
        "title_en": "Master",
        "order": 2,
        "labels": {
            "Adaptiv Magistr.pdf":         "Adaptiv jismoniy tarbiya (Magistratura)",
            "MArketing Magistr.pdf":        "Marketing (Magistratura)",
            "Menejment magistr.pdf":        "Menejment (Magistratura)",
            "Psixologiya Magistr.pdf":      "Psixologiya (Magistratura)",
            "Sport huquqi Magistr.pdf":     "Sport huquqi (Magistratura)",
            "sport faoliyati magistr.pdf":  "Sport faoliyati (Magistratura)",
        },
    },
}


class Command(BaseCommand):
    help = "O'quv rejalari PDF larini DB ga qo'shadi (mavjudlarini o'chirmaydi)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir',
            required=True,
            help="O'quv rejalari papkasi yo'li (Bakalavr va Magistratura subpapkalar bilan)",
        )

    def handle(self, *args, **options):
        root_dir = options['dir']

        if not os.path.isdir(root_dir):
            self.stdout.write(self.style.ERROR(f"Papka topilmadi: {root_dir}"))
            return

        try:
            root_cat = IlmiyFaoliyatCategory.objects.get(slug='oquv-rejalari')
        except IlmiyFaoliyatCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "'oquv-rejalari' kategoriyasi topilmadi! "
                "Avval: python manage.py seed_oquv_faoliyat"
            ))
            return

        self.stdout.write(f"[Topildi] Root kategoriya: {root_cat.title_uz}")

        total_added = 0
        total_skipped = 0

        for folder_name, block in BLOCKS.items():
            block_dir = os.path.join(root_dir, folder_name)
            if not os.path.isdir(block_dir):
                self.stdout.write(self.style.WARNING(f"  [O'tkazildi] Papka yo'q: {block_dir}"))
                continue

            child_slug = f"oquv-rejalari-{block['slug_suffix']}"
            child_cat, created = IlmiyFaoliyatCategory.objects.get_or_create(
                slug=child_slug,
                defaults={
                    'title_uz': block['title_uz'],
                    'title_ru': block['title_ru'],
                    'title_en': block['title_en'],
                    'parent':   root_cat,
                    'order':    block['order'],
                },
            )
            action = 'Yaratildi' if created else 'Mavjud'
            self.stdout.write(f"\n  [{action}] Child: {child_cat.title_uz}")

            last_order = (
                IlmiyFaoliyat.objects.filter(category=child_cat)
                .order_by('-order')
                .values_list('order', flat=True)
                .first()
            )
            next_order = (last_order or 0) + 1

            for filename in sorted(os.listdir(block_dir)):
                if not filename.lower().endswith('.pdf'):
                    continue

                label = block['labels'].get(filename, os.path.splitext(filename)[0].strip())
                filepath = os.path.join(block_dir, filename)

                if IlmiyFaoliyat.objects.filter(category=child_cat, title_uz=label).exists():
                    self.stdout.write(f"    [Mavjud]  {label[:80]}")
                    total_skipped += 1
                    continue

                item = IlmiyFaoliyat(
                    category=child_cat,
                    title_uz=label,
                    order=next_order,
                    is_active=True,
                )
                with open(filepath, 'rb') as f:
                    item.file.save(filename, File(f), save=False)
                item.save()

                self.stdout.write(self.style.SUCCESS(f"    [Qo'shildi] {label[:80]}"))
                total_added += 1
                next_order += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nTugadi: {total_added} ta qo'shildi, {total_skipped} ta mavjud edi."
        ))
