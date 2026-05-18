"""
Ilmiy anjuman va konferensiyalar uchun seed data.
Ishlatish:
    python manage.py seed_ilmiy_anjumanlar
    python manage.py seed_ilmiy_anjumanlar --clear
"""
from django.core.management.base import BaseCommand
from domains.activities.models import IlmiyAnjuman, AnjumanTuri, AnjumanStatus

ANJUMANLAR = [
    # ─── Kelgusi / rejalangan ───────────────────────────────────────────────
    {
        "title_uz": "Sport fiziologiyasi bo'yicha xalqaro ilmiy-amaliy konferensiya",
        "title_ru": "Международная научно-практическая конференция по физиологии спорта",
        "title_en": "International Scientific-Practical Conference on Sports Physiology",
        "description_uz": (
            "O'zbekiston davlat sport akademiyasi va xorijiy hamkor universitetlar "
            "tomonidan birgalikda o'tkaziladigan xalqaro konferensiya. Xorijiy "
            "ekspertlar ishtirokida sport fanidagi zamonaviy yondashuvlar va "
            "ilmiy-amaliy usullar muhokama qilinadi."
        ),
        "description_ru": (
            "Международная конференция, проводимая совместно Государственной академией "
            "физической культуры Узбекистана и зарубежными университетами-партнёрами. "
            "С участием иностранных экспертов обсуждаются современные подходы и "
            "научно-практические методы в области спортивной науки."
        ),
        "description_en": (
            "An international conference co-hosted by the Uzbekistan State Academy of Sports "
            "and international partner universities. International experts will discuss modern "
            "approaches and evidence-based methods in sports science."
        ),
        "date": "2026-05-24",
        "location_uz": "O'ZDSA, Toshkent — Konferensiya zali",
        "location_ru": "УГФКУ, Ташкент — Конференц-зал",
        "location_en": "USAS, Tashkent — Conference Hall",
        "turi": AnjumanTuri.XALQARO,
        "status": AnjumanStatus.UPCOMING,
        "order": 1,
    },
    {
        "title_uz": "Yosh tadqiqotchilar forumi: innovatsion g'oyalar taqdimoti",
        "title_ru": "Форум молодых исследователей: презентация инновационных идей",
        "title_en": "Young Researchers Forum: Innovation Pitch Session",
        "description_uz": (
            "Doktorant va magistrlar tomonidan 30 dan ortiq ilmiy loyiha va "
            "amaliy yechimlar prezentatsiya qilinadi. Forum yosh olimlarni "
            "ilmiy hamjamiyatga qo'shilishga va xalqaro loyihalarda ishtirok "
            "etishga undaydi."
        ),
        "description_ru": (
            "Аспиранты и магистранты представят более 30 научных проектов и прикладных "
            "решений. Форум направлен на включение молодых учёных в научное сообщество "
            "и участие в международных проектах."
        ),
        "description_en": (
            "Doctoral and master's students will present more than 30 research projects "
            "and applied solutions. The forum aims to engage young scientists in the academic "
            "community and encourage participation in international projects."
        ),
        "date": "2026-06-10",
        "location_uz": "O'ZDSA, Konferensiya zali",
        "location_ru": "УГФКУ, Конференц-зал",
        "location_en": "USAS, Conference Hall",
        "turi": AnjumanTuri.SEMINAR,
        "status": AnjumanStatus.UPCOMING,
        "order": 2,
    },
    {
        "title_uz": "Sport va ta'limdagi sun'iy intellekt: imkoniyat va muammolar",
        "title_ru": "Искусственный интеллект в спорте и образовании: возможности и вызовы",
        "title_en": "Artificial Intelligence in Sports and Education: Opportunities and Challenges",
        "description_uz": (
            "Sport va ta'lim sohasida AI texnologiyalarini qo'llash imkoniyatlari, "
            "zamonaviy tahlil tizimlar va raqamli transformatsiya masalalari ko'rib chiqiladi."
        ),
        "description_ru": (
            "Рассматриваются возможности применения технологий ИИ в спорте и образовании, "
            "современные аналитические системы и вопросы цифровой трансформации."
        ),
        "description_en": (
            "The conference covers opportunities for applying AI technologies in sports and "
            "education, modern analytics systems, and digital transformation challenges."
        ),
        "date": "2026-09-15",
        "location_uz": "O'ZDSA, Toshkent",
        "location_ru": "УГФКУ, Ташкент",
        "location_en": "USAS, Tashkent",
        "turi": AnjumanTuri.XALQARO,
        "status": AnjumanStatus.UPCOMING,
        "order": 3,
    },
    # ─── O'tkazilgan ─────────────────────────────────────────────────────────
    {
        "title_uz": "Murabbiylar va olimlar davra suhbati",
        "title_ru": "Круглый стол тренеров и учёных",
        "title_en": "Round Table for Coaches and Researchers",
        "description_uz": (
            "Sport tayyorgarligida ilmiy natijalarni amaliyotga joriy etish bo'yicha "
            "ochiq muloqot. Munosabat va tajribalar almashildi, yangi hamkorlik "
            "imkoniyatlari muhokama qilindi."
        ),
        "description_ru": (
            "Открытый диалог по внедрению научных результатов в практику подготовки "
            "спортсменов. Обменялись мнениями и опытом, обсудили новые возможности сотрудничества."
        ),
        "description_en": (
            "Open dialogue on integrating research outcomes into daily training programs. "
            "Participants exchanged views and experiences, and discussed new collaboration opportunities."
        ),
        "date": "2026-04-18",
        "location_uz": "O'ZDSA, Sport zali",
        "location_ru": "УГФКУ, Спортивный зал",
        "location_en": "USAS, Sports Hall",
        "turi": AnjumanTuri.DAVRA,
        "status": AnjumanStatus.PAST,
        "order": 4,
    },
    {
        "title_uz": "Respublika olimpiya tayyorgarlik konferensiyasi",
        "title_ru": "Республиканская конференция олимпийской подготовки",
        "title_en": "Republican Olympic Preparation Conference",
        "description_uz": (
            "Olimpiya o'yinlariga tayyorgarlikning ilmiy asoslari, sport tizimi tahlili "
            "va yuqori natijali sportchilarni tayyorlashdagi yangi metodikalar ko'rib chiqildi."
        ),
        "description_ru": (
            "Рассмотрены научные основы подготовки к Олимпийским играм, анализ спортивной "
            "системы и новые методики подготовки спортсменов высокого класса."
        ),
        "description_en": (
            "Scientific foundations of Olympic preparation, analysis of the sports system, "
            "and new methodologies for training high-performance athletes were reviewed."
        ),
        "date": "2026-03-05",
        "location_uz": "Milliy olimpiya qo'mitasi, Toshkent",
        "location_ru": "Национальный олимпийский комитет, Ташкент",
        "location_en": "National Olympic Committee, Tashkent",
        "turi": AnjumanTuri.RESPUBLIKA,
        "status": AnjumanStatus.PAST,
        "order": 5,
    },
    {
        "title_uz": "Jismoniy tarbiya sohasida innovatsion pedagogik texnologiyalar seminari",
        "title_ru": "Семинар по инновационным педагогическим технологиям в физическом воспитании",
        "title_en": "Seminar on Innovative Pedagogical Technologies in Physical Education",
        "description_uz": (
            "Jismoniy tarbiya darslarida raqamli va interaktiv o'qitish usullarini "
            "qo'llash bo'yicha amaliy seminar. DSc/PhD ilmiy darajalari himoyasidan "
            "oldingi ilmiy seminar sifatida o'tkazildi."
        ),
        "description_ru": (
            "Практический семинар по применению цифровых и интерактивных методов обучения "
            "на уроках физического воспитания. Проводился как научный семинар перед защитой "
            "учёных степеней DSc/PhD."
        ),
        "description_en": (
            "A practical seminar on applying digital and interactive teaching methods in "
            "physical education classes. Held as a pre-defense scientific seminar for DSc/PhD degrees."
        ),
        "date": "2026-02-14",
        "location_uz": "O'ZDSA, O'quv binosi 2-qavat",
        "location_ru": "УГФКУ, Учебный корпус 2-й этаж",
        "location_en": "USAS, Academic Building 2nd Floor",
        "turi": AnjumanTuri.SEMINAR,
        "status": AnjumanStatus.PAST,
        "order": 6,
    },
    {
        "title_uz": "Sport psixologiyasi: nazariya va amaliyot vebinari",
        "title_ru": "Спортивная психология: вебинар «Теория и практика»",
        "title_en": "Sports Psychology: Theory and Practice Webinar",
        "description_uz": (
            "Masofaviy formatdagi onlayn vebinar. Sportchilar va murabbiylar uchun "
            "amaliy psixologik ko'nikmalar, stress boshqaruvi va motivatsiya usullari "
            "bo'yicha mutaxassislar ma'ruza qildi."
        ),
        "description_ru": (
            "Онлайн-вебинар в дистанционном формате. Специалисты выступили с лекциями по "
            "практическим психологическим навыкам, управлению стрессом и методам мотивации "
            "для спортсменов и тренеров."
        ),
        "description_en": (
            "An online webinar in remote format. Experts delivered lectures on practical "
            "psychological skills, stress management, and motivation methods for athletes and coaches."
        ),
        "date": "2026-01-22",
        "location_uz": "Onlayn (Zoom)",
        "location_ru": "Онлайн (Zoom)",
        "location_en": "Online (Zoom)",
        "turi": AnjumanTuri.VEBINAR,
        "status": AnjumanStatus.PAST,
        "order": 7,
    },
]


class Command(BaseCommand):
    help = "Ilmiy anjuman va konferensiyalar uchun seed data yozadi"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear", action="store_true",
            help="Avval mavjud barcha yozuvlarni o'chirib qayta yozish",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = IlmiyAnjuman.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"{deleted} ta yozuv o'chirildi."))

        created_count = 0
        updated_count = 0

        for item in ANJUMANLAR:
            obj, created = IlmiyAnjuman.objects.update_or_create(
                title_uz=item["title_uz"],
                defaults={**item, "is_active": True},
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seed yakunlandi: {created_count} ta yaratildi, {updated_count} ta yangilandi."
        ))
