from django.db import migrations


STATS = [
    # (label_uz, value_uz, order)
    ("Fakultetlar soni",          "1 ta",      1),
    ("Kafedralar soni",           "2 ta",      2),
    ("Professor-o'qituvchilar soni", "31 nafar", 3),
    ("Talabalar soni",            "159 nafar", 4),
]

RESOURCE_CENTER_UZ = (
    "O'zbekiston davlat sport akademiyasining Axborot-resurs markazida o'quv-uslubiy ta'minotni "
    "tizimli ravishda yo'lga qo'yish maqsadida bakalavriat va magistratura bosqichi talabalari, "
    "shuningdek, professor-o'qituvchilar tarkibining ilmiy-pedagogik faoliyati ehtiyojlarini to'liq "
    "qondirishga yo'naltirilgan jami 546 nomdagi 8260 dona adabiyotlar fondi shakllantirilgan.\n\n"
    "Mazkur fond o'z ichiga 3752 dona darsliklar, 3474 dona o'quv qo'llanmalar, 440 dona "
    "monografiyalar, 105 dona badiiy adabiyotlar hamda 489 dona boshqa turdagi adabiyotlarni "
    "qamrab olan bo'lib, ta'lim jarayonining samaradorligini oshirish, zamonaviy bilim va "
    "ko'nikmalarni egallash hamda ilmiy-tadqiqot faoliyatini rivojlantirishga xizmat qiladi."
)

DETAIL_UZ = (
    'Fakultetlar soni: 1 ta — "Sport va parasport turlari fakulteti".\n\n'
    'Kafedralar soni: 2 ta — "Yakkakurash va suv sport turlari" hamda '
    '"Parasport va umumkasbiy fanlar" kafedralari.\n\n'
    "Ta'lim yo'nalishlari soni: Hozirda 2 ta ta'lim yo'nalishi negizida 14 ta sport turi va "
    "4 ta magistratura mutaxassisligi mavjud.\n\n"
    "Professor-o'qituvchilar soni: Jami 31 nafar professor-o'qituvchi faoliyat olib bormoqda. "
    "Shulardan 13 nafari asosiy, 4 nafari ichki o'rindosh va 14 nafari tashqi o'rindoshlik "
    "asosida faoliyat olib boradi.\n\n"
    "Talabalar soni: Akademiyada hozirda jami 159 nafar talaba tahsil olmoqda. Shundan 146 nafari "
    "bakalavriat, 13 nafari esa magistratura bosqichi talabalari hisoblanadi "
    "(2026-yil 2-aprel holatiga ko'ra)."
)


def seed(apps, schema_editor):
    AcademyStat = apps.get_model('academic', 'AcademyStat')
    AcademyDetailPage = apps.get_model('academic', 'AcademyDetailPage')

    existing_orders = set(AcademyStat.objects.values_list('order', flat=True))
    for label_uz, value_uz, order in STATS:
        if order not in existing_orders:
            AcademyStat.objects.create(
                label_uz=label_uz,
                value_uz=value_uz,
                order=order,
                is_active=True,
            )

    if not AcademyDetailPage.objects.exists():
        AcademyDetailPage.objects.create(
            edu_direction_count='2 ta',
            sport_type_count='14 ta',
            masters_count='4 ta',
            auditorium_count='22 ta',
            resource_center_uz=RESOURCE_CENTER_UZ,
            detail_uz=DETAIL_UZ,
        )


def unseed(apps, schema_editor):
    AcademyStat = apps.get_model('academic', 'AcademyStat')
    AcademyDetailPage = apps.get_model('academic', 'AcademyDetailPage')
    AcademyStat.objects.all().delete()
    AcademyDetailPage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0006_seed_fakultet_kafedra_data'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
