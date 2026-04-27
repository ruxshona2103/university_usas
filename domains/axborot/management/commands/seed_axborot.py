"""
python manage.py seed_axborot          # yaratadi / yangilaydi
python manage.py seed_axborot --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand

from domains.axborot.models import AxborotSection, AxborotVazifa
from domains.students.models import Person, PersonCategory


# ── Bo'limlar va vazifalar ─────────────────────────────────────────────────────

SECTIONS = [
    {
        "number": 5,
        "order": 1,
        "title_uz": "Axborot xizmati vazifalari",
        "title_ru": "Задачи информационной службы",
        "title_en": "Tasks of the Information Service",
        "items": [
            {
                "order": 1,
                "body_uz": (
                    "Akademiya tomonidan jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta "
                    "tayyorlash va malakasini oshirish sohasida amalga oshirilayotgan faoliyat hamda "
                    "zamonaviy talablarga muvofiq belgilanadigan axborot siyosatini shakllantirish va "
                    "keng ommaga yetkazishda ishtirok etish."
                ),
                "body_ru": (
                    "Участие в формировании и доведении до широкой общественности информационной "
                    "политики, осуществляемой Академией в сфере переподготовки и повышения "
                    "квалификации специалистов в области физической культуры и спорта, определяемой "
                    "в соответствии с современными требованиями."
                ),
                "body_en": (
                    "Participating in shaping and communicating to the public the information policy "
                    "defined in line with modern requirements regarding the Academy's activities in "
                    "retraining and professional development of specialists in physical culture and sports."
                ),
            },
            {
                "order": 2,
                "body_uz": (
                    "Axborot siyosati sohasida zimmasiga yuklangan vazifalarni amalga oshirishda "
                    "vazirlikning matbuot xizmati, sport boshqarmalari, boshqa davlat va xo'jalik "
                    "boshqaruvi organlarining axborot xizmatlari, sport turlari bo'yicha federatsiyalar "
                    "(uyushma) va boshqa tashkilotlar bilan samarali amaliy hamkorlikni yo'lga qo'yish."
                ),
                "body_ru": (
                    "Налаживание эффективного практического сотрудничества с пресс-службой "
                    "министерства, управлениями спорта, информационными службами других органов "
                    "государственного и хозяйственного управления, федерациями (ассоциациями) по "
                    "видам спорта и иными организациями при выполнении возложенных задач в сфере "
                    "информационной политики."
                ),
                "body_en": (
                    "Establishing effective practical cooperation with the ministry's press service, "
                    "sports departments, information services of other state and economic management "
                    "bodies, sports federations (associations), and other organizations in fulfilling "
                    "assigned tasks in the field of information policy."
                ),
            },
            {
                "order": 3,
                "body_uz": (
                    "Keng jamoatchilikni Akademiyaning faoliyati, uning sohaga doir normativ-huquqiy "
                    "hujjatlari to'g'risida xolisona, sifatli va tezkorlik bilan xabardor qilish."
                ),
                "body_ru": (
                    "Объективное, качественное и оперативное информирование широкой общественности "
                    "о деятельности Академии и её нормативно-правовых документах в данной сфере."
                ),
                "body_en": (
                    "Providing objective, high-quality, and timely information to the general public "
                    "about the Academy's activities and its regulatory documents in the field."
                ),
            },
            {
                "order": 4,
                "body_uz": (
                    "Muntazam ravishda ommaviy axborot vositalarida Akademiya rahbariyatining "
                    "chiqishlarini tashkil etish."
                ),
                "body_ru": (
                    "Регулярная организация выступлений руководства Академии в средствах "
                    "массовой информации."
                ),
                "body_en": (
                    "Regularly organizing appearances of the Academy's leadership in the mass media."
                ),
            },
            {
                "order": 5,
                "body_uz": (
                    "Ma'naviy-ma'rifiy ishlarning rejasini tuzish va ijrosini ta'minlashga "
                    "rahbarlik qilish."
                ),
                "body_ru": (
                    "Руководство составлением плана духовно-просветительской работы "
                    "и обеспечением его выполнения."
                ),
                "body_en": (
                    "Leading the planning and ensuring the implementation of spiritual and "
                    "educational activities."
                ),
            },
            {
                "order": 6,
                "body_uz": (
                    "Ommaviy axborot vositalari bilan samarali hamkorlik qilish, axborot xizmatlari "
                    "bilan doimiy ishlovchi jurnalistlar va blogerlar doirasida tezkor ma'lumotlarni "
                    "tarqatish, shuningdek, normativ-huquqiy hujjatlar loyihalarini muhokama qilishda "
                    "keng jamoatchilik ishtirokini ta'minlash maqsadida ekspertlar guruhini "
                    "shakllantirish."
                ),
                "body_ru": (
                    "Эффективное сотрудничество со СМИ, оперативное распространение информации "
                    "среди журналистов и блогеров, постоянно работающих с информационными службами, "
                    "а также формирование экспертных групп для обеспечения широкого участия "
                    "общественности в обсуждении проектов нормативно-правовых документов."
                ),
                "body_en": (
                    "Effectively cooperating with mass media, rapidly disseminating information "
                    "among journalists and bloggers regularly working with information services, "
                    "and forming expert groups to ensure broad public participation in discussing "
                    "draft regulatory documents."
                ),
            },
        ],
    },
    {
        "number": 6,
        "order": 2,
        "title_uz": (
            "Axborot vositalari va Internet tarmog'ida Akademiya faoliyatiga aloqador "
            "axborotni tarqatish bo'yicha ishlarni tashkil qilish"
        ),
        "title_ru": (
            "Организация работы по распространению информации, связанной с деятельностью "
            "Академии, в средствах массовой информации и сети Интернет"
        ),
        "title_en": (
            "Organizing the dissemination of information related to the Academy's activities "
            "in the media and on the Internet"
        ),
        "items": [
            {
                "order": 1,
                "body_uz": (
                    "Axborot maydoni monitoringini olib borish va tahlil qilish, ularga munosabat "
                    "bildirishning turli usullari va darajasi bo'yicha ekspertlar bilan birgalikda "
                    "takliflar tayyorlash, ommaviy axborot vositalari, shu jumladan, internet "
                    "tarmog'ida jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash "
                    "va malakasini oshirish sohasiga doir materiallarni tarqatish bo'yicha kompleks "
                    "ishlarni tashkil etish."
                ),
                "body_ru": (
                    "Проведение мониторинга и анализа информационного пространства, совместная с "
                    "экспертами подготовка предложений по различным способам и уровням реагирования, "
                    "организация комплексной работы по распространению в СМИ, в том числе в сети "
                    "Интернет, материалов по переподготовке и повышению квалификации специалистов "
                    "в области физической культуры и спорта."
                ),
                "body_en": (
                    "Monitoring and analysing the information space, jointly preparing proposals "
                    "with experts on various response methods and levels, and organising comprehensive "
                    "work to disseminate materials on retraining and professional development of "
                    "specialists in physical culture and sports across mass media, including the Internet."
                ),
            },
            {
                "order": 2,
                "body_uz": (
                    "Akademiyaning bo'limlari, kafedralari bilan hamkorlikda milliy va xorijiy "
                    "ommaviy axborot vositalarida tarqatish uchun xabar, axborot-ma'lumot materiallari, "
                    "sharhlar va axborot-tahliliy materiallar tayyorlash."
                ),
                "body_ru": (
                    "Подготовка в сотрудничестве с подразделениями и кафедрами Академии новостей, "
                    "информационно-справочных материалов, комментариев и аналитических материалов "
                    "для распространения в национальных и зарубежных СМИ."
                ),
                "body_en": (
                    "Preparing news, informational-reference materials, commentaries, and analytical "
                    "content for distribution in national and international media, in collaboration "
                    "with the Academy's departments and faculties."
                ),
            },
            {
                "order": 3,
                "body_uz": (
                    "Akademiyaning ijobiy imijini shakllantirish va ilgari surish, ijtimoiy so'rovlar "
                    "o'tkazish va boshqa shakllarda jamoatchilik fikrini o'rganish."
                ),
                "body_ru": (
                    "Формирование и продвижение положительного имиджа Академии, проведение "
                    "социальных опросов и изучение общественного мнения в иных формах."
                ),
                "body_en": (
                    "Shaping and promoting the Academy's positive image, conducting social surveys, "
                    "and studying public opinion through other forms."
                ),
            },
            {
                "order": 4,
                "body_uz": (
                    "Akademiya faoliyatini xorijiy ommaviy axborot vositalarida sifatli yoritish "
                    "maqsadida vakolatli vazirliklar va idoralar bilan hamkorlikda axborot materiallari "
                    "(foto, audio va videomateriallar, bosma mahsulotlar va shu kabilar) bilan "
                    "ta'minlash."
                ),
                "body_ru": (
                    "Обеспечение информационными материалами (фото, аудио- и видеоматериалами, "
                    "печатной продукцией и пр.) в сотрудничестве с уполномоченными министерствами "
                    "и ведомствами для качественного освещения деятельности Академии в зарубежных СМИ."
                ),
                "body_en": (
                    "Providing information materials (photos, audio and video content, print products, "
                    "etc.) in cooperation with authorised ministries and agencies, in order to achieve "
                    "quality coverage of the Academy's activities in foreign media."
                ),
            },
            {
                "order": 5,
                "body_uz": (
                    "Akademiya faoliyatiga nisbatan jamoatchilik fikrining holati hamda milliy va "
                    "xorijiy ommaviy axborot vositalari pozitsiyasini tahlil qilish va ular to'g'risida "
                    "Akademiya rahbariyatiga axborot berish."
                ),
                "body_ru": (
                    "Анализ состояния общественного мнения и позиции национальных и зарубежных СМИ "
                    "в отношении деятельности Академии и информирование руководства Академии "
                    "об этом."
                ),
                "body_en": (
                    "Analysing the state of public opinion and the position of national and foreign "
                    "media regarding the Academy's activities, and reporting to the Academy's "
                    "leadership."
                ),
            },
            {
                "order": 6,
                "body_uz": (
                    "Akademiyaning faoliyat sohasiga aloqador matnli, foto, audio va videomateriallar, "
                    "ma'lumotlar bazasini shakllantirish va yuritish."
                ),
                "body_ru": (
                    "Формирование и ведение базы данных текстовых, фото-, аудио- и "
                    "видеоматериалов, связанных со сферой деятельности Академии."
                ),
                "body_en": (
                    "Creating and maintaining a database of text, photo, audio, and video materials "
                    "related to the Academy's field of activity."
                ),
            },
            {
                "order": 7,
                "body_uz": (
                    "Milliy va xorijiy ommaviy axborot vositalarida Akademiya faoliyatining dolzarb "
                    "jihatlarini, jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash "
                    "va malakasini oshirish sohasidagi faoliyatini yoritish."
                ),
                "body_ru": (
                    "Освещение актуальных аспектов деятельности Академии и её работы в сфере "
                    "переподготовки и повышения квалификации специалистов по физической культуре "
                    "и спорту в национальных и зарубежных СМИ."
                ),
                "body_en": (
                    "Covering the most relevant aspects of the Academy's activities and its work in "
                    "retraining and professional development of physical culture and sports specialists "
                    "in national and foreign media."
                ),
            },
            {
                "order": 8,
                "body_uz": (
                    "Akademiyaning rasmiy veb-sayti, veb-resurslari, ochiq ma'lumotlar portali hamda "
                    "ijtimoiy tarmoqlardagi rasmiy kanallarini ishonchli axborot materiallari bilan "
                    "to'ldirib borish, shuningdek, jahon internet tarmog'idagi milliy kontentni "
                    "doimiy boyitib borish."
                ),
                "body_ru": (
                    "Наполнение официального веб-сайта, веб-ресурсов, портала открытых данных и "
                    "официальных каналов в социальных сетях Академии достоверными информационными "
                    "материалами, а также постоянное обогащение национального контента во всемирной "
                    "сети Интернет."
                ),
                "body_en": (
                    "Filling the Academy's official website, web resources, open data portal, and "
                    "official social media channels with reliable information materials, as well as "
                    "continuously enriching national content on the World Wide Web."
                ),
            },
            {
                "order": 9,
                "body_uz": (
                    "Akademiya faoliyati sohasidagi normativ-huquqiy hujjatlarning milliy ommaviy "
                    "axborot vositalarida e'lon qilinishini tashkil etish."
                ),
                "body_ru": (
                    "Организация публикации нормативно-правовых документов в сфере деятельности "
                    "Академии в национальных средствах массовой информации."
                ),
                "body_en": (
                    "Organising the publication of regulatory documents in the Academy's field of "
                    "activity in national mass media."
                ),
            },
        ],
    },
]


# ── Axborot xizmati xodimlari ──────────────────────────────────────────────────

CATEGORY_SLUG = 'axborot-xizmati'

PERSONS = [
    {
        "order": 1,
        "is_head": True,
        "full_name_uz": "Nazarov Jasur Aliyevich",
        "full_name_ru": "Назаров Жасур Алиевич",
        "full_name_en": "Jasur Aliyevich Nazarov",
        "title_uz": "Axborot xizmati boshlig'i",
        "title_ru": "Начальник информационной службы",
        "title_en": "Head of Information Service",
        "position_uz": "",
        "position_ru": "",
        "position_en": "",
        "phone": "+998 71 200 00 01",
        "email": "axborot@usas.uz",
        "reception": "Dushanba–Juma, 9:00–18:00",
        "address": "Toshkent shahri, Olimpiya shaharchasi",
    },
    {
        "order": 2,
        "is_head": False,
        "full_name_uz": "Xoliqova Dilnoza Baxtiyor qizi",
        "full_name_ru": "Холикова Дилноза Бахтиёровна",
        "full_name_en": "Dilnoza Baxtiyor qizi Xoliqova",
        "title_uz": "Matbuot kotibi",
        "title_ru": "Пресс-секретарь",
        "title_en": "Press Secretary",
        "position_uz": "",
        "position_ru": "",
        "position_en": "",
        "phone": "+998 71 200 00 02",
        "email": "press@usas.uz",
        "reception": "Dushanba–Juma, 9:00–18:00",
        "address": "Toshkent shahri, Olimpiya shaharchasi",
    },
    {
        "order": 3,
        "is_head": False,
        "full_name_uz": "Toshmatov Sherzod Karimovich",
        "full_name_ru": "Тошматов Шерзод Каримович",
        "full_name_en": "Sherzod Karimovich Toshmatov",
        "title_uz": "SMM va raqamli kontent mutaxassisi",
        "title_ru": "Специалист по SMM и цифровому контенту",
        "title_en": "SMM and Digital Content Specialist",
        "position_uz": "",
        "position_ru": "",
        "position_en": "",
        "phone": "+998 71 200 00 03",
        "email": "smm@usas.uz",
        "reception": "Dushanba–Juma, 9:00–18:00",
        "address": "Toshkent shahri, Olimpiya shaharchasi",
    },
]


class Command(BaseCommand):
    help = "Axborot xizmati bo'limlari, vazifalari va xodimlarini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Oldin mavjud ma'lumotlarni o'chiradi")

    def handle(self, *args, **options):
        if options['clear']:
            AxborotVazifa.objects.all().delete()
            AxborotSection.objects.all().delete()
            Person.objects.filter(category__slug=CATEGORY_SLUG).delete()
            from domains.students.models import PersonCategory
            PersonCategory.objects.filter(slug=CATEGORY_SLUG).delete()
            self.stdout.write(self.style.WARNING("Eski ma'lumotlar o'chirildi."))

        self._seed_sections()
        self._seed_persons()
        self.stdout.write(self.style.SUCCESS("Axborot xizmati ma'lumotlari muvaffaqiyatli saqlandi."))

    def _seed_sections(self):
        for sec_data in SECTIONS:
            items = sec_data.pop('items')
            section, _ = AxborotSection.objects.update_or_create(
                number=sec_data['number'],
                defaults=sec_data,
            )
            sec_data['items'] = items  # restore for idempotency on re-run

            for item in items:
                AxborotVazifa.objects.update_or_create(
                    section=section,
                    order=item['order'],
                    defaults={
                        'body_uz': item['body_uz'],
                        'body_ru': item.get('body_ru', ''),
                        'body_en': item.get('body_en', ''),
                        'is_active': True,
                    },
                )
            self.stdout.write(f"  + {section.number}-band: {len(items)} ta vazifa")

    def _seed_persons(self):
        from domains.students.models import PersonCategory

        category, _ = PersonCategory.objects.update_or_create(
            slug=CATEGORY_SLUG,
            defaults={
                'title_uz': "Axborot xizmati",
                'title_ru': "Информационная служба",
                'title_en': "Information Service",
                'order': 10,
            },
        )

        for p in PERSONS:
            Person.objects.update_or_create(
                full_name_uz=p['full_name_uz'],
                defaults={**p, 'category': category, 'is_active': True},
            )
            self.stdout.write(f"  + {p['full_name_uz']}")
