from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from domains.academic.models import OrganizationUnit
from domains.pages.models import NavbarSubItem


class Command(BaseCommand):
    help = (
        "Map OrganizationUnit objects to NavbarSubItem (Variant A). "
        "Default mode is dry-run. Use --apply to persist changes."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--apply',
            action='store_true',
            help='Apply changes to database. Without this flag command only previews.',
        )
        parser.add_argument(
            '--include-linked',
            action='store_true',
            help='Also remap already linked units. Default maps only units without navbar_item.',
        )

    def handle(self, *args, **options):
        apply_changes = options['apply']
        include_linked = options['include_linked']

        units_qs = OrganizationUnit.objects.select_related('navbar_item').order_by('id')
        if not include_linked:
            units_qs = units_qs.filter(navbar_item__isnull=True)

        units = list(units_qs)
        navbar_items = list(
            NavbarSubItem.objects.filter(
                is_active=True,
                page_type=NavbarSubItem.PageType.STATIC,
            ).select_related('category')
        )

        if not units:
            self.stdout.write(self.style.WARNING('No OrganizationUnit records to process.'))
            return

        by_slug = {item.slug: item for item in navbar_items}
        by_name_slug = defaultdict(list)
        for item in navbar_items:
            by_name_slug[slugify(item.name_uz)].append(item)

        matched = 0
        applied = 0
        ambiguous = 0
        conflicts = 0
        not_found = 0

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f"Mapping mode: {'APPLY' if apply_changes else 'DRY-RUN'} | units={len(units)} | navbar_candidates={len(navbar_items)}"
            )
        )

        for unit in units:
            target = by_slug.get(unit.slug)
            matched_by = 'slug'

            if target is None:
                candidates = by_name_slug.get(slugify(unit.title_uz), [])
                if len(candidates) == 1:
                    target = candidates[0]
                    matched_by = 'title_uz'
                elif len(candidates) > 1:
                    ambiguous += 1
                    self.stdout.write(
                        self.style.WARNING(
                            f"AMBIGUOUS unit#{unit.id} '{unit.title_uz}' -> multiple navbar candidates by title"
                        )
                    )
                    continue

            if target is None:
                not_found += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"NOT FOUND unit#{unit.id} '{unit.title_uz}' slug='{unit.slug}'"
                    )
                )
                continue

            if hasattr(target, 'academic_unit') and target.academic_unit_id != unit.id:
                conflicts += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"CONFLICT unit#{unit.id} '{unit.title_uz}' -> navbar '{target.slug}' already linked to unit#{target.academic_unit_id}"
                    )
                )
                continue

            matched += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"MATCH unit#{unit.id} '{unit.title_uz}' -> navbar#{target.id} '{target.slug}' (by {matched_by})"
                )
            )

            if apply_changes:
                with transaction.atomic():
                    unit.navbar_item = target
                    unit.save()
                applied += 1

        summary = (
            f"Summary: matched={matched}, applied={applied}, "
            f"not_found={not_found}, ambiguous={ambiguous}, conflicts={conflicts}"
        )
        self.stdout.write(self.style.MIGRATE_LABEL(summary))

        if not apply_changes:
            self.stdout.write(self.style.WARNING('Dry-run completed. Use --apply to save mappings.'))
