"""
python manage.py seed_almashinuv
python manage.py seed_almashinuv --clear
"""
from django.core.management.base import BaseCommand
from domains.international.models import AkademikAlmashinuv, AkademikAlmashinuvRasm

DATA = [
    {
        "order": 1,
        "title_uz": "Talabalar almashinuvi dasturi",
        "title_ru": "Программа обмена студентами",
        "title_en": "Student Exchange Programme",
        "body_uz": (
            "Talabalar almashinuvi dasturi — bu ta'lim muassasalari o'rtasida talabalarni o'zaro "
            "almashish bo'yicha tuziladigan kelishuvdir. Bunday dasturlar universitet talabalariga 1 yoki "
            "2 akademik semestr davomida xorijda tahsil olish va/yoki amaliyot o'tash imkonini beradi.\n\n"
            "Almashinuv universitetlar o'rtasida tuzilgan hamkorlik shartnomasi asosida amalga oshiriladi.\n\n"
            "Mazkur dasturlarning asosiy maqsadlari — ta'lim sifatini oshirish hamda mamlakatlar "
            "o'rtasida madaniy va iqtisodiy aloqalarni rivojlantirishdir.\n\n"
            "O'zbekiston davlat sport akademiyasi bir qator xorijiy universitetlar bilan hamkorlik "
            "shartnomalariga ega. Almashinuv dasturlari doirasidagi ta'lim talabaning shaxsiy "
            "mablag'lari hisobidan yoki turli grant dasturlari tomonidan ajratilgan mablag'lar "
            "asosida amalga oshirilishi mumkin.\n\n"
            "Talabalar mobilligini qo'llab-quvvatlovchi asosiy dastur — bu akademiya tomonidan "
            "Erasmus+ dasturining Key Action 1 yo'nalishi doirasida qo'lga kiritilgan Kredit "
            "mobilligi dasturidir."
        ),
        "body_ru": (
            "Программа обмена студентами — это соглашение об обоюдном обмене студентами между "
            "учебными заведениями. Такие программы дают студентам возможность учиться и/или "
            "проходить практику за рубежом в течение 1 или 2 академических семестров.\n\n"
            "Обмен осуществляется на основании договора о сотрудничестве, заключённого между "
            "университетами.\n\n"
            "Основные цели данных программ — повышение качества образования, а также развитие "
            "культурных и экономических связей между странами.\n\n"
            "Узбекистанская государственная спортивная академия имеет договоры о сотрудничестве "
            "с рядом зарубежных университетов. Обучение в рамках программ обмена может "
            "финансироваться за счёт личных средств студента или средств различных грантовых программ.\n\n"
            "Основная программа поддержки академической мобильности студентов — программа "
            "кредитной мобильности, реализуемая академией в рамках направления Key Action 1 "
            "программы Erasmus+."
        ),
        "body_en": (
            "The student exchange programme is an agreement on the mutual exchange of students "
            "between educational institutions. Such programmes give university students the "
            "opportunity to study and/or complete an internship abroad for 1 or 2 academic semesters.\n\n"
            "The exchange is carried out on the basis of a cooperation agreement concluded between "
            "the universities.\n\n"
            "The main objectives of these programmes are to improve the quality of education and "
            "to develop cultural and economic ties between countries.\n\n"
            "The Uzbekistan State Sports Academy has cooperation agreements with a number of foreign "
            "universities. Education within exchange programmes may be financed from the student's "
            "personal funds or through funding allocated by various grant programmes.\n\n"
            "The main programme supporting student academic mobility is the Credit Mobility "
            "programme, which the Academy has secured under Key Action 1 of the Erasmus+ programme."
        ),
    },
    {
        "order": 2,
        "title_uz": "Erasmus+ Kredit mobilligi dasturi",
        "title_ru": "Программа кредитной мобильности Erasmus+",
        "title_en": "Erasmus+ Credit Mobility Programme",
        "body_uz": (
            "Bu dastur talabalar, stajyorlar, professor-o'qituvchilar, yoshlar bilan ishlovchi "
            "mutaxassislar, ta'lim muassasalari xodimlari hamda fuqarolik jamiyati tashkilotlari "
            "vakillariga boshqa mamlakatda o'qish va kasbiy tajriba orttirish imkonini beradi.\n\n"
            "\"Kredit mobilligi\" dasturi oliy ta'limning barcha bosqichlarida (qisqa sikl, "
            "bakalavriat, magistratura, doktorantura) talabalar almashinuvini ikki tomonlama "
            "moliyalashtiradi.\n\n"
            "Talabalar va xodimlarga safar, viza, sug'urta xarajatlarini qoplaydigan hamda yashash "
            "uchun qo'shimcha mablag' ajratiladigan stipendiya taqdim etiladi. Ishtirok etuvchi "
            "universitetlar tomonidan talabalardan kontrakt to'lovi undirilmaydi."
        ),
        "body_ru": (
            "Данная программа предоставляет студентам, стажёрам, преподавателям, специалистам по "
            "работе с молодёжью, сотрудникам учебных заведений и представителям организаций "
            "гражданского общества возможность получить образование и профессиональный опыт в "
            "другой стране.\n\n"
            "Программа «Кредитная мобильность» финансирует двустороннее участие студентов на "
            "всех уровнях высшего образования (короткий цикл, бакалавриат, магистратура, "
            "докторантура).\n\n"
            "Студентам и сотрудникам выплачивается стипендия, покрывающая транспортные, визовые "
            "и страховые расходы, а также предоставляются дополнительные средства на проживание. "
            "Участвующие университеты не взимают с обменных студентов плату за контракт."
        ),
        "body_en": (
            "This programme gives students, trainees, academic staff, youth workers, staff of "
            "educational institutions, and representatives of civil society organisations the "
            "opportunity to study and gain professional experience in another country.\n\n"
            "The Credit Mobility programme provides bilateral funding for student participation "
            "at all levels of higher education (short cycle, bachelor's, master's, and doctoral).\n\n"
            "Students and staff receive a grant covering travel, visa, and insurance costs, as well "
            "as an additional living allowance. Participating universities do not charge exchange "
            "students a tuition fee."
        ),
    },
]


class Command(BaseCommand):
    help = "Akademik almashinuv bo'limlarini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Eski ma'lumotlarni o'chirib qayta yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = AkademikAlmashinuv.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        for d in DATA:
            obj, created = AkademikAlmashinuv.objects.update_or_create(
                order=d['order'],
                defaults={**d, 'is_active': True},
            )
            label = '+' if created else '~'
            title_safe = obj.title_uz.encode('ascii', 'replace').decode()
            self.stdout.write(f"  [{label}] {title_safe}")

        self.stdout.write(self.style.SUCCESS("Tayyor!"))
