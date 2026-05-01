"""
python manage.py seed_rector_appeal
python manage.py seed_rector_appeal --clear
"""
import datetime
from django.core.management.base import BaseCommand
from domains.contact.models import RectorAppeal, RectorAppealExtraField

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


APPEALS = [
    dict(
        sender_type='student', appeal_type='appeal',
        full_name='Aliyev Jasur Bekmurodovich',
        email='jasur.aliyev@student.uz', phone='+998901234567',
        faculty='Sport menejment', group='201-A',
        birth_date=datetime.date(2003, 5, 14),
        message='Yotoqxonadagi suv ta\'minoti muammosi hal qilinishini so\'rayman. Har kuni ertalab issiq suv bo\'lmaydi.',
        status='new',
        extra_data={'address': 'Toshkent sh., Yunusobod tumani', 'study_year': '2', 'academic_year': '2024-2025'},
    ),
    dict(
        sender_type='student', appeal_type='suggestion',
        full_name='Karimova Dilnoza Hamidovna',
        email='dilnoza.karimova@student.uz', phone='+998931112233',
        faculty='Jismoniy tarbiya', group='305-B',
        birth_date=datetime.date(2002, 8, 22),
        message='Kutubxonaga yangi sport va pedagogika bo\'yicha kitoblar qo\'shilsa yaxshi bo\'lardi. Hozirgi fondda zamonaviy adabiyotlar kam.',
        status='in_review',
        extra_data={'academic_year': '2024-2025', 'study_year': '3'},
    ),
    dict(
        sender_type='student', appeal_type='complaint',
        full_name='Toshmatov Sherzod Nurboyevich',
        email='sherzod.t@student.uz', phone='+998901239988',
        faculty='Sport menejment', group='102-A',
        birth_date=datetime.date(2004, 1, 10),
        message='O\'quv jadvalidagi o\'zgarishlar oldindan xabar qilinmayapti. Bu talabalar uchun jiddiy noqulaylik.',
        status='answered',
        extra_data={'issue_date': '2025-04-10', 'study_year': '1', 'academic_year': '2024-2025'},
    ),
    dict(
        sender_type='student', appeal_type='appeal',
        full_name='Nazarova Feruza Solijonovna',
        email='feruza.n@student.uz', phone='+998997654321',
        faculty='Magistratura', group='501-M',
        birth_date=datetime.date(2000, 11, 3),
        message='Magistratura talabalariga alohida o\'quv xonasi ajratilishini so\'rayman. Hozir joy yetishmaydi.',
        status='new',
        extra_data={'study_year': '1', 'academic_year': '2024-2025'},
    ),
    dict(
        sender_type='guest', appeal_type='appeal',
        full_name='Rahimov Behruz Akbarovich',
        email='behruz.r@gmail.com', phone='+998712345678',
        faculty='', group='',
        birth_date=datetime.date(1985, 3, 19),
        message='O\'g\'lim universitetga qabul jarayoni haqida batafsil ma\'lumot olishni istardim. Qabul shartlari va imtihonlar haqida yozib yuborish imkoni bormi?',
        status='new',
        extra_data={'address': 'Samarqand sh., Registon ko\'chasi 12'},
    ),
    dict(
        sender_type='guest', appeal_type='suggestion',
        full_name='Umarova Malika Ismoilovna',
        email='malika.u@mail.ru', phone='+998909876543',
        faculty='', group='',
        birth_date=None,
        message='Universitet veb-saytida ingliz tilidagi ma\'lumotlar ko\'paytirilsa xorijiy mehmonlar uchun qulay bo\'lardi.',
        status='in_review',
        extra_data={'attachment_note': 'Xorijiy universitetlar saytlarini namuna qilib ko\'rishingiz mumkin'},
    ),
    dict(
        sender_type='guest', appeal_type='complaint',
        full_name='Holiqov Mansur Tursunovich',
        email='mansur.h@yahoo.com', phone='+998911234455',
        faculty='', group='',
        birth_date=datetime.date(1978, 6, 25),
        message='Universitet hududidagi avtoturargoh muammosi bor. Tadbirlar paytida joy topolmaymiz.',
        status='new',
        extra_data={'issue_date': '2025-04-20', 'address': 'Toshkent sh., Chilonzor tumani'},
    ),
]


class Command(BaseCommand):
    help = "RectorAppealExtraField va RectorAppeal seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true')

    def handle(self, *args, **options):
        if options['clear']:
            RectorAppealExtraField.objects.all().delete()
            RectorAppeal.objects.all().delete()
            self.stdout.write(self.style.WARNING("Barcha ma'lumotlar o'chirildi"))

        self.stdout.write("--- Extra fieldlar ---")
        for data in EXTRA_FIELDS:
            obj, created = RectorAppealExtraField.objects.update_or_create(
                field_key=data['field_key'],
                defaults=data,
            )
            mark = '+' if created else '~'
            self.stdout.write(self.style.SUCCESS(f"[{mark}] {obj.field_key} — {obj.label_uz}"))

        self.stdout.write("--- Murojaatlar ---")
        for data in APPEALS:
            obj = RectorAppeal.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(
                f"[+] {obj.get_sender_type_display()} | {obj.get_appeal_type_display()} | {obj.full_name} ({obj.get_status_display()})"
            ))
