from django.core.management.base import BaseCommand

from domains.pages.models import AkademiyaMissiya, AkademiyaMissiyaYonalish


MISSION_DESCRIPTION_UZ = (
    "O'zbekiston davlat sport akademiyasining missiyasi - jismoniy tarbiya va sport "
    "sohasida raqobatbardosh mutaxassislarni tayyorlash, ilm-fan va innovatsiyalarni "
    "rivojlantirish hamda sog'lom turmush tarzini jamiyatda keng targ'ib qilishdir."
)

MISSION_ITEMS_UZ = [
    "Sport ta'limi uchun zamonaviy va amaliy o'quv dasturlarini joriy etish.",
    "Yoshlar salohiyatini ochishga xizmat qiladigan ilmiy-amaliy muhitni yaratish.",
    "Xalqaro hamkorlik, akademik almashinuv va qo'shma loyihalarni kengaytirish.",
    "Murabbiylar, pedagoglar va sport menejerlarini kasbiy tayyorlash sifatini oshirish.",
    "Milliy va umuminsoniy qadriyatlarga tayangan holda sog'lom avlodni tarbiyalash.",
]


class Command(BaseCommand):
    help = "Akademiya missiyasi va yo'nalishlari uchun boshlang'ich ma'lumotlarni yozadi"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Mavjud missiya yo'nalishlarini o'chirib qayta yozadi",
        )

    def handle(self, *args, **options):
        clear = options.get("clear", False)

        solo = AkademiyaMissiya.get_solo()
        solo.description_uz = MISSION_DESCRIPTION_UZ
        solo.description_ru = (
            solo.description_ru
            or "Миссия академии - подготовка конкурентоспособных специалистов в сфере спорта."
        )
        solo.description_en = (
            solo.description_en
            or "The academy mission is to prepare competitive professionals in sport."
        )
        solo.save()

        if clear:
            solo.yonalishlar.all().delete()

        if solo.yonalishlar.exists():
            self.stdout.write(
                self.style.WARNING("Missiya yo'nalishlari allaqachon mavjud, yangilash o'tkazib yuborildi.")
            )
            self.stdout.write(self.style.SUCCESS("Seed yakunlandi."))
            return

        for index, text_uz in enumerate(MISSION_ITEMS_UZ, start=1):
            AkademiyaMissiyaYonalish.objects.create(
                missiya=solo,
                order=index,
                text_uz=text_uz,
                text_ru=text_uz,
                text_en=text_uz,
            )

        self.stdout.write(self.style.SUCCESS("Akademiya missiyasi seed muvaffaqiyatli yozildi."))
