"""
python manage.py seed_kafedra           # yaratadi / yangilaydi
python manage.py seed_kafedra --clear   # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.academic.models import FakultetKafedra

KAFEDRAS = [
    {
        'slug': 'yakkakurash-va-suv-sport-turlari-kafedrasi',
        'type': FakultetKafedra.KAFEDRA,
        'order': 1,
        'name_uz': "Yakkakurash va suv sport turlari kafedrasi",
        'name_ru': "Кафедра единоборств и водных видов спорта",
        'name_en': "Department of Combat Sports and Aquatics",
        'description_uz': (
            "Yakkakurash va suv sport turlari kafedrasi O'zbekiston Respublikasi Prezidentining "
            "PQ-197-son, 2024-yil 28-may qaroriga asosan tashkil etilgan. Kafedra jismoniy "
            "tarbiya va sport sohasida yuqori malakali mutaxassislar tayyorlash, sport turlari "
            "bo'yicha ilmiy-uslubiy ta'minot va amaliy mashg'ulotlar olib borish maqsadida "
            "faoliyat yuritadi."
        ),
        'decree_info': "PQ-197-son, 2024-yil 28-may",
        'sport_types_uz': (
            "Dzyudo\n"
            "Taekvondo WT\n"
            "Boks\n"
            "Eshkak eshish\n"
            "Yengil atletika\n"
            "Og'ir atletika\n"
            "Yunon-rim kurash\n"
            "Erkin kurash\n"
            "Suzish\n"
            "Velosport\n"
            "Gimnastika\n"
            "Kamondan otish\n"
            "Qilichbozlik\n"
            "O'q otish"
        ),
        'sport_types_ru': (
            "Дзюдо\n"
            "Тхэквондо ВТ\n"
            "Бокс\n"
            "Гребля\n"
            "Лёгкая атлетика\n"
            "Тяжёлая атлетика\n"
            "Греко-римская борьба\n"
            "Вольная борьба\n"
            "Плавание\n"
            "Велоспорт\n"
            "Гимнастика\n"
            "Стрельба из лука\n"
            "Фехтование\n"
            "Стрельба"
        ),
        'bachelor_subjects_uz': (
            "Tayanch sport turlarini o'rgatish metodikasi (Suzish)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Dzyudo)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Taekvondo WT)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Boks)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Eshkak eshish)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Yengil atletika)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Og'ir atletika)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Yunon-rim kurash)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Erkin kurash)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Velosport)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Gimnastika)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Kamondan otish)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Qilichbozlik)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (O'q otish)\n"
            "Sport fiziologiyasi\n"
            "Sport pedagogikasi\n"
            "Sport psixologiyasi\n"
            "Jismoniy tarbiya nazariyasi va metodikasi"
        ),
        'master_subjects_uz': (
            "Sportda ilmiy tadqiqotlar\n"
            "Zamonaviy sport trenirovkasi nazariyasi\n"
            "Sport menejment\n"
            "Yuqori mahorat sporti\n"
            "Olimpiya harakati tarixi va falsafasi\n"
            "Sport pedagogikasi (magistratura)"
        ),
        'phone': '',
        'email': '',
    },
    {
        'slug': 'parasport-va-umumkasbiy-fanlar-kafedrasi',
        'type': FakultetKafedra.KAFEDRA,
        'order': 2,
        'name_uz': "Parasport va umumkasbiy fanlar kafedrasi",
        'name_ru': "Кафедра параспорта и общепрофессиональных дисциплин",
        'name_en': "Department of Parasport and General Professional Disciplines",
        'description_uz': (
            "Parasport va umumkasbiy fanlar kafedrasi nogironligi bo'lgan shaxslar o'rtasida "
            "sport madaniyatini rivojlantirish, paraolimpiya harakati g'oyalarini targ'ib qilish "
            "hamda sport sohasida umumkasbiy bilim va ko'nikmalarni shakllantirishga qaratilgan "
            "ta'lim faoliyatini olib boradi. Kafedra bakalavriat va magistratura dasturlari "
            "bo'yicha dars beradi, ilmiy-tadqiqot ishlarini amalga oshiradi."
        ),
        'decree_info': "",
        'sport_types_uz': "",
        'bachelor_subjects_uz': (
            "Sportda xorijiy til\n"
            "Rus tili\n"
            "O'zbekistonning eng yangi tarixi\n"
            "Huquqshunoslik\n"
            "Iqtisodiyot nazariyasi\n"
            "Falsafa\n"
            "Sotsiologiya\n"
            "Siyosatshunoslik\n"
            "Ekologiya va tabiatni muhofaza qilish\n"
            "Ma'naviyat asoslari\n"
            "Axborot texnologiyalari\n"
            "Statistika\n"
            "Menejment\n"
            "Marketing\n"
            "Moliya\n"
            "Buxgalteriya hisobi\n"
            "Parasport asoslari\n"
            "Paraolimpiya harakati tarixi\n"
            "Adaptiv jismoniy tarbiya\n"
            "Nogironligi bo'lgan shaxslar bilan ishlash metodikasi"
        ),
        'master_subjects_uz': (
            "Ilmiy tadqiqot metodologiyasi\n"
            "Sport morfologiyasi\n"
            "Sport biomexanikasi\n"
            "Sport fiziologiyasi (magistratura)\n"
            "Sport psixologiyasi (magistratura)\n"
            "Sport pedagogikasi (magistratura)\n"
            "Sport menejment (magistratura)\n"
            "Sport iqtisodiyoti\n"
            "Sport huquqi\n"
            "Xalqaro sport tashkilotlari\n"
            "Olimpiya va paraolimpiya harakati\n"
            "Adaptiv sport nazariyasi va metodikasi\n"
            "Nogironligi bo'lgan sportchilar bilan ishlash\n"
            "Sport tibbiyoti\n"
            "Reabilitatsiya va sport\n"
            "Doping nazorati\n"
            "Sport ovqatlanishi\n"
            "Zamonaviy trenirovka texnologiyalari\n"
            "Yuqori mahoratli sportchilarni tayyorlash\n"
            "Sport musobaqalarini tashkil etish\n"
            "Sport infratuzilmasi va inshootlari\n"
            "Ta'limda innovatsion texnologiyalar\n"
            "Xorijiy til (magistratura)\n"
            "Axborot-kommunikatsiya texnologiyalari (magistratura)\n"
            "Ilmiy maqola yozish metodikasi\n"
            "Magistrlik dissertatsiyasi yozish asoslari\n"
            "Pedagogik amaliyot"
        ),
        'phone': '',
        'email': 'sobirovalaylo90@gmail.com',
    },
]


class Command(BaseCommand):
    help = "Kafedra ma'lumotlarini to'ldiradi (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib, qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            slugs = [k['slug'] for k in KAFEDRAS]
            n = FakultetKafedra.objects.filter(slug__in=slugs).delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        created = updated = 0
        for data in KAFEDRAS:
            slug = data.pop('slug')
            obj, is_new = FakultetKafedra.objects.update_or_create(
                slug=slug,
                defaults=data,
            )
            data['slug'] = slug  # restore for idempotency
            if is_new:
                created += 1
            else:
                updated += 1
            self.stdout.write(f"  {'[+]' if is_new else '[~]'} {obj.name_uz}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created} yangi, {updated} yangilandi. Jami {len(KAFEDRAS)} ta kafedra."
        ))
