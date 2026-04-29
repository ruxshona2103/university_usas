"""
python manage.py seed_korrupsiya          # yaratadi (slug bo'yicha idempotent)
python manage.py seed_korrupsiya --clear  # barcha ma'lumotlarni o'chirib qaytadan yozadi
"""
from datetime import datetime, timezone as dt_timezone
from django.core.management.base import BaseCommand
from domains.news.models import Korrupsiya

_UTC = dt_timezone.utc

DATA = [
    {
        "slug": "akademiyada-korrupsiyaga-qarshi-targʻibot-tadbiri-2025",
        "date": datetime(2025, 4, 29, 10, 0, 0, tzinfo=_UTC),
        "title_uz": "Akademiyada korrupsiyaga qarshi kurashish siyosati bo'yicha targ'ibot tadbiri o'tkazildi",
        "title_ru": "В Академии прошло просветительское мероприятие по антикоррупционной политике",
        "title_en": "Awareness event on anti-corruption policy held at the Academy",
        "tavsif_uz": "O'zbekiston davlat sport akademiyasida \"Sport akademiyasida korrupsiyaga qarshi kurashish\" siyosati mavzusida taqdimot tadbiri tashkil etildi.",
        "tavsif_ru": "В Государственной академии спорта Узбекистана состоялось презентационное мероприятие на тему политики «Борьба с коррупцией в спортивной академии».",
        "tavsif_en": "A presentation event on the topic of \"Anti-Corruption Policy in the Sports Academy\" was organised at the Uzbekistan State Sports Academy.",
        "description_uz": """O'zbekiston davlat sport akademiyasida "Sport akademiyasida korrupsiyaga qarshi kurashish" siyosati mavzusida taqdimot tadbiri tashkil etildi.

Tadbir davomida Sport vazirligining korrupsiyaga qarshi kurashish siyosatining mazmun-mohiyati Akademiya professor-o'qituvchilari hamda xodimlariga batafsil tanishtirildi. Shuningdek, mazkur yo'nalishda amalga oshirilayotgan tizimli chora-tadbirlar, yaratilgan huquqiy va tashkiliy mexanizmlar haqida atroflicha ma'lumot berildi.

Ta'kidlanganidek, respublikamizda korrupsiyaga qarshi kurashish borasida qabul qilingan qonunchilik hujjatlari va qonunosti me'yoriy hujjatlar mazmuni xodimlarga yetkazildi. Ayniqsa, ta'lim jarayonini sifatli tashkil etish, mavjud imkoniyatlardan samarali foydalanish, xizmat vazifalarini vijdonan va mas'uliyat bilan bajarish har bir pedagog va xodimning ustuvor burchi ekani alohida qayd etildi.

Tadbir yakunida davlatimiz tomonidan yaratilayotgan keng imkoniyat va sharoitlarga munosib hissa qo'shish, korrupsiyaga nisbatan murosasiz munosabatni shakllantirish va uni oldini olishda barcha xodimlarning faol ishtiroki muhim ekani ta'kidlandi.""",
        "description_ru": """В Государственной академии спорта Узбекистана состоялось презентационное мероприятие на тему «Политика борьбы с коррупцией в спортивной академии».

В ходе мероприятия профессорско-преподавательскому составу и сотрудникам Академии была подробно представлена суть антикоррупционной политики Министерства спорта. Также была предоставлена исчерпывающая информация о системных мерах, реализуемых в данном направлении, и созданных правовых и организационных механизмах.

Как было отмечено, сотрудникам были доведены положения законодательных и подзаконных нормативных актов, принятых в Республике по борьбе с коррупцией. В частности, было особо подчёркнуто, что качественная организация учебного процесса, эффективное использование имеющихся возможностей, добросовестное и ответственное выполнение служебных обязанностей является приоритетным долгом каждого педагога и сотрудника.

По итогам мероприятия была подчёркнута важность достойного вклада в создаваемые государством широкие возможности и условия, формирования нетерпимого отношения к коррупции и активного участия всех сотрудников в её предотвращении.""",
        "description_en": """A presentation event on the topic of "Anti-Corruption Policy in the Sports Academy" was organised at the Uzbekistan State Sports Academy.

During the event, the essence of the Ministry of Sports' anti-corruption policy was presented in detail to the Academy's faculty and staff. Comprehensive information was also provided about the systematic measures being implemented in this area and the legal and organisational mechanisms that have been established.

As noted, staff were informed about the content of legislative and regulatory documents adopted in the Republic on anti-corruption. In particular, it was especially emphasised that the quality organisation of the educational process, effective use of available resources, and conscientious and responsible performance of official duties are the priority obligations of every teacher and employee.

At the conclusion of the event, the importance of making a worthy contribution to the wide opportunities and conditions being created by the state, forming an intolerant attitude towards corruption and the active participation of all employees in preventing it was emphasised.""",
        "is_published": True,
    },
    {
        "slug": "korrupsiyaga-qarshi-kurash-davlat-siyosati-2025",
        "date": datetime(2025, 3, 15, 10, 0, 0, tzinfo=_UTC),
        "title_uz": "Korrupsiyaga qarshi kurash — davlat siyosatining ustuvor yo'nalishi",
        "title_ru": "Борьба с коррупцией — приоритетное направление государственной политики",
        "title_en": "Anti-corruption — a priority of state policy",
        "tavsif_uz": "O'zbekistonda korrupsiyaga qarshi kurash bo'yicha amalga oshirilayotgan islohotlar va ularning natijalari haqida.",
        "tavsif_ru": "О реформах по борьбе с коррупцией в Узбекистане и их результатах.",
        "tavsif_en": "On anti-corruption reforms in Uzbekistan and their outcomes.",
        "description_uz": """O'zbekiston Respublikasida korrupsiyaga qarshi kurash davlat siyosatining ustuvor yo'nalishlaridan biri sifatida belgilangan.

2020-yilda qabul qilingan «Korrupsiyaga qarshi kurash to'g'risida»gi Qonun ushbu sohadagi asosiy huquqiy hujjat hisoblanadi. Qonunga ko'ra:

• Korrupsiya holatlari bo'yicha xabar berish mexanizmlari kuchaytirilgan
• Davlat xizmatchilarining mol-mulkini e'lon qilish majburiy etilgan
• Korrupsiyaga qarshi ta'lim tizimi joriy etilgan
• Jamoatchilik nazorati mexanizmlari mustahkamlangan

Akademiyamizda ham ushbu yo'nalishda tizimli ishlar olib borilmoqda. Xodimlar va talabalar o'rtasida korrupsiyaga qarshi targ'ibot tadbirlari muntazam o'tkazib kelinmoqda.""",
        "description_ru": """В Республике Узбекистан борьба с коррупцией определена как одно из приоритетных направлений государственной политики.

Принятый в 2020 году Закон «О противодействии коррупции» является основным правовым документом в этой сфере. Согласно Закону:

• Усилены механизмы сообщения о фактах коррупции
• Введено обязательное декларирование имущества государственными служащими
• Внедрена система антикоррупционного образования
• Укреплены механизмы общественного контроля

В нашей Академии также ведётся системная работа в этом направлении. Среди сотрудников и студентов регулярно проводятся просветительские мероприятия по противодействию коррупции.""",
        "description_en": """In the Republic of Uzbekistan, anti-corruption efforts have been designated as one of the priority areas of state policy.

The Law "On Combating Corruption" adopted in 2020 is the primary legal document in this area. According to the Law:

• Mechanisms for reporting corruption have been strengthened
• Mandatory declaration of property by civil servants has been introduced
• An anti-corruption education system has been implemented
• Public oversight mechanisms have been strengthened

Our Academy also conducts systematic work in this direction. Anti-corruption awareness events are regularly held among staff and students.""",
        "is_published": True,
    },
    {
        "slug": "akademiyada-korrupsiyaga-qarshi-seminar-2025",
        "date": datetime(2025, 4, 10, 9, 0, 0, tzinfo=_UTC),
        "title_uz": "Akademiyada «Korrupsiyaga qarshi kurash» mavzusida seminar o'tkazildi",
        "title_ru": "В Академии проведён семинар на тему «Борьба с коррупцией»",
        "title_en": "Anti-corruption seminar held at the Academy",
        "tavsif_uz": "O'zbekiston Davlat Sport Akademiyasida korrupsiyaga qarshi kurash mavzusida o'quv seminari bo'lib o'tdi.",
        "tavsif_ru": "В Государственной академии спорта Узбекистана прошёл учебный семинар по борьбе с коррупцией.",
        "tavsif_en": "An educational seminar on anti-corruption was held at the Uzbekistan State Sports Academy.",
        "description_uz": """O'zbekiston Davlat Sport Akademiyasida «Korrupsiyaga qarshi kurash» mavzusida seminar bo'lib o'tdi.

Seminarda akademiya xodimlari va talabalar qatnashdi. Tadbir davomida quyidagi masalalar muhokama qilindi:

• Korrupsiyaning sabablari va oqibatlari
• Korrupsiyaga qarshi kurashning huquqiy asoslari
• Xodimlarning huquq va majburiyatlari
• Korrupsiya holatlarini aniqlash va xabar berish tartibi
• Xalqaro tajriba va eng yaxshi amaliyotlar

Seminar yakunida ishtirokchilar savol-javob formatida o'z fikr-mulohazalarini baham ko'rdilar.""",
        "description_ru": """В Государственной академии спорта Узбекистана прошёл семинар на тему «Борьба с коррупцией».

В семинаре приняли участие сотрудники и студенты академии. В ходе мероприятия были обсуждены следующие вопросы:

• Причины и последствия коррупции
• Правовые основы борьбы с коррупцией
• Права и обязанности сотрудников
• Порядок выявления и сообщения о коррупции
• Международный опыт и лучшие практики

По итогам семинара участники поделились своими мнениями в формате вопросов и ответов.""",
        "description_en": """A seminar on "Anti-Corruption" was held at the Uzbekistan State Sports Academy.

The seminar was attended by Academy staff and students. The following issues were discussed during the event:

• Causes and consequences of corruption
• Legal foundations of anti-corruption efforts
• Rights and obligations of employees
• Procedures for identifying and reporting corruption
• International experience and best practices

At the end of the seminar, participants shared their thoughts in a Q&A format.""",
        "is_published": True,
    },
    {
        "slug": "korrupsiyaga-qarshi-hotline-ishga-tushirildi-2025",
        "date": datetime(2025, 5, 1, 8, 0, 0, tzinfo=_UTC),
        "title_uz": "Akademiyada korrupsiyaga qarshi «Ishonch telefoni» ishga tushirildi",
        "title_ru": "В Академии запущена антикоррупционная «горячая линия»",
        "title_en": "Anti-corruption hotline launched at the Academy",
        "tavsif_uz": "Akademiya xodimlari va talabalari korrupsiya holatlari haqida maxfiy ravishda xabar berish imkoniyatiga ega bo'ldi.",
        "tavsif_ru": "Сотрудники и студенты Академии получили возможность конфиденциально сообщать о фактах коррупции.",
        "tavsif_en": "Academy staff and students can now report corruption cases confidentially.",
        "description_uz": """O'zbekiston Davlat Sport Akademiyasida korrupsiyaga qarshi «Ishonch telefoni» rasman ishga tushirildi.

Ushbu xizmat orqali akademiya xodimlari, talabalari va tashqi manfaatdor tomonlar korrupsiya holatlari, suiiste'mollar va noqonuniy harakatlar to'g'risida maxfiy ravishda xabar berish imkoniyatiga ega bo'ldi.

Ishonch telefoni raqami: +998 71 000 00 00
Elektron pochta: ishonch@usas.uz
Ish vaqti: 24/7 rejimida ishlaydi

Barcha murojaatlar maxfiy saqlanadi va o'z vaqtida ko'rib chiqiladi. Xabar beruvchilar qonuniy himoyaga ega.""",
        "description_ru": """В Государственной академии спорта Узбекистана официально запущена антикоррупционная «горячая линия».

Через эту службу сотрудники академии, студенты и внешние заинтересованные стороны получили возможность конфиденциально сообщать о фактах коррупции, злоупотреблениях и незаконных действиях.

Номер горячей линии: +998 71 000 00 00
Электронная почта: ishonch@usas.uz
Режим работы: круглосуточно

Все обращения сохраняются в конфиденциальности и рассматриваются своевременно. Заявители находятся под правовой защитой.""",
        "description_en": """The anti-corruption "Hotline" has been officially launched at the Uzbekistan State Sports Academy.

Through this service, Academy staff, students, and external stakeholders can confidentially report corruption, abuse, and unlawful actions.

Hotline number: +998 71 000 00 00
Email: ishonch@usas.uz
Operating hours: 24/7

All applications are kept confidential and reviewed in a timely manner. Whistleblowers are protected by law.""",
        "is_published": True,
    },
    {
        "slug": "yoshlar-orasida-korrupsiyaga-qarshi-konkurs-2025",
        "date": datetime(2025, 5, 20, 11, 0, 0, tzinfo=_UTC),
        "title_uz": "Yoshlar o'rtasida «Korrupsiyasiz kelajak» nomli ijodiy tanlov e'lon qilindi",
        "title_ru": "Объявлен творческий конкурс «Будущее без коррупции» среди молодёжи",
        "title_en": "Creative contest 'A Future Without Corruption' announced for youth",
        "tavsif_uz": "Akademiya talabalari o'rtasida korrupsiyaga qarshi ijodiy tanlov e'lon qilindi.",
        "tavsif_ru": "Среди студентов Академии объявлен антикоррупционный творческий конкурс.",
        "tavsif_en": "An anti-corruption creative contest has been announced among Academy students.",
        "description_uz": """O'zbekiston Davlat Sport Akademiyasi «Korrupsiyasiz kelajak» nomli ijodiy tanlov e'lon qilmoqda.

TANLOV SHARTLARI:

Ishtirokchilar:
• Akademiya talabalari (bakalavriat va magistratura)

Nominatsiyalar:
1. Eng yaxshi esse — «Korrupsiya va uning jamiyatga ta'siri»
2. Eng yaxshi video rolik — 1-3 daqiqa
3. Eng yaxshi infografika yoki plakat

Topshirish muddati: 2025-yil 15-iyun
Manzil: akademiya axborot xizmati yoki elektron pochta orqali

G'oliblar mukofotlar va faxriy yorliqlar bilan taqdirlanadi.

Batafsil ma'lumot uchun: axborot@usas.uz""",
        "description_ru": """Государственная академия спорта Узбекистана объявляет творческий конкурс «Будущее без коррупции».

УСЛОВИЯ КОНКУРСА:

Участники:
• Студенты Академии (бакалавриат и магистратура)

Номинации:
1. Лучшее эссе — «Коррупция и её влияние на общество»
2. Лучший видеоролик — 1-3 минуты
3. Лучшая инфографика или плакат

Срок подачи: 15 июня 2025 года
Адрес: информационная служба академии или по электронной почте

Победители будут награждены призами и почётными грамотами.

Подробная информация: axborot@usas.uz""",
        "description_en": """The Uzbekistan State Sports Academy announces a creative contest titled "A Future Without Corruption".

CONTEST TERMS:

Participants:
• Academy students (bachelor's and master's)

Nominations:
1. Best essay — "Corruption and its impact on society"
2. Best video — 1-3 minutes
3. Best infographic or poster

Submission deadline: June 15, 2025
Address: Academy information service or by email

Winners will be awarded prizes and certificates of merit.

For more information: axborot@usas.uz""",
        "is_published": True,
    },
    {
        "slug": "korrupsiyaga-qarshi-xalqaro-kun-2025",
        "date": datetime(2025, 12, 9, 10, 0, 0, tzinfo=_UTC),
        "title_uz": "9-dekabr — Xalqaro Korrupsiyaga Qarshi Kurash Kuni munosabati bilan tadbir o'tkazildi",
        "title_ru": "9 декабря — мероприятие, посвящённое Международному дню борьбы с коррупцией",
        "title_en": "December 9 — event held on International Anti-Corruption Day",
        "tavsif_uz": "Xalqaro Korrupsiyaga Qarshi Kurash Kuni munosabati bilan akademiyada maxsus tadbir o'tkazildi.",
        "tavsif_ru": "В честь Международного дня борьбы с коррупцией в Академии прошло специальное мероприятие.",
        "tavsif_en": "A special event was held at the Academy to mark International Anti-Corruption Day.",
        "description_uz": """Har yili 9-dekabrda nishonlanadigan Xalqaro Korrupsiyaga Qarshi Kurash Kuni munosabati bilan O'zbekiston Davlat Sport Akademiyasida maxsus tadbir o'tkazildi.

Tadbirda akademiya rahbariyati, professor-o'qituvchilar va talabalar qatnashdi.

Dastur:
• Korrupsiyaga qarshi kurash bo'yicha ma'ruza
• «Korrupsiyasiz kelajak» tanlov g'oliblarini taqdirlash
• Korrupsiyaga qarshi video va infografika namoyishi
• Ishtirokchilar bilan suhbat

BMT Ma'lumotlari:
Korrupsiya yiliga global YaMM ning taxminan 5 foiziga, ya'ni 2,6 trillion AQSh dollariga teng zarar keltiradi.

Barcha fuqarolarni korrupsiyaga qarshi kurashda faol ishtirok etishga chaqiramiz!""",
        "description_ru": """В честь Международного дня борьбы с коррупцией, отмечаемого ежегодно 9 декабря, в Государственной академии спорта Узбекистана прошло специальное мероприятие.

В мероприятии приняли участие руководство академии, профессорско-преподавательский состав и студенты.

Программа:
• Доклад по борьбе с коррупцией
• Награждение победителей конкурса «Будущее без коррупции»
• Показ антикоррупционных видео и инфографики
• Беседа с участниками

По данным ООН:
Коррупция ежегодно наносит ущерб в размере около 5% мирового ВВП, то есть 2,6 триллиона долларов США.

Призываем всех граждан активно участвовать в борьбе с коррупцией!""",
        "description_en": """A special event was held at the Uzbekistan State Sports Academy to mark International Anti-Corruption Day, celebrated annually on December 9.

The event was attended by Academy management, faculty, and students.

Programme:
• Lecture on anti-corruption
• Award ceremony for "A Future Without Corruption" contest winners
• Screening of anti-corruption videos and infographics
• Discussion with participants

UN Data:
Corruption costs the global economy approximately 5% of global GDP — around $2.6 trillion — annually.

We call on all citizens to actively participate in the fight against corruption!""",
        "is_published": True,
    },
]


class Command(BaseCommand):
    help = "Korrupsiyaga qarshi kurash fake ma'lumotlarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = Korrupsiya.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        created = updated = 0
        for d in DATA:
            slug = d.pop('slug')
            obj, is_new = Korrupsiya.objects.update_or_create(
                slug=slug,
                defaults=d,
            )
            d['slug'] = slug
            if is_new:
                created += 1
            else:
                updated += 1
            self.stdout.write(f"  [{'Yaratildi' if is_new else 'Yangilandi'}] {obj.title_uz[:70]}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created} yangi, {updated} yangilandi. Jami {len(DATA)} ta."
        ))
