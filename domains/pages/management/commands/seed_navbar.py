"""
python manage.py seed_navbar           # create/update all navbar items
python manage.py seed_navbar --clear   # delete existing first, then seed
"""
import re
from django.core.management.base import BaseCommand
from domains.pages.models import NavbarCategory, NavbarSubItem

_UUID = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
    re.IGNORECASE,
)

CATEGORIES = [
    # (key, order, uz_label, ru_label, en_label)
    ("akademiya",        1,  "Akademiya",           "Академия",                "Academy"),
    ("faoliyat",         2,  "Faoliyat",            "Деятельность",            "Activity"),
    ("xalqaro-aloqalar", 3,  "Xalqaro aloqalar",    "Международные связи",     "International Relations"),
    ("talabalarga",      4,  "Talabalarga",         "Студентам",               "Students"),
    ("axborot-xizmati",  5,  "Axborot xizmati",     "Информационная служба",   "Information Service"),
    ("qabul",            6,  "Qabul",               "Приём",                   "Admissions"),
    ("rektorga-murojaat",7,  "Rektorga murojaat",   "Обращение к ректору",     "Rector Appeal"),
    ("faxrlarimiz",      8,  "Faxrlarimiz",         "Наша гордость",           "Our Pride"),
    ("aloqa",            9,  "Aloqa",               "Контакты",                "Contact"),
    ("virtual-sayohat",  10, "Virtual sayohat",     "Виртуальный тур",         "Virtual Tour"),
    ("reyting",          11, "Reyting",             "Рейтинг",                 "Rating"),
]

# (cat_key, id_slug, order, uz_name, ru_name, en_name, url)
ITEMS = [
    # ── AKADEMIYA ────────────────────────────────────────────────────────────────
    ("akademiya", "about-academy",        1,  "Akademiya haqida",                             "Об академии",                                      "About Academy",                 "/page/about-academy"),
    ("akademiya", "academy-in-numbers",   2,  "Akademiya raqamlarda",                         "Академия в цифрах",                                "Academy in Numbers",            "/page/academy-in-numbers"),
    ("akademiya", "rectorate",            3,  "Rektorat",                                     "Ректорат",                                         "Rectorate",                     "/api/categories/rektorat/"),
    ("akademiya", "academy-structure",    4,  "Tuzilma",                                      "Структура",                                        "Structure",                     "/page/academy-structure"),
    ("akademiya", "academy-details",      5,  "Rekvizitlar",                                  "Реквизиты",                                        "Details",                       "/page/academy-details"),
    ("akademiya", "academy-regulations",  6,  "Me'yoriy hujjatlar",                           "Нормативные документы",                            "Regulations",                   "/page/academy-regulations"),
    ("akademiya", "academy-buildings",    7,  "O'quv binolari va Sport inshootlari",           "Учебные корпуса",                                  "Academy Buildings",             "/page/academy-buildings"),
    ("akademiya", "academy-organizations",8,  "Akademiya huzuridagi tashkilotlar",            "Организации при академии",                         "Organizations",                 "/page/academy-organizations"),
    ("akademiya", "academy-council",      9,  "Akademiya kengashi",                           "Совет академии",                                   "Academy Council",               "/page/academy-council"),
    ("akademiya", "faculties",            10, "Fakultet",                                     "Факультеты",                                       "Faculties",                     "/page/faculties"),
    ("akademiya", "public-organizations", 11, "Jamoat tashkilotlari",                         "Общественные организации",                         "Public Organizations",          "/page/public-organizations"),
    ("akademiya", "centers",              12, "Markazlar",                                    "Центры",                                           "Centers",                       "/page/centers"),
    ("akademiya", "360-panorama",         13, "360° ko'rinish",                               "Просмотр 360°",                                    "360° View",                     "/360"),

    # ── FAOLIYAT ─────────────────────────────────────────────────────────────────
    ("faoliyat", "faoliyat-sport",    1, "Sport faoliyat",                "Спортивная деятельность",              "Sports Activity",              "/api/activities/faoliyat/?category=sport-faoliyat"),
    ("faoliyat", "faoliyat-ilmiy",    2, "Ilmiy faoliyat",               "Научная деятельность",                 "Scientific Activity",          "/api/activities/faoliyat/?category=ilmiy-faoliyat"),
    ("faoliyat", "faoliyat-oquv",     3, "O'quv faoliyat",               "Учебная деятельность",                 "Educational Activity",         "/api/activities/faoliyat/?category=oquv-faoliyat"),
    ("faoliyat", "faoliyat-manaviy",  4, "Ma'naviy-marifiy faoliyat",    "Духовно-просветительская деятельность","Spiritual & Educational",       "/api/activities/faoliyat/?category=manaviy-faoliyat"),
    ("faoliyat", "faoliyat-moliyaviy",5, "Moliyaviy faoliyat",           "Финансовая деятельность",              "Financial Activity",            "/api/activities/faoliyat/?category=moliyaviy-faoliyat"),

    # ── XALQARO ALOQALAR ─────────────────────────────────────────────────────────
    ("xalqaro-aloqalar", "international-partners",      1, "Xalqaro hamkor tashkilotlar",           "Международные партнёрские организации",       "International Partners",        "/page/international-partners"),
    ("xalqaro-aloqalar", "abroad-training",             2, "Xorijda malaka oshirish va ta'lim",     "Повышение квалификации и обучение за рубежом","Abroad Training",               "/page/abroad-training"),
    ("xalqaro-aloqalar", "international-announcements", 3, "Xalqaro bo'lim e'lonlari",              "Объявления международного отдела",            "International Announcements",   "/page/international-announcements"),
    ("xalqaro-aloqalar", "academic-mobility",           4, "Akademik almashinuv",                   "Академическая мобильность",                   "Academic Mobility",             "/page/academic-mobility"),
    ("xalqaro-aloqalar", "about-us-foreigners",         5, "Xorijliklar «Biz haqimizda»",           "Иностранцы «О нас»",                          "About Us (Foreigners)",         "/page/about-us-foreigners"),
    ("xalqaro-aloqalar", "foreign-professors",          6, "Xorijlik professor-o'qituvchilar",      "Иностранные профессора-преподаватели",         "Foreign Professors",            "/page/foreign-professors"),
    ("xalqaro-aloqalar", "rating-sportsmen",            7, "Sportchilarni reytingi",                "Рейтинг спортсменов",                         "Sportsmen Rating",              "/page/rating-sportsmen"),
    ("xalqaro-aloqalar", "rating-faculty",              8, "Professor-o'qituvchilarni reytingi",    "Рейтинг профессорско-преподавательского состава","Faculty Rating",              "/page/rating-faculty"),

    # ── TALABALARGA ──────────────────────────────────────────────────────────────
    ("talabalarga", "student-privileges",          1,  "Talabalarga imtiyozlar",          "Льготы для студентов",                    "Student Privileges",            "/page/student-privileges"),
    ("talabalarga", "st-news",                     2,  "So'nggi yangiliklar",             "Последние новости",                       "Latest News",                   "/api/news/"),
    ("talabalarga", "st-guide-student",            3,  "Yo'riqnoma (abituriyent)",        "Руководство (абитуриент)",                "Guide (Applicant)",             "/page/st-guide-student"),
    ("talabalarga", "st-guide",                    4,  "Yo'riqnoma (bakalavr)",           "Руководство (бакалавр)",                  "Bachelor Guide",                "/page/st-guide"),
    ("talabalarga", "grading-system",              5,  "Bakalavr baholash tizimi",        "Система оценивания бакалавриата",         "Grading System",                "/page/grading-system"),
    ("talabalarga", "gpa-credit",                  6,  "GPA va kredit talablari",         "Требования GPA и кредитов",               "GPA & Credit",                  "/page/gpa-credit"),
    ("talabalarga", "st-schedule",                 7,  "Dars jadvali",                    "Расписание занятий",                      "Class Schedule",                "/page/st-schedule"),
    ("talabalarga", "scholarships",                8,  "Stipendiyalar",                   "Стипендии",                               "Scholarships",                  "/page/scholarships"),
    ("talabalarga", "gifted-students",             9,  "Iqtidorli talabalar",             "Одарённые студенты",                      "Gifted Students",               "/page/gifted-students"),
    ("talabalarga", "final-control",               10, "Yakuniy nazorat",                 "Итоговый контроль",                       "Final Control",                 "/page/final-control"),
    ("talabalarga", "scholarships-magistratura",   11, "Magistratura: stipendiyalar",     "Магистратура: стипендии",                 "Masters Scholarships",          "/page/scholarships-magistratura"),
    ("talabalarga", "master-defense",              12, "Magistrlik dissertatsiyasi himoyasi","Защита магистерской диссертации",       "Masters Defense",               "/page/master-defense"),
    ("talabalarga", "master-topics",               13, "Magistrlik dissertatsiya mavzulari","Темы магистерских диссертаций",          "Masters Topics",                "/page/master-topics"),
    ("talabalarga", "masters-grading",             14, "Magistratura baholash tizimi",    "Система оценивания магистратуры",         "Masters Grading",               "/page/masters-grading"),
    ("talabalarga", "yada-schedule-magistratura",  15, "Magistratura: yakuniy o'tkazish jadvali","Магистратура: график итоговой аттестации","Masters YADA Schedule",    "/page/yada-schedule-magistratura"),
    ("talabalarga", "course-manual-magistratura",  16, "Magistratura: fanlar o'quv qo'llanmasi","Магистратура: учебное пособие по предметам","Masters Course Manual",    "/page/course-manual-magistratura"),

    # ── AXBOROT XIZMATI ──────────────────────────────────────────────────────────
    ("axborot-xizmati", "ax-news",          1, "Yangiliklar",                       "Новости",                             "News",                 "/api/news/"),
    ("axborot-xizmati", "rector-speeches",  2, "Rektor tabriklari va nutqlari",     "Поздравления и выступления ректора",  "Rector Speeches",      "/page/rector-speeches"),
    ("axborot-xizmati", "briefings",        3, "Brifinglar",                        "Брифинги",                            "Briefings",            "/page/briefings"),
    ("axborot-xizmati", "contests",         4, "Tanlovlar",                         "Конкурсы",                            "Contests",             "/page/contests"),
    ("axborot-xizmati", "press-service",    5, "Matbuot xizmati",                   "Пресс-служба",                        "Press Service",        "/page/press-service"),
    ("axborot-xizmati", "photo-gallery",    6, "Fotogalereya",                      "Фотогалерея",                         "Photo Gallery",        "/page/photo-gallery"),
    ("axborot-xizmati", "video-gallery",    7, "Video galereya",                    "Видеогалерея",                        "Video Gallery",        "/page/video-gallery"),

    # ── QABUL ────────────────────────────────────────────────────────────────────
    ("qabul", "admission-news",          1,  "Qabul yangiliklari",             "Новости приёма",                         "Admission News",                "/page/admission-news"),
    ("qabul", "admission-commission",    2,  "Qabul komissiya tarkibi",        "Состав приёмной комиссии",               "Commission Members",            "/page/admission-commission"),
    ("qabul", "admission-regulations",   3,  "Me'yoriy hujjatlar (Qabul)",     "Нормативные документы (приём)",          "Admission Regulations",         "/page/admission-regulations"),
    ("qabul", "admission-days",          4,  "Qabul kunlari",                  "Дни приёма",                             "Admission Days",                "/page/admission-days"),
    ("qabul", "call-center",             5,  "Call-center",                    "Колл-центр",                             "Call Center",                   "/page/call-center"),
    ("qabul", "applicant-guide",         6,  "Abituriyentlar uchun qo'llanma", "Руководство для абитуриентов",           "Applicant Guide",               "/page/applicant-guide"),
    ("qabul", "recommended-applicants",  7,  "Tavsiyanomaga ega abituriyentlar","Абитуриенты с рекомендацией",            "Recommended Applicants",        "/page/recommended-applicants"),
    ("qabul", "personal-documents",      8,  "Shaxsiy yig'ma jild hujjatlari", "Документы личного дела",                "Personal Documents",            "/page/personal-documents"),
    ("qabul", "admission-privileges",    9,  "Imtiyozlar",                     "Льготы",                                 "Privileges",                    "/page/admission-privileges"),
    ("qabul", "passing-scores",          10, "O'tish ballari",                 "Проходные баллы",                        "Passing Scores",                "/page/passing-scores"),
    ("qabul", "test-subjects",           11, "Test-sinovlari fanlari",         "Предметы тестовых испытаний",            "Test Subjects",                 "/page/test-subjects"),
    ("qabul", "transfer",                12, "O'qishni ko'chirish",            "Перевод обучения",                       "Transfer",                      "/page/transfer"),
    ("qabul", "visually-impaired",       13, "Ko'zi ojiz abituriyentlar uchun","Для слабовидящих абитуриентов",          "Visually Impaired",             "/page/visually-impaired"),
    ("qabul", "college-graduates",       14, "Texnikum bitiruvchilari",        "Выпускники техникумов",                  "College Graduates",             "/page/college-graduates"),
    ("qabul", "second-degree",           15, "Ikkinchi oliy ta'lim",           "Второе высшее образование",              "Second Degree",                 "/page/second-degree"),
    ("qabul", "admission-contracts",     16, "Shartnomalar",                   "Договоры",                               "Contracts",                     "/page/admission-contracts"),
    ("qabul", "increased-contract",      17, "Oshirilgan to'lov-shartnomasi",  "Повышенный платный договор",             "Increased Contract",            "/page/increased-contract"),
    ("qabul", "admission-contract-prices",18,"Kontrakt narxlari (Qabul)",      "Стоимость контракта (приём)",            "Contract Prices",               "/page/admission-contract-prices"),
    ("qabul", "bachelor-results",        19, "Bakalavr natijalari",            "Результаты бакалавриата",                "Bachelor Results",              "/page/bachelor-results"),
    ("qabul", "exam-schedule",           20, "Kasbiy imtihonlar jadvali",      "График профессиональных экзаменов",      "Exam Schedule",                 "/page/exam-schedule"),
    ("qabul", "masters-admission-plan",  21, "Magistratura qabul rejasi",      "План приёма в магистратуру",             "Masters Admission Plan",        "/page/masters-admission-plan"),
    ("qabul", "masters-documents",       22, "Magistratura hujjat topshirish", "Подача документов в магистратуру",       "Masters Documents",             "/page/masters-documents"),
    ("qabul", "masters-results",         23, "Magistratura natijalari",        "Результаты магистратуры",                "Masters Results",               "/page/masters-results"),
    ("qabul", "foreign-students-apply",  24, "Xorijiy talabalar uchun ariza",  "Заявка для иностранных студентов",       "Foreign Students Application",  "/page/foreign-students-apply"),
    ("qabul", "foreign-bachelor",        25, "Xorijiy talabalar — Bakalavr",   "Иностранные студенты — Бакалавриат",     "Foreign — Bachelor",            "/page/foreign-bachelor"),
    ("qabul", "foreign-masters",         26, "Xorijiy talabalar — Magistratura","Иностранные студенты — Магистратура",  "Foreign — Masters",             "/page/foreign-masters"),
    ("qabul", "dormitory",               27, "Talabalar turar joyi",           "Студенческое общежитие",                 "Dormitory",                     "/page/dormitory"),
    ("qabul", "joint-programs",          28, "Qo'shma ta'lim dasturlari",      "Совместные образовательные программы",  "Joint Programs",                "/page/joint-programs"),

    # ── REKTORGA MUROJAAT ────────────────────────────────────────────────────────
    ("rektorga-murojaat", "rector-appeal", 1, "Rektorga murojaat", "Обращение к ректору", "Rector Appeal", "/page/rector-appeal"),

    # ── FAXRLARIMIZ ──────────────────────────────────────────────────────────────
    ("faxrlarimiz", "graduates",              1, "Bitiruvchilarimiz",         "Наши выпускники",              "Graduates",              "/page/graduates"),
    ("faxrlarimiz", "honorary-teachers",      2, "Faxrli ustozlarimiz",       "Наши почётные наставники",     "Honorary Teachers",      "/page/honorary-teachers"),
    ("faxrlarimiz", "distinguished-scientists",3,"Ilg'or olimlarimiz",        "Наши выдающиеся учёные",       "Distinguished Scientists","/page/distinguished-scientists"),
    ("faxrlarimiz", "ozdsa-stars",            4, "O'ZDSA yulduzlari",         "Звёзды O'ZDSA",                "OZDSA Stars",            "/page/ozdsa-stars"),

    # ── ALOQA ────────────────────────────────────────────────────────────────────
    ("aloqa", "contact", 1, "Aloqa", "Контакты", "Contact", "/page/contact"),

    # ── VIRTUAL SAYOHAT ──────────────────────────────────────────────────────────
    ("virtual-sayohat", "virtual-tour", 1, "Virtual sayohat", "Виртуальный тур", "Virtual Tour", "/page/virtual-tour"),

    # ── REYTING ──────────────────────────────────────────────────────────────────
    ("reyting", "national-rating",      1, "Milliy reyting",    "Национальный рейтинг",                                  "National Rating",      "/page/national-rating"),
    ("reyting", "international-rating", 2, "Xalqaro reyting",   "Международный рейтинг (место академии среди вузов)",    "International Rating", "/page/international-rating"),
]

# Categories that have no sub-items — use direct_url from the single child above
_DIRECT_URL_CATS = {"rektorga-murojaat", "aloqa", "virtual-sayohat"}

# Static sahifalar uchun content_uz (slug → matn)
PAGE_CONTENT_UZ = {
    "st-guide": """Talabalarning o'qishini ko'chirish, qayta tiklash va o'qishdan chetlashtirish O'zbekiston Respublikasi Vazirlar Mahkamasining 2025-yil 13-sentabrdagi 578-son qarori bilan tasdiqlangan "Oliy ta'lim muassasalariga o'qishga qabul qilish, talabalar o'qishini ko'chirish, qayta tiklash va o'qishdan chetlashtirish tartibi to'g'risida Nizom"ga muvofiq amalga oshiriladi.

UMUMIY QOIDALAR

— Mos ta'lim yo'nalishlari — nomlanishi bir xil bo'lgan bakalavriat ta'lim yo'nalishlari.
— Turdosh ta'lim yo'nalishlari — o'quv rejalari mazmunan yaqin bo'lgan yo'nalishlar.
— O'qishni ko'chirish — talabaning bir OTMdan boshqasiga yoki bir yo'nalishdan boshqasiga ko'chirilishi.
— O'qishni ko'chirib tiklash — sobiq talabaning boshqa OTM yoki yo'nalishda o'qishini davom ettirishi.
— O'qishni qayta tiklash — sobiq talabaning xuddi shu yo'nalishda o'qishini davom ettirishi.

KO'CHIRISH MUDDATLARI

Kuzgi semestr: ariza — 15-iyul–5-avgust; ko'rib chiqish — 6–30-avgust.
Bahorgi semestr: ariza — 10–20-yanvar; ko'rib chiqish — 21-yanvar–10-fevral.

ZARUR HUJJATLAR

1. Ariza (muassasa, yo'nalish, sabablar).
2. Reyting daftarchasi yoki akademik ma'lumotnoma.
3. Pasport nusxasi.
4. Sababni asoslovchi hujjatlar nusxasi.

RUXSAT BERILMAYDIGAN HOLATLAR

— Akkreditatsiyasiz xorijiy OTMlardan ko'chirish.
— 1-kurs 1-semestriga ko'chirish (kasallik holatlari bundan mustasno).
— OTMda mos yo'nalish mavjud bo'lmasa.
— To'lov-kontrakt to'lovi bajarilmagan bo'lsa.
— Akademik ma'lumotnoma muddatida taqdim etilmasa.

AKADEMIK FARQLAR TALABI

— Reyting tizimida: farqlar 4 tadan oshmasligi lozim.
— Kreditlar tizimida: GPA ≥ 2,4 bo'lishi lozim.

O'QISHDAN CHETLASHTIRISH ASOSLARI

a) O'z xohishiga ko'ra.
b) O'qishni boshqa OTMga ko'chirish.
v) Ichki tartib-qoidalarni buzganlik.
g) Darslarni uzrsiz 74 soatdan ortiq qoldirish.
d) To'lov-kontrakt to'lovini o'z vaqtida to'lamaslik.
e) Sud tomonidan ozodlikdan mahrum etilish.
j) Kirish imtihonlarida tartibni buzish (qayta tiklanmaydi).
k) Vafot etish.""",

    "grading-system": """O'zbekiston davlat sport akademiyasida baholash balli tizimda olib boriladi.

90–100 ball — 5 (A'lo): a'lo natija
75–89 ball  — 4 (Yaxshi): yaxshi natija
60–74 ball  — 3 (Qoniqarli): qoniqarli natija
50–59 ball  — 2 (Qoniqarsiz): qayta topshirish kerak
0–49 ball   — 1 (Muvaffaqiyatsiz): juda past natija""",

    "gpa-credit": """GPA (Grade Point Average) — talabaning o'rtacha akademik ko'rsatkichi bo'lib, barcha fanlar bo'yicha olingan baholarni kreditlar bilan hisoblab chiqish orqali aniqlanadi.

O'zbekiston davlat sport akademiyasida minimal GPA 2,4 etib belgilangan.

Talaba ushbu ballni saqlashi yoki oshirishi kerak. Aks holda:
— O'qishni ko'chirish yoki tiklashda GPA ≥ 2,4 bo'lishi shart.
— GPA past bo'lsa, quyi kursdan o'qishni davom ettirish taklif qilinishi mumkin.
— Akademik ehtiyot choralar ko'rilishi mumkin.""",

    "scholarships": """O'zbekiston davlat sport akademiyasining bakalavriat ta'lim yo'nalishida hozirgi kunda jami 146 nafar talaba tahsil olmoqda.

Mazkur talabalar O'zbekiston Respublikasi amaldagi normativ-huquqiy hujjatlariga muvofiq ravishda to'liq davlat granti asosida o'qishga qabul qilingan bo'lib, ularning barchasi belgilangan tartibda davlat stipendiyasi bilan ta'minlanadi.""",

    "st-schedule": """O'zbekiston davlat sport akademiyasi bakalavriat ta'lim yo'nalishlarida dars mashg'ulotlari asosan ertalabki smenada tashkil etiladi.

Dars mashg'ulotlari quyidagi vaqt oralig'ida o'tkaziladi:

Juftlik     | Boshlanish | Tugash
------------+------------+-------
I-juftlik   | 09:00      | 10:20
II-juftlik  | 10:30      | 11:50
III-juftlik | 12:00      | 13:20
IV-juftlik  | 13:30      | 14:50
V-juftlik   | 15:00      | 16:20
VI-juftlik  | 16:30      | 17:50""",

    "final-control": """O'zbekiston davlat sport akademiyasi bakalavriat ta'lim yo'nalishlarida yakuniy nazorat turlari o'quv fanlarining xususiyatidan kelib chiqib tashkil etiladi.

Asosan, yakuniy nazoratlar fan sillabuslarida belgilangan shaklda o'tkaziladi:
— Og'zaki nazorat
— Yozma ish
— Amaliy sinov
— Test sinovi

Talabalarning fan bo'yicha o'zlashtirish darajasi, nazariy bilimlari hamda amaliy ko'nikmalari kompleks tarzda baholanadi.

Yakuniy nazorat jarayonlari belgilangan tartib va me'yoriy hujjatlar asosida shaffoflik va xolislik tamoyillariga amal qilgan holda tashkil etiladi.""",

    # ── XALQARO ALOQALAR ─────────────────────────────────────────────────────
    "international-partners": """O'zbekiston davlat sport akademiyasi xalqaro hamkorlik yo'nalishida bir qator nufuzli tashkilotlar bilan aloqalarni yo'lga qo'ygan.

ASOSIY HAMKOR TASHKILOTLAR

• Xalqaro Olimpiya Qo'mitasi (IOC)
• Jahon Anti-doping Agentligi (WADA)
• O'zbekiston Olimpiya va Sport Milliy Qo'mitasi
• Osiyo Olimpiya Kengashi (OCA)
• Xalqaro Sport Federatsiyalari (sport turlari bo'yicha)
• MDH mamlakatlari sport oliygohlar birlashmasi

HAMKORLIK YO'NALISHLARI

— Talabalar va o'qituvchilar akademik almashinuvi
— Qo'shma ilmiy tadqiqot loyihalari
— Xalqaro sport musobaqalariga birgalikda ishtirok etish
— Metodik va uslubiy materiallar almashish
— Malaka oshirish dasturlari va treninglar

SHARTNOMALAR

Akademiya 10 dan ortiq xorijiy oliy o'quv yurtlari va sport tashkilotlari bilan hamkorlik memorandumlari imzolagan. Batafsil ma'lumot uchun xalqaro aloqalar bo'limiga murojaat qilishingiz mumkin.""",

    "abroad-training": """XORIJDA MALAKA OSHIRISH VA TA'LIM

O'zbekiston davlat sport akademiyasi professor-o'qituvchilar va talabalariga xorijda malaka oshirish imkoniyatlarini taqdim etadi.

PROFESSOR-O'QITUVCHILAR UCHUN

— Xorijiy yetakchi sport universitetlarida qisqa muddatli kurslar (1–4 hafta)
— Xalqaro konferensiya va simpoziyumlarda qatnashish
— Ilmiy tadqiqot maqsadida xorijiy universitetlarda staj o'tash (1–6 oy)
— Xorijiy mutaxassislar tomonidan o'tkaziladigan treninglar

TALABALAR UCHUN

— Akademik almashinuv dasturlari orqali bir semestr yoki bir yil xorijda o'qish
— Xalqaro sport musobaqalariga akademiya vakili sifatida qatnashish
— Yozgi maktablar va intensiv kurslar

MUROJAAT TARTIBI

1. Xalqaro aloqalar bo'limiga ariza topshirish
2. Til bilimi sertifikati taqdim etish (ingliz yoki boshqa talab qilingan til)
3. Akademik ko'rsatkichlarni tasdiqlash (GPA ≥ 3,0 tavsiya etiladi)
4. Tanlov bo'yicha ishtirok etish

Batafsil ma'lumot va dolzarb takliflar uchun xalqaro aloqalar bo'limiga murojaat qiling yoki email orqali so'rov yuboring.""",

    "international-announcements": """XALQARO BO'LIM E'LONLARI

Bu sahifada O'zbekiston davlat sport akademiyasining xalqaro aloqalar bo'limi tomonidan chiqarilgan rasmiy e'lonlar joylashtiriladi.

E'LONLAR TURLARI

— Xorijda malaka oshirish va o'qish imkoniyatlari
— Xalqaro grant dasturlari va stipendiyalar
— Qo'shma tadqiqot loyihalari uchun tanlovlar
— Xorijiy universitetlar va sport tashkilotlari bilan hamkorlik takliflari
— Xalqaro konferensiya va simpoziyumlar

GRANT DASTURLARI

Akademiya talabalari va xodimlari quyidagi xalqaro grant dasturlarida qatnashish imkoniyatiga ega:
— O'zbekiston Respublikasi Prezidenti stipendiyalari (xorijda o'qish uchun)
— El-Yurt Umidi jamg'armasi grantlari
— Erasmus+ dasturi
— Hamkor universitetlarning ichki grantlari

MUROJAAT

Xalqaro aloqalar bo'limi
Ish vaqti: dushanba–juma, 09:00–18:00
Akademiya bosh binosining 2-qavatida joylashgan.""",

    "academic-mobility": """AKADEMIK ALMASHINUV DASTURI

Akademik almashinuv (Academic Mobility) — talabalar va o'qituvchilarning bir semestr yoki o'quv yili davomida xorijiy universitetda tahsil olish yoki dars berish imkoniyatidir.

KIMLAR QATNASHA OLADI?

Talabalar uchun talablar:
— Kamida 2-kurs talabasi bo'lish
— GPA ko'rsatkichi 3,0 va undan yuqori bo'lish
— Xorijiy til bilimi (ingliz yoki boshqa talab qilingan til)
— Akademik qarzdorligi bo'lmasligi

O'qituvchilar uchun:
— Akademiyada kamida 1 yil ishlagan bo'lish
— Ilmiy unvon yoki akademik daraja (tavsiya etiladi)

ALMASHINUV TARTIBI

1. Xalqaro aloqalar bo'limiga ariza topshirish (o'quv yili boshlanishidan 3 oy oldin)
2. Kerakli hujjatlarni tayyorlash
3. Qabul qiluvchi universitetning tasdig'ini olish
4. Akademiya rektori buyrug'iga asosan jo'natish

O'QISH NATIJALARI

Xorijda o'qitilgan fanlar akademiyaning o'quv rejasi doirasida hisobga olinadi. Kreditlarni o'tkazish tartibi xalqaro aloqalar bo'limi va o'quv ishlari bo'limi bilan kelishiladi.""",

    "about-us-foreigners": """XORIJLIKLAR «BIZ HAQIMIZDA»

O'zbekiston davlat sport akademiyasi xalqaro hamkorlar va xorijiy mutaxassislar tomonidan yuqori baholanmoqda.

XORIJIY HAMKORLARNING FIKRI

Akademiya O'zbekistonda sport ta'limini rivojlantirishda muhim rol o'ynaydi. Sport fanlari bo'yicha ixtisoslashgan yagona davlat akademiyasi sifatida u mintaqada noyob o'rin tutadi.

Akademiya bizning hamkorimiz sifatida professional munosabatlar, ilmiy hamkorlik va talabalar almashinuvi borasida ishonchli va ochiq tashkilot ekanligini isbotladi.

XALQARO HAMKORLIK NATIJALARI

— Xorijiy universitetlar bilan 10+ hamkorlik memorandumi
— Har yili xorijda malaka oshirayotgan 5–10 nafar o'qituvchi
— Xalqaro musobaqalarda medallar qozongan talabalar
— Xorijiy ekspertlar bilan o'tkazilgan qo'shma seminarlar va treninglar

AKADEMIYA HAQIDA

O'zbekiston davlat sport akademiyasi 2022-yilda tashkil etilgan bo'lib, sport mutaxassislari va trenerlarini tayyorlashga ixtisoslashgan. Akademiya O'zbekiston sport tizimini rivojlantirishga munosib hissa qo'shmoqda.""",

    "foreign-professors": """XORIJLIK PROFESSOR-O'QITUVCHILAR

O'zbekiston davlat sport akademiyasi xorijiy mutaxassislarni dars berish, ilmiy hamkorlik va malaka oshirish dasturlariga jalb etadi.

XORIJLIK MUTAXASSISLAR ISHTIROKI

Akademiyada xorijiy professor-o'qituvchilar quyidagi shakllarda faoliyat yuritadi:

— Vaqtincha o'qitish (visiting professor): bir semestr yoki o'quv yili davomida maxsus kurslar o'qitish
— Qisqa muddatli treninglar va master-klasslar (1 hafta–1 oy)
— Onlayn darslar va vebinarlar
— Qo'shma ilmiy tadqiqotlarda hamkorlik

TAKLIF QILINAYOTGAN YO'NALISHLAR

— Sport pedagogikasi va metodikasi
— Sport fiziologiyasi va biomexanikasi
— Sport psixologiyasi
— Olimpiya tayyorgarligi va yuqori natijalar menejmenti
— Xalqaro sport huquqi va boshqaruvi

MUROJAAT

Xorijlik mutaxassislarni jalb etish yoki o'z nomzodingizni taklif qilish uchun xalqaro aloqalar bo'limiga murojaat qiling. Ariza va rezyume elektron pochta orqali yuborilishi mumkin.""",

    "rating-sportsmen": """SPORTCHILARNI REYTINGI

O'zbekiston davlat sport akademiyasi talabalarining xalqaro va milliy musobaqalardagi natijalari asosida reyting tuziladi.

REYTING MEZONLARI

Sportchi reytingi quyidagi ko'rsatkichlar asosida shakllanadi:
— Olimpiya o'yinlaridagi natijalar
— Jahon chempionatlari natijalari
— Osiyo o'yinlari va chempionatlaridagi natijalar
— O'zbekiston chempionati natijalari
— Xalqaro reytingdagi o'rin (sport turi bo'yicha)

SPORT TURLARI

Akademiyada quyidagi sport turlari bo'yicha talabalar tahsil oladi va musobaqalarda ishtirok etadi:
kurash, judo, boks, karate, taekwondo, gimnastika, yengil atletika, og'ir atletika, suzish, velosipord sport, stol tennisi, tennis va boshqalar.

YUTUQLAR

Akademiya talabalari va bitiruvchilari milliy va xalqaro musobaqalarda yuqori natijalar ko'rsatib kelmoqda. Batafsil natijalar va statistika uchun axborot xizmati bo'limiga murojaat qiling.""",

    "rating-faculty": """PROFESSOR-O'QITUVCHILARNI REYTINGI

O'zbekiston davlat sport akademiyasida professor-o'qituvchilar ilmiy va pedagogik faoliyati asosida baholanadi.

REYTING MEZONLARI

Professor-o'qituvchilar reytingi quyidagi ko'rsatkichlar bo'yicha tuziladi:

Ilmiy faoliyat:
— Xalqaro va mahalliy jurnallardagi maqolalar soni (Scopus, Web of Science)
— Monografiyalar va o'quv qo'llanmalar
— Ilmiy loyihalarda ishtirok

Pedagogik faoliyat:
— Talabalar tomonidan berilgan baholash
— O'quv-uslubiy ishlanmalar va sillabuslar
— Xalqaro konferensiyalarda ma'ruzalar

Ijtimoiy faoliyat:
— Amaliyot bazalari bilan hamkorlik
— Talabalar ilmiy ishlarini rahbarlik qilish
— Malaka oshirish kurslari

NATIJALAR

Reyting natijalari har o'quv yili yakunida e'lon qilinadi. Yuqori ko'rsatkichlarga erishgan professor-o'qituvchilar rag'batlantirish tizimi doirasida mukofotlanadi.""",
}


class Command(BaseCommand):
    help = "Navbar bo'limlari va sahifalarini database'ga qo'shadi (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='Mavjud navbar yozuvlarini o\'chirib, qaytadan yaratadi',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted_items = NavbarSubItem.objects.all().delete()[0]
            deleted_cats  = NavbarCategory.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(
                f"O'chirildi: {deleted_cats} kategoriya, {deleted_items} sahifa"
            ))

        # ── 1. Kategoriyalar ────────────────────────────────────────────────────
        cat_map = {}
        for key, order, uz, ru, en in CATEGORIES:
            cat, created = NavbarCategory.objects.update_or_create(
                slug=key,
                defaults={
                    'name_uz':   uz,
                    'name_ru':   ru,
                    'name_en':   en,
                    'order':     order,
                    'is_active': True,
                    'direct_url': '',
                },
            )
            cat_map[key] = cat
            verb = 'yaratildi' if created else 'yangilandi'
            self.stdout.write(f"  [kat] {verb}: {uz}")

        # ── 2. Sub-itemlar ──────────────────────────────────────────────────────
        created_count = updated_count = 0
        for cat_key, slug, order, uz, ru, en, url in ITEMS:
            cat = cat_map.get(cat_key)
            if cat is None:
                self.stdout.write(self.style.WARNING(f"  [skip] kategoriya topilmadi: {cat_key}"))
                continue

            page_type = NavbarSubItem.PageType.STATIC if url.startswith('/page/') else NavbarSubItem.PageType.REDIRECT
            redirect   = '' if page_type == NavbarSubItem.PageType.STATIC else url

            defaults = {
                'category':    cat,
                'name_uz':     uz,
                'name_ru':     ru,
                'name_en':     en,
                'page_type':   page_type,
                'redirect_url': redirect,
                'order':       order,
                'is_active':   True,
            }
            if slug in PAGE_CONTENT_UZ:
                defaults['content_uz'] = PAGE_CONTENT_UZ[slug]

            item, created = NavbarSubItem.objects.update_or_create(
                slug=slug,
                defaults=defaults,
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created_count} yangi sahifa qo'shildi, "
            f"{updated_count} ta yangilandi."
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Jami: {len(CATEGORIES)} kategoriya, {len(ITEMS)} sahifa."
        ))
