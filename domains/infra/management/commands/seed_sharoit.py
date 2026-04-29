"""
python manage.py seed_sharoit          # yaratadi / yangilaydi
python manage.py seed_sharoit --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.infra.models import Sharoit

SPORT = [
    {
        "title_uz": "Futbol maydoni",
        "title_ru": "Футбольное поле",
        "title_en": "Football Field",
        "description_uz": "Standart o'lchamdagi sun'iy qoplamali futbol maydoni. Talabalar va sport jamoalari uchun ochiq.",
        "description_ru": "Футбольное поле стандартного размера с искусственным покрытием.",
        "description_en": "Standard-size football field with artificial turf, open for students and sports teams.",
        "icon": "⚽", "order": 1,
    },
    {
        "title_uz": "Suzish havzasi",
        "title_ru": "Бассейн",
        "title_en": "Swimming Pool",
        "description_uz": "Olimpiya standartidagi 50 metrli suzish havzasi. Talabalar va sportchilar uchun muntazam mashg'ulotlar o'tkaziladi.",
        "description_ru": "50-метровый бассейн олимпийского стандарта для тренировок студентов и спортсменов.",
        "description_en": "Olympic-standard 50-metre swimming pool with regular training sessions for students and athletes.",
        "icon": "🏊", "order": 2,
    },
    {
        "title_uz": "Velosport majmuasi",
        "title_ru": "Велоспортивный комплекс",
        "title_en": "Cycling Complex",
        "description_uz": "Zamonaviy velosport treki va mashg'ulot bazasi. Velosiped sport turlari bo'yicha ixtisoslashtirilgan trenerlar rahbarligida mashg'ulotlar.",
        "description_ru": "Современный велотрек и тренировочная база с квалифицированными тренерами.",
        "description_en": "Modern cycling track and training facility with specialised coaches.",
        "icon": "🚴", "order": 3,
    },
    {
        "title_uz": "Sport o'yinlari majmuasi",
        "title_ru": "Комплекс спортивных игр",
        "title_en": "Sports Games Complex",
        "description_uz": "Basketbol, voleybol, stol tennisi va boshqa sport o'yinlari uchun zamonaviy zallar va maydonlar.",
        "description_ru": "Современные залы и площадки для баскетбола, волейбола, настольного тенниса и других спортивных игр.",
        "description_en": "Modern halls and courts for basketball, volleyball, table tennis and other sports games.",
        "icon": "🏀", "order": 4,
    },
    {
        "title_uz": "Yakkakurash sport turlari majmuasi",
        "title_ru": "Комплекс единоборств",
        "title_en": "Martial Arts Complex",
        "description_uz": "Judo, kurash, boks, karate va boshqa yakkakurash sport turlari uchun ixtisoslashtirilgan zallar. Tatami va zarur jihozlar bilan ta'minlangan.",
        "description_ru": "Специализированные залы для дзюдо, кураша, бокса, каратэ и других единоборств. Оснащены татами и необходимым инвентарём.",
        "description_en": "Specialised halls for judo, kurash, boxing, karate and other martial arts, equipped with tatami and necessary gear.",
        "icon": "🥋", "order": 5,
    },
    {
        "title_uz": "Trenajyor zal",
        "title_ru": "Тренажёрный зал",
        "title_en": "Fitness Gym",
        "description_uz": "Zamonaviy trenajyorlar bilan jihozlangan katta trenajyor zal. Kuch va kardio mashqlari uchun barcha sharoitlar mavjud.",
        "description_ru": "Большой тренажёрный зал с современным оборудованием для силовых и кардиотренировок.",
        "description_en": "Large gym equipped with modern machines for strength and cardio training.",
        "icon": "🏋️", "order": 6,
    },
    {
        "title_uz": "Respublika olimpiya va paralimpiya sport turlariga tayyorlash markazi",
        "title_ru": "Республиканский центр подготовки по олимпийским и паралимпийским видам спорта",
        "title_en": "Republican Centre for Olympic and Paralympic Sports Training",
        "description_uz": "Milliy terma jamoalar uchun yuqori darajali tayyorgarlik markazi. Zamonaviy sport bazasi va malakali mutaxassislar.",
        "description_ru": "Центр высококвалифицированной подготовки для национальных сборных команд.",
        "description_en": "High-level training centre for national teams with modern facilities and qualified specialists.",
        "icon": "🏅", "order": 7,
    },
    {
        "title_uz": "Suv sport turlari maktabi (Toshkent dengizi)",
        "title_ru": "Школа водных видов спорта (Ташкентское море)",
        "title_en": "Water Sports School (Tashkent Sea)",
        "description_uz": "Toshkent dengizi sohilida joylashgan suv sport turlari maktabi. Eshkak eshish, suzish va boshqa suv sport turlarini o'rgatish.",
        "description_ru": "Школа водных видов спорта на берегу Ташкентского водохранилища: гребля, плавание и другие дисциплины.",
        "description_en": "Water sports school on the shore of Tashkent Reservoir, covering rowing, swimming and other aquatic disciplines.",
        "icon": "🚣", "order": 8,
    },
    {
        "title_uz": "Gimnastika bo'yicha respublika ixtisoslashtirilgan olimpiya zahiralari bolalar-o'smirlar sport maktabi",
        "title_ru": "Республиканская специализированная ДЮСШ олимпийского резерва по гимнастике",
        "title_en": "Republican Specialised Youth Sports School of Olympic Reserve in Gymnastics",
        "description_uz": "Yosh gimnastlar uchun ixtisoslashtirilgan sport maktabi. Olimpiya zahirasini tayyorlash dasturi asosida ishlaydi.",
        "description_ru": "Специализированная спортивная школа для юных гимнастов по программе подготовки олимпийского резерва.",
        "description_en": "Specialised sports school for young gymnasts operating under the Olympic reserve preparation programme.",
        "icon": "🤸", "order": 9,
    },
]

TALIM = [
    {
        "title_uz": "Malakali professor-o'qituvchilar hamda trenerlar tarkibi",
        "title_ru": "Квалифицированный профессорско-преподавательский и тренерский состав",
        "title_en": "Qualified Teaching Staff and Coaching Personnel",
        "description_uz": "Yuqori malakali professor-o'qituvchilar va xalqaro tajribaga ega trenerlar jamoasi. Fan doktorlari, professorlar va xalqaro musobaqalar g'oliblari.",
        "description_ru": "Команда высококвалифицированных преподавателей и тренеров с международным опытом, докторов наук, профессоров и победителей международных соревнований.",
        "description_en": "Team of highly qualified teaching staff and coaches with international experience, including PhDs, professors and international competition winners.",
        "icon": "👨‍🏫", "order": 1,
    },
    {
        "title_uz": "Axborot resurs markazi",
        "title_ru": "Информационный ресурсный центр",
        "title_en": "Information Resource Centre",
        "description_uz": "Zamonaviy kutubxona va axborot markazi. Minglab ilmiy kitoblar, elektron bazalar va o'quv materiallari mavjud.",
        "description_ru": "Современная библиотека и информационный центр с тысячами научных книг, электронными базами данных и учебными материалами.",
        "description_en": "Modern library and information centre with thousands of academic books, electronic databases and study materials.",
        "icon": "📚", "order": 2,
    },
    {
        "title_uz": "Zamonaviy auditoriyalar",
        "title_ru": "Современные аудитории",
        "title_en": "Modern Classrooms",
        "description_uz": "Interaktiv doska, proyektor va zamonaviy o'quv jihozlari bilan ta'minlangan auditoriyalar. Qulay o'quv muhiti.",
        "description_ru": "Аудитории, оснащённые интерактивными досками, проекторами и современным учебным оборудованием.",
        "description_en": "Classrooms equipped with interactive whiteboards, projectors and modern teaching equipment.",
        "icon": "🎓", "order": 3,
    },
    {
        "title_uz": "Xorijiy tillarni o'rgatish markazi",
        "title_ru": "Центр обучения иностранным языкам",
        "title_en": "Foreign Language Learning Centre",
        "description_uz": "Ingliz, rus va boshqa xorijiy tillarni o'rgatish markazi. Zamonaviy til laboratoriyalari va malakali o'qituvchilar.",
        "description_ru": "Центр обучения английскому, русскому и другим иностранным языкам с современными языковыми лабораториями.",
        "description_en": "Centre for teaching English, Russian and other foreign languages with modern language labs and qualified teachers.",
        "icon": "🌐", "order": 4,
    },
    {
        "title_uz": "Laboratoriya xonasi",
        "title_ru": "Лабораторный кабинет",
        "title_en": "Laboratory Room",
        "description_uz": "Sport fiziologiyasi, biomexanika va sport tibbiyoti bo'yicha zamonaviy laboratoriyalar. Ilmiy tadqiqotlar va amaliy mashg'ulotlar uchun.",
        "description_ru": "Современные лаборатории по спортивной физиологии, биомеханике и спортивной медицине для научных исследований и практических занятий.",
        "description_en": "Modern laboratories for sports physiology, biomechanics and sports medicine, used for research and practical sessions.",
        "icon": "🔬", "order": 5,
    },
    {
        "title_uz": "Sport psixologiyasi xonasi",
        "title_ru": "Кабинет спортивной психологии",
        "title_en": "Sports Psychology Room",
        "description_uz": "Sportchilar va talabalar uchun psixologik yordam ko'rsatish xonasi. Malakali sport psixologlari bilan individual va guruh mashg'ulotlari.",
        "description_ru": "Кабинет психологической поддержки спортсменов и студентов с квалифицированными спортивными психологами.",
        "description_en": "Psychological support room for athletes and students with qualified sports psychologists for individual and group sessions.",
        "icon": "🧠", "order": 6,
    },
    {
        "title_uz": "Sportchi talabalar mehmonxonasi",
        "title_ru": "Общежитие для студентов-спортсменов",
        "title_en": "Student-Athlete Dormitory",
        "description_uz": "Qulay sharoitli talabalar turar joyi. Barcha zaruriy qulayliklar: Wi-Fi, laundry, dam olish xonalari va boshqalar.",
        "description_ru": "Комфортабельное общежитие для студентов-спортсменов со всеми удобствами: Wi-Fi, прачечная, комнаты отдыха и др.",
        "description_en": "Comfortable dormitory for student-athletes with all amenities including Wi-Fi, laundry and recreation rooms.",
        "icon": "🏠", "order": 7,
    },
    {
        "title_uz": "Sportchi talabalar oshxonasi",
        "title_ru": "Столовая для студентов-спортсменов",
        "title_en": "Student-Athlete Canteen",
        "description_uz": "Sportchilar ehtiyojlarini hisobga olgan holda tayyorlangan maxsus ovqatlanish dasturi. Sog'lom va to'liq ovqatlanish.",
        "description_ru": "Специальная программа питания с учётом потребностей спортсменов. Здоровое и полноценное питание.",
        "description_en": "Special nutrition programme tailored to athletes' needs, providing healthy and balanced meals.",
        "icon": "🍽️", "order": 8,
    },
    {
        "title_uz": "Sportchi talabalar uchun kun tartibi bo'yicha 5 mahol ovqatlanish (bir sutkada o'rtacha 9560 kkal)",
        "title_ru": "5-разовое питание по распорядку дня (в среднем 9560 ккал в сутки)",
        "title_en": "5-meal daily nutrition schedule (average 9,560 kcal per day)",
        "description_uz": "Har kuni 5 mahol tartibli ovqatlanish: nonushta, ikkinchi nonushta, tushlik, kechki ovqat va kechqurun. Sutkalik kaloriya miqdori o'rtacha 9560 kkal.",
        "description_ru": "Ежедневное 5-разовое питание по расписанию: завтрак, второй завтрак, обед, ужин и поздний ужин. Суточная калорийность в среднем 9560 ккал.",
        "description_en": "Daily 5-meal schedule: breakfast, second breakfast, lunch, dinner and evening meal. Average daily calorie intake of 9,560 kcal.",
        "icon": "🥗", "order": 9,
    },
]


class Command(BaseCommand):
    help = "Sharoit va imkoniyatlar (sport va ta'lim bo'limlari) ma'lumotlarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = Sharoit.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        self.stdout.write("\n--- SPORT INSHOOTLAR ---")
        s_created = s_updated = 0
        for d in SPORT:
            obj, is_new = Sharoit.objects.update_or_create(
                title_uz=d['title_uz'],
                category='sport',
                defaults={**d, 'category': 'sport'},
            )
            if is_new:
                s_created += 1
            else:
                s_updated += 1
            self.stdout.write(f"  [{'+'if is_new else '~'}] {obj.title_uz[:70].encode('ascii', 'replace').decode()}")

        self.stdout.write("\n--- TA'LIM SHAROITLARI ---")
        t_created = t_updated = 0
        for d in TALIM:
            obj, is_new = Sharoit.objects.update_or_create(
                title_uz=d['title_uz'],
                category='talim',
                defaults={**d, 'category': 'talim'},
            )
            if is_new:
                t_created += 1
            else:
                t_updated += 1
            self.stdout.write(f"  [{'+'if is_new else '~'}] {obj.title_uz[:70].encode('ascii', 'replace').decode()}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: Sport — {s_created} yangi, {s_updated} yangilandi | "
            f"Ta'lim — {t_created} yangi, {t_updated} yangilandi"
        ))
