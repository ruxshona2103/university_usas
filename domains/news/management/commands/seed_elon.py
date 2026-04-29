"""
python manage.py seed_elon          # yaratadi / yangilaydi
python manage.py seed_elon --clear  # o'chirib qaytadan yozadi
"""
from django.utils import timezone
from django.core.management.base import BaseCommand
from domains.news.models import InformationContent

ELONLAR = [
    {
        "title_uz": "«Zakovat intellektual» o'yiniga taklif",
        "title_ru": "Приглашение на интеллектуальную игру «Закоят»",
        "title_en": "Invitation to the Zakovat Intellectual Game",
        "description_uz": (
            "O'zbekiston davlat sport akademiyasi tomonidan talabalarni zukkolikka chorlash hamda "
            "ijodiy fikrlash qobiliyatini rivojlantirish maqsadida «Zakovat intellektual» o'yini tashkil etilmoqda.\n\n"
            "Mazkur o'yinda ishtirok etish uchun magistratura bosqichi talabalari taklif etiladi. "
            "Shuningdek, jamoalarni qo'llab-quvvatlash maqsadida barcha Akademiya xodimlari va talabalari ham "
            "faol ishtirok etishga chorlanadi.\n\n"
            "💬 Ro'yxatdan o'tish va qo'shimcha ma'lumotlar uchun «Iqtidorli talabalar bo'limi»ga murojaat qilishingiz mumkin."
        ),
        "description_ru": (
            "Государственная академия спорта Узбекистана организует интеллектуальную игру «Закоят» "
            "с целью развития эрудиции и творческого мышления студентов.\n\n"
            "К участию в игре приглашаются студенты магистратуры. Также все сотрудники и студенты Академии "
            "приглашаются к активному участию в поддержке команд.\n\n"
            "💬 По вопросам регистрации и дополнительной информации обращайтесь в «Отдел талантливых студентов»."
        ),
        "description_en": (
            "The State Academy of Sports of Uzbekistan is organising the Zakovat Intellectual Game "
            "to encourage students to develop their erudition and creative thinking.\n\n"
            "Master's degree students are invited to participate. All Academy staff and students are also "
            "welcome to attend and support the teams.\n\n"
            "💬 For registration and further information, please contact the 'Department of Talented Students'."
        ),
        "date": timezone.now(),
        "external_url": "",
        "is_published": True,
    },
]


class Command(BaseCommand):
    help = "E'lonlar (elon) fake ma'lumotlarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = InformationContent.objects.filter(content_type='elon').delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta e'lon"))

        created = updated = 0
        for d in ELONLAR:
            obj, is_new = InformationContent.objects.update_or_create(
                title_uz=d['title_uz'],
                content_type='elon',
                defaults=d,
            )
            if is_new:
                created += 1
            else:
                updated += 1
            self.stdout.write(f"  [{'+'if is_new else '~'}] {obj.title_uz[:70].encode('ascii', 'replace').decode()}")

        self.stdout.write(self.style.SUCCESS(f"\nNatija: {created} yangi, {updated} yangilandi"))
