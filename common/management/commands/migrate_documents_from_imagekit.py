"""
ImageKit'dagi document fayllarni (PDF/DOC) lokal `media/` papkasiga ko'chirib,
DB'dagi `LinkBlock.document_file` qiymatlarini yangi (lokal) yo'lga yangilaydi.

Ishlatish:
    # Quruq ishga tushirish (faqat ko'rsatadi, hech narsa o'zgartirmaydi):
    python manage.py migrate_documents_from_imagekit --dry-run

    # Haqiqiy migratsiya:
    python manage.py migrate_documents_from_imagekit

    # Faqat bitta yozuvni sinash:
    python manage.py migrate_documents_from_imagekit --id <linkblock-uuid>

    # ImageKit'dagi 403 muammosini chetlab o'tish — admin API orqali yuklash:
    python manage.py migrate_documents_from_imagekit --use-admin-api
"""
import os
import urllib.parse
from pathlib import Path

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from domains.pages.models import LinkBlock


class Command(BaseCommand):
    help = "Document fayllarni ImageKit'dan lokal storage'ga ko'chiradi"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Hech narsa o'zgartirmasdan, nima qilinishini ko'rsatadi",
        )
        parser.add_argument(
            "--id",
            type=str,
            default=None,
            help="Faqat bitta LinkBlock UUID'sini ko'chirish",
        )
        parser.add_argument(
            "--use-admin-api",
            action="store_true",
            help=(
                "ImageKit Admin API orqali yuklab oladi (PRIVATE_KEY ishlatadi). "
                "403 muammosini chetlab o'tadi."
            ),
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        target_id = options["id"]
        use_admin_api = options["use_admin_api"]

        qs = LinkBlock.objects.exclude(document_file="").exclude(
            document_file__isnull=True
        )
        if target_id:
            qs = qs.filter(id=target_id)

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("Ko'chiriladigan fayl topilmadi."))
            return

        self.stdout.write(
            self.style.NOTICE(f"Topildi: {total} ta yozuv. Boshlanmoqda...\n")
        )

        media_root = Path(settings.MEDIA_ROOT)
        media_root.mkdir(parents=True, exist_ok=True)

        # ImageKit private key (admin API uchun)
        private_key = os.getenv("IMAGEKIT_PRIVATE_KEY", "")
        auth = None
        if use_admin_api and private_key:
            # Basic auth: PRIVATE_KEY:
            auth = (private_key, "")

        ok = 0
        fail = 0
        skipped = 0

        for obj in qs.iterator():
            name = obj.document_file.name  # e.g. "documents/2026/05/file.doc"
            self.stdout.write(f"\n[{obj.pk}] {name}")

            # 1) URL ni olish (storage backend qaysi bo'lsa ham)
            try:
                file_url = obj.document_file.url
            except Exception as exc:
                self.stdout.write(self.style.ERROR(f"  URL olib bo'lmadi: {exc}"))
                fail += 1
                continue

            self.stdout.write(f"  URL: {file_url}")

            # 2) Lokal yo'l aniqlash
            # `name` ko'rinishi: documents/2026/05/file.doc
            local_path = media_root / name
            if local_path.exists() and local_path.stat().st_size > 0:
                self.stdout.write(
                    self.style.WARNING(f"  Lokal'da allaqachon mavjud: {local_path}")
                )
                skipped += 1
                continue

            if dry_run:
                self.stdout.write(
                    self.style.NOTICE(f"  [DRY-RUN] Yuklanadi: {local_path}")
                )
                continue

            # 3) Faylni yuklab olish
            try:
                resp = requests.get(file_url, timeout=60, auth=auth)
                if resp.status_code == 403 and not use_admin_api and private_key:
                    # Admin API bilan qayta urinish
                    self.stdout.write(
                        self.style.WARNING(
                            "  403 — admin API (PRIVATE_KEY) bilan qayta urinilyapti..."
                        )
                    )
                    resp = requests.get(file_url, timeout=60, auth=(private_key, ""))
                resp.raise_for_status()
            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(f"  Yuklab bo'lmadi: {exc}")
                )
                fail += 1
                continue

            # 4) Lokal'ga yozish
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(resp.content)
            size_kb = len(resp.content) / 1024
            self.stdout.write(
                self.style.SUCCESS(f"  Saqlandi: {local_path} ({size_kb:.1f} KB)")
            )

            # 5) DB'da `name` o'zgarmaydi (relative path bir xil), lekin
            # storage backend o'zgargani uchun .url endi lokal'dan kelishi kerak.
            # Eski yozuv'ni qaytadan saqlash kerak emas — fayl path o'sha bo'lib turibdi.
            ok += 1

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"Muvaffaqiyatli: {ok}"))
        self.stdout.write(self.style.WARNING(f"O'tkazib yuborildi: {skipped}"))
        if fail:
            self.stdout.write(self.style.ERROR(f"Xato: {fail}"))
        self.stdout.write("=" * 50)

        if not dry_run and ok > 0:
            self.stdout.write(
                "\nKeyingi qadam: download endpoint endi lokal fayllarni stream qiladi.\n"
                "Tekshirish uchun: GET /api/meyoriy-hujjatlar/<id>/download/"
            )
