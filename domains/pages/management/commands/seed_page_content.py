"""
python manage.py seed_page_content          # yaratadi / yangilaydi
python manage.py seed_page_content --clear  # content_uz larni tozalab qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.pages.models import NavbarSubItem

# (slug, title_for_log, content_uz)
PAGES = [
    (
        "st-guide",
        "Yo'riqnoma (bakalavr)",
        """Talabalarning o'qishini ko'chirish, qayta tiklash va o'qishdan chetlashtirish O'zbekiston Respublikasi Vazirlar Mahkamasining 2025-yil 13-sentabrdagi 578-son qarori bilan tasdiqlangan "Oliy ta'lim muassasalariga o'qishga qabul qilish, talabalar o'qishini ko'chirish, qayta tiklash va o'qishdan chetlashtirish tartibi to'g'risida Nizom"ga muvofiq amalga oshiriladi.

UMUMIY QOIDALAR

Mos va turdosh yo'nalishlar belgilash mezonlari:
• Mos ta'lim yo'nalishlari — nomlanishi bir xil bo'lgan bakalavriat ta'lim yo'nalishlari (magistratura mutaxassisliklari).
• Turdosh ta'lim yo'nalishlari — o'quv rejalari va dasturlari mazmunan yaqin bo'lgan bakalavriat ta'lim yo'nalishlari. Ro'yxati Vazirlik tomonidan tasdiqlanadi.
• O'qishni ko'chirish — talabaning bir oliy ta'lim tashkilotidan boshqasiga yoki bir ta'lim yo'nalishidan boshqasiga ko'chirilishi.
• O'qishni ko'chirib tiklash — sobiq talabaning boshqa OTM yoki yo'nalishda o'qishini davom ettirish uchun ko'chirib tiklanishi.
• O'qishni qayta tiklash — sobiq talabaning xuddi shu ta'lim yo'nalishida o'qishini davom ettirishi uchun tiklanishi.

KO'CHIRISH MUDDATLARI

Kuzgi semestr: ariza topshirish — 15-iyuldan 5-avgustgacha; ko'rib chiqish — 6-avgustdan 30-avgustgacha.
Bahorgi semestr: ariza topshirish — 10-yanvardan 20-yanvargacha; ko'rib chiqish — 21-yanvardan 10-fevralgacha.

ZARUR HUJJATLAR

1. Ariza (o'qigan muassasa, yo'nalish, sabablar ko'rsatilgan holda).
2. Reyting daftarchasi yoki akademik ma'lumotnoma (transkript).
3. Pasport nusxasi.
4. Sababni asoslovchi hujjatlar nusxasi (nikoh guvohnomasi, buyruq va h.k.).

RUXSAT BERILMAYDIGAN HOLATLAR

• Akkreditatsiyaga ega bo'lmagan xorijiy OTMlardan ko'chirish.
• Birinchi kursning birinchi semestriga ko'chirish (kasallik, yo'nalish mavjud emasligi holatlari bundan mustasno).
• OTMda mos (turdosh) ta'lim yo'nalishi mavjud bo'lmasa.
• To'lov-kontrakt to'lovi bajarilmagan bo'lsa.
• Akademik ma'lumotnoma belgilangan muddatda taqdim etilmagan bo'lsa.
• Maqsadli qabul qilinganlar boshqa yo'nalishga.
• Talaba qo'shma ta'lim dasturida tahsil olayotgan bo'lsa.

AKADEMIK FARQLAR TALABI

• Reyting tizimida: umumkasbiy va ixtisoslik fanlar bo'yicha farqlar 4 tadan oshmasligi lozim.
• Kreditlar tizimida: GPA ko'rsatkichi 2,4 va undan yuqori bo'lishi lozim.

QAYTA TIKLASH

Ariza topshirish: kuzgi semestr — 15-iyul–5-avgust; bahorgi semestr — 10-yanvar–20-yanvar.
Qaror qabul qilish: kuzgi semestr — 6-avgust–31-avgust; bahorgi semestr — 21-yanvar–10-fevral.
Barcha o'quv shakllari bo'yicha qayta tiklash to'lov-kontrakt asosida amalga oshiriladi. Davlat granti bo'yicha tiklanish faqat yetimlar, I–II guruh nogironligi bo'lgan shaxslar, muddatli harbiy xizmatni o'tagan va akademik ta'tildan belgilangan muddatda qaytgan shaxslar uchun istisno tariqasida mumkin.

O'QISHDAN CHETLASHTIRISH ASOSLARI

• O'z xohishiga ko'ra.
• O'qishni boshqa OTMga ko'chirish.
• Ichki tartib-qoidalar va odob-axloq qoidalarini buzganlik.
• Darslarni uzrsiz 74 soatdan ortiq qoldirganlik (tibbiy ma'lumotnoma mavjud bo'lmasa).
• To'lov-kontrakt to'lovini o'z vaqtida amalga oshirmagan (to'lov-kontrakt bo'yicha talabalar uchun).
• Sud tomonidan ozodlikdan mahrum etilganlik.
• Kirish imtihonlarida tartibni buzganlik (bunday talabalar qayta tiklanmaydi).
• Vafot etganlik.""",
    ),
    (
        "grading-system",
        "Bakalavr baholash tizimi",
        """O'zbekiston davlat sport akademiyasida baholash balli tizimda olib boriladi:

90–100 ball — 5 (A'lo): a'lo natija
75–89 ball  — 4 (Yaxshi): yaxshi natija
60–74 ball  — 3 (Qoniqarli): qoniqarli, yetarli natija
50–59 ball  — 2 (Qoniqarsiz): qayta topshirish kerak
0–49 ball   — 1 (Muvaffaqiyatsiz): juda past natija""",
    ),
    (
        "gpa-credit",
        "GPA va kredit talablari",
        """GPA (Grade Point Average) — talabaning o'rtacha akademik ko'rsatkichi bo'lib, barcha fanlar bo'yicha olingan baholarni kreditlar bilan hisoblab chiqish orqali aniqlanadi.

O'zbekiston davlat sport akademiyasida minimal GPA 2,4 etib belgilangan.

Talaba ushbu ballni saqlashi yoki oshirishi kerak. Aks holda:
• O'qishni ko'chirish yoki tiklash paytida GPA talabi bajarilishi shart (≥ 2,4).
• GPA past bo'lsa, talabaga quyi kursdan (semestrdan) o'qishini davom ettirish taklif qilinishi mumkin.
• Akademik ehtiyot choralar ko'rilishi mumkin.""",
    ),
    (
        "scholarships",
        "Stipendiyalar",
        """O'zbekiston davlat sport akademiyasining bakalavriat ta'lim yo'nalishida hozirgi kunda jami 146 nafar talaba tahsil olmoqda.

Mazkur talabalar O'zbekiston Respublikasi amaldagi normativ-huquqiy hujjatlariga muvofiq ravishda to'liq davlat granti asosida o'qishga qabul qilingan bo'lib, ularning barchasi belgilangan tartibda davlat stipendiyasi bilan ta'minlanadi.""",
    ),
    (
        "st-schedule",
        "Dars jadvali",
        """O'zbekiston davlat sport akademiyasi bakalavriat ta'lim yo'nalishlarida dars mashg'ulotlari asosan ertalabki smenada tashkil etiladi.

Dars mashg'ulotlari quyidagi vaqt oralig'ida o'tkaziladi:

Juftlik    | Boshlanish | Tugash
-----------+------------+-------
I-juftlik  | 09:00      | 10:20
II-juftlik | 10:30      | 11:50
III-juftlik| 12:00      | 13:20
IV-juftlik | 13:30      | 14:50
V-juftlik  | 15:00      | 16:20
VI-juftlik | 16:30      | 17:50""",
    ),
    (
        "final-control",
        "Yakuniy nazorat",
        """O'zbekiston davlat sport akademiyasi bakalavriat ta'lim yo'nalishlarida yakuniy nazorat turlari o'quv fanlarining xususiyatidan kelib chiqib tashkil etiladi.

Asosan, yakuniy nazoratlar fan sillabuslarida belgilangan shaklda o'tkaziladi:
• Og'zaki nazorat
• Yozma ish
• Amaliy sinov
• Test sinovi

Talabalarning fan bo'yicha o'zlashtirish darajasi, nazariy bilimlari hamda amaliy ko'nikmalari kompleks tarzda baholanadi.

Yakuniy nazorat jarayonlari belgilangan tartib va me'yoriy hujjatlar asosida shaffoflik va xolislik tamoyillariga amal qilgan holda tashkil etiladi.""",
    ),
]


class Command(BaseCommand):
    help = "NavbarSubItem static sahifalariga content_uz yozadi (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="content_uz ni tozalab qaytadan yozadi")

    def handle(self, *args, **options):
        updated = skipped = 0
        for slug, title, content_uz in PAGES:
            try:
                item = NavbarSubItem.objects.get(slug=slug)
            except NavbarSubItem.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  [!] topilmadi: {slug}"))
                skipped += 1
                continue

            if options['clear'] or not item.content_uz:
                item.content_uz = content_uz
                item.page_type  = NavbarSubItem.PageType.STATIC
                item.save(update_fields=['content_uz', 'page_type', 'updated_at'])
                self.stdout.write(f"  [~] yozildi: {title}")
                updated += 1
            else:
                self.stdout.write(f"  [=] o'tkazildi (allaqachon bor): {title}")

        self.stdout.write(self.style.SUCCESS(
            f"\nNatija: {updated} ta sahifa yangilandi, {skipped} ta topilmadi."
        ))
