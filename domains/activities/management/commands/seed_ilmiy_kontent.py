"""
4 ta PDF mazmunini DB'ga yozadi:
- Ilmiy jurnallar
- Ilmiy kengash va seminar
- Ilmiy loyihalar
- Ilmiy maktablar
"""
from django.core.management.base import BaseCommand

from domains.activities.models import (
    IlmiyKategoriya, IlmiyKontentSahifa,
    IlmiyJurnal, IlmiyKengashSeminar, IlmiyLoyiha, IlmiyMaktab,
)


SAHIFALAR = [
    {
        "kategoriya": IlmiyKategoriya.JURNALLAR,
        "title_uz": "Ilmiy jurnallar",
        "intro_uz": "O‘zbekiston davlat sport akademiyasi huzuridagi ta’lim tashkilotlarida mavjud ilmiy jurnallar.",
    },
    {
        "kategoriya": IlmiyKategoriya.KENGASH,
        "title_uz": "Ilmiy kengash va seminar",
        "intro_uz": (
            "O‘zbekiston davlat sport akademiyasi huzuridagi Jismoniy tarbiya va sport "
            "ilmiy tadqiqotlar instituti huzuridagi Ilmiy darajalar beruvchi ilmiy kengash "
            "va uning huzuridagi ilmiy seminar to‘g‘risida ma’lumot."
        ),
    },
    {
        "kategoriya": IlmiyKategoriya.LOYIHALAR,
        "title_uz": "Ilmiy loyihalar",
        "intro_uz": (
            "O‘zbekiston davlat sport akademiyasi va uning huzuridagi ta’lim tashkilotlarida "
            "olib borilayotgan halqaro, startap, fundamental, amaliy, innovatsion hamda "
            "ho‘jalik shartnomalari to‘g‘risida ma’lumot."
        ),
    },
    {
        "kategoriya": IlmiyKategoriya.MAKTABLAR,
        "title_uz": "Ilmiy maktablar",
        "intro_uz": (
            "O‘zbekiston davlat sport akademiyasi hamda uning huzuridagi Jismoniy tarbiya "
            "va sport ilmiy tadqiqotlar instituti va Jismoniy tarbiya va sport bo‘yicha "
            "mutaxassislarni qayta tayyorlash va malakasini oshirish institutida fanning "
            "turli sohalarida o‘ziga xos tadqiqot tamoyillariga, usullariga ega bo‘lgan "
            "ilmiy maktablar yaratilgan bo‘lib, bu ilmiy maktablarni yaratgan olimlar va "
            "ularning izdoshlari ilm-fanning yangi yo‘nalishlariga asos soldilar, "
            "mamlakatimiz jismoniy tarbiya va sport ta’limi rivojiga munosib hissa qo‘shdilar."
        ),
    },
]


JURNALLAR = [
    {"name_uz": "\"Sportda ilmiy tadqiqotlar\" ilmiy-nazariy jurnali", "order": 1},
    {"name_uz": "\"Sport ilm-fanining dolzarb muammolari\" xalqaro ilmiy-nazariy jurnali", "order": 2},
]


KENGASH_SEMINAR = [
    {
        "tipi": "kengash",
        "shifr": "DSc.28/2025.27.12.Ped.01.01 (pedagogika fanlari bo‘yicha)",
        "buyruq_sanasi": "27.12.2025 №1599",
        "ixtisoslik_shifri": "13.00.04 (Bir martalik: 13.00.01, 13.00.07)",
        "ixtisoslik_nomi_uz": (
            "Jismoniy tarbiya, sport mashg‘ulotlari, sog‘lomlashtirish va "
            "adaptiv jismoniy tarbiya nazariyasi va metodikasi"
        ),
        "rais_uz": "Talipdjanov Askar Imamdjanovich",
        "rais_lavozim_uz": "rais, pedagogika fanlari doktori (DSc), professor",
        "kotib_uz": "Egamov Duryod Yaxyo o‘g‘li",
        "kotib_lavozim_uz": "ilmiy kotib, pedagogika fanlari bo‘yicha falsafa doktori (PhD)",
        "order": 1,
    },
    {
        "tipi": "seminar",
        "shifr": "DSc.28/2025.27.12.Ped.01.01 (pedagogika fanlari bo‘yicha)",
        "buyruq_sanasi": "27.12.2025 №1599",
        "ixtisoslik_shifri": "13.00.04",
        "ixtisoslik_nomi_uz": (
            "Jismoniy tarbiya, sport mashg‘ulotlari, sog‘lomlashtirish va "
            "adaptiv jismoniy tarbiya nazariyasi va metodikasi"
        ),
        "rais_uz": "Hayitov Oybek Eshboyevich",
        "rais_lavozim_uz": "Ilmiy seminar raisi, psixologiya fanlari doktori (DSc), professor",
        "kotib_uz": "Nematov Bobirbek Ilxomjonovich",
        "kotib_lavozim_uz": "Ilmiy seminar kotibi, pedagogika fanlari bo‘yicha falsafa doktori (PhD), professor",
        "order": 1,
    },
]


LOYIHALAR = [
    {
        "raqami_uz": "Bajarilishi 2027-2028 - yillarga mo‘ljallangan Amaliy loyiha",
        "mavzusi_uz": (
            "Talaba-yoshlarni musobaqa faoliyatiga samarali tayyorlashda funksional va "
            "jismoniy holatini diagnostika qilish dasturiy ta’minotini yaratish"
        ),
        "order": 1,
    },
    {
        "raqami_uz": "Bajarilishi 2027-2028 - yillarga mo‘ljallangan Amaliy loyiha",
        "mavzusi_uz": (
            "Sportchilar harakatlarini analitik tahlil qilish asosida texnik "
            "tayyorgarligini oshiruvchi innovatsion mexanizmlarni ishlab chiqish"
        ),
        "order": 2,
    },
    {
        "raqami_uz": "Bajarilishi 2027-2028 - yillarga mo‘ljallangan Amaliy loyiha",
        "mavzusi_uz": (
            "Sog‘lom turmush tarzini rivojlantirishga yo‘naltirilgan sog‘lomlashtirish, "
            "fitnes texnikalarini ishlab chiqish"
        ),
        "order": 3,
    },
    {
        "raqami_uz": "Bajarilishi 2027-2028 - yillarga mo‘ljallangan Amaliy loyiha",
        "mavzusi_uz": (
            "Ultrabinafsha nurlaridan jismoniy tarbiya va sport sohasida foydalanish "
            "texnologiyasini yaratish"
        ),
        "order": 4,
    },
    {
        "raqami_uz": "Bajarilishi 2027-2029 - yillarga mo‘ljallangan Amaliy loyiha",
        "mavzusi_uz": (
            "Talabalarni ommaviy sport bilan muntazam shug‘ullanishga jalb etish uchun "
            "raqamli texnologiyalarni ishlab chiqish"
        ),
        "order": 5,
    },
    {
        "raqami_uz": "Bajarilishi 2026-2028 - yillarga mo‘ljallangan Amaliy loyiha",
        "mavzusi_uz": (
            "Jismoniy tarbiya va sport orqali aholining barcha qatlamlarini "
            "sog‘lomlashtirishda sun’iy intellektdan foydalanish mexanizmlari"
        ),
        "order": 6,
    },
]


MAKTABLAR = [
    {
        "nomi_uz": "Jismoniy tarbiya va sport bo‘yicha mutaxassislarni qayta tayyorlash va malakasini oshirish ilmiy maktabi",
        "asoschi_uz": "professor Tursunaliyev Ilhomjon Axmedovich",
        "order": 1,
    },
    {
        "nomi_uz": "Futbol analitikasi ilmiy maktabi",
        "asoschi_uz": "professor Talipdjanov Askar Imamdjanovich",
        "order": 2,
    },
    {
        "nomi_uz": "Paralimpia sporti ilmiy maktabi",
        "asoschi_uz": "professor Mirjamalov Mehriddin Xayriddinovich",
        "order": 3,
    },
    {
        "nomi_uz": "Sport psixologiyasi ilmiy maktabi",
        "asoschi_uz": "professor Hayitov Oybek Eshboyevich",
        "order": 4,
    },
    {
        "nomi_uz": "Yengil atletika sporti ilmiy maktabi",
        "asoschi_uz": "professor Normuradov Ashur Nazarovich",
        "order": 5,
    },
    {
        "nomi_uz": "Sport o‘yinlari ilmiy maktabi",
        "asoschi_uz": "professorlar Israilov Shoakram Xolmatovich, Jumanov Ortug‘mat Sangilbayevich",
        "order": 6,
    },
]


class Command(BaseCommand):
    help = "Ilmiy kontent (4 ta PDF) mazmunini DB'ga yozadi"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear", action="store_true", help="Avval mavjudlarini o'chirib qayta yozish"
        )

    def handle(self, *args, **options):
        clear = options.get("clear", False)

        # Sahifa intro'lari
        for s in SAHIFALAR:
            obj, created = IlmiyKontentSahifa.objects.update_or_create(
                kategoriya=s["kategoriya"],
                defaults={
                    "title_uz": s["title_uz"],
                    "intro_uz": s["intro_uz"],
                },
            )
            self.stdout.write(self.style.SUCCESS(
                f"Sahifa: {obj.get_kategoriya_display()} {'yaratildi' if created else 'yangilandi'}"
            ))

        if clear:
            IlmiyJurnal.objects.all().delete()
            IlmiyKengashSeminar.objects.all().delete()
            IlmiyLoyiha.objects.all().delete()
            IlmiyMaktab.objects.all().delete()

        for j in JURNALLAR:
            IlmiyJurnal.objects.update_or_create(
                name_uz=j["name_uz"], defaults={"order": j["order"], "is_active": True}
            )
        self.stdout.write(self.style.SUCCESS(f"Jurnallar: {len(JURNALLAR)} ta"))

        for k in KENGASH_SEMINAR:
            IlmiyKengashSeminar.objects.update_or_create(
                shifr=k["shifr"], tipi=k["tipi"],
                defaults={**k, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"Kengash/seminar: {len(KENGASH_SEMINAR)} ta"))

        for l in LOYIHALAR:
            IlmiyLoyiha.objects.update_or_create(
                mavzusi_uz=l["mavzusi_uz"],
                defaults={**l, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"Loyihalar: {len(LOYIHALAR)} ta"))

        for m in MAKTABLAR:
            IlmiyMaktab.objects.update_or_create(
                nomi_uz=m["nomi_uz"],
                defaults={**m, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS(f"Maktablar: {len(MAKTABLAR)} ta"))

        self.stdout.write(self.style.SUCCESS("\nSeed yakunlandi."))
