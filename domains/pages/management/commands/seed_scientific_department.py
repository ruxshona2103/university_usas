from django.core.management.base import BaseCommand

from domains.pages.models import IlmiyBolim, IlmiyBolimYonalish


DESC_UZ = (
    "Ilmiy bo'lim akademiyada ilmiy-tadqiqot faoliyatini tashkil etadi, "
    "innovatsion loyihalarni qo'llab-quvvatlaydi va ilmiy natijalarni amaliyotga joriy etishni muvofiqlashtiradi."
)

ITEMS_UZ = [
    "Ilmiy loyihalar va grant dasturlarini rejalashtirish hamda monitoring qilish.",
    "Professor-o'qituvchilar va tadqiqotchilar nashr faoliyatini qo'llab-quvvatlash.",
    "Ilmiy konferensiya, seminar va forumlarni tashkil etish.",
    "Yosh olimlar va doktorantlar bilan tizimli ishlash.",
    "Ilmiy natijalarni tijoratlashtirish va innovatsiyalarni ommalashtirish.",
]


class Command(BaseCommand):
    help = "Ilmiy bo'lim uchun boshlang'ich ma'lumotlarni yuklaydi"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        clear = options.get("clear", False)

        solo = IlmiyBolim.get_solo()
        solo.description_uz = DESC_UZ
        solo.description_ru = solo.description_ru or "Научный отдел координирует исследовательскую деятельность академии."
        solo.description_en = solo.description_en or "The scientific department coordinates the academy's research activities."
        solo.save()

        if clear:
            solo.yonalishlar.all().delete()

        if solo.yonalishlar.exists():
            self.stdout.write(self.style.WARNING("Ilmiy bo'lim yo'nalishlari mavjud, qayta yozilmadi."))
            return

        for idx, text in enumerate(ITEMS_UZ, start=1):
            IlmiyBolimYonalish.objects.create(
                bolim=solo,
                order=idx,
                text_uz=text,
                text_ru=text,
                text_en=text,
            )

        self.stdout.write(self.style.SUCCESS("Ilmiy bo'lim seed muvaffaqiyatli qo'shildi."))
