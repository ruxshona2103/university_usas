"""
Sync selected /api/pages/{slug}/ sources into academic FakultetKafedra records.

Usage:
  python manage.py sync_page_slugs_to_academic
  python manage.py sync_page_slugs_to_academic --slugs xotin-qizlar-qomitasi,yoshlar-ittifoqi,kasaba-uyushmasi
"""

from django.core.management.base import BaseCommand
from django.db.models import Q

from domains.academic.models import FakultetKafedra
from domains.pages.models import NavbarSubItem


DEFAULT_SLUGS = (
    "xotin-qizlar-qomitasi",
    "yoshlar-ittifoqi",
    "kasaba-uyushmasi",
)

SLUG_NAME_HINTS = {
    "xotin-qizlar-qomitasi": "xotin-qizlar qo'mitasi",
    "yoshlar-ittifoqi": "yoshlar ittifoqi",
    "kasaba-uyushmasi": "kasaba uyushmasi",
}


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


def _find_page_by_slug_hint(slug):
    # 1) Exact slug (active/inactive)
    qs = NavbarSubItem.objects.filter(slug=slug).order_by("-is_active", "-updated_at")
    obj = qs.first()
    if obj:
        return obj

    # 2) Redirect URL references
    page_url = f"/page/{slug}"
    qs = NavbarSubItem.objects.filter(redirect_url=page_url).order_by("-is_active", "-updated_at")
    obj = qs.first()
    if obj:
        return obj

    # 3) Name fallback for known slugs
    hint = SLUG_NAME_HINTS.get(slug, "")
    if hint:
        qs = NavbarSubItem.objects.filter(
            Q(name_uz__iexact=hint) | Q(name_ru__iexact=hint) | Q(name_en__iexact=hint)
        ).order_by("-is_active", "-updated_at")
        obj = qs.first()
        if obj:
            return obj

    return None


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

        created = 0
        updated = 0
        missed = 0

        for slug in slugs:
            page_obj = _find_page_by_slug_hint(slug)
            if not page_obj:
                missed += 1
                self.stdout.write(self.style.WARNING(f"[!] Page topilmadi: {slug}"))
                continue

            # Ensure related objects are fetched for description building
            page_obj = (
                NavbarSubItem.objects
                .filter(pk=page_obj.pk)
                .prefetch_related("contentblock_items", "linkblock_items")
                .first()
            )
            self.stdout.write(f"[i] Source page: requested={slug}, found={page_obj.slug}")

            defaults = {
                "type": FakultetKafedra.TASHKILOT,
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
