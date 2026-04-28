"""
python manage.py seed_oquv_grafigi --dir "C:/Users/user/Desktop/OʻzDSA Oʻquv-faoliyat hujjatlari/Oʻquv grafigi"

O'quv grafigi bo'limiga PDF fayllarni qo'shadi.
Mavjud ma'lumotlarni o'chirmaydi.
"""

import os

from django.core.files import File
from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

LABELS = {
    "Oʻquv jarayon grafigi.pdf": "O'quv jarayon grafigi",
}


class Command(BaseCommand):
    help = "O'quv grafigi PDF larini DB ga qo'shadi (mavjudlarini o'chirmaydi)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir',
            required=True,
            help="O'quv grafigi PDF fayllar joylashgan papka yo'li",
        )

    def handle(self, *args, **options):
        pdf_dir = options['dir']

        if not os.path.isdir(pdf_dir):
            self.stdout.write(self.style.ERROR(f"Papka topilmadi: {pdf_dir}"))
            return

        try:
            root_cat = IlmiyFaoliyatCategory.objects.get(slug='oquv-grafigi')
        except IlmiyFaoliyatCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "'oquv-grafigi' kategoriyasi topilmadi! "
                "Avval: python manage.py seed_oquv_faoliyat"
            ))
            return

        self.stdout.write(f"[Topildi] Root kategoriya: {root_cat.title_uz}")

        last_order = (
            IlmiyFaoliyat.objects.filter(category=root_cat)
            .order_by('-order')
            .values_list('order', flat=True)
            .first()
        )
        next_order = (last_order or 0) + 1

        added = 0
        skipped = 0

        for filename in sorted(os.listdir(pdf_dir)):
            if not filename.lower().endswith('.pdf'):
                continue

            label = LABELS.get(filename, os.path.splitext(filename)[0].strip())
            filepath = os.path.join(pdf_dir, filename)

            if IlmiyFaoliyat.objects.filter(category=root_cat, title_uz=label).exists():
                self.stdout.write(f"  [Mavjud]  {label[:80]}")
                skipped += 1
                continue

            item = IlmiyFaoliyat(
                category=root_cat,
                title_uz=label,
                order=next_order,
                is_active=True,
            )
            with open(filepath, 'rb') as f:
                item.file.save(filename, File(f), save=False)
            item.save()

            self.stdout.write(self.style.SUCCESS(f"  [Qo'shildi] {label[:80]}"))
            added += 1
            next_order += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nTugadi: {added} ta qo'shildi, {skipped} ta mavjud edi."
        ))
