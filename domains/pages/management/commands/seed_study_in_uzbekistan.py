"""
python manage.py seed_study_in_uzbekistan
python manage.py seed_study_in_uzbekistan --clear   # bloklarni o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand

from domains.pages.models import NavbarCategory, NavbarSubItem, ContentBlock


INTRO_TEXT_UZ = """
<h2>Xush kelibsiz! Hurmatli abituriyent(talaba)!</h2>
<p>
O'zbekiston davlat sport akademiyasi haqida yanada ko'proq ma'lumot qiziqtirsa,
siz <strong>Study in Uzbekistan</strong> veb portalidagi akademiyamiz profiliga
tashrif buyurishingiz mumkin.
</p>
<p>
Study in Uzbekistan maxsus veb portalida O'zbekistonda ta'lim olish afzalliklari,
talabalar turar joylari, viza rasmiylashtirilishi haqida ma'lumotlar, universitetlar,
ta'lim dasturlari, kontrakt narxlari, O'zbekiston taomilari va iqlimi kabi
ko'plab o'zingizni qiziqtirgan savollarga javob topishingiz mumkin.
</p>
""".strip()

INTRO_TEXT_RU = """
<h2>Добро пожаловать! Уважаемый абитуриент(студент)!</h2>
<p>
Если вас интересует больше информации о Государственной спортивной академии Узбекистана,
вы можете посетить профиль нашей академии на вeb-портале <strong>Study in Uzbekistan</strong>.
</p>
<p>
На специальном веб-портале Study in Uzbekistan вы можете найти ответы на многие
интересующие вас вопросы о преимуществах обучения в Узбекистане, общежитиях для студентов,
оформлении визы, университетах, образовательных программах, стоимости обучения по контракту,
кухне и климате Узбекистана.
</p>
""".strip()

INTRO_TEXT_EN = """
<h2>Welcome! Dear applicant(student)!</h2>
<p>
If you want to learn more about the Uzbekistan State Sports Academy,
you can visit our academy's profile on the <strong>Study in Uzbekistan</strong> web portal.
</p>
<p>
On the Study in Uzbekistan portal you can find answers to many questions:
advantages of studying in Uzbekistan, student dormitories, visa procedures,
universities, educational programs, tuition fees, Uzbek cuisine and climate.
</p>
""".strip()

ANNOUNCEMENT_UZ = "O'zbekiston davlat sport akademiyasida doktorantura (PhD va DSc) bosqichlarida tahsil olmog'i bo'lgan xorijiy fuqarolar hujjat topshirishlari uchun quyidagi havola orqali ro'yxatdan o'tishlari mumkin:"
ANNOUNCEMENT_RU = "Иностранные граждане, желающие обучаться в докторантуре (PhD и DSc) Государственной спортивной академии Узбекистана, могут зарегистрироваться для подачи документов по следующей ссылке:"
ANNOUNCEMENT_EN = "Foreign citizens wishing to study in doctoral programs (PhD and DSc) at the Uzbekistan State Sports Academy can register to submit documents via the following link:"

BUTTON_TEXT_UZ = "Study in Uzbekistan"
BUTTON_TEXT_RU = "Study in Uzbekistan"
BUTTON_TEXT_EN = "Study in Uzbekistan"

STUDY_URL = "https://studyinuzbekistan.com"
DARAJA_URL = "https://daraja.ilmiy.uz"


class Command(BaseCommand):
    help = "study-in-uzbekistan sahifasini yaratadi yoki yangilaydi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Mavjud bloklarni o'chirib qayta yaratadi")

    def handle(self, *args, **options):
        clear = options['clear']

        # ── 1. NavbarCategory — "Xalqaro aloqalar" yoki "Talabalarga" ──
        category, _ = NavbarCategory.objects.get_or_create(
            slug='xalqaro-aloqalar',
            defaults={
                'name_uz': "Xalqaro aloqalar",
                'name_ru': "Международные отношения",
                'name_en': "International Relations",
                'order': 5,
            }
        )

        # ── 2. NavbarSubItem — study-in-uzbekistan ──
        page, created = NavbarSubItem.objects.get_or_create(
            slug='study-in-uzbekistan',
            defaults={
                'category':   category,
                'name_uz':    'Study in Uzbekistan',
                'name_ru':    'Study in Uzbekistan',
                'name_en':    'Study in Uzbekistan',
                'subtitle_uz': "O'zbekistonda tahsil olish haqida to'liq ma'lumot",
                'subtitle_ru': "Полная информация об обучении в Узбекистане",
                'subtitle_en': "Complete guide to studying in Uzbekistan",
                'page_type':  NavbarSubItem.PageType.STATIC,
                'order':      10,
                'is_active':  True,
            }
        )

        if not created and clear:
            page.contentblock_items.filter(is_active=True).update(is_active=False)
            self.stdout.write(self.style.WARNING("Mavjud bloklar o'chirildi."))

        if not created and not clear:
            self.stdout.write(self.style.NOTICE(
                f"Sahifa allaqachon mavjud (slug={page.slug}). --clear bilan qayta yaratish mumkin."
            ))
            return

        # ── 3. Intro rich-text bloki ──
        intro = ContentBlock.objects.create(
            block_type='rich-text',
            title_uz='Kirish matni',
            description_uz=INTRO_TEXT_UZ,
            description_ru=INTRO_TEXT_RU,
            description_en=INTRO_TEXT_EN,
            order=10,
        )
        intro.navbar_items.add(page)

        # ── 4. E'lon / Announcement bloki ──
        ann = ContentBlock.objects.create(
            block_type='announcement',
            title_uz="E'lon:",
            title_ru="Объявление:",
            title_en="Announcement:",
            description_uz=ANNOUNCEMENT_UZ,
            description_ru=ANNOUNCEMENT_RU,
            description_en=ANNOUNCEMENT_EN,
            link=DARAJA_URL,
            json_data={
                'variant':   'warning',
                'icon':      '🔔',
                'link_text': 'daraja.ilmiy.uz',
            },
            order=20,
        )
        ann.navbar_items.add(page)

        # ── 5. Tugma bloki — Study in Uzbekistan ──
        btn = ContentBlock.objects.create(
            block_type='button-link',
            title_uz=BUTTON_TEXT_UZ,
            title_ru=BUTTON_TEXT_RU,
            title_en=BUTTON_TEXT_EN,
            link=STUDY_URL,
            json_data={
                'target':  '_blank',
                'variant': 'primary',
            },
            order=40,
        )
        btn.navbar_items.add(page)

        self.stdout.write(self.style.SUCCESS(
            f"✅ study-in-uzbekistan sahifasi muvaffaqiyatli yaratildi!\n"
            f"   Slug: {page.slug}\n"
            f"   Admin: /admin/pages/navbarsubitem/{page.pk}/change/\n"
            f"   Bloklar: intro + e'lon + tugma\n"
            f"   Rasm bloki admin orqali qo'shing: 'image' tur, order=30"
        ))
