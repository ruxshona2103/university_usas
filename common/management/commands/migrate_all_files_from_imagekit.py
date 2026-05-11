"""
ImageKit'dagi BARCHA fayllarni (rasm, video, hujjat) lokal `media/` papkasiga
ko'chiradi va DB'dagi har bir FileField/ImageField qiymatini yangi (lokal)
yo'lga yangilaydi.

Storage backend (PatchedMediaImagekitStorage) DB'da fayl nomi sifatida
ImageKit'ning ichki **file_id** (24 hex belgi, masalan: `69f724e35c7cd75eb891e80b`)
saqlaydi. Skript har bir file_id uchun:

  1) ImageKit Admin API'dan metadata (url, filePath, name, createdAt) oladi
  2) Faylni yuklab oladi (private_key bilan, 403 bo'lmaydi)
  3) `media/<upload_to_pattern>/<original_filename>` ga yozadi
  4) DB'dagi FieldFile.name ni yangi lokal yo'lga yangilaydi

Lokal yo'l qoidasi:
  - Modeldagi `upload_to` papkasi olinadi (masalan, 'tenders/%Y/%m/').
  - `%Y/%m` ImageKit'dagi `createdAt` dan to'ldiriladi (yo'q bo'lsa: 'unknown').
  - Fayl nomi mavjud bo'lsa, `_1`, `_2` qo'shiladi (overwrite emas).

Ishlatish:

    # Quruq ishga tushirish — hech narsa o'zgartirmaydi, faqat reja:
    python manage.py migrate_all_files_from_imagekit --dry-run

    # Haqiqiy migratsiya — hamma model'lar bo'yicha:
    python manage.py migrate_all_files_from_imagekit

    # Faqat bitta app'ni ko'chirish:
    python manage.py migrate_all_files_from_imagekit --app news

    # Faqat bitta model:
    python manage.py migrate_all_files_from_imagekit --model news.Article

    # Skip qilingan/xatolikka uchragan fayllarni qayta urinish:
    python manage.py migrate_all_files_from_imagekit --retry-failed
"""
import datetime
import os
import re
import time
from pathlib import Path

import requests
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models, transaction


IMAGEKIT_API_BASE = "https://api.imagekit.io/v1"

# ImageKit file_id: 24-belgi hex (MongoDB ObjectId formatida)
FILE_ID_RE = re.compile(r"^[a-f0-9]{24}$")


class Command(BaseCommand):
    help = (
        "Loyihadagi barcha FileField/ImageField qiymatlarini ImageKit'dan "
        "lokal media/ ga ko'chiradi va DB'ni yangilaydi."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Hech narsa o'zgartirmasdan, nima qilinishini ko'rsatadi",
        )
        parser.add_argument(
            "--app",
            type=str,
            default=None,
            help="Faqat shu app_label ichidagi modellarni ko'chirish "
                 "(masalan: --app news)",
        )
        parser.add_argument(
            "--model",
            type=str,
            default=None,
            help="Faqat bitta model: 'app_label.ModelName' (masalan: --model news.Article)",
        )
        parser.add_argument(
            "--sleep",
            type=float,
            default=0.1,
            help="Har bir fayldan keyin kutish (sekund). ImageKit rate limit uchun. Default 0.1",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Eng ko'pi bilan shuncha faylni ko'chirish (0 = cheklov yo'q)",
        )

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        self.sleep = options["sleep"]
        only_app = options["app"]
        only_model = options["model"]
        limit = options["limit"]

        private_key = os.getenv("IMAGEKIT_PRIVATE_KEY", "").strip()
        if not private_key:
            self.stderr.write(
                self.style.ERROR(
                    "IMAGEKIT_PRIVATE_KEY topilmadi. .env yoki environment'ni tekshiring."
                )
            )
            return

        self.auth = (private_key, "")
        self.media_root = Path(settings.MEDIA_ROOT)
        self.media_root.mkdir(parents=True, exist_ok=True)

        # 1) Barcha file/image field'larni topish
        field_specs = self._collect_file_fields(only_app=only_app, only_model=only_model)
        if not field_specs:
            self.stderr.write(
                self.style.WARNING("Hech qanday FileField/ImageField topilmadi.")
            )
            return

        self.stdout.write(
            self.style.NOTICE(
                f"Topildi: {len(field_specs)} ta field. Boshlanmoqda...\n"
            )
        )

        # Statistika
        totals = {"ok": 0, "fail": 0, "skipped_local": 0, "skipped_empty": 0, "not_found": 0}
        processed = 0

        for spec in field_specs:
            model = spec["model"]
            field_name = spec["field_name"]
            upload_to = spec["upload_to"]
            label = f"{model._meta.app_label}.{model.__name__}.{field_name}"

            qs = model.objects.exclude(**{field_name: ""}).exclude(
                **{f"{field_name}__isnull": True}
            )
            count = qs.count()
            if count == 0:
                continue

            self.stdout.write(
                self.style.NOTICE(f"\n=== {label} — {count} ta yozuv ===")
            )

            for obj in qs.iterator():
                if limit and processed >= limit:
                    self._print_summary(totals)
                    return

                file_field = getattr(obj, field_name)
                stored_name = file_field.name or ""
                if not stored_name:
                    totals["skipped_empty"] += 1
                    continue

                # Allaqachon lokal (slash bor yoki file_id formatida emas)
                if "/" in stored_name or not FILE_ID_RE.match(stored_name):
                    self.stdout.write(
                        f"  [{obj.pk}] {stored_name!r} — lokal yo'l, skip"
                    )
                    totals["skipped_local"] += 1
                    continue

                result = self._migrate_one(
                    obj=obj,
                    field_name=field_name,
                    file_id=stored_name,
                    upload_to=upload_to,
                )
                totals[result] = totals.get(result, 0) + 1
                processed += 1

                if self.sleep:
                    time.sleep(self.sleep)

        self._print_summary(totals)

    # ── helpers ──────────────────────────────────────────────────────────────

    def _collect_file_fields(self, only_app=None, only_model=None):
        """Loyihadagi barcha FileField/ImageField'larni topadi."""
        results = []
        for model in apps.get_models():
            label = model._meta.label  # 'app_label.ModelName'
            if only_app and model._meta.app_label != only_app:
                continue
            if only_model and label != only_model:
                continue

            for field in model._meta.get_fields():
                if isinstance(field, models.FileField):
                    results.append(
                        {
                            "model": model,
                            "field_name": field.name,
                            "upload_to": getattr(field, "upload_to", "") or "",
                        }
                    )
        return results

    def _resolve_upload_dir(self, upload_to, created_at_iso):
        """
        upload_to ni real yo'lga aylantiradi.

        Misol:
          'tenders/%Y/%m/'  +  '2024-08-15T12:00:00Z'  →  'tenders/2024/08'
          'partners/logos/'                            →  'partners/logos'
          callable                                     →  'misc'  (fallback)
        """
        if callable(upload_to):
            return "misc"

        path = str(upload_to or "").strip("/")
        if not path:
            return "misc"

        dt = None
        if created_at_iso:
            try:
                dt = datetime.datetime.fromisoformat(
                    created_at_iso.replace("Z", "+00:00")
                )
            except Exception:
                dt = None

        if dt:
            path = dt.strftime(path)
        else:
            # %Y, %m, %d larni 'unknown' ga almashtirish
            path = re.sub(r"%[YymdHMSj]", "unknown", path)

        return path.strip("/")

    def _migrate_one(self, obj, field_name, file_id, upload_to):
        """Bitta fayl uchun: metadata olish, yuklash, DB yangilash."""
        label = f"[{obj.__class__.__name__}#{obj.pk}.{field_name}]"

        # 1) Metadata
        try:
            meta_resp = requests.get(
                f"{IMAGEKIT_API_BASE}/files/{file_id}/details",
                auth=self.auth,
                timeout=30,
            )
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"{label} metadata so'rovi xato: {exc}"))
            return "fail"

        if meta_resp.status_code == 404:
            self.stderr.write(
                self.style.WARNING(f"{label} ImageKit'da topilmadi (404): {file_id}")
            )
            return "not_found"

        if not meta_resp.ok:
            self.stderr.write(
                self.style.ERROR(
                    f"{label} metadata {meta_resp.status_code}: {meta_resp.text[:200]}"
                )
            )
            return "fail"

        try:
            meta = meta_resp.json()
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"{label} JSON xato: {exc}"))
            return "fail"

        file_url = meta.get("url")
        file_name = meta.get("name") or os.path.basename(
            (meta.get("filePath") or "").lstrip("/")
        )
        created_at = meta.get("createdAt", "")

        if not file_url or not file_name:
            self.stderr.write(
                self.style.ERROR(f"{label} metadata'da url/name yo'q")
            )
            return "fail"

        # 2) Lokal yo'l
        upload_dir = self._resolve_upload_dir(upload_to, created_at)
        new_relative = f"{upload_dir}/{file_name}"
        local_path = self.media_root / new_relative

        # Konflikt — counter qo'shish
        if local_path.exists() and local_path.stat().st_size > 0:
            stem, ext = os.path.splitext(file_name)
            n = 1
            while True:
                candidate = f"{stem}_{n}{ext}"
                cand_rel = f"{upload_dir}/{candidate}"
                cand_path = self.media_root / cand_rel
                if not cand_path.exists():
                    local_path = cand_path
                    new_relative = cand_rel
                    break
                n += 1

        self.stdout.write(f"{label} {file_id} → {new_relative}")

        if self.dry_run:
            return "ok"

        # 3) Yuklab olish
        try:
            resp = requests.get(file_url, timeout=180, auth=self.auth, stream=True)
            resp.raise_for_status()
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"{label} yuklash xato: {exc}"))
            return "fail"

        # 4) Lokal'ga yozish
        local_path.parent.mkdir(parents=True, exist_ok=True)
        size = 0
        try:
            with open(local_path, "wb") as fh:
                for chunk in resp.iter_content(chunk_size=64 * 1024):
                    if chunk:
                        fh.write(chunk)
                        size += len(chunk)
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"{label} disk yozish xato: {exc}"))
            # Yarim yozilgan faylni o'chirish
            try:
                local_path.unlink(missing_ok=True)
            except Exception:
                pass
            return "fail"

        # 5) DB yangilash
        try:
            with transaction.atomic():
                file_field = getattr(obj, field_name)
                file_field.name = new_relative
                obj.save(update_fields=[field_name])
        except Exception as exc:
            self.stderr.write(self.style.ERROR(f"{label} DB yangilanmadi: {exc}"))
            return "fail"

        self.stdout.write(
            self.style.SUCCESS(f"  ✓ {size/1024:.1f} KB saqlandi, DB yangilandi")
        )
        return "ok"

    def _print_summary(self, totals):
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS(f"Muvaffaqiyatli (ok):  {totals.get('ok', 0)}"))
        self.stdout.write(self.style.WARNING(f"Topilmadi (404):      {totals.get('not_found', 0)}"))
        self.stdout.write(self.style.WARNING(f"Lokal (skip):         {totals.get('skipped_local', 0)}"))
        self.stdout.write(self.style.WARNING(f"Bo'sh (skip):         {totals.get('skipped_empty', 0)}"))
        if totals.get("fail"):
            self.stdout.write(self.style.ERROR(f"Xato (fail):          {totals['fail']}"))
        self.stdout.write("=" * 60)
        if self.dry_run:
            self.stdout.write(
                self.style.NOTICE(
                    "\nDRY-RUN — hech narsa o'zgarmadi. Haqiqiy ishga tushirish uchun "
                    "--dry-run ni olib tashlang."
                )
            )
