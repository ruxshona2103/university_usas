"""
python manage.py seed_kafedra           # yaratadi / yangilaydi
python manage.py seed_kafedra --clear   # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.academic.models import FakultetKafedra

DATA = [
    # ── FAKULTET ──────────────────────────────────────────────────────────────
    {
        'slug':    'sport-va-parasport-turlari-fakulteti',
        'type':    FakultetKafedra.FAKULTET,
        'order':   1,
        'name_uz': "Sport va parasport turlari fakulteti",
        'name_ru': "Факультет видов спорта и параспорта",
        'name_en': "Faculty of Sports and Parasports",
        'description_uz': (
            "Sport va parasport turlari fakulteti 2025-yilda tashkil topgan. "
            "Fakultetda bakalavriat va magistratura ta'lim yo'nalishlari bo'yicha "
            "yuqori malakali mutaxassislar tayyorlanadi. Fakultet manzili: Olimpiya shaharchasi."
        ),
        'description_ru': (
            "Факультет видов спорта и параспорта основан в 2025 году. "
            "На факультете ведётся подготовка высококвалифицированных специалистов "
            "по направлениям бакалавриата и магистратуры."
        ),
        'description_en': (
            "The Faculty of Sports and Parasports was established in 2025. "
            "The faculty trains highly qualified specialists in bachelor's and master's programmes."
        ),
        'decree_info': "",
        'phone':   "996828208",
        'email':   "jahanger_kr@mail.ru",
        # Dekan
        'dean_name_uz': "Kaipov Jaxanger Askarovich",
        'dean_name_ru': "Каипов Яхангер Аскарович",
        'dean_name_en': "Kaipov Jakhanger Askarovich",
        'dean_phone':   "996828208",
        'dean_email':   "jahanger_kr@mail.ru",
        # O'rinbosar
        'vice_dean_name_uz': "Ortiqov Ma'rufjon Abdullayevich",
        'vice_dean_name_ru': "Ортиков Маруфжон Абдуллаевич",
        'vice_dean_name_en': "Ortiqov Marufjon Abdullayevich",
        'vice_dean_phone':   "",
        'vice_dean_email':   "",
        # bachelor_subjects maydoni → bakalavriat yo'nalishlari
        'bachelor_subjects_uz': (
            "61010200 — Sport faoliyati\n"
            "61010300 — Adaptiv jismoniy tarbiya va sport (parasport)"
        ),
        'bachelor_subjects_ru': (
            "61010200 — Спортивная деятельность\n"
            "61010300 — Адаптивная физическая культура и спорт (параспорт)"
        ),
        'bachelor_subjects_en': (
            "61010200 — Sports Activity\n"
            "61010300 — Adaptive Physical Education and Sports (Parasport)"
        ),
        # master_subjects maydoni → magistratura yo'nalishlari
        'master_subjects_uz': (
            "71010301 — Adaptiv jismoniy tarbiya va sport\n"
            "70310301 — Psixologiya\n"
            "71010201 — Sport faoliyati\n"
            "70410801 — Menejment\n"
            "70411201 — Marketing"
        ),
        'master_subjects_ru': (
            "71010301 — Адаптивная физическая культура и спорт\n"
            "70310301 — Психология\n"
            "71010201 — Спортивная деятельность\n"
            "70410801 — Менеджмент\n"
            "70411201 — Маркетинг"
        ),
        'master_subjects_en': (
            "71010301 — Adaptive Physical Education and Sports\n"
            "70310301 — Psychology\n"
            "71010201 — Sports Activity\n"
            "70410801 — Management\n"
            "70411201 — Marketing"
        ),
        'sport_types_uz': "",
        'sport_types_ru': "",
        'sport_types_en': "",
    },

    # ── KAFEDRALAR ────────────────────────────────────────────────────────────
    {
        'slug':    'yakkakurash-va-suv-sport-turlari-kafedrasi',
        'type':    FakultetKafedra.KAFEDRA,
        'order':   2,
        'name_uz': "Yakkakurash va suv sport turlari kafedrasi",
        'name_ru': "Кафедра единоборств и водных видов спорта",
        'name_en': "Department of Combat Sports and Aquatics",
        'description_uz': (
            "O'zbekiston Respublikasi Prezidentining 2024-yil 28-maydagi PQ-197-son qarori bilan "
            "O'zbekiston davlat sport akademiyasi tashkil qilindi. Akademiyaning \"Yakkakurash va "
            "suv sport turlari\" kafedrasida 2025-yil 2-sentabrdan boshlab Dzyudo, Taekvondo WT, "
            "Boks, Eshkak eshish, Yengil atletika, O'g'ir atletika, Yunon-rim kurash, Erkin kurash, "
            "Suzish, Velosport, Gimnastika, Komondan otish, Qilichbozlik, O'q otish sport turlari "
            "kafedra tarkibiga kiritildi."
        ),
        'description_ru': (
            "На основании Постановления Президента Республики Узбекистан № ПП-197 от 28 мая 2024 года "
            "была создана Академия государственного спорта Узбекистана. С 2 сентября 2025 года в состав "
            "кафедры единоборств и водных видов спорта включены: дзюдо, тхэквондо ВТ, бокс, академическая "
            "гребля, лёгкая атлетика, тяжёлая атлетика, греко-римская борьба, вольная борьба, плавание, "
            "велоспорт, гимнастика, стрельба из лука, фехтование, стрельба."
        ),
        'description_en': (
            "By Decree No. PQ-197 of the President of the Republic of Uzbekistan dated May 28, 2024, "
            "the Uzbekistan State Sports Academy was established. From September 2, 2025, the Department "
            "of Combat Sports and Aquatics includes: Judo, Taekwondo WT, Boxing, Rowing, Athletics, "
            "Weightlifting, Greco-Roman Wrestling, Freestyle Wrestling, Swimming, Cycling, Gymnastics, "
            "Archery, Fencing, Shooting."
        ),
        'decree_info': "PQ-197-son, 2024-yil 28-may",
        'phone':   "",
        'email':   "qodirov.sirojiddin@list.ru",
        # Mudiri
        'mudiri_name_uz':   "Qodirov Sirojiddin Erkinboyevich",
        'mudiri_name_ru':   "Кодиров Сирожиддин Эркинбоевич",
        'mudiri_name_en':   "Qodirov Sirojiddin Erkinboyevich",
        'mudiri_phone':     "",
        'mudiri_email':     "qodirov.sirojiddin@list.ru",
        'mudiri_degree_uz': "Jismoniy tarbiya va sport fanlari nomzodi, dotsent",
        'mudiri_degree_ru': "Кандидат наук по физической культуре и спорту, доцент",
        'mudiri_degree_en': "Candidate of Sciences in Physical Education and Sports, Associate Professor",
        'sport_types_uz': (
            "Dzyudo\n"
            "Taekvondo WT\n"
            "Boks\n"
            "Eshkak eshish\n"
            "Yengil atletika\n"
            "O'g'ir atletika\n"
            "Yunon-rim kurash\n"
            "Erkin kurash\n"
            "Suzish\n"
            "Velosport\n"
            "Gimnastika\n"
            "Komondan otish\n"
            "Qilichbozlik\n"
            "O'q otish"
        ),
        'sport_types_ru': (
            "Дзюдо\n"
            "Тхэквондо ВТ\n"
            "Бокс\n"
            "Академическая гребля\n"
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
        'sport_types_en': (
            "Judo\n"
            "Taekwondo WT\n"
            "Boxing\n"
            "Rowing\n"
            "Athletics\n"
            "Weightlifting\n"
            "Greco-Roman Wrestling\n"
            "Freestyle Wrestling\n"
            "Swimming\n"
            "Cycling\n"
            "Gymnastics\n"
            "Archery\n"
            "Fencing\n"
            "Shooting"
        ),
        'bachelor_subjects_uz': (
            "Tayanch sport turlarini o'rgatish metodikasi (Suzish)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Sport va xarakatli o'yinlar)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Yengil atletika)\n"
            "Tayanch sport turlarini o'rgatish metodikasi (Gimnastika)\n"
            "Taekvondo nazariyasi va uslubiyati\n"
            "Dzyudo nazariyasi va uslubiyati\n"
            "Boks nazariyasi va uslubiyati\n"
            "Eshkak eshish nazariyasi va uslubiyati\n"
            "Yengil atletika nazariyasi va uslubiyati\n"
            "O'g'ir atletika nazariyasi va uslubiyati\n"
            "Yunon-rim kurash nazariyasi va uslubiyati\n"
            "Erkin kurash nazariyasi va uslubiyati\n"
            "Suzish nazariyasi va uslubiyati\n"
            "Velosport nazariyasi va uslubiyati\n"
            "Gimnastika nazariyasi va uslubiyati\n"
            "Komondan otish nazariyasi va uslubiyati\n"
            "Qilichbozlik nazariyasi va uslubiyati\n"
            "O'q otish nazariyasi va uslubiyati"
        ),
        'bachelor_subjects_ru': "",
        'bachelor_subjects_en': "",
        'master_subjects_uz': (
            "Sportda ilmiy tadqiqotlar\n"
            "Sportda saralash, modellashtirish va bashorat qilish\n"
            "Taekvondoda sportchilarni tayyorlashning ilmiy-uslubiy asoslari\n"
            "Boksda sportchilarni tayyorlashning ilmiy-uslubiy asoslari\n"
            "Dzyudo-da sportchilarni tayyorlashning ilmiy-uslubiy asoslari\n"
            "Eshkak eshishda sportchilarni tayyorlashning ilmiy-uslubiy asoslari"
        ),
        'master_subjects_ru': "",
        'master_subjects_en': "",
    },
    {
        'slug':    'parasport-va-umumkasbiy-fanlar-kafedrasi',
        'type':    FakultetKafedra.KAFEDRA,
        'order':   3,
        'name_uz': "Parasport va umumkasbiy fanlar kafedrasi",
        'name_ru': "Кафедра параспорта и общепрофессиональных дисциплин",
        'name_en': "Department of Parasport and General Professional Disciplines",
        'description_uz': (
            "O'zbekiston Respublikasi Prezidentining 2022-yil 18-fevraldagi PQ-197-sonli "
            "\"O'zbekiston davlat sport akademiyasini tashkil etish to'g'risida\"gi Qaroriga muvofiq "
            "mamlaktimizda jismoniy tarbiya va sport sohasida yuqori malakali mutaxassislar "
            "tayyorlashning zamonaviy tizimi yo'lga qo'yildi. Kafedra parasport yo'nalishida "
            "mutaxassislar tayyorlash, nogironligi bo'lgan shaxslar bilan ishlash metodikasini "
            "rivojlantirish, shuningdek, talabalarni umumkasbiy fanlar bo'yicha nazariy va amaliy "
            "bilimlar bilan ta'minlashga ixtisoslashgan."
        ),
        'description_ru': (
            "В соответствии с Постановлением Президента Республики Узбекистан № ПП-197 от 18 февраля "
            "2022 года в стране была создана современная система подготовки высококвалифицированных "
            "специалистов в области физической культуры и спорта. Кафедра специализируется на "
            "подготовке специалистов по параспорту, развитии методики работы с лицами с ограниченными "
            "возможностями здоровья, а также обеспечении студентов теоретическими и практическими "
            "знаниями по общепрофессиональным дисциплинам."
        ),
        'description_en': (
            "In accordance with the Decree of the President of the Republic of Uzbekistan No. PQ-197 "
            "dated February 18, 2022, a modern system for training highly qualified specialists in "
            "physical culture and sports was established. The department specialises in training "
            "parasport specialists, developing methodologies for working with persons with disabilities, "
            "and providing students with theoretical and practical knowledge in general professional disciplines."
        ),
        'decree_info': "PQ-197-son, 2022-yil 18-fevral",
        'phone':   "",
        'email':   "sobirovalaylo90@gmail.com",
        # Mudiri
        'mudiri_name_uz':   "Sobirova Laylo Baxromovna",
        'mudiri_name_ru':   "Собирова Лайло Бахромовна",
        'mudiri_name_en':   "Sobirova Laylo Baxromovna",
        'mudiri_phone':     "",
        'mudiri_email':     "sobirovalaylo90@gmail.com",
        'mudiri_degree_uz': "Pedagogika fanlari nomzodi, dotsent",
        'mudiri_degree_ru': "Кандидат педагогических наук, доцент",
        'mudiri_degree_en': "Candidate of Pedagogical Sciences, Associate Professor",
        'sport_types_uz': "",
        'sport_types_ru': "",
        'sport_types_en': "",
        'bachelor_subjects_uz': (
            "Sportda xorijiy til\n"
            "Rus tili\n"
            "O'zbekistonning eng yangi tarixi\n"
            "Jismoniy tarbiya va olimpiya harakati tarixi\n"
            "Bioximiya va sport bioximiyasi\n"
            "Anatomiya\n"
            "Sportda axborot-kommunikasiya texnologiyalari\n"
            "Dinshunoslik\n"
            "Adaptiv jismoniy tarbiya va paralimpiya harakati\n"
            "Para sport turlarini o'rgatish metodikasi (siklik, asiklik, sport o'yinlari, yakkakurash)\n"
            "Adaptiv jismoniy tarbiya va sport nazariyasi va uslubiyati (7 ta qism)\n"
            "Falsafa\n"
            "Sport pedagogikasi\n"
            "Sport biomexanikasi\n"
            "Fiziologiya va sport fiziologiyasi (1, 2-qism)\n"
            "Sport psixologiyasi\n"
            "Jismoniy tarbiya va sport nazariyasi (1-qism)\n"
            "Para sport turlarini o'rgatish metodikasi (sport o'yinlari)\n"
            "Para sport turlarini o'rgatish metodikasi (yakkakurash)\n"
            "Tanlov fanlar"
        ),
        'bachelor_subjects_ru': "",
        'bachelor_subjects_en': "",
        'master_subjects_uz': (
            "Ilmiy tadqiqot metodologiyasi\n"
            "Sport morfologiyasi\n"
            "Sportda matematik-statistik tahlil (1 va 2-qism)\n"
            "Tanlangan sport turining fiziologik tasnifi\n"
            "Sport faoliyatining huquqiy ta'minlanishi\n"
            "Adaptiv sog'lomlashtirish jismoniy tarbiya texnologiyalari\n"
            "Adaptiv jismoniy tarbiyada nazorat turlari va sport klassifikatsiyasi (1 va 2-qism)\n"
            "Adaptiv jismoniy tarbiya va parasportning tibbiy-biologik asoslari\n"
            "Adaptiv jismoniy tarbiya va sportni boshqarish\n"
            "Psixologiyada tadqiqotlarni rejalashtirish\n"
            "Sportda psixotexnologiyalar (1 va 2-qism)\n"
            "Paralimpiya sportida psixologik tayyorgarlik\n"
            "Sport kauchingi texnologiyalari\n"
            "Sport psixologiyasi metodologiyasi\n"
            "Sportda marketing kommunikasiyasi\n"
            "Sport sohasida raqamli iqtisodiyot\n"
            "Sport inshootlari marketing\n"
            "Sport marketingi (1 va 2-qism)\n"
            "Xalqaro sport huquqi\n"
            "Sportda matematik modellashtirish\n"
            "Sportda tadbirkorlik\n"
            "Sport iqtisodiyoti va menejmenti\n"
            "Menejmentda zamonaviy kommunikasiyalar\n"
            "Sport inshootlarini boshqarish\n"
            "Sport menejmenti (1 va 2-qism)\n"
            "Korporativ menejment\n"
            "Event-menejmenti"
        ),
        'master_subjects_ru': "",
        'master_subjects_en': "",
    },

    # ── TASHKILOTLAR ──────────────────────────────────────────────────────────
    {
        'slug':    'xotin-qizlar-qomitasi',
        'type':    FakultetKafedra.TASHKILOT,
        'order':   1,
        'name_uz': "Xotin-qizlar masalalari bo'yicha maslahat kengashi",
        'name_ru': "Консультативный совет по вопросам женщин",
        'name_en': "Women's Advisory Council",
        'description_uz': (
            "Akademiya xotin-qizlar kengashi raisiga O'zbekiston Respublikasi Oliy va o'rta "
            "maxsus ta'lim vazirining 2020-yil 17-iyun № 326 buyrug'iga asosan xotin-qizlar "
            "masalalari bo'yicha rektor maslahatchisi maqomi berilgan.\n\n"
            "O'zbekiston davlat sport akademiyasi jamoasida 1023 ga yaqin ayollar faoliyat "
            "ko'rsatmoqdalar. Ulardan: 501 ta professor o'qituvchilar bo'lib, 522 xodimlar. "
            "Talaba qizlarimiz soni 11714 tani, shundan 2150 tasi oilali qizlarni tashkil qiladi.\n\n"
            "Akademiya xotin-qizlar kengashining nizomi mavjud bo'lib, ushbu nizom bo'yicha "
            "faoliyat olib boradi. Xotin-qizlar kengashi jamoat tashkiloti sifatida o'z faoliyatini "
            "O'zbekiston Respublikasi Konstitutsiyasi, \"Nodavlat notijorat tashkilotlari to'g'risida\"gi "
            "va \"O'zbekiston Respublikasida jamoat birlashmalari to'g'risida\"gi Qonunlarga muvofiq "
            "olib boradi.\n\n"
            "Akademiya xotin-qizlar kengashi professor–o'qituvchi, xodimlar hamda talaba qizlarning "
            "jamiyatda siyosiy, ijtimoiy, iqtisodiy sohalaridagi vazifalarni hal qilishdagi faolligini "
            "kuchaytirish, xotin-qizlarni har tomonlama qo'llab-quvvatlash, ijtimoiy-iqtisodiy ahvolini "
            "yaxshilash, ularning huquq va manfaatlarini himoya qilish va ta'minlash, kasbiy mahoratini "
            "oshirish, milliy va ma'naviy qadriyatlarimizga asoslangan holda oila munosabatlarini "
            "mustahkamlash maqsadida ish olib boradi.\n\n"
            "Oilada sog'lom turmush tarzini shakllantirish, reproduktiv salomatlikni yaxshilash, "
            "onalik va bolalikni muhofaza qilish bo'yicha tadbirlarni universitet \"Sog'lom avlod\" "
            "markazi hamda \"Ibn Sino\" markazi bilan hamkorlikda amalga oshiradi."
        ),
        'description_ru': (
            "Председателю женского совета академии присвоен статус советника ректора по вопросам женщин "
            "на основании приказа № 326 министра высшего и среднего специального образования "
            "Республики Узбекистан от 17 июня 2020 года.\n\n"
            "В коллективе Государственной академии спорта Узбекистана работают около 1023 женщин. "
            "Из них 501 — преподаватели, 522 — сотрудники. Число студенток составляет 11 714, "
            "из которых 2150 — замужние.\n\n"
            "Женский совет академии действует на основании своего устава в соответствии с Конституцией "
            "Республики Узбекистан и соответствующими законами о некоммерческих и общественных "
            "организациях."
        ),
        'description_en': (
            "The chairperson of the Academy's Women's Council was granted the status of Rector's "
            "Adviser on Women's Issues under Order No. 326 of the Minister of Higher and Secondary "
            "Specialised Education of the Republic of Uzbekistan dated 17 June 2020.\n\n"
            "Approximately 1,023 women work at the Uzbekistan State Sports Academy: 501 teaching "
            "staff and 522 administrative staff. The number of female students is 11,714, "
            "of whom 2,150 are married.\n\n"
            "The Women's Council operates under its own charter in accordance with the Constitution "
            "of the Republic of Uzbekistan and relevant laws on non-commercial and public organisations."
        ),
        'about_uz': (
            "Xotin-qizlarni qo'llab-quvvatlash, gender tenglikni ta'minlash va oila institutini "
            "mustahkamlash maqsadida kengash quyidagilarni asosiy yo'nalishlar etib belgilaydi:\n\n"
            "1. Xotin-qizlarni qo'llab-quvvatlashga doir davlat siyosatining samarali amalga "
            "oshirilishini ta'minlash, ularning huquqlari, erkinliklari va qonuniy manfaatlarini "
            "himoya qilish, universitetning ijtimoiy-siyosiy, ilmiy va ma'naviy hayotidagi faolligi "
            "hamda liderlik salohiyatini oshirish.\n\n"
            "2. Universitetdagi xotin-qizlarning muammolarini o'z vaqtida aniqlash, ijtimoiy himoyaga "
            "muhtoj, og'ir turmush sharoitiga tushib qolgan, nogironligi bo'lgan hamda yordamga "
            "ehtiyoji mavjud xotin-qizlarning manzilli ro'yxatini shakllantirish, ularga "
            "ijtimoiy-huquqiy, psixologik, ma'naviy va moddiy ko'mak ko'rsatish.\n\n"
            "3. Universitetdagi xotin-qizlar uchun munosib mehnat va ta'lim sharoitlarini yaratish, "
            "ularning bandligini ta'minlash, tadbirkorlik tashabbuslarini qo'llab-quvvatlash, "
            "kasb-hunar va zamonaviy ko'nikmalarni egallashiga ko'maklashish.\n\n"
            "4. Talaba-qizlarning, ayniqsa talabalar turar joyida va ijarada yashayotgan qizlarning "
            "bo'sh vaqtlarini mazmunli tashkil etish, sport, madaniyat, san'at, ilm-fan va innovatsion "
            "loyihalarga keng jalb etish orqali ularning ijtimoiy faolligini oshirish.\n\n"
            "5. Universitetdagi xotin-qizlar o'rtasida huquqbuzarliklar, zo'ravonlik, tazyiq va salbiy "
            "holatlarning oldini olish, muammoli guruhlar bilan yakka tartibda ishlash hamda sog'lom "
            "ma'naviy-axloqiy muhitni mustahkamlash.\n\n"
            "6. Oilaviy qadriyatlarni mustahkamlash, sog'lom oila muhitini shakllantirish, yoshlarni "
            "oilaviy hayotga tayyorlash, farzand tarbiyasi va ma'naviy barkamollik masalalarida "
            "targ'ibot ishlarini kuchaytirish.\n\n"
            "7. Gender tenglik tamoyillarini keng joriy etish, xotin-qizlarning boshqaruv, ta'lim, "
            "sport va ilmiy faoliyatdagi ulushini oshirish, ularning tashabbus va iqtidorlarini "
            "ro'yobga chiqarishga ko'maklashish."
        ),
        'about_ru': "",
        'about_en': "",
        'decree_info': "O'zMTSTV №326 buyruq, 2020-yil 17-iyun",
        'phone':   "95 080 7001",
        'email':   "xudayberdiyeva89@mail.ru",
        'sport_types_uz': "",
        'sport_types_ru': "",
        'sport_types_en': "",
        'bachelor_subjects_uz': "",
        'bachelor_subjects_ru': "",
        'bachelor_subjects_en': "",
        'master_subjects_uz': "",
        'master_subjects_ru': "",
        'master_subjects_en': "",
    },
]


class Command(BaseCommand):
    help = "Fakultet va kafedra ma'lumotlarini to'ldiradi (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib, qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            slugs = [d['slug'] for d in DATA]
            n = FakultetKafedra.objects.filter(slug__in=slugs).delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        created = updated = 0
        for data in DATA:
            slug = data.pop('slug')
            obj, is_new = FakultetKafedra.objects.update_or_create(
                slug=slug,
                defaults=data,
            )
            data['slug'] = slug
            if is_new:
                created += 1
            else:
                updated += 1
            label = '[+]' if is_new else '[~]'
            self.stdout.write(f"  {label} {obj.name_uz}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created} yangi, {updated} yangilandi. Jami {len(DATA)} ta."
        ))
