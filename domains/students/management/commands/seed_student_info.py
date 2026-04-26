"""
python manage.py seed_student_info          # yaratadi / yangilaydi
python manage.py seed_student_info --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.students.models import StudentInfoCategory, StudentInfo

CATEGORIES = [
    # (slug, order, uz, ru, en)
    # Bakalavr
    ("st-guide",              1,  "Yo'riqnoma (bakalavr)",       "Руководство (бакалавр)",              "Bachelor Guide"),
    ("grading-system",        2,  "Bakalavr baholash tizimi",    "Система оценивания бакалавриата",     "Grading System"),
    ("gpa-credit",            3,  "GPA va kredit talablari",     "Требования GPA и кредитов",           "GPA & Credit"),
    ("scholarships",          4,  "Stipendiyalar",               "Стипендии",                           "Scholarships"),
    ("final-control",         5,  "Yakuniy nazorat",             "Итоговый контроль",                   "Final Control"),
    ("bakalavriat-malumotnoma", 6, "Bakalavriat ma'lumotnomasi", "Справочник бакалавриата",             "Bachelor's Reference"),
]

ITEMS = [
    # ══ YO'RIQNOMA ════════════════════════════════════════════════════════════════
    (
        "st-guide", 1,
        "Yo'riqnoma",
        "Руководство",
        "Guide",
        # content_uz
        """Talabalarning o'qishini ko'chirish, qayta tiklash va o'qishdan chetlashtirish O'zbekiston Respublikasi Vazirlar Mahkamasining 2025-yil 13-sentabrdagi 578-son qarori bilan tasdiqlangan "Oliy ta'lim muassasalariga o'qishga qabul qilish, talabalar o'qishini ko'chirish, qayta tiklash va o'qishdan chetlashtirish tartibi to'g'risida Nizom"ga muvofiq amalga oshiriladi.

TALABALAR O'QISHINI KO'CHIRISH VA QAYTA TIKLASHNING UMUMIY QOIDALARI

Mos va turdosh yo'nalishlar (mutaxassisliklar) belgilash mezonlari:
— mos ta'lim yo'nalishlari (mutaxassisliklar) — oliy ta'lim tashkilotlari talabalari o'qishini ko'chirish va qayta tiklashda nomlanishi bir xil bo'lgan bakalavriat ta'lim yo'nalishlari (magistratura mutaxassisliklari);
— turdosh ta'lim yo'nalishlari — kadrlar tayyorlash yo'nalishlari, o'quv rejalari va dasturlari mazmunan yaqin bo'lgan bakalavriat ta'lim yo'nalishlari. Bunda ularning ro'yxati Vazirlik tomonidan tasdiqlanadi;
— o'qishni ko'chirish — talabaning arizasiga muvofiq uning o'qishini bir oliy ta'lim tashkilotidan boshqasiga yoki bir oliy ta'lim tashkiloti doirasida bir ta'lim yo'nalishidan boshqasiga belgilangan tartibda Davlat komissiyasi yoki Oliy ta'lim, fan va innovatsiyalar vazirligi (tegishli vazirlik (idora)) yoxud oliy ta'lim tashkiloti qaroriga asosan ko'chirilishi;
— o'qishni ko'chirib tiklash — sobiq talabaning arizasiga muvofiq uning o'qishining boshqa oliy ta'lim tashkilotida yoki bir oliy ta'lim tashkiloti doirasida boshqa bakalavriat ta'lim yo'nalishida davom ettirishi uchun belgilangan tartibda ko'chirib tiklanishi;
— o'qishni qayta tiklash — sobiq talabaning arizasiga muvofiq uning o'qishining muayyan bakalavriat ta'lim yo'nalishi yoki magistratura mutaxassisligida davom ettirishi uchun qayta tiklanishi.

KO'CHIRISH MUDDATLARI

Kuzgi semestr: ariza topshirish — 15-iyuldan 5-avgustgacha; ko'rib chiqish — 6-avgustdan 30-avgustgacha.
Bahorgi semestr: ariza topshirish — 10-yanvardan 20-yanvargacha; ko'rib chiqish — 21-yanvardan 10-fevralgacha.

ZARUR HUJJATLAR

1. Ariza (o'qigan muassasa, yo'nalish, sabablar ko'rsatilgan holda).
2. Reyting daftarchasi yoki akademik ma'lumotnoma (transkript).
3. Pasport nusxasi.
4. Sababni asoslovchi hujjatlar nusxasi (nikoh guvohnomasi, buyruq va h.k.).

RUXSAT BERILMAYDIGAN HOLATLAR

— Akkreditatsiyaga ega bo'lmagan xorijiy OTMlardan ko'chirish.
— Birinchi kursning birinchi semestriga ko'chirish (kasallik va yo'nalish mavjud emasligi holatlari bundan mustasno).
— OTMda mos (turdosh) ta'lim yo'nalishi mavjud bo'lmasa.
— To'lov-kontrakt to'lovi bajarilmagan bo'lsa.
— Akademik ma'lumotnoma belgilangan muddatda taqdim etilmagan bo'lsa.
— Maqsadli qabul qilinganlar boshqa yo'nalishga.
— Talaba qo'shma ta'lim dasturida tahsil olayotgan bo'lsa.

AKADEMIK FARQLAR TALABI

— Reyting tizimida: umumkasbiy va ixtisoslik fanlar bo'yicha farqlar 4 tadan oshmasligi lozim.
— Kreditlar tizimida: GPA ko'rsatkichi 2,4 va undan yuqori bo'lishi lozim.

QAYTA TIKLASH

Ariza topshirish: kuzgi semestr — 15-iyul–5-avgust; bahorgi semestr — 10-yanvar–20-yanvar.
Qaror qabul qilish: kuzgi semestr — 6-avgust–31-avgust; bahorgi semestr — 21-yanvar–10-fevral.
Barcha o'quv shakllari bo'yicha qayta tiklash to'lov-kontrakt asosida amalga oshiriladi. Davlat granti bo'yicha tiklanish faqat yetimlar, I–II guruh nogironligi bo'lgan shaxslar, muddatli harbiy xizmatni o'tagan va akademik ta'tildan belgilangan muddatda qaytgan shaxslar uchun istisno tariqasida mumkin.

O'QISHDAN CHETLASHTIRISH ASOSLARI

a) O'z xohishiga ko'ra.
b) O'qishni boshqa OTMga ko'chirish.
v) Ichki tartib-qoidalar va odob-axloq qoidalarini buzganlik.
g) Darslarni uzrsiz 74 soatdan ortiq qoldirganlik (tibbiy ma'lumotnoma mavjud bo'lmasa).
d) To'lov-kontrakt to'lovini o'z vaqtida amalga oshirmagan (to'lov-kontrakt bo'yicha talabalar uchun).
e) Sud tomonidan ozodlikdan mahrum etilganlik.
j) Kirish imtihonlarida tartibni buzganlik (bunday talabalar qayta tiklanmaydi).
z) Kursda qoldirilgan talaba belgilangan muddatlarda murojaat qilmaganda.
i) Taqdim etilgan hujjatlarning qalbakiligi yoki talablarga javob bermasligi aniqlansa.
k) Vafot etganlik.

Harbiy xizmat, salomatlikni tiklash, homiladorlik va tug'ish, bolalarni parvarish qilish ta'tillari davrida talabaga belgilangan tartibda akademik ta'til berilishi mumkin.""",
        # content_ru
        """Перевод, восстановление и отчисление студентов осуществляется в соответствии с «Положением о порядке приёма в высшие учебные заведения, перевода, восстановления и отчисления студентов», утверждённым постановлением Кабинета Министров Республики Узбекистан от 13 сентября 2025 года № 578.

ОБЩИЕ ПРАВИЛА ПЕРЕВОДА И ВОССТАНОВЛЕНИЯ СТУДЕНТОВ

Критерии определения соответствующих и родственных направлений:
— соответствующие направления (специальности) — направления бакалавриата с одинаковым наименованием;
— родственные направления — направления бакалавриата, учебные планы и программы которых близки по содержанию;
— перевод — перевод студента из одного вуза в другой или с одного направления на другое;
— перевод с восстановлением — продолжение обучения бывшего студента в другом вузе или на другом направлении;
— восстановление — продолжение обучения бывшего студента на том же направлении.

СРОКИ ПЕРЕВОДА

Осенний семестр: подача заявлений — с 15 июля по 5 августа; рассмотрение — с 6 по 30 августа.
Весенний семестр: подача заявлений — с 10 по 20 января; рассмотрение — с 21 января по 10 февраля.

НЕОБХОДИМЫЕ ДОКУМЕНТЫ

1. Заявление (учебное заведение, направление, причины).
2. Зачётная книжка или академическая справка (транскрипт).
3. Копия паспорта.
4. Документы, подтверждающие причину (свидетельство о браке, приказ и т.д.).

СЛУЧАИ ОТКАЗА

— Перевод из иностранных вузов без аккредитации.
— Перевод на первый семестр первого курса (кроме случаев болезни).
— Отсутствие соответствующего направления в вузе.
— Неоплата контракта в установленные сроки.
— Непредставление академической справки в срок.

ТРЕБОВАНИЯ К АКАДЕМИЧЕСКОЙ РАЗНИЦЕ

— Рейтинговая система: разница по общепрофессиональным и специальным дисциплинам не должна превышать 4.
— Кредитная система: показатель GPA должен быть не ниже 2,4.

ВОССТАНОВЛЕНИЕ

Подача заявлений: осенний семестр — 15 июля–5 августа; весенний — 10–20 января.
Рассмотрение: осенний — 6–31 августа; весенний — 21 января–10 февраля.""",
        # content_en
        """Transfer, reinstatement and expulsion of students is carried out in accordance with the "Regulations on admission, transfer, reinstatement and expulsion of students" approved by Resolution No. 578 of the Cabinet of Ministers of the Republic of Uzbekistan dated 13 September 2025.

GENERAL RULES FOR TRANSFER AND REINSTATEMENT

— Corresponding directions: bachelor's programmes with identical names.
— Related directions: bachelor's programmes with similar curricula and content.
— Transfer: moving a student from one institution or programme to another.
— Transfer with reinstatement: resuming studies of a former student at another institution or programme.
— Reinstatement: resuming studies of a former student in the same programme.

TRANSFER DEADLINES

Autumn semester: application — 15 July to 5 August; review — 6 to 30 August.
Spring semester: application — 10 to 20 January; review — 21 January to 10 February.

REQUIRED DOCUMENTS

1. Application (institution, programme, reasons).
2. Grade book or academic transcript.
3. Passport copy.
4. Supporting documents (marriage certificate, order, etc.).

ACADEMIC DIFFERENCE REQUIREMENTS

— Rating system: differences in professional and specialisation subjects must not exceed 4.
— Credit system: GPA must be 2.4 or higher.

REINSTATEMENT

Applications: autumn — 15 July–5 August; spring — 10–20 January.
Review: autumn — 6–31 August; spring — 21 January–10 February.""",
    ),
    (
        "grading-system", 1,
        "Baholash tizimi",
        "Система оценивания",
        "Grading System",
        # content_uz
        """O'zbekiston davlat sport akademiyasida baholash balli tizimda olib boriladi.

90–100 ball — 5 (A'lo): a'lo natija
75–89 ball  — 4 (Yaxshi): yaxshi natija
60–74 ball  — 3 (Qoniqarli): qoniqarli, yetarli natija
50–59 ball  — 2 (Qoniqarsiz): qayta topshirish kerak
0–49 ball   — 1 (Muvaffaqiyatsiz): juda past natija""",
        # content_ru
        """В Узбекистанской государственной спортивной академии применяется балльная система оценивания.

90–100 баллов — 5 (Отлично): отличный результат
75–89 баллов  — 4 (Хорошо): хороший результат
60–74 балла   — 3 (Удовлетворительно): удовлетворительный результат
50–59 баллов  — 2 (Неудовлетворительно): требуется пересдача
0–49 баллов   — 1 (Неудовлетворительно): очень низкий результат""",
        # content_en
        """Uzbekistan State Sports Academy uses a point-based grading system.

90–100 points — 5 (Excellent): excellent result
75–89 points  — 4 (Good): good result
60–74 points  — 3 (Satisfactory): satisfactory result
50–59 points  — 2 (Unsatisfactory): re-examination required
0–49 points   — 1 (Fail): very low result""",
    ),
    (
        "gpa-credit", 1,
        "GPA va kredit talablari",
        "Требования GPA и кредитов",
        "GPA & Credit Requirements",
        # content_uz
        """GPA (Grade Point Average) — talabaning o'rtacha akademik ko'rsatkichi bo'lib, barcha fanlar bo'yicha olingan baholarni kreditlar bilan hisoblab chiqish orqali aniqlanadi.

O'zbekiston davlat sport akademiyasida minimal GPA 2,4 etib belgilangan.

Talaba ushbu ballni saqlashi yoki oshirishi kerak. Aks holda:
— O'qishni ko'chirish yoki tiklash paytida GPA talabi bajarilishi shart (≥ 2,4).
— GPA past bo'lsa, talabaga quyi kursdan (semestrdan) o'qishini davom ettirish taklif qilinishi mumkin.
— Akademik ehtiyot choralar ko'rilishi mumkin.""",
        # content_ru
        """GPA (Grade Point Average) — средний академический показатель студента, определяемый путём расчёта оценок по всем дисциплинам с учётом кредитов.

В Узбекистанской государственной спортивной академии минимальный GPA установлен на уровне 2,4.

Студент обязан поддерживать или повышать этот показатель. В противном случае:
— При переводе или восстановлении требование GPA должно быть выполнено (≥ 2,4).
— При низком GPA студенту может быть предложено продолжить обучение с более низкого курса (семестра).
— Могут быть приняты академические предупредительные меры.""",
        # content_en
        """GPA (Grade Point Average) is a student's average academic score calculated by weighting grades in all subjects by their credit values.

At Uzbekistan State Sports Academy the minimum required GPA is 2.4.

Students must maintain or improve this score. Otherwise:
— A GPA of ≥ 2.4 is mandatory for transfer or reinstatement.
— A student with a low GPA may be offered to continue from a lower course (semester).
— Academic probation measures may be applied.""",
    ),
    (
        "scholarships", 1,
        "Stipendiyalar",
        "Стипендии",
        "Scholarships",
        # content_uz
        """O'zbekiston davlat sport akademiyasining bakalavriat ta'lim yo'nalishida hozirgi kunda jami 146 nafar talaba tahsil olmoqda.

Mazkur talabalar O'zbekiston Respublikasi amaldagi normativ-huquqiy hujjatlariga muvofiq ravishda to'liq davlat granti asosida o'qishga qabul qilingan bo'lib, ularning barchasi belgilangan tartibda davlat stipendiyasi bilan ta'minlanadi.""",
        # content_ru
        """В настоящее время на направлениях бакалавриата Узбекистанской государственной спортивной академии обучаются 146 студентов.

Все они приняты на обучение на основе полного государственного гранта в соответствии с действующими нормативно-правовыми документами Республики Узбекистан и в установленном порядке обеспечены государственными стипендиями.""",
        # content_en
        """Currently 146 students are enrolled in bachelor's programmes at Uzbekistan State Sports Academy.

All of them have been admitted on a full state grant in accordance with the current regulatory framework of the Republic of Uzbekistan and are provided with state scholarships in the prescribed manner.""",
    ),
    (
        "final-control", 1,
        "Yakuniy nazorat",
        "Итоговый контроль",
        "Final Control",
        # content_uz
        """O'zbekiston davlat sport akademiyasi bakalavriat ta'lim yo'nalishlarida yakuniy nazorat turlari o'quv fanlarining xususiyatidan kelib chiqib tashkil etiladi.

Asosan, yakuniy nazoratlar fan sillabuslarida belgilangan shaklda o'tkaziladi:
— Og'zaki nazorat
— Yozma ish
— Amaliy sinov
— Test sinovi

Talabalarning fan bo'yicha o'zlashtirish darajasi, nazariy bilimlari hamda amaliy ko'nikmalari kompleks tarzda baholanadi.

Yakuniy nazorat jarayonlari belgilangan tartib va me'yoriy hujjatlar asosida shaffoflik va xolislik tamoyillariga amal qilgan holda tashkil etiladi.""",
        # content_ru
        """В Узбекистанской государственной спортивной академии виды итогового контроля определяются исходя из специфики учебных дисциплин.

Как правило, итоговый контроль проводится в форме, установленной в силлабусе дисциплины:
— Устный опрос
— Письменная работа
— Практический экзамен
— Тестирование

Уровень усвоения дисциплины, теоретические знания и практические навыки студентов оцениваются комплексно.

Итоговый контроль организуется в соответствии с установленными правилами и нормативными документами с соблюдением принципов прозрачности и объективности.""",
        # content_en
        """At Uzbekistan State Sports Academy the types of final control are determined by the nature of each academic subject.

Final assessments are generally conducted in the form specified in the course syllabus:
— Oral examination
— Written work
— Practical test
— Multiple-choice test

Students' level of subject mastery, theoretical knowledge and practical skills are assessed comprehensively.

Final control is organised in accordance with established rules and regulatory documents, adhering to the principles of transparency and objectivity.""",
    ),

    # ══ BAKALAVRIAT MA'LUMOTNOMASI ═══════════════════════════════════════════════
    (
        "bakalavriat-malumotnoma", 1,
        "O'quv-uslubiy adabiyotlar fondi",
        "Фонд учебно-методической литературы",
        "Educational Resource Fund",
        # content_uz
        """O'zbekiston davlat sport akademiyasining Axborot-resurs markazida o'quv-uslubiy ta'minotni tizimli ravishda yo'lga qo'yish maqsadida bakalavriat va magistratura bosqichi talabalari, shuningdek, professor-o'qituvchilar tarkibining ilmiy-pedagogik faoliyati ehtiyojlarini to'liq qondirishga yo'naltirilgan jami 546 nomdagi 8 260 dona adabiyotlar fondi shakllantirilgan.

Fond tarkibi:
— Darsliklar:          3 752 dona
— O'quv qo'llanmalar:  3 474 dona
— Monografiyalar:        440 dona
— Badiiy adabiyotlar:    105 dona
— Boshqa adabiyotlar:    489 dona
— Jami:              8 260 dona (546 nom)

Mazkur fond ta'lim jarayonining samaradorligini oshirish, zamonaviy bilim va ko'nikmalarni egallash hamda ilmiy-tadqiqot faoliyatini rivojlantirishga xizmat qiladi.""",
        # content_ru
        """В информационно-ресурсном центре Узбекистанской государственной спортивной академии сформирован фонд учебно-методической литературы в количестве 8 260 экземпляров 546 наименований, направленный на полное удовлетворение потребностей студентов бакалавриата и магистратуры, а также профессорско-преподавательского состава.

Состав фонда:
— Учебники:               3 752 экз.
— Учебные пособия:        3 474 экз.
— Монографии:               440 экз.
— Художественная литература: 105 экз.
— Прочие издания:           489 экз.
— Итого:                 8 260 экз. (546 наименований)

Фонд служит повышению эффективности учебного процесса, освоению современных знаний и навыков, а также развитию научно-исследовательской деятельности.""",
        # content_en
        """The Information Resource Centre of Uzbekistan State Sports Academy has formed a collection of 8,260 copies of 546 titles of educational and methodological literature, designed to fully meet the needs of bachelor's and master's students as well as academic staff.

Collection breakdown:
— Textbooks:           3,752 copies
— Study guides:        3,474 copies
— Monographs:            440 copies
— Fiction:               105 copies
— Other publications:    489 copies
— Total:             8,260 copies (546 titles)

The collection serves to enhance the effectiveness of the educational process, acquisition of modern knowledge and skills, and development of research activities.""",
    ),
]


class Command(BaseCommand):
    help = "StudentInfoCategory va StudentInfo yozuvlarini to'ldiradi (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib, qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            ni = StudentInfo.objects.all().delete()[0]
            nc = StudentInfoCategory.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {nc} kategoriya, {ni} ma'lumot"))

        # ── Kategoriyalar ───────────────────────────────────────────────────────
        cat_map = {}
        for slug, order, uz, ru, en in CATEGORIES:
            cat, created = StudentInfoCategory.objects.update_or_create(
                slug=slug,
                defaults=dict(title_uz=uz, title_ru=ru, title_en=en, order=order),
            )
            cat_map[slug] = cat
            self.stdout.write(f"  [kat] {'[+]' if created else '[~]'} {uz}")

        # Eski "bakalavriat" slug bilan qolgan kategoriyani ham slug o'zgartirib yangilaymiz
        from django.utils.text import slugify
        old = StudentInfoCategory.objects.filter(slug='bakalavriat').first()
        if old:
            old.delete()
            self.stdout.write(self.style.WARNING("  [del] eski 'bakalavriat' kategoriya o'chirildi"))

        # ── Yozuvlar ────────────────────────────────────────────────────────────
        created_n = updated_n = 0
        for cat_slug, order, t_uz, t_ru, t_en, c_uz, c_ru, c_en in ITEMS:
            if cat_slug is None:
                cat = None
            else:
                cat = cat_map.get(cat_slug)
                if cat is None:
                    self.stdout.write(self.style.WARNING(f"  kategoriya topilmadi: {cat_slug}"))
                    continue
            _, is_new = StudentInfo.objects.update_or_create(
                category=cat, order=order,
                defaults=dict(
                    title_uz=t_uz, title_ru=t_ru, title_en=t_en,
                    content_uz=c_uz, content_ru=c_ru, content_en=c_en,
                    is_active=True,
                ),
            )
            if is_new:
                created_n += 1
            else:
                updated_n += 1
            self.stdout.write(f"    {'[+]' if is_new else '[~]'} {t_uz}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created_n} yangi, {updated_n} yangilandi. Jami {len(ITEMS)} ta yozuv."
        ))
