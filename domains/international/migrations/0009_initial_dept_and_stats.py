import datetime
from django.db import migrations


TASKS_UZ = """\
ta'lim sifati va samaradorligini oshirish maqsadida respublika oliy o'quv yurtlari bilan aloqalar o'rnatish;
ta'limning sifati va samaradorligini oshirish hamda xorijiy mamlakatlarning ta'lim sohasidagi yutuqlarini o'rganishga qaratilgan respublika va chet el jamg'armalari bilan bevosita hamkorlik qilishni tashkil etish;
turli yo'nalishlar bo'yicha xalqaro loyihalarni tuzishga, ularni amalga oshirishga rahbarlik qilish;
xorijiy mamlakatlarni ta'lim sohasidagi yutuqlarini o'rganish va tajriba almashish maqsadida chet el olimlari, professor-o'qituvchi hamda mutaxassislarini taklif etish ishlarini tashkil etish;
pedogog xodimlarni xorijiy mamlakatlar oliy ta'lim muassasalariga tajriba almashish maqsadida yuborilishini tashkil etish;
xorijiy mamlakatlar hamda respublika hududida o'tkaziladigan xalqaro anjumanlarda Akademiya jamoasining qatnashishi va tajriba almashishini tashkil etish;
ta'lim berishning texnologik jarayonida chet el pedagogikasining eng ilg'or tajribalarini o'rganish va ularni Akademiya rahbariyati bilan muhokama etish;
rivojlangan davlatlarning sohaga oid istiqbolli modellarini o'rganish, ularni mahalliy sharoitga moslagan holda ta'lim jarayoniga tatbiq etish bo'yicha ta'lim muassasasi pedagoglari bilan hamkorlikda tavsiyalar ishlab chiqish;"""

MEMORANDUMS = [
    {
        'organization_uz': "O'zbekiston davlat sport akademiyasi",
        'foreign_count': 2,
        'domestic_count': 6,
        'order': 1,
    },
    {
        'organization_uz': (
            "O'zbekiston davlat sport akademiyasi huzuridagi Jismoniy tarbiya va sport "
            "bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish instituti"
        ),
        'foreign_count': 5,
        'domestic_count': 65,
        'order': 2,
    },
    {
        'organization_uz': (
            "O'zbekiston davlat sport akademiyasi huzuridagi "
            "Jismoniy tarbiya va sport ilmiy tadqiqotlar instituti"
        ),
        'foreign_count': 14,
        'domestic_count': 46,
        'order': 3,
    },
]

BLOCK3_CONTENT = (
    "Akademiya professor-o'qituvchilari xalqaro tadbirda faol ishtirok etdi.\n\n"
    "2025-yilning 22-31-oktyabr va 3-15-noyabr kunlari \"QS Word University Rankings\" "
    "reytingida 621 o'rinda turgan M.Avezov nomidagi janubiy Qozog'iston universitetida "
    "Ilmiy ishlar va innovatsiyalar bo'yicha prorektor Z.Rasulov, \"Parasport va umumkasbiy "
    "fanlar\" kafedrasi professori N.Xudayberdiyeva va \"Yakkakurash va suv sport turlari\" "
    "kafedrasi dotsenti M.Suleymonovlar o'quv-uslubiy va ilmiy-tadqiqot yo'nalishida tajriba "
    "almashish maqsadida ma'ruzachi sifatida ishtirok etdilar.\n\n"
    "Mazkur tashrif doirasida o'quv-uslubiy birlashma yo'nalishlari bo'yicha forsayt sessiya "
    "tashkil etilib, unda ta'lim jarayonini takomillashtirish, zamonaviy pedagogik yondashuvlarni "
    "joriy etish hamda o'quv dasturlarini xalqaro standartlar asosida rivojlantirish masalalari "
    "muhokama qilindi.\n\n"
    "Shuningdek, xalqaro akademik mobillik dasturi doirasida Akademiya vakillari tomonidan "
    "universitet talabalari va magistrantlari uchun ma'ruza va amaliy mashg'ulotlar o'tkazildi. "
    "Mashg'ulotlar davomida ishtirokchilarga zamonaviy bilim va ko'nikmalar berilib, o'zaro "
    "tajriba almashish imkoniyati yaratildi.\n\n"
    "Mazkur tadbir ikki tomonlama ilmiy va ta'limiy hamkorlikni yanada mustahkamlash, "
    "professor-o'qituvchilar o'rtasida tajriba almashuvini kengaytirish hamda xalqaro "
    "aloqalarni rivojlantirishda muhim ahamiyat kasb etdi."
)


def seed_data(apps, schema_editor):
    InternationalDeptConfig = apps.get_model('international', 'InternationalDeptConfig')
    MemorandumStat          = apps.get_model('international', 'MemorandumStat')
    InternationalPost       = apps.get_model('international', 'InternationalPost')

    InternationalDeptConfig.objects.get_or_create(
        pk=1,
        defaults=dict(
            head_name_uz="Karimova Farangiz Narzillo qizi",
            head_position_uz="Bo'lim boshlig'i",
            head_working_hours="Dushanba-Juma 10:00-16:00",
            head_phone="+998947551135",
            head_email="info@usas.uz, farangizkarimova100@gmail.com",
            tasks_uz=TASKS_UZ,
        ),
    )

    for item in MEMORANDUMS:
        MemorandumStat.objects.get_or_create(
            organization_uz=item['organization_uz'],
            defaults=dict(
                foreign_count=item['foreign_count'],
                domestic_count=item['domestic_count'],
                order=item['order'],
            ),
        )

    InternationalPost.objects.get_or_create(
        title_uz="Akademiya professor-o'qituvchilari xalqaro tadbirda faol ishtirok etdi",
        post_type='training',
        defaults=dict(
            content_uz=BLOCK3_CONTENT,
            date=datetime.date(2025, 11, 15),
            order=1,
            is_active=True,
        ),
    )


def unseed_data(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('international', '0008_internationaldeptconfig_memorandumstat'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]
