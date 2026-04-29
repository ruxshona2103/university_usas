"""
python manage.py seed_markazlar
python manage.py seed_markazlar --clear
"""
from django.core.management.base import BaseCommand
from domains.pages.models import Markaz, MarkazSubBolim

MARKAZLAR = [
    {
        "name_uz": "Reja-moliya sektori",
        "name_ru": "Планово-финансовый сектор",
        "name_en": "Planning and Finance Sector",
        "description_uz": "Akademiyaning moliyaviy rejalashtirishini amalga oshiruvchi, byudjet tuzish va moliyaviy hisobotlarni boshqaruvchi sektor.",
        "description_ru": "Сектор, осуществляющий финансовое планирование академии, составление бюджета и управление финансовой отчётностью.",
        "description_en": "Sector responsible for financial planning, budgeting and financial reporting of the academy.",
        "slug": "reja-moliya-sektori",
        "order": 1,
        "sub_bolimlar": [],
    },
    {
        "name_uz": "Buxgalteriya",
        "name_ru": "Бухгалтерия",
        "name_en": "Accounting Department",
        "description_uz": "Akademiyaning moliyaviy operatsiyalarini hisobga oluvchi, daromad va xarajatlar hisobini yurituvchi bo'lim.",
        "description_ru": "Подразделение, ведущее учёт финансовых операций академии, доходов и расходов.",
        "description_en": "Department responsible for recording financial operations, income and expenditure of the academy.",
        "slug": "buxgalteriya",
        "order": 2,
        "sub_bolimlar": [],
    },
    {
        "name_uz": "Fuqaro va mehnat muhofazasi bo'limi",
        "name_ru": "Отдел гражданской и трудовой защиты",
        "name_en": "Civil and Labour Protection Department",
        "description_uz": "Akademiya xodimlarining mehnat sharoitlarini nazorat qiluvchi, mehnat muhofazasi va xavfsizlik texnikasi bo'yicha ishlarni amalga oshiruvchi bo'lim.",
        "description_ru": "Отдел, контролирующий условия труда сотрудников академии, осуществляющий мероприятия по охране труда и технике безопасности.",
        "description_en": "Department controlling working conditions of academy staff, implementing labour protection and safety measures.",
        "slug": "fuqaro-mehnat-muhofazasi",
        "order": 3,
        "sub_bolimlar": [],
    },
    {
        "name_uz": "O'qitishning texnik vositalari bo'limi",
        "name_ru": "Отдел технических средств обучения",
        "name_en": "Department of Technical Teaching Aids",
        "description_uz": "O'quv jarayonida ishlatiladigan texnik vositalarni ta'minlash, ularga texnik xizmat ko'rsatish va yangilab turish bilan shug'ullanuvchi bo'lim.",
        "description_ru": "Подразделение, обеспечивающее технические средства, используемые в учебном процессе, их техническое обслуживание и обновление.",
        "description_en": "Department responsible for providing, maintaining and updating technical equipment used in the educational process.",
        "slug": "texnik-vositalar-bolimi",
        "order": 4,
        "sub_bolimlar": [],
    },
    {
        "name_uz": "Bosh muhandis",
        "name_ru": "Главный инженер",
        "name_en": "Chief Engineer",
        "description_uz": "Akademiyaning barcha muhandislik tizimlarini — elektr ta'minoti, issiqlik, suv ta'minoti va boshqa infratuzilmalarni boshqaruvchi muhandislik xizmati.",
        "description_ru": "Инженерная служба, управляющая всеми инженерными системами академии — электроснабжением, теплоснабжением, водоснабжением и другой инфраструктурой.",
        "description_en": "Engineering service managing all engineering systems of the academy — power supply, heating, water supply and other infrastructure.",
        "slug": "bosh-muhandis",
        "order": 5,
        "sub_bolimlar": [],
    },
    {
        "name_uz": "Marketing va talabalar amaliyoti bo'limi",
        "name_ru": "Отдел маркетинга и студенческой практики",
        "name_en": "Marketing and Student Internship Department",
        "description_uz": "Akademiyani targ'ib qilish, yangi talabalar jalb etish va talabalarning ishlab chiqarish amaliyotini tashkil etish bilan shug'ullanuvchi bo'lim.",
        "description_ru": "Отдел, занимающийся продвижением академии, привлечением новых студентов и организацией производственной практики студентов.",
        "description_en": "Department engaged in promoting the academy, attracting new students and organising student internships.",
        "slug": "marketing-talabalar-amaliyoti",
        "order": 6,
        "sub_bolimlar": [],
    },
    # Rektor yordamchisi ostidagi bo'limlar (rasmda o'ng tomonda ko'rsatilgan)
    {
        "name_uz": "Rektor yordamchisi huzuridagi bo'limlar",
        "name_ru": "Подразделения при помощнике ректора",
        "name_en": "Departments under the Rector's Assistant",
        "description_uz": "Akademiya rektor yordamchisi nazoratidagi nazorat, huquqiy va ma'muriy bo'limlar majmui.",
        "description_ru": "Комплекс контрольных, правовых и административных подразделений под надзором помощника ректора академии.",
        "description_en": "A set of supervisory, legal and administrative units under the supervision of the academy rector's assistant.",
        "slug": "rektor-yordamchisi-bolimlar",
        "order": 7,
        "sub_bolimlar": [
            {
                "name_uz": "Ta'lim sifatini nazorat qilish bo'limi",
                "name_ru": "Отдел контроля качества образования",
                "name_en": "Education Quality Control Department",
                "description_uz": "O'quv jarayoni sifatini monitoring qiluvchi, ichki baholash va akkreditatsiya ishlarini olib boruvchi bo'lim.",
                "description_ru": "Отдел, осуществляющий мониторинг качества учебного процесса, внутреннюю оценку и аккредитацию.",
                "description_en": "Department monitoring the quality of the educational process, conducting internal assessment and accreditation.",
                "order": 1,
            },
            {
                "name_uz": "Jismoniy va yuridik shaxslar murojaatlari bilan ishlash, nazorat va monitoring sektori",
                "name_ru": "Сектор работы с обращениями физических и юридических лиц, контроля и мониторинга",
                "name_en": "Sector for Working with Appeals of Individuals and Legal Entities, Control and Monitoring",
                "description_uz": "Fuqarolar va tashkilotlarning murojaatlarini qabul qilib ko'ruvchi, monitoring va nazoratni amalga oshiruvchi sektor.",
                "description_ru": "Сектор, рассматривающий обращения граждан и организаций, осуществляющий мониторинг и контроль.",
                "description_en": "Sector that reviews appeals from citizens and organisations, conducting monitoring and oversight.",
                "order": 2,
            },
            {
                "name_uz": "Korrupsiyaga qarshi kurashish \"Komplaens-nazorat\" tizimini boshqarish bo'limi",
                "name_ru": "Отдел управления системой «Комплаенс-контроль» по противодействию коррупции",
                "name_en": "Anti-Corruption Compliance Control Management Department",
                "description_uz": "Akademiyada korrupsiyaga qarshi kurashish, komplaens-nazorat tizimini joriy etish va nazorat qilish bilan shug'ullanuvchi bo'lim.",
                "description_ru": "Отдел, занимающийся противодействием коррупции в академии, внедрением и контролем системы комплаенс.",
                "description_en": "Department dealing with anti-corruption measures, implementing and overseeing compliance control system in the academy.",
                "order": 3,
            },
            {
                "name_uz": "Matbuot kotibi",
                "name_ru": "Пресс-секретарь",
                "name_en": "Press Secretary",
                "description_uz": "Akademiyaning ommaviy axborot vositalari bilan munosabatlarini boshqaruvchi, rasmiy bayonotlar va media aloqalarni amalga oshiruvchi xodim.",
                "description_ru": "Сотрудник, управляющий отношениями академии со СМИ, осуществляющий официальные заявления и медиакоммуникации.",
                "description_en": "Staff member managing the academy's relations with the media, making official statements and handling media communications.",
                "order": 4,
            },
            {
                "name_uz": "Xodimlar bo'limi",
                "name_ru": "Отдел кадров",
                "name_en": "Human Resources Department",
                "description_uz": "Akademiya xodimlarini yollash, ro'yxatga olish, mehnat shartnomalari va kadrlar zaxirasini boshqaruvchi bo'lim.",
                "description_ru": "Отдел, занимающийся подбором, учётом персонала академии, трудовыми договорами и кадровым резервом.",
                "description_en": "Department managing recruitment, registration of academy staff, employment contracts and personnel reserve.",
                "order": 5,
            },
            {
                "name_uz": "Devonxona va arxiv",
                "name_ru": "Делопроизводство и архив",
                "name_en": "Records Management and Archive",
                "description_uz": "Akademiyaning rasmiy hujjatlarini yuritish, arxivlash va saqlash bilan shug'ullanuvchi bo'lim.",
                "description_ru": "Подразделение, занимающееся ведением официальных документов академии, архивированием и хранением.",
                "description_en": "Department responsible for maintaining, archiving and storing official documents of the academy.",
                "order": 6,
            },
            {
                "name_uz": "Yuriskonsult",
                "name_ru": "Юрисконсульт",
                "name_en": "Legal Counsel",
                "description_uz": "Akademiyaning huquqiy masalalarini ko'ruvchi, shartnomalar va nizolarni huquqiy jihatdan ta'minlovchi yuridik xizmat.",
                "description_ru": "Юридическая служба, рассматривающая правовые вопросы академии, юридически обеспечивающая договоры и споры.",
                "description_en": "Legal service reviewing legal matters of the academy and providing legal support for contracts and disputes.",
                "order": 7,
            },
            {
                "name_uz": "Birinchi bo'lim",
                "name_ru": "Первый отдел",
                "name_en": "First Department",
                "description_uz": "Akademiyada maxfiy ma'lumotlar va davlat sirlarini muhofaza qilish bilan shug'ullanuvchi bo'lim.",
                "description_ru": "Отдел, занимающийся защитой секретных сведений и государственной тайны в академии.",
                "description_en": "Department responsible for protecting classified information and state secrets in the academy.",
                "order": 8,
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Markazlar va sub-bo'limlar ma'lumotlarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = Markaz.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        created_m = updated_m = created_s = 0

        for data in MARKAZLAR:
            sub_list = data.pop('sub_bolimlar', [])
            obj, is_new = Markaz.objects.update_or_create(
                slug=data['slug'],
                defaults=data,
            )
            if is_new:
                created_m += 1
            else:
                updated_m += 1

            name = obj.name_uz.encode('ascii', 'replace').decode()
            self.stdout.write(f"  [{'+'if is_new else '~'}] {name}")

            for s in sub_list:
                _, s_new = MarkazSubBolim.objects.update_or_create(
                    markaz=obj,
                    name_uz=s['name_uz'],
                    defaults=s,
                )
                created_s += s_new
                sub_name = s['name_uz'].encode('ascii', 'replace').decode()
                self.stdout.write(f"      [{'+'if s_new else '~'}] {sub_name}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {created_m} markaz yangi, {updated_m} yangilandi | {created_s} sub-bo'lim yaratildi"
        ))
