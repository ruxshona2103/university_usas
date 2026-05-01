"""
python manage.py seed_rector_appeal
python manage.py seed_rector_appeal --clear
"""
from django.core.management.base import BaseCommand
from domains.contact.models import RectorAppealExtraField

EXTRA_FIELDS = [
    dict(
        label_uz="Manzil (yashash joyi)",
        label_ru="Адрес (место проживания)",
        label_en="Address (place of residence)",
        field_key="address",
        field_type="text",
        is_required=False,
        order=10,
    ),
    dict(
        label_uz="Muammo yuzaga kelgan sana",
        label_ru="Дата возникновения проблемы",
        label_en="Date of issue",
        field_key="issue_date",
        field_type="date",
        is_required=False,
        order=20,
    ),
    dict(
        label_uz="Ilova yoki havola (link)",
        label_ru="Приложение или ссылка",
        label_en="Attachment or link",
        field_key="attachment_note",
        field_type="textarea",
        is_required=False,
        order=30,
    ),
    dict(
        label_uz="O'quv yili",
        label_ru="Учебный год",
        label_en="Academic year",
        field_key="academic_year",
        field_type="text",
        is_required=False,
        order=40,
    ),
    dict(
        label_uz="Kurs (1–4)",
        label_ru="Курс (1–4)",
        label_en="Year of study (1–4)",
        field_key="study_year",
        field_type="number",
        is_required=False,
        order=50,
    ),
]


class Command(BaseCommand):
    help = "RectorAppealExtraField seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            RectorAppealExtraField.objects.all().delete()
            self.stdout.write(self.style.WARNING("Barcha extra fieldlar o'chirildi"))

        for data in EXTRA_FIELDS:
            obj, created = RectorAppealExtraField.objects.update_or_create(
                field_key=data['field_key'],
                defaults=data,
            )
            mark = '+' if created else '~'
            self.stdout.write(self.style.SUCCESS(f"[{mark}] {obj.field_key} — {obj.label_uz}"))
