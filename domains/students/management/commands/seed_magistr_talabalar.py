from django.core.management.base import BaseCommand
from domains.students.models import MagistrTalaba

STUDENTS = [
    {
        "order": 1,
        "full_name": "Xolmatova Nozima",
        "specialty_code": "",
        "specialty_name_uz": "Magistratura ta'lim bosqichi",
        "bio_uz": (
            "Akademiyaning magistratura mutaxassisliklariga qabul qilingan talabalar uchun "
            "o'quv mashg'ulot jarayonlarini sifatli tashkil qilish va monitoringini olib borishga mas'ul."
        ),
    },
    {
        "order": 2,
        "full_name": "Maxamadsalieva Madinobonu Umidjon qizi",
        "bio_uz": (
            "O'zbekiston davlat sport akademiyasi \"Yakkakurash va suv sport turlari\" kafedrasi "
            "MSF 25-01 guruh magistranti. "
            "Taekwondo WT sport turining Pumse yo'nalishi bo'yicha O'zbekiston chempioni va \"Sport ustasi\"."
        ),
    },
    {
        "order": 3,
        "full_name": "Kaldarbekova Madinabonu Saydulla qizi",
        "bio_uz": (
            "Kaldarbekova Madinabonu Saydulla qizi sport menejmenți yo'nalishi magistranti."
        ),
    },
    {
        "order": 4,
        "full_name": "Shodiyeva Kamola Said qizi",
        "bio_uz": (
            "Shodiyeva Kamola Said qizi. "
            "Sport faoliyati — dzyudo. "
            "2 karra O'zbekiston chempioni, bir necha marotaba sovrindor. "
            "Sport ustasi."
        ),
    },
    {
        "order": 5,
        "full_name": "Isoyeva Nigina O'tkirovna",
        "bio_uz": (
            "O'zbekiston davlat sport akademiyasi Adaptiv jismoniy tarbiya va sport "
            "mutaxassisligi 1-bosqich magistranti. "
            "Yengil atletika bo'yicha Markaziy Osiyo, Xalqaro va ko'p karra O'zbekiston chempioni."
        ),
    },
    {
        "order": 6,
        "full_name": "Eshnazarova Marjona Obid qizi",
        "bio_uz": (
            "Eshnazarova Marjona Obid qizi. "
            "Sport faoliyati — dzyudo. "
            "O'zbekiston sport ustasi nomzodi."
        ),
    },
    {
        "order": 7,
        "full_name": "Ikromov Xikmatillo Akramjon o'g'li",
        "bio_uz": (
            "Ikromov Xikmatillo Akramjon o'g'li. "
            "Yo'nalish: Menejment — sport menejmenți. "
            "Erishgan yutugi: IELTS 6."
        ),
    },
    {
        "order": 8,
        "full_name": "Asqarova Sabina Shavkat qizi",
        "bio_uz": (
            "Asqarova Sabina Shavkat qizi. "
            "Adaptiv jismoniy tarbiya va sport mutaxassisligi. "
            "O'zbekiston sport ustasi nomzodi. "
            "Milliy kurash bo'yicha 1-razriyadi sohibi. "
            "Turk tili sertifikati sohibi."
        ),
    },
    {
        "order": 9,
        "full_name": "Odilova Umida Uktamovna",
        "bio_uz": (
            "Odilova Umida Uktamovna. "
            "Sport psixologiyasi mutaxassisligi. "
            "Turk tili sertifikati sohibasi."
        ),
    },
    {
        "order": 10,
        "full_name": "Guliyev Artur Marlenovich",
        "bio_uz": (
            "Guliyev Artur Marlenovich — O'zbekiston davlat sport akademiyasi "
            "Sport faoliyati (eshkak eshish) M EE 25-01 guruh magistranti. "
            "Eshkak eshish sport turi bo'yicha O'zbekiston milliy terma jamoasi va "
            "\"Mard o'g'loni\" davlat mukofoti sohibi."
        ),
    },
    {
        "order": 11,
        "full_name": "Aymuratov Musa Tatlimurat uli",
        "bio_uz": (
            "Aymuratov Musa Tatlimurat uli — O'zbekiston davlat sport akademiyasi "
            "\"Qilishbozlik sport turi\" kafedrasi MMN 25-01 guruh magistranti. "
            "Qilishbozlik sport turining xalqaro toifadagi sport ustasi, "
            "6 karra Osiyo chempioni va jahon chempionati sovrindori."
        ),
    },
]


class Command(BaseCommand):
    help = "Magistratura talabalari bio ma'lumotlarini yangilaydi"

    def handle(self, *args, **options):
        updated = 0
        for data in STUDENTS:
            name = data["full_name"]
            qs = MagistrTalaba.objects.filter(full_name__icontains=name.split()[0])
            # Try exact match first, then fuzzy
            obj = MagistrTalaba.objects.filter(full_name=name).first()
            if not obj:
                # Try by order
                obj = MagistrTalaba.objects.filter(order=data["order"]).first()
            if obj:
                obj.bio_uz = data.get("bio_uz", obj.bio_uz)
                if data.get("specialty_name_uz"):
                    obj.specialty_name_uz = data["specialty_name_uz"]
                obj.save(update_fields=["bio_uz", "specialty_name_uz"])
                self.stdout.write(self.style.SUCCESS(f"  OK {obj.order}. {obj.full_name}"))
                updated += 1
            else:
                self.stdout.write(self.style.WARNING(f"  ! Topilmadi: {name}"))

        self.stdout.write(self.style.SUCCESS(f"\nJami yangilandi: {updated} ta talaba"))
