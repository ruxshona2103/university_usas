"""
Sync selected /api/pages/{slug}/ sources into academic FakultetKafedra records.

Usage:
  python manage.py sync_page_slugs_to_academic
  python manage.py sync_page_slugs_to_academic --slugs xotin-qizlar-qomitasi,yoshlar-ittifoqi,kasaba-uyushmasi
"""

from django.core.management.base import BaseCommand

from domains.academic.models import FakultetKafedra
from domains.pages.models import NavbarSubItem


DEFAULT_SLUGS = (
    "xotin-qizlar-qomitasi",
    "yoshlar-ittifoqi",
    "kasaba-uyushmasi",
)


def _lang_value(obj, base, lang):
    return (getattr(obj, f"{base}_{lang}", "") or "").strip()


def _collect_blocks_text(page_obj, lang):
    lines = []

    content_blocks = (
        page_obj.contentblock_items.filter(is_active=True)
        .order_by("order", "created_at")
    )
    for block in content_blocks:
        title = _lang_value(block, "title", lang)
        desc = _lang_value(block, "description", lang)
        if title:
            lines.append(title)
        if desc:
            lines.append(desc)

    link_blocks = (
        page_obj.linkblock_items.filter(is_active=True)
        .order_by("order", "created_at")
    )
    for block in link_blocks:
        title = _lang_value(block, "title", lang)
        link = (block.link or "").strip()
        if title and link:
            lines.append(f"{title}: {link}")
        elif title:
            lines.append(title)
        elif link:
            lines.append(link)

    return "\n\n".join(lines).strip()


def _build_description(page_obj, lang):
    content = _lang_value(page_obj, "content", lang)
    blocks_text = _collect_blocks_text(page_obj, lang)
    if content and blocks_text:
        return f"{content}\n\n{blocks_text}"
    return content or blocks_text


class Command(BaseCommand):
    help = (
        "Selected pages sluglarini academic/fakultet-kafedra jadvaliga "
        "shu slug va kontenti bilan ko'chiradi (idempotent)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--slugs",
            type=str,
            default=",".join(DEFAULT_SLUGS),
            help="Vergul bilan ajratilgan sluglar ro'yxati.",
        )

    def handle(self, *args, **options):
        slugs_raw = (options.get("slugs") or "").strip()
        slugs = tuple(s.strip() for s in slugs_raw.split(",") if s.strip())
        if not slugs:
            self.stdout.write(self.style.WARNING("Sync uchun slug berilmadi."))
            return

        pages = {
            p.slug: p
            for p in NavbarSubItem.objects.filter(slug__in=slugs, is_active=True)
            .prefetch_related("contentblock_items", "linkblock_items")
        }

        created = 0
        updated = 0
        missed = 0

        for slug in slugs:
            page_obj = pages.get(slug)
            if not page_obj:
                missed += 1
                self.stdout.write(self.style.WARNING(f"[!] Page topilmadi: {slug}"))
                continue

            defaults = {
                "type": FakultetKafedra.KAFEDRA,
                "order": page_obj.order,
                "is_active": page_obj.is_active,
                "name_uz": page_obj.name_uz,
                "name_ru": page_obj.name_ru or page_obj.name_uz,
                "name_en": page_obj.name_en or page_obj.name_uz,
                "description_uz": _build_description(page_obj, "uz"),
                "description_ru": _build_description(page_obj, "ru"),
                "description_en": _build_description(page_obj, "en"),
                "sport_types_uz": "",
                "sport_types_ru": "",
                "sport_types_en": "",
                "bachelor_subjects_uz": "",
                "bachelor_subjects_ru": "",
                "bachelor_subjects_en": "",
                "master_subjects_uz": "",
                "master_subjects_ru": "",
                "master_subjects_en": "",
                "decree_info": "",
                "phone": "",
                "email": "",
                "link": f"/page/{slug}",
            }

            _, is_new = FakultetKafedra.objects.update_or_create(
                slug=slug,
                defaults=defaults,
            )
            if is_new:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"[+] Yaratildi: {slug}"))
            else:
                updated += 1
                self.stdout.write(f"[~] Yangilandi: {slug}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. created={created}, updated={updated}, missed={missed}"
            )
        )
