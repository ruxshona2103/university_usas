"""
python manage.py seed_interaktiv_xizmat
python manage.py seed_interaktiv_xizmat --clear
"""
from django.core.management.base import BaseCommand
from domains.pages.models import InteraktivXizmat

XIZMATLAR = [
    {
        "icon_class": "book-open",
        "title_uz": "Elektron kutubxona",
        "title_ru": "Электронная библиотека",
        "title_en": "Electronic Library",
        "description_uz": "Akademiya elektron kutubxonasiga kirish. Minglab ilmiy maqolalar, darsliklar va monografiyalar mavjud.",
        "description_ru": "Доступ к электронной библиотеке академии. Тысячи научных статей, учебников и монографий.",
        "description_en": "Access to the academy's electronic library. Thousands of scientific articles, textbooks and monographs.",
        "link": "https://library.usas.uz",
        "order": 1,
    },
    {
        "icon_class": "graduation-cap",
        "title_uz": "HEMIS",
        "title_ru": "HEMIS",
        "title_en": "HEMIS",
        "description_uz": "Oliy ta'lim boshqaruv axborot tizimi. Talabalar va o'qituvchilar uchun shaxsiy kabinet.",
        "description_ru": "Информационная система управления высшим образованием. Личный кабинет для студентов и преподавателей.",
        "description_en": "Higher Education Management Information System. Personal account for students and teachers.",
        "link": "https://hemis.edu.uz",
        "order": 2,
    },
    {
        "icon_class": "laptop",
        "title_uz": "Dasturlar",
        "title_ru": "Программы",
        "title_en": "Software",
        "description_uz": "O'quv jarayonida ishlatiladigan dasturiy ta'minotlar va ruxsat etilgan dasturlar ro'yxati.",
        "description_ru": "Список программного обеспечения и разрешённых программ, используемых в учебном процессе.",
        "description_en": "List of software and licensed programmes used in the educational process.",
        "link": "",
        "order": 3,
    },
    {
        "icon_class": "message-square",
        "title_uz": "Virtual qabulxona",
        "title_ru": "Виртуальная приёмная",
        "title_en": "Virtual Reception",
        "description_uz": "Akademiya rahbariyatiga murojaat, shikoyat va takliflarni onlayn yuborish imkoniyati.",
        "description_ru": "Возможность онлайн-обращения, жалоб и предложений руководству академии.",
        "description_en": "Online submission of appeals, complaints and suggestions to the academy management.",
        "link": "https://pm.gov.uz",
        "order": 4,
    },
    {
        "icon_class": "monitor",
        "title_uz": "LMS",
        "title_ru": "LMS",
        "title_en": "LMS",
        "description_uz": "O'quv boshqaruv tizimi. Onlayn kurslar, topshiriqlar va baholash platformasi.",
        "description_ru": "Система управления обучением. Платформа для онлайн-курсов, заданий и оценки.",
        "description_en": "Learning Management System. Platform for online courses, assignments and assessment.",
        "link": "https://lms.usas.uz",
        "order": 5,
    },
    {
        "icon_class": "wifi",
        "title_uz": "Masofaviy ta'lim",
        "title_ru": "Дистанционное обучение",
        "title_en": "Distance Learning",
        "description_uz": "Masofaviy ta'lim platformasi. Uydan turib o'qish, video darslar va onlayn imtihonlar.",
        "description_ru": "Платформа дистанционного обучения. Учёба из дома, видеоуроки и онлайн-экзамены.",
        "description_en": "Distance learning platform. Study from home, video lessons and online exams.",
        "link": "",
        "order": 6,
    },
]


class Command(BaseCommand):
    help = "Interaktiv xizmatlar ma'lumotlarini qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval o'chirib qaytadan yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = InteraktivXizmat.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta yozuv"))

        created = updated = 0
        for d in XIZMATLAR:
            obj, is_new = InteraktivXizmat.objects.update_or_create(
                title_uz=d['title_uz'],
                defaults=d,
            )
            if is_new:
                created += 1
            else:
                updated += 1
            self.stdout.write(f"  [{'+'if is_new else '~'}] {obj.title_uz}")

        self.stdout.write(self.style.SUCCESS(f"\nNatija: {created} yangi, {updated} yangilandi"))
