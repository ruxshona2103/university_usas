"""
python manage.py seed_psixolog          # yaratadi / yangilaydi
python manage.py seed_psixolog --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand

from domains.students.models import PsixologXizmat, PsixologSection

XIZMATLAR = [
    # (order, uz, ru, en)
    (
        1,
        "Individual maslahat — har bir talaba psixolog bilan yakkama-yakka uchrashuv o'tkazishi mumkin;",
        "Индивидуальная консультация — каждый студент может встретиться с психологом один на один;",
        "Individual consultation — every student can have a one-on-one meeting with a psychologist;",
    ),
    (
        2,
        "Guruhli treninglar — stress boshqarish, jamoada ishlash, ijodiy tafakkurni rivojlantirish;",
        "Групповые тренинги — управление стрессом, работа в команде, развитие творческого мышления;",
        "Group trainings — stress management, teamwork, creative thinking development;",
    ),
    (
        3,
        "Sport psixologiyasi — musobaqalarga psixologik tayyorgarlik, motivatsiya va natijaga yo'naltirish;",
        "Спортивная психология — психологическая подготовка к соревнованиям, мотивация и ориентация на результат;",
        "Sports psychology — psychological preparation for competitions, motivation and result orientation;",
    ),
    (
        4,
        "Anonim maslahat — talabalar shaxsiy ma'lumotlarini oshkor etish xavfisiz murojaat qilishi mumkin.",
        "Анонимная консультация — студенты могут обратиться без опасений за раскрытие личных данных.",
        "Anonymous consultation — students can apply without fear of disclosing personal data.",
    ),
]

SECTIONS = [
    # (order, uz_title, ru_title, en_title, uz_content, ru_content, en_content)
    (
        1,
        "Sport psixologiyasi",
        "Спортивная психология",
        "Sports psychology",
        (
            "Sport psixologiyasi sohasida talaba-sportchilar musobaqalarga psixologik "
            "tayyorgarlik ko'radi, qiyinchiliklarni engish strategiyalarini o'rganadi va "
            "motivatsiya bilan ishlaydi. Akademiyamizning psixologi milliy jamoalar tayyorgarlik "
            "tsikllarida faol ishtirok etadi."
        ),
        (
            "В сфере спортивной психологии студенты-спортсмены проходят психологическую "
            "подготовку к соревнованиям, изучают стратегии преодоления трудностей и работают "
            "с мотивацией. Наш психолог активно участвует в подготовительных циклах "
            "национальных команд."
        ),
        (
            "In the field of sports psychology, student athletes undergo psychological preparation "
            "for competitions, learn strategies for overcoming difficulties and work with motivation. "
            "Our psychologist actively participates in the preparation cycles of national teams."
        ),
    ),
    (
        2,
        "Murojaat qilish tartibi",
        "Порядок обращения",
        "How to apply",
        (
            "Psixologik yordam olish uchun akademiya psixologlari bilan to'g'ridan-to'g'ri "
            "bog'lanish yoki dekanat orqali uchrashuv belgilash mumkin. Barcha murojaatlar "
            "maxfiy saqlanadi. Ish vaqti: dushanba–juma, soat 9:00–17:00."
        ),
        (
            "Для получения психологической помощи можно напрямую связаться с психологами "
            "академии или записаться на приём через деканат. Все обращения сохраняются в "
            "конфиденциальности. Часы работы: понедельник–пятница, 9:00–17:00."
        ),
        (
            "To receive psychological assistance, you can contact the academy psychologists "
            "directly or schedule an appointment through the dean's office. All applications "
            "are kept confidential. Working hours: Monday–Friday, 9:00–17:00."
        ),
    ),
]


class Command(BaseCommand):
    help = "Psixolog maslahatlari uchun seed ma'lumotlarni yuklaydi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Avval tozalaydi")

    def handle(self, *args, **options):
        if options['clear']:
            PsixologXizmat.objects.all().delete()
            PsixologSection.objects.all().delete()
            self.stdout.write(self.style.WARNING("Barcha psixolog ma'lumotlari o'chirildi."))

        for order, title_uz, title_ru, title_en in XIZMATLAR:
            obj, created = PsixologXizmat.objects.update_or_create(
                order=order,
                defaults=dict(
                    title_uz=title_uz,
                    title_ru=title_ru,
                    title_en=title_en,
                    is_active=True,
                ),
            )
            action = "Yaratildi" if created else "Yangilandi"
            self.stdout.write(f"  {action}: {obj.title_uz[:60]}")

        for order, title_uz, title_ru, title_en, content_uz, content_ru, content_en in SECTIONS:
            obj, created = PsixologSection.objects.update_or_create(
                order=order,
                defaults=dict(
                    title_uz=title_uz,
                    title_ru=title_ru,
                    title_en=title_en,
                    content_uz=content_uz,
                    content_ru=content_ru,
                    content_en=content_en,
                    is_active=True,
                ),
            )
            action = "Yaratildi" if created else "Yangilandi"
            self.stdout.write(f"  {action}: {obj.title_uz}")

        self.stdout.write(self.style.SUCCESS(
            f"Psixolog seed: {len(XIZMATLAR)} xizmat, {len(SECTIONS)} bo'lim yozildi."
        ))
