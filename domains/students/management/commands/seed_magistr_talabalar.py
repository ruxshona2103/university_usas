from django.core.management.base import BaseCommand
from domains.students.models import MagistrTalaba, Person, PersonCategory


TALABALAR = [
    {
        "full_name": "Xolmatova Nozima",
        "photo_filename": "magistr_1.jpg",
        "specialty_code": "",
        "specialty_name_uz": "Magistratura ta'lim bosqichi",
        "specialty_name_ru": "Магистратура",
        "specialty_name_en": "Master's degree",
        "dissertation_topic_uz": (
            "Akademiyaning magistratura mutaxassisliklariga qabul qilingan talabalar uchun "
            "o'quv mashg'ulot jarayonlarini sifatli tashkil qilish va monitoringini olib borishga mas'ul"
        ),
        "dissertation_topic_ru": (
            "Ответственная за качественную организацию учебного процесса и мониторинг "
            "студентов магистратуры академии"
        ),
        "dissertation_topic_en": (
            "Responsible for quality organization of educational process and monitoring "
            "of master's degree students of the Academy"
        ),
        "year": "2025-2026",
        "order": 1,
    },
    {
        "full_name": "Maxamadsalieva Madinobonu Umidjon qizi",
        "photo_filename": "magistr_2.jpg",
        "specialty_code": "MSF 25-01",
        "specialty_name_uz": "Yakkakurash va suv sport turlari",
        "specialty_name_ru": "Единоборства и водные виды спорта",
        "specialty_name_en": "Martial arts and water sports",
        "dissertation_topic_uz": (
            "O'zbekiston davlat sport akademiyasi \"Yakkakurash va suv sport turlari\" kafedrasi "
            "MSF 25-01 guruh magistranti. Taekwondo WT sport turining Pumse yo'nalishi bo'yicha "
            "O'zbekiston chempioni va \"Sport ustasi\"."
        ),
        "dissertation_topic_ru": (
            "Магистрант группы MSF 25-01 кафедры \"Единоборства и водные виды спорта\" ГАСУ. "
            "Чемпион Узбекистана по Taekwondo WT (Pumse) и \"Мастер спорта\"."
        ),
        "dissertation_topic_en": (
            "Master's student of MSF 25-01 group, Martial arts and water sports department. "
            "Champion of Uzbekistan in Taekwondo WT (Pumse) and Master of Sports."
        ),
        "year": "2025-2026",
        "order": 2,
    },
    {
        "full_name": "Kaldarbekova Madinabonu Saydulla qizi",
        "photo_filename": "magistr_3.jpg",
        "specialty_code": "",
        "specialty_name_uz": "Sport menejment",
        "specialty_name_ru": "Спортивный менеджмент",
        "specialty_name_en": "Sports management",
        "dissertation_topic_uz": "Kaldarbekova Madinabonu Saydulla qizi — sport menejmenti yo'nalishi magistranti.",
        "dissertation_topic_ru": "Калдарбекова Мадинабону Сайдулла кизи — магистрант направления спортивного менеджмента.",
        "dissertation_topic_en": "Kaldarbekova Madinabonu — master's student in sports management.",
        "year": "2025-2026",
        "order": 3,
    },
    {
        "full_name": "Shodiyeva Kamola Said qizi",
        "photo_filename": "magistr_4.jpg",
        "specialty_code": "",
        "specialty_name_uz": "Sport faoliyati (dzyudo)",
        "specialty_name_ru": "Спортивная деятельность (дзюдо)",
        "specialty_name_en": "Sports activity (judo)",
        "dissertation_topic_uz": (
            "Shodiyeva Kamola Said qizi. Sport faoliyati — dzyudo. "
            "2 karra O'zbekiston chempioni, bir necha marotaba sovrindor. Sport ustasi."
        ),
        "dissertation_topic_ru": (
            "Шодиева Камола Саид кизи. Вид спорта — дзюдо. "
            "2-кратная чемпионка Узбекистана, многократный призёр. Мастер спорта."
        ),
        "dissertation_topic_en": (
            "Shodiyeva Kamola Said. Sports activity — judo. "
            "2-time champion of Uzbekistan, multiple medalist. Master of Sports."
        ),
        "year": "2025-2026",
        "order": 4,
    },
    {
        "full_name": "Isoyeva Nigina O'tkirovna",
        "photo_filename": "magistr_5.jpg",
        "specialty_code": "",
        "specialty_name_uz": "Adaptiv jismoniy tarbiya va sport",
        "specialty_name_ru": "Адаптивная физическая культура и спорт",
        "specialty_name_en": "Adaptive physical education and sports",
        "dissertation_topic_uz": (
            "Isoyeva Nigina O'tkirovna. O'zbekiston davlat sport akademiyasi Adaptiv jismoniy tarbiya "
            "va sport mutaxassisligi 1-bosqich magistranti. Yengil atletika bo'yicha Markaziy Osiyo, "
            "Xalqaro va ko'p karra O'zbekiston chempioni."
        ),
        "dissertation_topic_ru": (
            "Исоева Нигина Уткировна. Магистрант 1-й ступени специальности АФКиС ГАСУ. "
            "Чемпион Центральной Азии, международный и многократный чемпион Узбекистана по лёгкой атлетике."
        ),
        "dissertation_topic_en": (
            "Isoyeva Nigina. 1st year master's student in Adaptive physical education and sports. "
            "Champion of Central Asia, international and multiple champion of Uzbekistan in athletics."
        ),
        "year": "2025-2026",
        "order": 5,
    },
    {
        "full_name": "Eshnazarova Marjona Obid qizi",
        "photo_filename": "magistr_6.jpg",
        "specialty_code": "",
        "specialty_name_uz": "Sport faoliyati (dzyudo)",
        "specialty_name_ru": "Спортивная деятельность (дзюдо)",
        "specialty_name_en": "Sports activity (judo)",
        "dissertation_topic_uz": (
            "Eshnazarova Marjona Obid qizi. Sport faoliyati — dzyudo. "
            "O'zbekiston sport ustasi nomzodi."
        ),
        "dissertation_topic_ru": (
            "Эшназарова Маржона Обид кизи. Вид спорта — дзюдо. "
            "Кандидат в мастера спорта Узбекистана."
        ),
        "dissertation_topic_en": (
            "Eshnazarova Marjona. Sports activity — judo. "
            "Candidate Master of Sports of Uzbekistan."
        ),
        "year": "2025-2026",
        "order": 6,
    },
    {
        "full_name": "Ikromov Xikmatillo Akramjon o'g'li",
        "photo_filename": "magistr_7.jpg",
        "specialty_code": "",
        "specialty_name_uz": "Menejment: sport menejmenti",
        "specialty_name_ru": "Менеджмент: спортивный менеджмент",
        "specialty_name_en": "Management: sports management",
        "dissertation_topic_uz": (
            "Ikromov Xikmatillo Akramjon o'g'li. Yo'nalish: Menejment — sport menejmenti. "
            "Erishgan yutugi: IELTS 6."
        ),
        "dissertation_topic_ru": (
            "Икромов Хикматилло Акрамжон угли. Направление: Менеджмент — спортивный менеджмент. "
            "Достижение: IELTS 6."
        ),
        "dissertation_topic_en": (
            "Ikromov Xikmatillo. Direction: Management — sports management. "
            "Achievement: IELTS 6."
        ),
        "year": "2025-2026",
        "order": 7,
    },
    {
        "full_name": "Asqarova Sabina Shavkat qizi",
        "photo_filename": "magistr_8.jpg",
        "specialty_code": "",
        "specialty_name_uz": "Adaptiv jismoniy tarbiya va sport",
        "specialty_name_ru": "Адаптивная физическая культура и спорт",
        "specialty_name_en": "Adaptive physical education and sports",
        "dissertation_topic_uz": (
            "Asqarova Sabina Shavkat qizi. Adaptiv jismoniy tarbiya va sport mutaxassisligi. "
            "O'zbekiston sport ustasi nomzodi. Milliy kurash bo'yicha 1-razryad sohibi. "
            "Turk tili sertifikati sohibi."
        ),
        "dissertation_topic_ru": (
            "Аскарова Сабина Шавкат кизи. Специальность — АФКиС. "
            "Кандидат в мастера спорта Узбекистана. Первый разряд по национальной борьбе. "
            "Сертификат турецкого языка."
        ),
        "dissertation_topic_en": (
            "Asqarova Sabina. Specialty — Adaptive physical education and sports. "
            "Candidate Master of Sports of Uzbekistan. 1st grade in national wrestling. "
            "Turkish language certificate."
        ),
        "year": "2025-2026",
        "order": 8,
    },
    {
        "full_name": "Odilova Umida Uktamovna",
        "photo_filename": "magistr_9.jpg",
        "specialty_code": "",
        "specialty_name_uz": "Sport psixologiyasi",
        "specialty_name_ru": "Спортивная психология",
        "specialty_name_en": "Sports psychology",
        "dissertation_topic_uz": (
            "Odilova Umida Uktamovna. Sport psixologiyasi mutaxassisligi. "
            "Turk tili sertifikati sohibasi."
        ),
        "dissertation_topic_ru": (
            "Одилова Умида Уктамовна. Специальность — спортивная психология. "
            "Сертификат турецкого языка."
        ),
        "dissertation_topic_en": (
            "Odilova Umida. Specialty — sports psychology. "
            "Turkish language certificate holder."
        ),
        "year": "2025-2026",
        "order": 9,
    },
    {
        "full_name": "Guliyev Artur Marlenovich",
        "photo_filename": "magistr_10.jpg",
        "specialty_code": "M EE 25-01",
        "specialty_name_uz": "Sport faoliyati (eshkak eshish)",
        "specialty_name_ru": "Спортивная деятельность (гребля)",
        "specialty_name_en": "Sports activity (rowing)",
        "dissertation_topic_uz": (
            "Guliyev Artur Marlenovich. O'zbekiston davlat sport akademiyasi Sport faoliyati "
            "(eshkak eshish) M EE 25-01 guruh magistranti. Eshkak eshish sport turi bo'yicha "
            "O'zbekiston milliy terma jamoasi va \"Mard o'g'loni\" davlat mukofoti sohibi."
        ),
        "dissertation_topic_ru": (
            "Гулиев Артур Марленович. Магистрант группы M EE 25-01, специальность — гребля. "
            "Член национальной сборной Узбекистана по гребле, обладатель государственной награды \"Мард углони\"."
        ),
        "dissertation_topic_en": (
            "Guliyev Artur. Master's student M EE 25-01, sports activity (rowing). "
            "Member of Uzbekistan national rowing team, holder of state award \"Mard o'g'loni\"."
        ),
        "year": "2025-2026",
        "order": 10,
    },
    {
        "full_name": "Aymuratov Musa Tatlimurat uli",
        "photo_filename": "magistr_11.jpg",
        "specialty_code": "MMN 25-01",
        "specialty_name_uz": "Qilichbozlik sport turi",
        "specialty_name_ru": "Фехтование",
        "specialty_name_en": "Fencing",
        "dissertation_topic_uz": (
            "Aymuratov Musa Tatlimurat uli. O'zbekiston davlat sport akademiyasi "
            "\"Qilichbozlik sport turi\" kafedrasi MMN 25-01 guruh magistranti. "
            "Qilichbozlik sport turining xalqaro toifadagi sport ustasi, "
            "6 karra Osiyo chempioni va jahon chempionati sovrindori."
        ),
        "dissertation_topic_ru": (
            "Аймуратов Муса Татлимурат ули. Магистрант группы MMN 25-01 кафедры \"Фехтование\" ГАСУ. "
            "Мастер спорта международного класса по фехтованию, "
            "6-кратный чемпион Азии и призёр чемпионата мира."
        ),
        "dissertation_topic_en": (
            "Aymuratov Musa. Master's student MMN 25-01, fencing department. "
            "International Master of Sports in fencing, "
            "6-time Asian champion and World Championship medalist."
        ),
        "year": "2025-2026",
        "order": 11,
    },
]


class Command(BaseCommand):
    help = "Magistratura talabalari seed data"

    def handle(self, *args, **options):
        # Kategoriya topish yoki yaratish
        cat, _ = PersonCategory.objects.get_or_create(
            slug='magistratura-talabalari',
            defaults={
                'title_uz': 'Magistratura talabalari',
                'title_ru': 'Студенты магистратуры',
                'title_en': "Master's students",
                'order': 99,
            }
        )

        created_count = 0
        for i, data in enumerate(TALABALAR):
            # MagistrTalaba yozuvi yaratish
            obj, created = MagistrTalaba.objects.get_or_create(
                full_name=data['full_name'],
                year=data['year'],
                defaults={
                    'specialty_code':      data['specialty_code'],
                    'specialty_name_uz':   data['specialty_name_uz'],
                    'specialty_name_ru':   data['specialty_name_ru'],
                    'specialty_name_en':   data['specialty_name_en'],
                    'dissertation_topic_uz': data['dissertation_topic_uz'],
                    'dissertation_topic_ru': data['dissertation_topic_ru'],
                    'dissertation_topic_en': data['dissertation_topic_en'],
                    'order':               data['order'],
                    'is_active':           True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"  + {data['full_name']}")
            else:
                # mavjud bo'lsa yangilash
                for field in ['specialty_name_uz', 'specialty_name_ru', 'specialty_name_en',
                              'dissertation_topic_uz', 'dissertation_topic_ru', 'dissertation_topic_en',
                              'specialty_code', 'order']:
                    setattr(obj, field, data[field])
                obj.save()
                self.stdout.write(f"  ~ {data['full_name']} (yangilandi)")

        self.stdout.write(self.style.SUCCESS(
            f"\nJami: {len(TALABALAR)} ta talaba, {created_count} ta yangi qoshildi."
        ))
        for d in TALABALAR:
            self.stdout.write(f"  {d['order']}. {d['photo_filename']} - {d['full_name']}")
