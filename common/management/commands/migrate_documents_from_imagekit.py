"""
ImageKit'dagi document fayllarni (PDF/DOC) lokal `media/` papkasiga ko'chirib,
DB'dagi `LinkBlock.document_file` qiymatlarini yangi (lokal) yo'lga yangilaydi.

DB'da `document_file.name` ImageKit'ning ichki **file_id** ko'rinishida saqlanadi
(masalan: `69f724e35c7cd75eb891e80b`). Skript ImageKit Admin API orqali har bir
file_id ga mos haqiqiy fayl URL'ini topadi, faylni yuklab oladi va lokal
`media/documents/YYYY/MM/<original_filename>` ga saqlaydi. So'ng DB'dagi
`document_file.name` ni yangi lokal yo'lga yangilaydi.

Ishlatish:
    # Quruq ishga tushirish (hech narsa o'zgartirmaydi):
    python manage.py migrate_documents_from_imagekit --dry-run

    # Haqiqiy migratsiya:
    python manage.py migrate_documents_from_imagekit

    # Faqat bitta yozuvni sinash:
    python manage.py migrate_documents_from_imagekit --id <linkblock-uuid>
"""
import datetime
import os
from pathlib import Path

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from domains.pages.models import LinkBlock


IMAGEKIT_API_BASE = "https://api.imagekit.io/v1"


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

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        target_id = options["id"]

        private_key = os.getenv("IMAGEKIT_PRIVATE_KEY", "").strip()
        if not private_key:
            self.stdout.write(
                self.style.ERROR(
                    ".env'da IMAGEKIT_PRIVATE_KEY topilmadi — admin API'ga "
                    "ulanib bo'lmaydi."
                )
            )
            return

        auth = (private_key, "")

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

        ok = 0
        fail = 0
        skipped = 0

        for obj in qs.iterator():
            stored_name = obj.document_file.name
            self.stdout.write(f"\n[{obj.pk}] DB name: {stored_name}")

            # 1) ImageKit'dan file_id orqali metadata olish
            #    GET https://api.imagekit.io/v1/files/<fileId>/details
            try:
                meta_resp = requests.get(
                    f"{IMAGEKIT_API_BASE}/files/{stored_name}/details",
                    auth=auth,
                    timeout=30,
                )
                if meta_resp.status_code == 404:
                    self.stdout.write(
                        self.style.ERROR(
                            f"  ImageKit'da topilmadi (404): {stored_name}"
                        )
                    )
                    fail += 1
                    continue
                meta_resp.raise_for_status()
                meta = meta_resp.json()
            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(f"  Metadata olib bo'lmadi: {exc}")
                )
                fail += 1
                continue

            file_url = meta.get("url")
            file_path = (meta.get("filePath") or "").lstrip("/")
            file_name = meta.get("name") or os.path.basename(file_path)
            created_at = meta.get("createdAt", "")

            self.stdout.write(f"  ImageKit URL:  {file_url}")
            self.stdout.write(f"  ImageKit path: {file_path}")
            self.stdout.write(f"  Original name: {file_name}")

            # 2) Lokal yo'l aniqlash — created_at dan YYYY/MM olish
            year_month = "unknown"
            if created_at:
                try:
                    dt = datetime.datetime.fromisoformat(
                        created_at.replace("Z", "+00:00")
                    )
                    year_month = dt.strftime("%Y/%m")
                except Exception:
                    pass

            new_relative = f"documents/{year_month}/{file_name}"
            local_path = media_root / new_relative

            # Agar shu nom band bo'lsa — counter qo'shish
            if local_path.exists() and local_path.stat().st_size > 0:
                stem, ext = os.path.splitext(file_name)
                n = 1
                while local_path.exists():
                    candidate = f"{stem}_{n}{ext}"
                    local_path = media_root / f"documents/{year_month}/{candidate}"
                    new_relative = f"documents/{year_month}/{candidate}"
                    n += 1

            self.stdout.write(f"  Lokal yo'l:    {local_path}")

            if dry_run:
                self.stdout.write(
                    self.style.NOTICE("  [DRY-RUN] Hech narsa qilinmadi")
                )
                continue

            # 3) Faylni yuklab olish (admin API'dan, 403'ni chetlab o'tadi)
            try:
                resp = requests.get(file_url, timeout=120, auth=auth)
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
                self.style.SUCCESS(
                    f"  Saqlandi ({size_kb:.1f} KB)"
                )
            )

            # 5) DB'da name'ni yangi lokal yo'lga yangilash
            obj.document_file.name = new_relative
            obj.save(update_fields=["document_file"])
            self.stdout.write(
                self.style.SUCCESS(f"  DB yangilandi: name → {new_relative}")
            )
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
