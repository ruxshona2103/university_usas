"""
python manage.py seed_bitiruvchilar_ustozlar          # yaratadi / yangilaydi
python manage.py seed_bitiruvchilar_ustozlar --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.students.models import Person, PersonCategory, PersonContent
from common.models import Tag


TAGS = [
    ("biografiya",  "Biografiya",       "Биография",      "Biography"),
    ("yutuqlar",    "Yutuqlar",          "Достижения",     "Achievements"),
    ("faoliyat",    "Ilmiy faoliyat",    "Научная деятельность", "Academic Activity"),
]


# ── BITIRUVCHILAR ──────────────────────────────────────────────────────────────

BITIRUVCHILAR = [
    # ═══════════════════════════════════════════════════════════════════════════
    # 1. Hasanboy Dusmatov
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 1,
        "is_head": False,
        "full_name_uz": "Dusmatov Hasanboy Yusupovich",
        "full_name_ru": "Дусматов Хасанбой Юсупович",
        "full_name_en": "Hasanboy Yusupovich Dusmatov",
        "title_uz": "O'zbekiston terma jamoasi bokschi, Olimpiya chempioni",
        "title_ru": "Боксёр сборной Узбекистана, олимпийский чемпион",
        "title_en": "Uzbekistan national team boxer, Olympic champion",
        "position_uz": "Jismoniy tarbiya va sport magistri",
        "position_ru": "Магистр физической культуры и спорта",
        "position_en": "Master of Physical Culture and Sports",
        "phone": "",
        "email": "",
        "reception": "",
        "address": "Toshkent shahri",
        "bio_uz": (
            "Dusmatov Hasanboy Yusupovich 1994-yil 9-yanvarda Toshkent viloyatida tug'ilgan. "
            "O'zbekiston davlat sport akademiyasini magistratura bosqichida 2019-yilda tamomlagan. "
            "2016-yil Rio-de-Janeyro Olimpiya o'yinlarida 49 kg vazn toifasida oltin medal sohibi bo'lgan — "
            "mazkur Olimpiadaning eng yaxshi bokseri sifatida Val Barker kubogi bilan taqdirlangan. "
            "2015 va 2019-yillardagi Jahon chempionatlarida oltin medal qozongan. "
            "Xalqaro musobaqalarda O'zbekistonni munosib namoyish etib, \"Shon-sharaf\" ordeni bilan "
            "taqdirlangan. Hozirda yosh bokschilarni tayyorlash bo'yicha murabbiylik faoliyatini olib boradi."
        ),
        "bio_ru": (
            "Дусматов Хасанбой Юсупович родился 9 января 1994 года в Ташкентской области. "
            "В 2019 году окончил магистратуру Государственной спортивной академии Узбекистана. "
            "На Олимпийских играх 2016 года в Рио-де-Жанейро завоевал золотую медаль в весовой "
            "категории до 49 кг и был удостоен Кубка Вэла Баркера как лучший боксёр Олимпиады. "
            "Чемпион мира 2015 и 2019 годов. Награждён орденом «Шон-шараф» за достойное "
            "представление Узбекистана на международных соревнованиях. "
            "В настоящее время занимается тренерской деятельностью по подготовке молодых боксёров."
        ),
        "bio_en": (
            "Hasanboy Yusupovich Dusmatov was born on January 9, 1994, in Tashkent Region. "
            "He completed his master's degree at the Uzbekistan State Sports Academy in 2019. "
            "At the 2016 Rio de Janeiro Olympic Games, he won the gold medal in the 49 kg weight "
            "category and was awarded the Val Barker Cup as the best boxer of the Olympics. "
            "He is a World Champion in 2015 and 2019. He was awarded the 'Shon-sharaf' Order for "
            "his distinguished representation of Uzbekistan in international competitions. "
            "He currently works as a coach preparing young boxers."
        ),
        "achievement_uz": (
            "2016 Rio Olimpiadasi — Oltin medal (49 kg)\n"
            "2016 Rio — Val Barker kubogi (olimpiadaning eng yaxshi bokseri)\n"
            "2015 Jahon chempionati — Oltin medal\n"
            "2019 Jahon chempionati — Oltin medal\n"
            "Osiyo o'yinlari — Oltin medal\n"
            "\"Shon-sharaf\" ordeni sohibi"
        ),
        "achievement_ru": (
            "Олимпиада 2016 Рио — Золотая медаль (49 кг)\n"
            "Рио 2016 — Кубок Вэла Баркера (лучший боксёр Олимпиады)\n"
            "Чемпионат мира 2015 — Золотая медаль\n"
            "Чемпионат мира 2019 — Золотая медаль\n"
            "Азиатские игры — Золотая медаль\n"
            "Орден «Шон-шараф»"
        ),
        "achievement_en": (
            "2016 Rio Olympics — Gold Medal (49 kg)\n"
            "Rio 2016 — Val Barker Cup (best boxer of the Olympics)\n"
            "2015 World Championship — Gold Medal\n"
            "2019 World Championship — Gold Medal\n"
            "Asian Games — Gold Medal\n"
            "Order of 'Shon-sharaf'"
        ),
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # 2. Oksana Chusovitina
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 2,
        "is_head": False,
        "full_name_uz": "Chusovitina Oksana Aleksandrovna",
        "full_name_ru": "Чусовитина Оксана Александровна",
        "full_name_en": "Oksana Aleksandrovna Chusovitina",
        "title_uz": "O'zbekiston sport gimnastikasi ustasi, Olimpiya chempioni",
        "title_ru": "Заслуженный мастер спорта Узбекистана по спортивной гимнастике, олимпийская чемпионка",
        "title_en": "Honored Master of Sports of Uzbekistan in artistic gymnastics, Olympic champion",
        "position_uz": "Jismoniy tarbiya va sport magistri",
        "position_ru": "Магистр физической культуры и спорта",
        "position_en": "Master of Physical Culture and Sports",
        "phone": "",
        "email": "",
        "reception": "",
        "address": "Toshkent shahri",
        "bio_uz": (
            "Chusovitina Oksana Aleksandrovna 1975-yil 19-iyunda O'zbekistoning Buxoro shahrida "
            "tug'ilgan. O'zbekiston davlat sport akademiyasini 2003-yilda tamomlagan. "
            "Dunyo sportida 30 yildan ortiq faoliyat yuritib, 1992-yildan boshlab jami 8 ta Olimpiada "
            "o'yinlarida qatnashgan — olimpiya tarixida eng uzoq qatnashgan gimnast hisoblanadi. "
            "1992-yil Barselona Olimpiadasida jamoa ko'rinishida oltin medal sohibi. "
            "Jahon chempionatlarida 11 ta medal qozongan. 2006-yilda Germaniya fuqarolariga o'tib, "
            "ikki davlat nomidan musobaqalarda qatnashgan. 2013-yildan O'zbekistonga qaytib, "
            "2021-yil Tokio Olimpiadasida ham mamlakati nomidan ishtirok etgan."
        ),
        "bio_ru": (
            "Чусовитина Оксана Александровна родилась 19 июня 1975 года в Бухаре (Узбекистан). "
            "Окончила Государственную спортивную академию Узбекистана в 2003 году. "
            "На протяжении более 30 лет выступала на мировых соревнованиях и приняла участие "
            "в 8 Олимпийских играх начиная с 1992 года, став самым долго выступающим гимнастом "
            "в олимпийской истории. В 1992 году в Барселоне стала олимпийской чемпионкой в командном "
            "многоборье. Завоевала 11 медалей на чемпионатах мира. В 2006 году получила гражданство "
            "Германии и выступала за две страны. Вернувшись в Узбекистан в 2013 году, участвовала "
            "в Олимпийских играх в Токио 2021 года под флагом своей страны."
        ),
        "bio_en": (
            "Oksana Aleksandrovna Chusovitina was born on June 19, 1975, in Bukhara, Uzbekistan. "
            "She graduated from the Uzbekistan State Sports Academy in 2003. "
            "Over a career spanning more than 30 years, she competed in 8 Olympic Games starting "
            "from 1992, becoming the longest-competing gymnast in Olympic history. "
            "She won a team gold medal at the 1992 Barcelona Olympics and earned 11 medals at "
            "World Championships. In 2006, she acquired German citizenship and competed for both "
            "countries at different periods. After returning to Uzbekistan in 2013, she participated "
            "in the 2021 Tokyo Olympics representing her home country."
        ),
        "achievement_uz": (
            "1992 Barselona Olimpiadasi — Oltin medal (jamoa)\n"
            "8 ta Olimpiada o'yinlari ishtirokchisi (1992–2021)\n"
            "Jahon chempionatlarida 11 ta medal\n"
            "Osiyo o'yinlari — 2 ta oltin medal\n"
            "O'zbekiston sport gimnastikasining asoschisi va rivojlantiruvchisi\n"
            "\"Jasorat\" ordeni sohibi"
        ),
        "achievement_ru": (
            "Олимпиада 1992 Барселона — Золотая медаль (команда)\n"
            "Участница 8 Олимпийских игр (1992–2021)\n"
            "11 медалей на чемпионатах мира\n"
            "2 золотые медали Азиатских игр\n"
            "Основатель и популяризатор спортивной гимнастики Узбекистана\n"
            "Орден «Жасорат»"
        ),
        "achievement_en": (
            "1992 Barcelona Olympics — Gold Medal (team)\n"
            "Participant of 8 Olympic Games (1992–2021)\n"
            "11 medals at World Championships\n"
            "2 gold medals at Asian Games\n"
            "Pioneer and ambassador of artistic gymnastics in Uzbekistan\n"
            "Order of 'Jasorat'"
        ),
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # 3. Ruslan Nurudinov
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 3,
        "is_head": False,
        "full_name_uz": "Nurudinov Ruslan Mirzoahmadovich",
        "full_name_ru": "Нурудинов Руслан Мирзоахмадович",
        "full_name_en": "Ruslan Mirzoahmadovich Nurudinov",
        "title_uz": "O'zbekiston shtanga ko'tarish sport ustasi, Olimpiya chempioni",
        "title_ru": "Заслуженный мастер спорта Узбекистана по тяжёлой атлетике, олимпийский чемпион",
        "title_en": "Honored Master of Sports of Uzbekistan in weightlifting, Olympic champion",
        "position_uz": "Jismoniy tarbiya va sport magistri",
        "position_ru": "Магистр физической культуры и спорта",
        "position_en": "Master of Physical Culture and Sports",
        "phone": "",
        "email": "",
        "reception": "",
        "address": "Toshkent shahri",
        "bio_uz": (
            "Nurudinov Ruslan Mirzoahmadovich 1991-yil 23-avgustda Tojikistonda tug'ilib, keyinchalik "
            "O'zbekiston fuqaroligini qabul qilgan. O'zbekiston davlat sport akademiyasini 2016-yilda "
            "tamomlagan. 2016-yil Rio-de-Janeyro Olimpiya o'yinlarida 85 kg vazn toifasida oltin medal "
            "sohibi bo'lgan. Osiyo va Dunyo chempionatlari g'olibi. O'zbekiston shtanga ko'tarish "
            "sportining ravnaqiga katta hissa qo'shgan. Hozirda Olimpiya zaxiralari bilan ishlaydi va "
            "keyingi avlod sportchilarini tayyorlashda faol ishtirok etadi."
        ),
        "bio_ru": (
            "Нурудинов Руслан Мирзоахмадович родился 23 августа 1991 года в Таджикистане, "
            "впоследствии принял гражданство Узбекистана. Окончил Государственную спортивную "
            "академию Узбекистана в 2016 году. На Олимпийских играх 2016 года в Рио-де-Жанейро "
            "завоевал золотую медаль в весовой категории до 85 кг. Победитель азиатских и "
            "мировых чемпионатов. Внёс значительный вклад в развитие тяжёлой атлетики Узбекистана. "
            "В настоящее время работает с олимпийским резервом и активно участвует в подготовке "
            "следующего поколения спортсменов."
        ),
        "bio_en": (
            "Ruslan Mirzoahmadovich Nurudinov was born on August 23, 1991, in Tajikistan, and later "
            "acquired Uzbek citizenship. He graduated from the Uzbekistan State Sports Academy in 2016. "
            "At the 2016 Rio de Janeiro Olympic Games, he won the gold medal in the 85 kg weight "
            "category. He is a champion of Asian and World Championships. He has made a significant "
            "contribution to the development of weightlifting in Uzbekistan and currently works with "
            "the Olympic reserve, actively participating in training the next generation of athletes."
        ),
        "achievement_uz": (
            "2016 Rio Olimpiadasi — Oltin medal (85 kg)\n"
            "Osiyo chempionati — Oltin medal\n"
            "Jahon chempionati — Kumush medal\n"
            "O'zbekiston chempioni (ko'p marta)\n"
            "\"Shon-sharaf\" ordeni sohibi"
        ),
        "achievement_ru": (
            "Олимпиада 2016 Рио — Золотая медаль (85 кг)\n"
            "Чемпионат Азии — Золотая медаль\n"
            "Чемпионат мира — Серебряная медаль\n"
            "Многократный чемпион Узбекистана\n"
            "Орден «Шон-шараф»"
        ),
        "achievement_en": (
            "2016 Rio Olympics — Gold Medal (85 kg)\n"
            "Asian Championship — Gold Medal\n"
            "World Championship — Silver Medal\n"
            "Multiple Uzbekistan Champion\n"
            "Order of 'Shon-sharaf'"
        ),
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # 4. Yulduz Jumaeva
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 4,
        "is_head": False,
        "full_name_uz": "Jumaeva Yulduz Nematovna",
        "full_name_ru": "Жумаева Юлдуз Нематовна",
        "full_name_en": "Yulduz Nematovna Jumaeva",
        "title_uz": "O'zbekiston yengil atletika sport ustasi, Osiyo chempioni",
        "title_ru": "Заслуженный мастер спорта Узбекистана по лёгкой атлетике, чемпионка Азии",
        "title_en": "Honored Master of Sports of Uzbekistan in athletics, Asian champion",
        "position_uz": "Jismoniy tarbiya va sport o'qituvchisi (bakalavr)",
        "position_ru": "Преподаватель физической культуры и спорта (бакалавр)",
        "position_en": "Physical Culture and Sports Teacher (bachelor's degree)",
        "phone": "",
        "email": "",
        "reception": "",
        "address": "Samarqand viloyati",
        "bio_uz": (
            "Jumaeva Yulduz Nematovna 1998-yil 14-martda Samarqand viloyatida tug'ilgan. "
            "O'zbekiston davlat sport akademiyasini 2020-yilda bakalavr bosqichida tamomlagan. "
            "Uzun sakrash va uch qadam sakrash bo'yicha ixtisoslashgan. "
            "2022-yil Osiyo atletika chempionatida uzun sakrashda birinchi o'rinni egallagan. "
            "Ko'p yillar davomida O'zbekiston terma jamoasi a'zosi sifatida Xalqaro musobaqalarda "
            "yuqori natijalar ko'rsatib kelgan. Hozirda o'qituvchilik va sport murabbiyligini "
            "muvaffaqiyatli qo'shib olib boradi."
        ),
        "bio_ru": (
            "Жумаева Юлдуз Нематовна родилась 14 марта 1998 года в Самаркандской области. "
            "Окончила бакалавриат Государственной спортивной академии Узбекистана в 2020 году. "
            "Специализируется в прыжках в длину и тройном прыжке. "
            "В 2022 году заняла первое место в прыжках в длину на чемпионате Азии по лёгкой атлетике. "
            "На протяжении многих лет является членом сборной команды Узбекистана, показывая "
            "высокие результаты на международных соревнованиях. "
            "В настоящее время совмещает педагогическую и тренерскую деятельность."
        ),
        "bio_en": (
            "Yulduz Nematovna Jumaeva was born on March 14, 1998, in Samarkand Region. "
            "She completed her bachelor's degree at the Uzbekistan State Sports Academy in 2020. "
            "She specialises in long jump and triple jump. "
            "In 2022, she won first place in the long jump at the Asian Athletics Championships. "
            "For many years, she has been a member of the Uzbekistan national team, showing high "
            "results at international competitions. "
            "She currently combines teaching and sports coaching successfully."
        ),
        "achievement_uz": (
            "2022 Osiyo atletika chempionati — Uzun sakrashda Oltin medal\n"
            "Markaziy Osiyo chempionati — Ko'p marta g'olib\n"
            "O'zbekiston chempionatida rekord ko'rsatkich\n"
            "Xalqaro Grand Prix musobaqalarida qatnashuvchi"
        ),
        "achievement_ru": (
            "Чемпионат Азии по лёгкой атлетике 2022 — Золотая медаль в прыжках в длину\n"
            "Чемпионат Центральной Азии — Многократный победитель\n"
            "Рекордные показатели на чемпионате Узбекистана\n"
            "Участница международных соревнований Grand Prix"
        ),
        "achievement_en": (
            "2022 Asian Athletics Championships — Gold Medal in long jump\n"
            "Central Asian Championship — Multiple winner\n"
            "Record performance at Uzbekistan Championship\n"
            "Participant of international Grand Prix competitions"
        ),
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # 5. Shamsiddin Toshpulatov
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 5,
        "is_head": False,
        "full_name_uz": "Toshpulatov Shamsiddin Rahimjonovich",
        "full_name_ru": "Тошпулатов Шамсиддин Рахимжонович",
        "full_name_en": "Shamsiddin Rahimjonovich Toshpulatov",
        "title_uz": "O'zbekiston kurash sport ustasi, Xalqaro musobaqalar g'olibi",
        "title_ru": "Заслуженный мастер спорта Узбекистана по курашу, победитель международных соревнований",
        "title_en": "Honored Master of Sports of Uzbekistan in kurash, international competition winner",
        "position_uz": "Jismoniy tarbiya va sport magistri, sport menejmenti mutaxassisi",
        "position_ru": "Магистр физической культуры и спорта, специалист по спортивному менеджменту",
        "position_en": "Master of Physical Culture and Sports, sports management specialist",
        "phone": "",
        "email": "",
        "reception": "",
        "address": "Farg'ona viloyati",
        "bio_uz": (
            "Toshpulatov Shamsiddin Rahimjonovich 1995-yil 7-iyulda Farg'ona viloyatida tug'ilgan. "
            "O'zbekiston davlat sport akademiyasini magistratura bosqichida 2021-yilda tamomlagan, "
            "sport menejment ixtisosligi bo'yicha ilmiy ish yoqlagan. "
            "Milliy kurash turida 90 kg vazn toifasida Dunyo chempionati g'olibi. "
            "Osiyo va Markaziy Osiyo chempionatlarida ko'p marta g'olib chiqkan. "
            "Hozirda O'zbekiston kurash federatsiyasida xalqaro munosabatlar bo'yicha maslahatchi "
            "sifatida faoliyat yuritadi va yoshlar trenerlik faoliyatini davom ettiradi."
        ),
        "bio_ru": (
            "Тошпулатов Шамсиддин Рахимжонович родился 7 июля 1995 года в Ферганской области. "
            "Окончил магистратуру Государственной спортивной академии Узбекистана в 2021 году "
            "по специальности «Спортивный менеджмент». Победитель чемпионата мира по национальной "
            "борьбе «Кураш» в весовой категории до 90 кг. Многократный победитель чемпионатов "
            "Азии и Центральной Азии. В настоящее время работает советником по международным "
            "отношениям в Федерации кураша Узбекистана и продолжает тренерскую деятельность с молодёжью."
        ),
        "bio_en": (
            "Shamsiddin Rahimjonovich Toshpulatov was born on July 7, 1995, in Fergana Region. "
            "He completed his master's degree at the Uzbekistan State Sports Academy in 2021, "
            "specialising in sports management. He is a World Champion in national wrestling "
            "'Kurash' in the 90 kg weight category. He has won multiple Asian and Central Asian "
            "Championships. He currently works as an international relations consultant at the "
            "Uzbekistan Kurash Federation and continues coaching youth athletes."
        ),
        "achievement_uz": (
            "Kurash Jahon chempionati — Oltin medal (90 kg)\n"
            "Osiyo kurash chempionati — Oltin medal\n"
            "Markaziy Osiyo chempionati — Ko'p marta g'olib\n"
            "O'zbekiston chempioni (4 marta)\n"
            "\"Sportdagi xizmatlar uchun\" ko'krak nishoni"
        ),
        "achievement_ru": (
            "Чемпионат мира по кураш — Золотая медаль (90 кг)\n"
            "Чемпионат Азии по кураш — Золотая медаль\n"
            "Чемпионат Центральной Азии — Многократный победитель\n"
            "Чемпион Узбекистана (4 раза)\n"
            "Нагрудный знак «За заслуги в спорте»"
        ),
        "achievement_en": (
            "Kurash World Championship — Gold Medal (90 kg)\n"
            "Asian Kurash Championship — Gold Medal\n"
            "Central Asian Championship — Multiple winner\n"
            "Uzbekistan Champion (4 times)\n"
            "Badge 'For Services in Sports'"
        ),
    },
]


# ── FAXRLI-USTOZLAR ────────────────────────────────────────────────────────────

FAXRLI_USTOZLAR = [
    # ═══════════════════════════════════════════════════════════════════════════
    # 1. Prof. Hamid Normatov
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 1,
        "is_head": True,
        "full_name_uz": "Normatov Hamid Sobirjonovich",
        "full_name_ru": "Норматов Хамид Собиржонович",
        "full_name_en": "Hamid Sobirjonovich Normatov",
        "title_uz": "Faxrli ustoz, jismoniy tarbiya pedagogikasi bo'yicha professor",
        "title_ru": "Почётный преподаватель, профессор педагогики физической культуры",
        "title_en": "Honorary Teacher, Professor of Physical Education Pedagogy",
        "position_uz": "Pedagogika fanlari doktori, professor",
        "position_ru": "Доктор педагогических наук, профессор",
        "position_en": "Doctor of Pedagogical Sciences, Professor",
        "phone": "+998 71 200 01 10",
        "email": "normatov@usas.uz",
        "reception": "Seshanba, 10:00–12:00",
        "address": "Toshkent shahri, Olimpiya shaharchasi",
        "bio_uz": (
            "Normatov Hamid Sobirjonovich 1955-yil 12-aprelda Namangan viloyatida tug'ilgan. "
            "1978-yilda O'zbekiston Davlat jismoniy tarbiya institutini tamomlagan, 1985-yilda "
            "pedagogika fanlari nomzodi, 1998-yilda pedagogika fanlari doktori ilmiy darajasini "
            "olgan. 40 yildan ortiq ilmiy va pedagogik faoliyat yuritgan. Jismoniy tarbiya "
            "pedagogikasi sohasida 150 dan ortiq ilmiy maqola, 12 ta darslik va o'quv qo'llanma "
            "muallifi. O'zbekistonda zamonaviy sport ta'limi metodologiyasini shakllantirgan "
            "ilmiy maktab asoschisi. 1995–2010 yillarda kafedra mudiri, 2010–2020 yillarda "
            "institutda ilmiy ishlar bo'yicha prorektor lavozimida ishlagan. "
            "O'zbekiston Faxriy o'qituvchisi, \"Mehnat shuhrati\" ordeni sohibi."
        ),
        "bio_ru": (
            "Норматов Хамид Собиржонович родился 12 апреля 1955 года в Наманганской области. "
            "В 1978 году окончил Узбекский государственный институт физической культуры, "
            "в 1985 году получил степень кандидата педагогических наук, в 1998 году — "
            "доктора педагогических наук. Ведёт научную и педагогическую деятельность более "
            "40 лет. Является автором более 150 научных статей, 12 учебников и учебных пособий "
            "в области педагогики физической культуры. Основатель научной школы, сформировавшей "
            "методологию современного спортивного образования в Узбекистане. В 1995–2010 годах "
            "занимал должность заведующего кафедрой, в 2010–2020 годах — проректора по научной "
            "работе в институте. Заслуженный учитель Узбекистана, кавалер ордена «Мехнат шухрати»."
        ),
        "bio_en": (
            "Hamid Sobirjonovich Normatov was born on April 12, 1955, in Namangan Region. "
            "He graduated from the Uzbekistan State Institute of Physical Culture in 1978, "
            "received his Candidate of Pedagogical Sciences degree in 1985, and his Doctor of "
            "Pedagogical Sciences degree in 1998. He has been engaged in scientific and pedagogical "
            "activities for more than 40 years. He is the author of over 150 scientific articles, "
            "12 textbooks, and educational manuals in the field of physical education pedagogy. "
            "He is the founder of a scientific school that shaped the methodology of modern sports "
            "education in Uzbekistan. From 1995 to 2010, he served as head of department, and "
            "from 2010 to 2020, as Vice-Rector for Research at the institute. "
            "He is an Honored Teacher of Uzbekistan and holder of the 'Mehnat shuhrati' Order."
        ),
        "activity_uz": (
            "Jismoniy tarbiya pedagogikasi\nSport psixologiyasi\nOliy ta'lim metodologiyasi\n"
            "Yoshlar sport ta'limi tizimi\nMualliflik 150+ ilmiy maqola, 12 darslik"
        ),
        "activity_ru": (
            "Педагогика физической культуры\nСпортивная психология\nМетодология высшего образования\n"
            "Система спортивного образования молодёжи\nАвтор 150+ научных статей, 12 учебников"
        ),
        "activity_en": (
            "Physical Education Pedagogy\nSports Psychology\nHigher Education Methodology\n"
            "Youth Sports Education System\nAuthor of 150+ scientific articles, 12 textbooks"
        ),
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # 2. Prof. Muazzam Xasanova
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 2,
        "is_head": False,
        "full_name_uz": "Xasanova Muazzam Ibrohimovna",
        "full_name_ru": "Хасанова Муаззам Ибрахимовна",
        "full_name_en": "Muazzam Ibrohimovna Xasanova",
        "title_uz": "Faxrli ustoz, sport psixologiyasi bo'yicha professor",
        "title_ru": "Почётный преподаватель, профессор по спортивной психологии",
        "title_en": "Honorary Teacher, Professor of Sports Psychology",
        "position_uz": "Psixologiya fanlari doktori, professor",
        "position_ru": "Доктор психологических наук, профессор",
        "position_en": "Doctor of Psychological Sciences, Professor",
        "phone": "+998 71 200 01 11",
        "email": "xasanova@usas.uz",
        "reception": "Chorshanba, 14:00–16:00",
        "address": "Toshkent shahri, Olimpiya shaharchasi",
        "bio_uz": (
            "Xasanova Muazzam Ibrohimovna 1960-yil 3-martda Toshkent shahrida tug'ilgan. "
            "1983-yilda Toshkent davlat pedagogika institutini, 1990-yilda aspiranturani tamomlagan. "
            "1992-yilda psixologiya fanlari nomzodi, 2005-yilda psixologiya fanlari doktori "
            "ilmiy darajasini olgan. O'zbekistonda sport psixologiyasini fan sifatida "
            "rivojlantirgan birinchi tadqiqotchilardan biri. Olimpiya va professional sportchilar "
            "uchun psixologik tayyorgarlik metodikasi bo'yicha ilmiy ishlar olib borgan. "
            "35 yildan ortiq O'zbekiston sport akademiyasida pedagoglik qilgan. "
            "Xalqaro sport psixologiya assotsiatsiyasining a'zosi, \"Xalq ta'limi a'lochisi\" "
            "ko'krak nishoni sohibi."
        ),
        "bio_ru": (
            "Хасанова Муаззам Ибрахимовна родилась 3 марта 1960 года в Ташкенте. "
            "В 1983 году окончила Ташкентский государственный педагогический институт, "
            "в 1990 году — аспирантуру. В 1992 году получила степень кандидата психологических "
            "наук, в 2005 году — доктора психологических наук. "
            "Является одной из первых исследователей, развивших спортивную психологию как науку "
            "в Узбекистане. Провела научные исследования по методике психологической подготовки "
            "для олимпийских и профессиональных спортсменов. Преподавала в спортивной академии "
            "Узбекистана более 35 лет. Член Международной ассоциации спортивной психологии, "
            "обладательница нагрудного знака «Отличник народного образования»."
        ),
        "bio_en": (
            "Muazzam Ibrohimovna Xasanova was born on March 3, 1960, in Tashkent. "
            "She graduated from Tashkent State Pedagogical Institute in 1983 and completed her "
            "postgraduate studies in 1990. She received her Candidate of Psychological Sciences "
            "degree in 1992 and her Doctor of Psychological Sciences degree in 2005. "
            "She is one of the first researchers to develop sports psychology as a scientific "
            "discipline in Uzbekistan. She has conducted research on psychological preparation "
            "methodology for Olympic and professional athletes. She taught at the Uzbekistan "
            "Sports Academy for more than 35 years. She is a member of the International Society "
            "of Sport Psychology and holder of the 'Excellence in Public Education' badge."
        ),
        "activity_uz": (
            "Sport psixologiyasi\nOlimpiya sportchilar psixologik tayyorgarligi\n"
            "Kognitiv psixologiya va sport\n80+ ilmiy maqola, 5 monografiya\n"
            "Xalqaro konferensiyalar ishtirokchisi"
        ),
        "activity_ru": (
            "Спортивная психология\nПсихологическая подготовка олимпийских спортсменов\n"
            "Когнитивная психология и спорт\n80+ научных статей, 5 монографий\n"
            "Участница международных конференций"
        ),
        "activity_en": (
            "Sports Psychology\nPsychological preparation of Olympic athletes\n"
            "Cognitive psychology and sport\n80+ scientific articles, 5 monographs\n"
            "Participant of international conferences"
        ),
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # 3. Prof. Baxtiyor Tursunov
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 3,
        "is_head": False,
        "full_name_uz": "Tursunov Baxtiyor Alimjonovich",
        "full_name_ru": "Турсунов Бахтиёр Алимжонович",
        "full_name_en": "Baxtiyor Alimjonovich Tursunov",
        "title_uz": "Faxrli ustoz, sport tibbiyoti bo'yicha professor",
        "title_ru": "Почётный преподаватель, профессор спортивной медицины",
        "title_en": "Honorary Teacher, Professor of Sports Medicine",
        "position_uz": "Tibbiyot fanlari doktori, professor, akademik",
        "position_ru": "Доктор медицинских наук, профессор, академик",
        "position_en": "Doctor of Medical Sciences, Professor, Academician",
        "phone": "+998 71 200 01 12",
        "email": "tursunov.b@usas.uz",
        "reception": "Juma, 11:00–13:00",
        "address": "Toshkent shahri, Olimpiya shaharchasi",
        "bio_uz": (
            "Tursunov Baxtiyor Alimjonovich 1952-yil 18-noyabrda Samarqand shahrida tug'ilgan. "
            "1976-yilda Toshkent davlat tibbiyot institutini tamomlagan. 1981-yilda tibbiyot "
            "fanlari nomzodi, 2000-yilda tibbiyot fanlari doktori ilmiy darajasini olgan. "
            "O'zbekiston Tibbiyot fanlari akademiyasining haqiqiy a'zosi (akademik). "
            "Sport tibbiyoti va sportchi reabilitatsiyasi sohasida 50 yillik tajribaga ega. "
            "Olimpiya terma jamoalarining bosh shifokorlari orasida 1988–2008 yillarda ishlagan. "
            "200 dan ortiq ilmiy asarlar, 7 patent, 8 monografiya muallifi. "
            "O'zbekistonda sport tibbiyoti yo'nalishini asoslagan olimlardan biri. "
            "\"O'zbekiston Respublikasida xizmat ko'rsatgan shifokor\" unvoni sohibi."
        ),
        "bio_ru": (
            "Турсунов Бахтиёр Алимжонович родился 18 ноября 1952 года в Самарканде. "
            "В 1976 году окончил Ташкентский государственный медицинский институт. "
            "В 1981 году получил степень кандидата медицинских наук, в 2000 году — "
            "доктора медицинских наук. Является действительным членом (академиком) "
            "Академии медицинских наук Узбекистана. Имеет 50-летний опыт в области "
            "спортивной медицины и реабилитации спортсменов. С 1988 по 2008 год работал "
            "главным врачом олимпийских сборных команд. Автор более 200 научных работ, "
            "7 патентов и 8 монографий. Является одним из учёных, основавших направление "
            "спортивной медицины в Узбекистане. Удостоен звания «Заслуженный врач "
            "Республики Узбекистан»."
        ),
        "bio_en": (
            "Baxtiyor Alimjonovich Tursunov was born on November 18, 1952, in Samarkand. "
            "He graduated from Tashkent State Medical Institute in 1976. "
            "He received his Candidate of Medical Sciences degree in 1981 and his Doctor of "
            "Medical Sciences degree in 2000. He is a Full Member (Academician) of the Academy "
            "of Medical Sciences of Uzbekistan. He has 50 years of experience in sports medicine "
            "and athlete rehabilitation. From 1988 to 2008, he served as the chief physician of "
            "Uzbekistan's Olympic national teams. He is the author of over 200 scientific works, "
            "7 patents, and 8 monographs. He is one of the scientists who founded the field of "
            "sports medicine in Uzbekistan. He holds the title of 'Honored Doctor of the "
            "Republic of Uzbekistan'."
        ),
        "activity_uz": (
            "Sport tibbiyoti va reabilitatsiya\nOlimpiya sportchilari tibbiy ta'minoti\n"
            "Jismoniy yuklamalar fiziologiyasi\n200+ ilmiy asar, 7 patent, 8 monografiya\n"
            "O'zbekiston Tibbiyot fanlari akademiyasi akademigi"
        ),
        "activity_ru": (
            "Спортивная медицина и реабилитация\nМедицинское обеспечение олимпийских спортсменов\n"
            "Физиология физических нагрузок\n200+ научных работ, 7 патентов, 8 монографий\n"
            "Академик Академии медицинских наук Узбекистана"
        ),
        "activity_en": (
            "Sports Medicine and Rehabilitation\nMedical support of Olympic athletes\n"
            "Physiology of physical loads\n200+ scientific works, 7 patents, 8 monographs\n"
            "Academician of the Academy of Medical Sciences of Uzbekistan"
        ),
    },
    # ═══════════════════════════════════════════════════════════════════════════
    # 4. Prof. Aziz Karimov
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "order": 4,
        "is_head": False,
        "full_name_uz": "Karimov Aziz Xolmatovich",
        "full_name_ru": "Каримов Азиз Холматович",
        "full_name_en": "Aziz Xolmatovich Karimov",
        "title_uz": "Faxrli ustoz, yengil atletika bo'yicha O'zbekistonning xizmat ko'rsatgan murabbiyi",
        "title_ru": "Почётный преподаватель, заслуженный тренер Узбекистана по лёгкой атлетике",
        "title_en": "Honorary Teacher, Honored Coach of Uzbekistan in Athletics",
        "position_uz": "Pedagogika fanlari nomzodi, dotsent",
        "position_ru": "Кандидат педагогических наук, доцент",
        "position_en": "Candidate of Pedagogical Sciences, Associate Professor",
        "phone": "+998 71 200 01 13",
        "email": "karimov.a@usas.uz",
        "reception": "Dushanba, 14:00–16:00",
        "address": "Toshkent shahri, Olimpiya shaharchasi",
        "bio_uz": (
            "Karimov Aziz Xolmatovich 1958-yil 25-avgustda Toshkent viloyatida tug'ilgan. "
            "1981-yilda O'zbekiston Davlat jismoniy tarbiya institutini tamomlagan, 1989-yilda "
            "pedagogika fanlari nomzodi ilmiy darajasini olgan. Yengil atletika, ayniqsa "
            "o'rta va uzun masofali yugurish bo'yicha mutaxassis. "
            "1985–2015 yillarda O'zbekiston terma jamoasining murabbiylar guruhi a'zosi sifatida "
            "Osiyo o'yinlari, Jahon chempionatlarida jamoani tayyorlagan. "
            "Tayyorlagan sportchilar orasida 6 ta Osiyo chempioni, 2 ta Olimpiada ishtirokchisi bor. "
            "30 yildan ortiq O'zbekiston sport akademiyasida pedagoglik faoliyatini olib borgan, "
            "yengil atletika nazariyasi va uslubiyati bo'yicha 60 dan ortiq ilmiy ish chop ettirgan. "
            "\"O'zbekiston Respublikasida xizmat ko'rsatgan murabbiyi\" unvoni sohibi."
        ),
        "bio_ru": (
            "Каримов Азиз Холматович родился 25 августа 1958 года в Ташкентской области. "
            "В 1981 году окончил Узбекский государственный институт физической культуры, "
            "в 1989 году получил степень кандидата педагогических наук. Специалист по лёгкой "
            "атлетике, особенно в беге на средние и длинные дистанции. С 1985 по 2015 год "
            "являлся членом тренерского штаба сборной Узбекистана, подготавливая команду к "
            "Азиатским играм и чемпионатам мира. Среди подготовленных им спортсменов — 6 "
            "чемпионов Азии и 2 участника Олимпийских игр. Более 30 лет преподавал в "
            "спортивной академии Узбекистана, опубликовал более 60 научных работ по теории "
            "и методике лёгкой атлетики. Удостоен звания «Заслуженный тренер Республики Узбекистан»."
        ),
        "bio_en": (
            "Aziz Xolmatovich Karimov was born on August 25, 1958, in Tashkent Region. "
            "He graduated from the Uzbekistan State Institute of Physical Culture in 1981 and "
            "received his Candidate of Pedagogical Sciences degree in 1989. He is a specialist "
            "in athletics, especially middle and long-distance running. From 1985 to 2015, "
            "he was a member of the coaching staff of the Uzbekistan national team, preparing "
            "the team for the Asian Games and World Championships. Among the athletes he trained "
            "are 6 Asian champions and 2 Olympic participants. He taught at the Uzbekistan Sports "
            "Academy for over 30 years and published more than 60 scientific works on the theory "
            "and methodology of athletics. He holds the title of 'Honored Coach of the Republic "
            "of Uzbekistan'."
        ),
        "activity_uz": (
            "Yengil atletika nazariyasi va uslubiyati\nO'rta va uzun masofali yugurish texnikasi\n"
            "Murabbiylik metodologiyasi\n60+ ilmiy maqola\n"
            "6 ta Osiyo chempioni, 2 ta Olimpiada ishtirokchisi tayyorlagan"
        ),
        "activity_ru": (
            "Теория и методика лёгкой атлетики\nТехника бега на средние и длинные дистанции\n"
            "Методология тренерской деятельности\n60+ научных статей\n"
            "Подготовил 6 чемпионов Азии и 2 участников Олимпийских игр"
        ),
        "activity_en": (
            "Theory and Methodology of Athletics\nMiddle and long-distance running techniques\n"
            "Coaching methodology\n60+ scientific articles\n"
            "Trained 6 Asian champions and 2 Olympic participants"
        ),
    },
]


# ── Management command ─────────────────────────────────────────────────────────

class Command(BaseCommand):
    help = "Bitiruvchilar va Faxrli-ustozlar kategoriyalari va shaxslarini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Eski ma'lumotlarni o'chirib qayta yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            for slug in ('bitiruvchilar', 'faxrli-ustozlar'):
                qs = Person.objects.filter(category__slug=slug)
                for p in qs:
                    p.tabs.all().delete()
                qs.delete()
                PersonCategory.objects.filter(slug=slug).delete()
            self.stdout.write(self.style.WARNING("Eski ma'lumotlar o'chirildi."))

        # ── Taglar ─────────────────────────────────────────────────────────────
        tag_map = {}
        for slug, name_uz, name_ru, name_en in TAGS:
            tag, _ = Tag.objects.update_or_create(
                slug=slug,
                defaults={'name_uz': name_uz, 'name_ru': name_ru, 'name_en': name_en},
            )
            tag_map[slug] = tag

        bio_tag        = tag_map['biografiya']
        achievement_tag = tag_map['yutuqlar']
        activity_tag   = tag_map['faoliyat']

        # ── Bitiruvchilar ──────────────────────────────────────────────────────
        self._seed_category(
            slug='bitiruvchilar',
            title_uz='Bitiruvchilar', title_ru='Выпускники', title_en='Graduates',
            order=20,
            persons=BITIRUVCHILAR,
            bio_tag=bio_tag,
            second_tag=achievement_tag,
            second_key='achievement',
        )

        # ── Faxrli-ustozlar ────────────────────────────────────────────────────
        self._seed_category(
            slug='faxrli-ustozlar',
            title_uz='Faxrli ustozlar', title_ru='Почётные преподаватели', title_en='Honorary Teachers',
            order=21,
            persons=FAXRLI_USTOZLAR,
            bio_tag=bio_tag,
            second_tag=activity_tag,
            second_key='activity',
        )

        self.stdout.write(self.style.SUCCESS("Bitiruvchilar va faxrli-ustozlar muvaffaqiyatli saqlandi."))

    def _seed_category(self, slug, title_uz, title_ru, title_en, order, persons, bio_tag, second_tag, second_key):
        category, created = PersonCategory.objects.update_or_create(
            slug=slug,
            defaults={
                'title_uz': title_uz, 'title_ru': title_ru, 'title_en': title_en,
                'order': order,
            },
        )
        self.stdout.write(f"\n  [{'+' if created else '~'}] Kategoriya: {title_uz}")

        for data in persons:
            person, is_new = Person.objects.update_or_create(
                full_name_uz=data['full_name_uz'],
                category=category,
                defaults={
                    'full_name_ru':  data['full_name_ru'],
                    'full_name_en':  data['full_name_en'],
                    'title_uz':      data['title_uz'],
                    'title_ru':      data['title_ru'],
                    'title_en':      data['title_en'],
                    'position_uz':   data['position_uz'],
                    'position_ru':   data['position_ru'],
                    'position_en':   data['position_en'],
                    'phone':         data.get('phone', ''),
                    'email':         data.get('email', ''),
                    'address':       data.get('address', ''),
                    'reception':     data.get('reception', ''),
                    'is_head':       data['is_head'],
                    'is_active':     True,
                    'order':         data['order'],
                },
            )

            # Tab 1 — Biografiya
            tab1, _ = PersonContent.objects.update_or_create(
                person=person, order=1,
                defaults={
                    'content_uz': data['bio_uz'],
                    'content_ru': data['bio_ru'],
                    'content_en': data['bio_en'],
                },
            )
            if not tab1.tags.filter(pk=bio_tag.pk).exists():
                tab1.tags.add(bio_tag)

            # Tab 2 — Yutuqlar yoki Ilmiy faoliyat
            uz_key = f"{second_key}_uz"
            tab2, _ = PersonContent.objects.update_or_create(
                person=person, order=2,
                defaults={
                    'content_uz': data.get(uz_key, ''),
                    'content_ru': data.get(f"{second_key}_ru", ''),
                    'content_en': data.get(f"{second_key}_en", ''),
                },
            )
            if not tab2.tags.filter(pk=second_tag.pk).exists():
                tab2.tags.add(second_tag)

            self.stdout.write(f"    {'[+]' if is_new else '[~]'} {data['full_name_uz']}")
