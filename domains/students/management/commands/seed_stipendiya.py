"""
python manage.py seed_stipendiya          # yaratadi / yangilaydi
python manage.py seed_stipendiya --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand

from domains.students.models import Stipendiya, StudentInfoCategory, StudentInfo


# ── Stipendiya miqdorlari jadvali ─────────────────────────────────────────────

STIPENDIYALAR = [
    {
        "order": 1,
        "status_uz": "Bazaviy stipendiya",
        "status_ru": "Базовая стипендия",
        "status_en": "Basic scholarship",
        "amount": 569670,
        "note_uz": "",
        "note_ru": "",
        "note_en": "",
    },
    {
        "order": 2,
        "status_uz": '"A\'lochi" stipendiya',
        "status_ru": '"Отличник" стипендия',
        "status_en": '"Honors" scholarship',
        "amount": 669736,
        "note_uz": "+20%",
        "note_ru": "+20%",
        "note_en": "+20%",
    },
    {
        "order": 3,
        "status_uz": '"Nogiron" stipendiyasi',
        "status_ru": 'Стипендия для лиц с инвалидностью',
        "status_en": 'Disability scholarship',
        "amount": 854502,
        "note_uz": "+50%",
        "note_ru": "+50%",
        "note_en": "+50%",
    },
    {
        "order": 4,
        "status_uz": "Doktorantura",
        "status_ru": "Докторантура",
        "status_en": "Doctoral studies",
        "amount": 7959848,
        "note_uz": "",
        "note_ru": "",
        "note_en": "",
    },
    {
        "order": 5,
        "status_uz": "Tayanch doktorantura",
        "status_ru": "Базовая докторантура",
        "status_en": "Base doctoral program",
        "amount": 6229999,
        "note_uz": "",
        "note_ru": "",
        "note_en": "",
    },
    {
        "order": 6,
        "status_uz": "Stajer-tadqiqotchi",
        "status_ru": "Стажёр-исследователь",
        "status_en": "Researcher-trainee",
        "amount": 5515120,
        "note_uz": "",
        "note_ru": "",
        "note_en": "",
    },
]


# ── Matn bo'limlari (StudentInfo) ─────────────────────────────────────────────

CATEGORY_SLUG = "stipendiyalar"

TEXT_ITEMS = [
    {
        "order": 1,
        "title_uz": "Stipendiyalar haqida",
        "title_ru": "О стипендиях",
        "title_en": "About scholarships",
        "content_uz": (
            "Akademiyada stipendiya tayinlash o'quv yilida ikki marotaba o'tkaziladi va "
            "stipendiya avvalgi (tugallangan) semestr yakuniy nazorat natijalari e'lon "
            "qilinganidan so'ng, rektorning buyrug'i bilan har bir o'quv semestri oyining "
            "birinchi kunidan boshlab tayinlanadi va to'lanadi.\n\n"
            "Davlat granti asosida ta'lim olayotgan, o'quv semestri uchun o'zlashtirish "
            "natijalari bo'yicha uzrsiz sabablarga ko'ra akademik qarzi (bir yoki undan ortiq "
            "fanlar bo'yicha 55 foizdan kam reytingga) bo'lgan talabalar keyingi o'quv semestri "
            "oyining birinchi kunidan boshlab stipendiya olish huquqidan mahrum qilinadi. "
            "Belgilangan tartibda akademik qarzini bartaraf etgan (tegishli fanlar bo'yicha 55 va "
            "undan ortiq foiz to'plagan) va fanlardan o'zlashtirish ko'rsatkichlarining 30 foizdan "
            "kam qismi «qoniqarli» baho (reyting ko'rsatkichi 71 balldan kam) bo'lgan "
            "talabalarga stipendiya akademik qarzni bartaraf etish muddati tugaganidan keyingi "
            "oyning birinchi kunidan boshlab, stipendiyaning bazaviy miqdorida keyingi o'quv "
            "semestriga qadar tayinlanadi.\n\n"
            "Stipendiyali to'lov-kontrakt asosida ta'lim olayotgan talabalarga o'quv semestri "
            "yakuni bo'yicha fanlardan o'zlashtirish ko'rsatkichlaridan qat'i nazar bazaviy "
            "miqdordagi stipendiya tayinlanadi va to'lanadi."
        ),
        "content_ru": (
            "Назначение стипендии в Академии осуществляется дважды в учебном году и назначается "
            "с первого числа каждого учебного семестра приказом ректора после объявления "
            "результатов итогового контроля предыдущего (завершённого) семестра.\n\n"
            "Студенты, обучающиеся на основе государственного гранта, имеющие академическую "
            "задолженность (рейтинг менее 55% по одному и более предметам) по результатам "
            "освоения за учебный семестр по неуважительным причинам, лишаются права на получение "
            "стипендии с первого числа месяца следующего учебного семестра. Студентам, "
            "ликвидировавшим академическую задолженность в установленном порядке (набравшим 55 и "
            "более процентов по соответствующим предметам) и у которых менее 30% показателей "
            "успеваемости по предметам оценены как «удовлетворительно» (рейтинговый показатель "
            "менее 71 балла), стипендия назначается в базовом размере с первого числа месяца "
            "после истечения срока ликвидации академической задолженности до следующего учебного "
            "семестра.\n\n"
            "Студентам, обучающимся на основе платного контракта со стипендией, стипендия "
            "назначается и выплачивается в базовом размере вне зависимости от показателей "
            "успеваемости по предметам по итогам учебного семестра."
        ),
        "content_en": (
            "Scholarships in the Academy are awarded twice per academic year and are assigned "
            "from the first day of each academic semester by the rector's order, after the "
            "results of the final assessments of the previous (completed) semester are announced.\n\n"
            "Students studying on a state grant who have academic debt (a rating below 55% in "
            "one or more subjects) based on the semester's academic performance for unjustified "
            "reasons, lose the right to receive a scholarship from the first day of the following "
            "academic semester. Students who have resolved their academic debt in the prescribed "
            "manner (scoring 55% or more in the relevant subjects) and whose academic performance "
            "in less than 30% of subjects is rated as 'satisfactory' (rating below 71 points) "
            "are awarded a scholarship at the base amount from the first day of the month after "
            "the academic debt resolution period ends, until the next academic semester.\n\n"
            "Students studying on a paid contract with scholarship are awarded and paid a "
            "scholarship in the base amount regardless of their subject performance at the end "
            "of the academic semester."
        ),
    },
    {
        "order": 2,
        "title_uz": "O'zbekiston Respublikasi Prezidenti va nomli davlat stipendiyalari",
        "title_ru": "Президентские и именные государственные стипендии Республики Узбекистан",
        "title_en": "Presidential and Named State Scholarships of the Republic of Uzbekistan",
        "content_uz": (
            "O'zbekiston Respublikasi Prezidenti va nomli davlat stipendiyalari mamlakatimizning "
            "eng yaxshi, iqtidorli talabalariga beriladi. Mazkur stipendiyalar O'zbekiston "
            "Respublikasi Vazirlar Mahkamasi tomonidan belgilangan tartibda tayinlanadi."
        ),
        "content_ru": (
            "Президентские и именные государственные стипендии Республики Узбекистан "
            "присуждаются лучшим и наиболее одарённым студентам страны. Данные стипендии "
            "назначаются в порядке, установленном Кабинетом Министров Республики Узбекистан."
        ),
        "content_en": (
            "The Presidential and Named State Scholarships of the Republic of Uzbekistan are "
            "awarded to the best and most talented students in the country. These scholarships "
            "are assigned in the manner established by the Cabinet of Ministers of the Republic "
            "of Uzbekistan."
        ),
    },
    {
        "order": 3,
        "title_uz": "Magistrlik dissertatsiyasi himoyasi",
        "title_ru": "Защита магистерской диссертации",
        "title_en": "Master's Thesis Defense",
        "content_uz": "Magistrlik dissertatsiyasi himoyasi 2026-2027 o'quv yili yakuniga rejalashtirilgan.",
        "content_ru": "Защита магистерской диссертации запланирована на конец 2026-2027 учебного года.",
        "content_en": "The master's thesis defense is scheduled for the end of the 2026–2027 academic year.",
    },
]


class Command(BaseCommand):
    help = "Stipendiyalar jadvalini va matn bo'limlarini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Oldin mavjud ma'lumotlarni o'chiradi")

    def handle(self, *args, **options):
        if options['clear']:
            Stipendiya.objects.all().delete()
            StudentInfo.objects.filter(category__slug=CATEGORY_SLUG).delete()
            StudentInfoCategory.objects.filter(slug=CATEGORY_SLUG).delete()
            self.stdout.write(self.style.WARNING("Eski stipendiya ma'lumotlari o'chirildi."))

        self._seed_amounts()
        self._seed_text()
        self.stdout.write(self.style.SUCCESS("Stipendiya ma'lumotlari muvaffaqiyatli saqlandi."))

    def _seed_amounts(self):
        for item in STIPENDIYALAR:
            obj, created = Stipendiya.objects.update_or_create(
                order=item['order'],
                defaults=item,
            )
            action = "Yaratildi" if created else "Yangilandi"
            self.stdout.write(f"  {action}: {obj.status_uz} — {obj.amount:,}")

    def _seed_text(self):
        category, _ = StudentInfoCategory.objects.update_or_create(
            slug=CATEGORY_SLUG,
            defaults={
                'title_uz': "Stipendiyalar",
                'title_ru': "Стипендии",
                'title_en': "Scholarships",
                'order': 20,
            },
        )
        for item in TEXT_ITEMS:
            StudentInfo.objects.update_or_create(
                category=category,
                order=item['order'],
                defaults={**item, 'is_active': True},
            )
            self.stdout.write(f"  + Matn: {item['title_uz']}")
