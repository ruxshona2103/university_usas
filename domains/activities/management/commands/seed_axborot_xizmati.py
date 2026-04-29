"""
python manage.py seed_axborot_xizmati

Axborot xizmati uchun:
  - 11 ta vazifa (5-6-bandlar bo'yicha)
  - 1 ta xodim: Mexrangiz
"""

import uuid
from django.core.management.base import BaseCommand
from domains.activities.models import AxborotVazifa, AxborotXodim

VAZIFALAR = [
    {
        "id": "a0000001-0001-0001-0001-000000000001",
        "title_uz": "Akademiya tomonidan jismoniy tarbiya va sport bo'yicha mutaxassislarni qayta tayyorlash va malakasini oshirish sohasida amalga oshirilayotgan faoliyat hamda zamonaviy talablarga muvofiq belgilanadigan axborot siyosatini shakllantirish va keng ommaga yetkazishda ishtirok etish.",
        "title_ru": "Участие в формировании и доведении до широкой общественности информационной политики, определяемой в соответствии с современными требованиями, а также деятельности академии по переподготовке и повышению квалификации специалистов в области физической культуры и спорта.",
        "title_en": "Participation in shaping and communicating the information policy defined in accordance with modern requirements, as well as the activities of the academy in retraining and improving the qualifications of specialists in the field of physical education and sports.",
        "order": 1,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000002",
        "title_uz": "Axborot siyosati sohasida zimmasiga yuklangan vazifalarni amalga oshirishda vazirlikning matbuot xizmati, sport boshqarmalari, boshqa davlat va xo'jalik boshqaruvi organlarining axborot xizmatlari, sport turlari bo'yicha federatsiyalar (uyushma) va boshqa tashkilotlar bilan samarali amaliy hamkorlikni yo'lga qo'yish.",
        "title_ru": "Налаживание эффективного практического сотрудничества с пресс-службой министерства, управлениями спорта, информационными службами других органов государственного и хозяйственного управления, федерациями (ассоциациями) по видам спорта и другими организациями.",
        "title_en": "Establishing effective practical cooperation with the ministry's press service, sports departments, information services of other state and economic management bodies, sports federations (associations) and other organizations.",
        "order": 2,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000003",
        "title_uz": "Keng jamoatchilikni Akademiyaning faoliyati, uning sohaga doir normativ-huquqiy hujjatlari to'g'risida xolisona, sifatli va tezkorlik bilan xabardor qilish.",
        "title_ru": "Своевременное, качественное и объективное информирование широкой общественности о деятельности Академии, её нормативно-правовых документах, касающихся данной сферы.",
        "title_en": "Timely, high-quality and objective informing of the general public about the activities of the Academy and its regulatory documents related to this field.",
        "order": 3,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000004",
        "title_uz": "Muntazam ravishda ommaviy axborot vositalarida Akademiya rahbariyatining chiqishlarini tashkil etish.",
        "title_ru": "Регулярная организация выступлений руководства Академии в средствах массовой информации.",
        "title_en": "Regular organization of appearances of the Academy's leadership in the mass media.",
        "order": 4,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000005",
        "title_uz": "Ma'naviy-ma'rifiy ishlarning rejasini tuzish va ijrosini ta'minlashga rahbarlik qilish.",
        "title_ru": "Руководство составлением и обеспечением выполнения плана духовно-просветительской работы.",
        "title_en": "Leading the planning and implementation of spiritual and educational activities.",
        "order": 5,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000006",
        "title_uz": "Ommaviy axborot vositalari bilan samarali hamkorlik qilish, axborot xizmatlari bilan doimiy ishlovchi jurnalistlar va blogerlar doirasida tezkor ma'lumotlarni tarqatish, shuningdek, normativ-huquqiy hujjatlar loyihalarini muhokama qilishda keng jamoatchilik ishtirokini ta'minlash maqsadida ekspertlar guruhini shakllantirish.",
        "title_ru": "Эффективное сотрудничество со СМИ, распространение оперативной информации среди журналистов и блогеров, постоянно работающих с информационными службами, а также формирование экспертной группы в целях обеспечения широкого участия общественности в обсуждении проектов нормативно-правовых документов.",
        "title_en": "Effective cooperation with mass media, dissemination of prompt information among journalists and bloggers working permanently with information services, as well as forming an expert group to ensure broad public participation in discussing draft regulatory documents.",
        "order": 6,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000007",
        "title_uz": "Axborot maydoni monitoringini olib borish va tahlil qilish, ularga munosabat bildirishning turli usullari va darajasi bo'yicha ekspertlar bilan birgalikda takliflar tayyorlash, ommaviy axborot vositalarida jismoniy tarbiya va sport sohasiga doir materiallarni tarqatish bo'yicha kompleks ishlarni tashkil etish.",
        "title_ru": "Проведение мониторинга и анализа информационного пространства, подготовка совместно с экспертами предложений по различным методам и уровням реагирования, организация комплексной работы по распространению материалов по физической культуре и спорту в СМИ.",
        "title_en": "Conducting monitoring and analysis of the information space, preparing proposals together with experts on various methods and levels of response, organizing comprehensive work on disseminating materials on physical culture and sports in the media.",
        "order": 7,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000008",
        "title_uz": "Akademiyaning bo'limlari, kafedralari bilan hamkorlikda milliy va xorijiy ommaviy axborot vositalarida tarqatish uchun xabar, axborot-ma'lumot materiallari, sharhlar va axborot-tahliliy materiallar tayyorlash.",
        "title_ru": "Подготовка совместно с подразделениями и кафедрами Академии новостей, информационно-справочных материалов, комментариев и информационно-аналитических материалов для распространения в национальных и зарубежных СМИ.",
        "title_en": "Preparing news, information materials, comments and analytical materials together with the Academy's departments and chairs for distribution in national and foreign media.",
        "order": 8,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000009",
        "title_uz": "Akademiyaning ijobiy imijini shakllantirish va ilgari surish, ijtimoiy so'rovlar o'tkazish va boshqa shakllarda jamoatchilik fikrini o'rganish.",
        "title_ru": "Формирование и продвижение положительного имиджа Академии, проведение социальных опросов и изучение общественного мнения в иных формах.",
        "title_en": "Shaping and promoting the positive image of the Academy, conducting social surveys and studying public opinion in other forms.",
        "order": 9,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000010",
        "title_uz": "Akademiyaning rasmiy veb-sayti, veb-resurslari, ochiq ma'lumotlar portali hamda ijtimoiy tarmoqlardagi rasmiy kanallarini ishonchli axborot materiallari bilan to'ldirib borish, shuningdek, jahon internet tarmog'idagi milliy kontentni doimiy boyitib borish.",
        "title_ru": "Регулярное наполнение официального веб-сайта, веб-ресурсов, портала открытых данных и официальных каналов Академии в социальных сетях достоверными информационными материалами, а также постоянное обогащение национального контента в мировой сети Интернет.",
        "title_en": "Regularly filling the Academy's official website, web resources, open data portal and official social media channels with reliable information materials, as well as continuously enriching national content on the global internet.",
        "order": 10,
    },
    {
        "id": "a0000001-0001-0001-0001-000000000011",
        "title_uz": "Akademiya faoliyati sohasidagi normativ-huquqiy hujjatlarning milliy ommaviy axborot vositalarida e'lon qilinishini tashkil etish.",
        "title_ru": "Организация публикации нормативно-правовых документов в сфере деятельности Академии в национальных средствах массовой информации.",
        "title_en": "Organizing the publication of regulatory documents in the field of the Academy's activities in national mass media.",
        "order": 11,
    },
]

XODIMLAR = [
    {
        "id":          "b0000002-0002-0002-0002-000000000001",
        "full_name_uz": "Mexrangiz",
        "full_name_ru": "Мехрангиз",
        "full_name_en": "Mehrangiz",
        "position_uz":  "Axborot xizmati mutaxassisi",
        "position_ru":  "Специалист информационной службы",
        "position_en":  "Information Service Specialist",
        "phone":        "+998 90 000 00 00",
        "email":        "mexrangiz@usas.uz",
        "order":        1,
    },
]


class Command(BaseCommand):
    help = "Axborot xizmati vazifalari va xodimlarini DB ga qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Mavjud axborot datalarni o'chiradi")

    def handle(self, *args, **options):
        if options['clear']:
            AxborotVazifa.objects.all().delete()
            AxborotXodim.objects.all().delete()
            self.stdout.write(self.style.WARNING("Mavjud axborot xizmati ma'lumotlari o'chirildi."))

        self.stdout.write("\n--- VAZIFALAR ---")
        for d in VAZIFALAR:
            obj, created = AxborotVazifa.objects.update_or_create(
                id=uuid.UUID(d['id']),
                defaults={k: v for k, v in d.items() if k != 'id'},
            )
            label = obj.title_uz[:60] + '...'
            self.stdout.write(f"  [{'Yaratildi' if created else 'Yangilandi'}] {label}")

        self.stdout.write("\n--- XODIMLAR ---")
        for d in XODIMLAR:
            obj, created = AxborotXodim.objects.update_or_create(
                id=uuid.UUID(d['id']),
                defaults={k: v for k, v in d.items() if k != 'id'},
            )
            self.stdout.write(f"  [{'Yaratildi' if created else 'Yangilandi'}] {obj.full_name_uz} — {obj.position_uz}")

        self.stdout.write(self.style.SUCCESS(
            f"\nJami: {len(VAZIFALAR)} vazifa | {len(XODIMLAR)} xodim!"
        ))
