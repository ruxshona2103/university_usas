"""
python manage.py seed_oav_press          # yaratadi / yangilaydi
python manage.py seed_oav_press --clear  # o'chirib qaytadan yozadi
"""
import datetime

from django.utils import timezone
from django.core.management.base import BaseCommand
from domains.news.models import InformationContent

OAV_ITEMS = [
    {
        "title_uz": "Fabio Kannavaro: Jahon chempionatiga jiddiy tayyorgarlik ko'ryapmiz",
        "title_ru": "Фабио Канаваро: Мы серьёзно готовимся к чемпионату мира",
        "title_en": "Fabio Cannavaro: We are seriously preparing for the World Cup",
        "description_uz": (
            "Sport.uz nashri O'zbekiston milliy terma jamoa bosh murabbiyi Fabio Kannavaro bilan "
            "muloqot qildi. Murabbiyi jahon chempionati uchun tayyorgarlik, o'yinchilar holati "
            "va kelajak rejalari haqida so'zladi."
        ),
        "description_ru": (
            "Издание Sport.uz пообщалось с главным тренером сборной Узбекистана Фабио Канаваро. "
            "Тренер рассказал о подготовке к чемпионату мира, состоянии игроков и планах на будущее."
        ),
        "description_en": (
            "Sport.uz spoke with the head coach of the Uzbekistan national team Fabio Cannavaro. "
            "The coach talked about preparation for the World Cup, player conditions, and future plans."
        ),
        "date": timezone.datetime(2026, 5, 12, 10, 0, tzinfo=datetime.timezone.utc),
        "external_url": "https://sport.uz",
        "is_published": True,
    },
    {
        "title_uz": "Otabek Umarov: VIII Toshkent xalqaro marafoni yuqori saviyada o'tadi",
        "title_ru": "Отабек Умаров: VIII Ташкентский международный марафон пройдёт на высоком уровне",
        "title_en": "Otabek Umarov: The 8th Tashkent International Marathon will be held at a high level",
        "description_uz": (
            "Akademiya rektori Otabek Umarov VIII Toshkent xalqaro marafoni haqida matbuot "
            "xodimlariga intervyu berdi. Rektor marafonning sport rivojidagi ahamiyatini ta'kidladi."
        ),
        "description_ru": (
            "Ректор академии Отабек Умаров дал интервью прессе о VIII Ташкентском международном "
            "марафоне. Ректор подчеркнул значимость марафона в развитии спорта."
        ),
        "description_en": (
            "Academy rector Otabek Umarov gave an interview to the press about the 8th Tashkent "
            "International Marathon, emphasising its importance in the development of sport."
        ),
        "date": timezone.datetime(2026, 4, 5, 10, 0, tzinfo=datetime.timezone.utc),
        "external_url": "https://uza.uz",
        "is_published": True,
    },
    {
        "title_uz": "Diyora Keldiyorova: Katta sportga qaytayapman",
        "title_ru": "Дийора Келдиёрова: Я возвращаюсь в большой спорт",
        "title_en": "Diyora Keldiyorova: I am returning to big sport",
        "description_uz": (
            "Akademiya bitiruvchisi, karate bo'yicha jahon chempioni Diyora Keldiyorova "
            "Kun.uz nashriga intervyu berdi va katta sportga qaytish niyatini ma'lum qildi."
        ),
        "description_ru": (
            "Выпускница академии, чемпионка мира по карате Дийора Келдиёрова дала интервью "
            "Kun.uz и заявила о намерении вернуться в большой спорт."
        ),
        "description_en": (
            "Academy graduate and world karate champion Diyora Keldiyorova gave an interview "
            "to Kun.uz and announced her intention to return to big sport."
        ),
        "date": timezone.datetime(2026, 4, 4, 10, 0, tzinfo=datetime.timezone.utc),
        "external_url": "https://kun.uz",
        "is_published": True,
    },
    {
        "title_uz": "O'zbekiston sport akademiyasi xalqaro reyting ko'rsatkichlarini yaxshiladi",
        "title_ru": "Академия спорта Узбекистана улучшила показатели в международных рейтингах",
        "title_en": "Uzbekistan Sports Academy improves international ranking indicators",
        "description_uz": (
            "Daryo.uz nashri O'zbekiston Davlat Sport Akademiyasining xalqaro reytinglardagi "
            "muvaffaqiyatlari haqida batafsil maqola chiqardi."
        ),
        "description_ru": (
            "Издание Daryo.uz опубликовало подробную статью об успехах Государственной академии "
            "спорта Узбекистана в международных рейтингах."
        ),
        "description_en": (
            "Daryo.uz published a detailed article about the achievements of the State Sports "
            "Academy of Uzbekistan in international rankings."
        ),
        "date": timezone.datetime(2026, 3, 20, 9, 0, tzinfo=datetime.timezone.utc),
        "external_url": "https://daryo.uz",
        "is_published": True,
    },
    {
        "title_uz": "Akademiya ilmiy jurnali Scopus bazasiga kiritildi",
        "title_ru": "Научный журнал академии включён в базу Scopus",
        "title_en": "Academy scientific journal included in the Scopus database",
        "description_uz": (
            "Gazeta.uz nashri Akademiyaning ilmiy jurnali Scopus xalqaro ma'lumotlar bazasiga "
            "kiritilishi munosabati bilan suhbat o'tkazdi."
        ),
        "description_ru": (
            "Gazeta.uz провела интервью в связи с включением научного журнала академии "
            "в международную базу данных Scopus."
        ),
        "description_en": (
            "Gazeta.uz conducted an interview following the inclusion of the Academy's "
            "scientific journal in the international Scopus database."
        ),
        "date": timezone.datetime(2026, 3, 10, 9, 0, tzinfo=datetime.timezone.utc),
        "external_url": "https://gazeta.uz",
        "is_published": True,
    },
]


class Command(BaseCommand):
    help = "OAV biz haqimizda (press) namuna ma'lumotlarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = InformationContent.objects.filter(content_type='press').delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta press item"))

        created = updated = 0
        for d in OAV_ITEMS:
            obj, is_new = InformationContent.objects.update_or_create(
                title_uz=d['title_uz'],
                content_type='press',
                defaults=d,
            )
            if is_new:
                created += 1
            else:
                updated += 1
            self.stdout.write(
                f"  [{'+'if is_new else '~'}] {obj.title_uz[:70].encode('ascii', 'replace').decode()}"
            )

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created} yangi, {updated} yangilandi\n"
            "Admindan InformationContent > PressService bo'limiga kirib rasm qo'shing."
        ))
