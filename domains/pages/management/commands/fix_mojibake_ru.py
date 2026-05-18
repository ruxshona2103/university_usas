from __future__ import annotations

from django.core.management.base import BaseCommand

from domains.pages.models import ContentBlock, NavbarSubItem


def looks_mojibake(text: str) -> bool:
    if not text:
        return False
    markers = ("Р", "С", "вЂ", "ѓ", "�")
    return any(m in text for m in markers)


def fix_text(text: str) -> str:
    if not text or not looks_mojibake(text):
        return text
    # Typical case: UTF-8 bytes were decoded as cp1251.
    for source_encoding in ("cp1251", "latin1"):
        try:
            repaired = text.encode(source_encoding).decode("utf-8")
            if repaired and repaired != text:
                return repaired
        except Exception:
            continue
    return text


class Command(BaseCommand):
    help = "Fix mojibake in Russian fields for NavbarSubItem and ContentBlock."

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Persist changes. Without this flag it runs as dry-run.",
        )

    def handle(self, *args, **options):
        apply_changes = bool(options.get("apply"))
        total_fixes = 0

        self.stdout.write(self.style.NOTICE("Checking NavbarSubItem..."))
        for item in NavbarSubItem.objects.all():
            changed = False
            for field in ("name_ru", "subtitle_ru", "content_ru"):
                old = getattr(item, field, "") or ""
                new = fix_text(old)
                if new != old:
                    changed = True
                    total_fixes += 1
                    self.stdout.write(f"- NavbarSubItem[{item.slug}] {field}: will fix")
                    if apply_changes:
                        setattr(item, field, new)
            if changed and apply_changes:
                item.save(update_fields=["name_ru", "subtitle_ru", "content_ru", "updated_at"])

        self.stdout.write(self.style.NOTICE("Checking ContentBlock..."))
        for block in ContentBlock.objects.all():
            changed = False
            for field in ("title_ru", "description_ru"):
                old = getattr(block, field, "") or ""
                new = fix_text(old)
                if new != old:
                    changed = True
                    total_fixes += 1
                    self.stdout.write(f"- ContentBlock[{block.id}] {field}: will fix")
                    if apply_changes:
                        setattr(block, field, new)
            if changed and apply_changes:
                block.save(update_fields=["title_ru", "description_ru", "updated_at"])

        if apply_changes:
            self.stdout.write(self.style.SUCCESS(f"Done. Fixed fields: {total_fixes}"))
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Dry-run complete. Candidate fixes: {total_fixes}. Run with --apply to save."
                )
            )

