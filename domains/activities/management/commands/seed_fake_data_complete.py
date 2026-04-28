"""
python manage.py seed_fake_data_complete

Mavjud IlmiyFaoliyat itemlariga to'liq fake data qo'shadi:
  - description_ru, description_en
  - image (picsum.photos dan fake rasm URL)
  - file (namunali PDF URL)
"""

from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

# Har bir item uchun to'liq ma'lumot
# kalit = (category_slug, order)
ITEM_DATA = {

    # ──────────────────────────────── SPORT FAOLIYAT ────────────────────────────────

    ("sport-faoliyati", 1): {
        "title_ru":        "План спортивных мероприятий 2025 года",
        "title_en":        "Sports Events Plan 2025",
        "description_uz":  "Akademiyada o'tkaziladigan sport tadbirlarining to'liq yillik rejasi. Barcha bo'limlar va musobaqalar shu rejaga asoslanadi.",
        "description_ru":  "Полный годовой план спортивных мероприятий, проводимых в академии. Все секции и соревнования основаны на этом плане.",
        "description_en":  "Complete annual plan of sports events held at the academy. All sections and competitions are based on this plan.",
        "image": "https://picsum.photos/seed/sport-plan-2025/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("sport-faoliyati", 2): {
        "title_ru":        "Методическое пособие по физической культуре",
        "title_en":        "Physical Education Methodological Guide",
        "description_uz":  "Talabalar uchun jismoniy tarbiya darslarini samarali tashkil qilish bo'yicha uslubiy ko'rsatmalar va mashqlar to'plami.",
        "description_ru":  "Методические указания и комплекс упражнений для эффективной организации занятий физической культурой для студентов.",
        "description_en":  "Methodological guidelines and a set of exercises for effective organization of physical education classes for students.",
        "image": "https://picsum.photos/seed/sport-method/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("sport-faoliyati", 3): {
        "title_ru":        "Результаты спортивных соревнований 2025",
        "title_en":        "Sports Competition Results 2025",
        "description_uz":  "2025-yilgi barcha ichki va respublika miqyosidagi sport musobaqalarining yakuniy natijalari va g'oliblar ro'yxati.",
        "description_ru":  "Итоговые результаты и список победителей всех внутренних и республиканских спортивных соревнований 2025 года.",
        "description_en":  "Final results and list of winners of all internal and republican sports competitions of 2025.",
        "image": "https://picsum.photos/seed/sport-results/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },

    ("sport-klublari-hayoti", 1): {
        "title_ru":        "Отчёт о деятельности футбольного клуба",
        "title_en":        "Football Club Activity Report",
        "description_uz":  "Akademiya futbol jamoasining 2025-yilgi barcha o'yinlari, trenirovkalar jadvali va g'alaba-mag'lubiyat statistikasi.",
        "description_ru":  "Все игры, расписание тренировок и статистика побед и поражений футбольной команды академии за 2025 год.",
        "description_en":  "All games, training schedule and win-loss statistics of the academy football team for 2025.",
        "image": "https://picsum.photos/seed/football-club/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("sport-klublari-hayoti", 2): {
        "title_ru":        "Клубы борьбы и дзюдо",
        "title_en":        "Wrestling and Judo Clubs",
        "description_uz":  "Akademiyadagi kurash va judo sport klublari: a'zolar soni, trenirovka jadvali, musobaqalardagi yutuqlar.",
        "description_ru":  "Клубы борьбы и дзюдо в академии: количество участников, расписание тренировок, достижения в соревнованиях.",
        "description_en":  "Wrestling and judo clubs at the academy: membership count, training schedule, competition achievements.",
        "image": "https://picsum.photos/seed/kurash-judo/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("sport-klublari-hayoti", 3): {
        "title_ru":        "Соревнования по плаванию",
        "title_en":        "Swimming Competitions",
        "description_uz":  "Suzish bo'yicha o'tkazilgan ichki musobaqalar, ishtirokchilar ro'yxati va protokollar.",
        "description_ru":  "Внутренние соревнования по плаванию, список участников и протоколы.",
        "description_en":  "Internal swimming competitions, participant list and protocols.",
        "image": "https://picsum.photos/seed/swimming/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("sport-klublari-hayoti", 4): {
        "title_ru":        "Велосипедный спортивный клуб",
        "title_en":        "Cycling Sports Club",
        "description_uz":  "Velosiped sport klubi faoliyati, yo'nalishlari, musobaqa taqvimi va klub a'zolari haqida ma'lumot.",
        "description_ru":  "Деятельность велосипедного спортивного клуба, направления, календарь соревнований и информация об участниках.",
        "description_en":  "Cycling sports club activities, directions, competition calendar and information about members.",
        "image": "https://picsum.photos/seed/cycling/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },

    ("ekologik-faol-talabalar", 1): {
        "title_ru":        "Зелёная спортивная инициатива 2025",
        "title_en":        "Green Sports Initiative 2025",
        "description_uz":  "Talabalar tomonidan tashkil etilgan ekologik tozalikka bag'ishlangan yashil sport tadbirlari va ularga qo'shilish tartibi.",
        "description_ru":  "Зелёные спортивные мероприятия, посвящённые экологической чистоте, организованные студентами, и порядок участия.",
        "description_en":  "Green sports events dedicated to environmental cleanliness organized by students and the process of joining them.",
        "image": "https://picsum.photos/seed/green-sport/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("ekologik-faol-talabalar", 2): {
        "title_ru":        "Проект озеленения",
        "title_en":        "Greening Project",
        "description_uz":  "Akademiya hududini ko'kalamzorlashtirish bo'yicha talabalar loyihasi: o'simliklar ro'yxati, ish jadvali va hisobot.",
        "description_ru":  "Студенческий проект по озеленению территории академии: список растений, график работ и отчёт.",
        "description_en":  "Student project for greening the academy territory: plant list, work schedule and report.",
        "image": "https://picsum.photos/seed/greening/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },

    # ──────────────────────────────── ILMIY FAOLIYAT ────────────────────────────────

    ("ilmiy-loyihalar", 1): {
        "title_ru":        "Научный проект по спортивной биомеханике",
        "title_en":        "Scientific Project on Sports Biomechanics",
        "description_uz":  "Atletlar harakatini biomexanik tahlil qilish loyihasi. Yugurishda oyoq-qo'l harakati va muvozanat ko'rsatkichlari o'rganilmoqda.",
        "description_ru":  "Проект биомеханического анализа движений атлетов. Изучаются показатели движения конечностей и баланса при беге.",
        "description_en":  "A project for biomechanical analysis of athlete movements. Limb movement and balance indicators during running are being studied.",
        "image": "https://picsum.photos/seed/biomechanics/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("ilmiy-loyihalar", 2): {
        "title_ru":        "Исследование эффективности физического воспитания",
        "title_en":        "Research on Physical Education Effectiveness",
        "description_uz":  "Zamonaviy innovatsion usullar yordamida jismoniy tarbiya darslarining samaradorligini o'lchash va takomillashtirish tadqiqoti.",
        "description_ru":  "Исследование измерения и совершенствования эффективности уроков физкультуры с помощью современных инновационных методов.",
        "description_en":  "Research on measuring and improving the effectiveness of physical education classes using modern innovative methods.",
        "image": "https://picsum.photos/seed/pe-research/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("ilmiy-loyihalar", 3): {
        "title_ru":        "Исследование спортивной психологии",
        "title_en":        "Sports Psychology Research",
        "description_uz":  "Musobaqa paytida sportchilar psixologik holatini baholash va ruhiy chidamlilikni oshirish usullarini ishlab chiqish.",
        "description_ru":  "Оценка психологического состояния спортсменов во время соревнований и разработка методов повышения психологической устойчивости.",
        "description_en":  "Assessing the psychological state of athletes during competition and developing methods to increase mental resilience.",
        "image": "https://picsum.photos/seed/sport-psych/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("ilmiy-loyihalar", 4): {
        "title_ru":        "Связь питания и спортивных результатов",
        "title_en":        "Nutrition and Sports Performance Correlation",
        "description_uz":  "Sportchi kundalik ovqatlanish tarkibi va sport natijalari o'rtasidagi ilmiy bog'liqlikni aniqlash maqsadidagi kuzatuv tadqiqoti.",
        "description_ru":  "Наблюдательное исследование, направленное на установление научной связи между ежедневным рационом спортсмена и спортивными результатами.",
        "description_en":  "Observational research aimed at determining the scientific relationship between an athlete's daily diet and sports performance.",
        "image": "https://picsum.photos/seed/nutrition-sport/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },

    ("doktorantura", 1): {
        "title_ru":        "Порядок приёма в докторантуру DSc",
        "title_en":        "DSc Doctoral Admission Procedure",
        "description_uz":  "DSc darajasiga da'vogar bo'lish uchun zarur hujjatlar, qabul bosqichlari, imtihon turlari va muddatlar haqida to'liq qo'llanma.",
        "description_ru":  "Полное руководство о необходимых документах, этапах поступления, видах экзаменов и сроках для поступления на степень DSc.",
        "description_en":  "Complete guide on required documents, admission stages, exam types and deadlines for enrolling in a DSc degree program.",
        "image": "https://picsum.photos/seed/dsc-admission/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("doktorantura", 2): {
        "title_ru":        "Направления докторантуры PhD",
        "title_en":        "PhD Doctoral Directions",
        "description_uz":  "Akademiyada mavjud PhD ixtisosliklari, har bir yo'nalish bo'yicha ilmiy rahbarlar va qabul kvotalari.",
        "description_ru":  "Доступные специальности PhD в академии, научные руководители по каждому направлению и квоты приёма.",
        "description_en":  "Available PhD specialties at the academy, scientific supervisors for each direction and admission quotas.",
        "image": "https://picsum.photos/seed/phd-directions/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("doktorantura", 3): {
        "title_ru":        "Руководство по написанию диссертации",
        "title_en":        "Dissertation Writing Guide",
        "description_uz":  "Dissertatsiya tuzilishi, har bir bob hajmi, adabiyotlar ro'yxatini rasmiylashtirish va mudofaa jarayonini tavsiflovchi qo'llanma.",
        "description_ru":  "Руководство, описывающее структуру диссертации, объём каждой главы, оформление списка литературы и процесс защиты.",
        "description_en":  "A guide describing dissertation structure, volume of each chapter, formatting of the bibliography and the defence process.",
        "image": "https://picsum.photos/seed/dissertation/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("doktorantura", 4): {
        "title_ru":        "Критерии выбора научного руководителя",
        "title_en":        "Scientific Supervisor Selection Criteria",
        "description_uz":  "Ilmiy rahbar tanlashda e'tiborga olish kerak bo'lgan ilmiy unvon, tajriba va mutaxassislik yo'nalishi bo'yicha mezonlar.",
        "description_ru":  "Критерии по научному званию, опыту и специализации, которые необходимо учитывать при выборе научного руководителя.",
        "description_en":  "Criteria on academic title, experience and specialization to consider when selecting a scientific supervisor.",
        "image": "https://picsum.photos/seed/supervisor/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },

    ("ilmiy-konferensiyalar", 1): {
        "title_ru":        "Международная конференция по спортивным наукам 2025",
        "title_en":        "International Sports Sciences Conference 2025",
        "description_uz":  "2025-yil may oyida bo'lib o'tadigan xalqaro ilmiy konferensiya. Ishtirok etish tartibi, mavzular va tashkilot haqida ma'lumot.",
        "description_ru":  "Международная научная конференция в мае 2025 года. Информация о порядке участия, темах и организации.",
        "description_en":  "International scientific conference in May 2025. Information on the participation procedure, topics and organization.",
        "image": "https://picsum.photos/seed/conference-2025/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("ilmiy-konferensiyalar", 2): {
        "title_ru":        "Республиканский молодёжный научный форум",
        "title_en":        "Republican Youth Scientific Forum",
        "description_uz":  "Yosh olimlar va doktorantlar uchun mo'ljallangan respublika miqyosidagi ilmiy anjuman. Maqola taqdim etish qoidalari.",
        "description_ru":  "Республиканский научный форум для молодых учёных и докторантов. Правила подачи статей.",
        "description_en":  "Republican scientific forum for young scientists and doctoral students. Rules for submitting articles.",
        "image": "https://picsum.photos/seed/youth-forum/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("ilmiy-konferensiyalar", 3): {
        "title_ru":        "Симпозиум по инновациям в физическом воспитании",
        "title_en":        "Physical Education Innovations Symposium",
        "description_uz":  "Zamonaviy texnologiyalarni jismoniy tarbiyaga tatbiq etish bo'yicha mutaxassislar simpozium dasturi va spiker ro'yxati.",
        "description_ru":  "Программа симпозиума специалистов по применению современных технологий в физическом воспитании и список спикеров.",
        "description_en":  "Programme of the symposium of specialists on applying modern technologies in physical education and list of speakers.",
        "image": "https://picsum.photos/seed/symposium-pe/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },

    ("ilmiy-ishlar-va-innovatsiyalar", 1): {
        "title_ru":        "Сборник научных работ профессоров и преподавателей академии",
        "title_en":        "Academy Faculty Scientific Works Collection",
        "description_uz":  "2024–2025 yillarda chop etilgan ilmiy maqolalar, monografiyalar va tadqiqot natijalari to'plami.",
        "description_ru":  "Сборник научных статей, монографий и результатов исследований, опубликованных в 2024–2025 годах.",
        "description_en":  "Collection of scientific articles, monographs and research results published in 2024–2025.",
        "image": "https://picsum.photos/seed/sci-collection/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("ilmiy-ishlar-va-innovatsiyalar", 2): {
        "title_ru":        "Инновации в спортивных технологиях",
        "title_en":        "Sports Technology Innovation",
        "description_uz":  "Sensörlar, video tahlil va sun'iy intellektni sportchilar tayyorgarligiga joriy qilish bo'yicha ilmiy ishlar.",
        "description_ru":  "Научные работы по внедрению датчиков, видеоанализа и искусственного интеллекта в подготовку спортсменов.",
        "description_en":  "Scientific works on introducing sensors, video analysis and artificial intelligence into athlete preparation.",
        "image": "https://picsum.photos/seed/sport-tech/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("ilmiy-ishlar-va-innovatsiyalar", 3): {
        "title_ru":        "Платформа цифрового спортивного анализа",
        "title_en":        "Digital Sports Analysis Platform",
        "description_uz":  "Sportchilar ko'rsatkichlarini real vaqtda raqamli tahlil qiluvchi platforma: funksiyalar, foydalanish qo'llanmasi.",
        "description_ru":  "Платформа для цифрового анализа показателей спортсменов в реальном времени: функции, руководство пользователя.",
        "description_en":  "Platform for real-time digital analysis of athlete performance: features and user manual.",
        "image": "https://picsum.photos/seed/digital-platform/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("ilmiy-ishlar-va-innovatsiyalar", 4): {
        "title_ru":        "Список патентов и интеллектуальной собственности",
        "title_en":        "Patent and Intellectual Property List",
        "description_uz":  "Akademiya olimlari tomonidan 2020–2025-yillarda olingan patentlar va mualliflik guvohnomalari ro'yxati.",
        "description_ru":  "Список патентов и авторских свидетельств, полученных учёными академии в 2020–2025 годах.",
        "description_en":  "List of patents and copyright certificates obtained by academy scientists in 2020–2025.",
        "image": "https://picsum.photos/seed/patents/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },

    # ──────────────────────────────── MA'NAVIY FAOLIYAT ─────────────────────────────

    ("manaviyat-rukni", 1): {
        "title_ru":        "Программа национальных ценностей и духовности",
        "title_en":        "National Values and Spirituality Program",
        "description_uz":  "Talabalar qalbida milliy g'urur, vatanparvarlik va ma'naviy poklikni shakllantirishga qaratilgan yillik dastur.",
        "description_ru":  "Годовая программа, направленная на формирование национальной гордости, патриотизма и духовной чистоты у студентов.",
        "description_en":  "Annual programme aimed at forming national pride, patriotism and spiritual purity among students.",
        "image": "https://picsum.photos/seed/national-values/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("manaviyat-rukni", 2): {
        "title_ru":        "Методология духовно-нравственного воспитания",
        "title_en":        "Spiritual and Moral Education Methodology",
        "description_uz":  "Talabalar axloqiy tarbiyasida qo'llaniladigan pedagogik usullar, darslik materiallari va amaliy mashg'ulotlar to'plami.",
        "description_ru":  "Набор педагогических методов, учебных материалов и практических занятий, применяемых в нравственном воспитании студентов.",
        "description_en":  "Set of pedagogical methods, teaching materials and practical exercises used in the moral education of students.",
        "image": "https://picsum.photos/seed/moral-edu/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("manaviyat-rukni", 3): {
        "title_ru":        "План патриотических мероприятий 2025",
        "title_en":        "Patriotic Events Plan 2025",
        "description_uz":  "Mustaqillik kuni, Xotira va qadrlash kuni va boshqa milliy bayramlar munosabati bilan rejalashtirilgan tadbirlar.",
        "description_ru":  "Мероприятия, запланированные в связи с Днём независимости, Днём памяти и уважения и другими национальными праздниками.",
        "description_en":  "Events planned in connection with Independence Day, Day of Memory and Honour and other national holidays.",
        "image": "https://picsum.photos/seed/patriotic-2025/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("manaviyat-rukni", 4): {
        "title_ru":        "Руководство по работе с молодёжью",
        "title_en":        "Youth Engagement Guide",
        "description_uz":  "Yoshlar bilan ma'naviy ishlarni tashkil qilishda qo'llaniladigan samarali kommunikatsiya va motivatsiya usullari.",
        "description_ru":  "Эффективные методы коммуникации и мотивации, применяемые при организации духовной работы с молодёжью.",
        "description_en":  "Effective communication and motivation methods used in organising spiritual work with young people.",
        "image": "https://picsum.photos/seed/youth-guide/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
    ("manaviyat-rukni", 5): {
        "title_ru":        "Отчёт о духовных мероприятиях 2024",
        "title_en":        "Spiritual Events Report 2024",
        "description_uz":  "2024-yilda o'tkazilgan barcha ma'naviy-tarbiyaviy tadbirlar, ularda qatnashganlar soni va erishilgan natijalar hisoboti.",
        "description_ru":  "Отчёт обо всех духовно-воспитательных мероприятиях 2024 года, количестве участников и достигнутых результатах.",
        "description_en":  "Report on all spiritual and educational events of 2024, number of participants and results achieved.",
        "image": "https://picsum.photos/seed/spiritual-report/600/400",
        "file":  "https://www.w3.org/WAI/WCAG21/wcag21.pdf",
    },
}


class Command(BaseCommand):
    help = "Mavjud IlmiyFaoliyat itemlariga to'liq fake data (ru/en tavsif, rasm, fayl) qo'shadi"

    def handle(self, *args, **options):
        updated = 0
        skipped = 0

        for (cat_slug, order), data in ITEM_DATA.items():
            try:
                item = IlmiyFaoliyat.objects.get(
                    category__slug=cat_slug,
                    order=order,
                )
            except IlmiyFaoliyat.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"  [YO'Q] ({cat_slug}, order={order}) — topilmadi, o'tkazildi"
                ))
                skipped += 1
                continue

            item.title_ru        = data.get("title_ru", item.title_ru or '')
            item.title_en        = data.get("title_en", item.title_en or '')
            item.description_uz  = data.get("description_uz", item.description_uz or '')
            item.description_ru  = data.get("description_ru", '')
            item.description_en  = data.get("description_en", '')
            item.image.name      = data["image"]
            item.file.name       = data["file"]
            item.save(update_fields=[
                'title_ru', 'title_en',
                'description_uz', 'description_ru', 'description_en',
                'image', 'file',
            ])
            self.stdout.write(f"  [OK] {item.title_uz[:60]}")
            updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nYangilandi: {updated} ta | O'tkazildi: {skipped} ta"
        ))
