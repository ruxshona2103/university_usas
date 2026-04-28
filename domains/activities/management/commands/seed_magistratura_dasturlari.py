"""
python manage.py seed_magistratura_dasturlari --dir "C:/Users/user/Desktop/OʻzDSA Oʻquv-faoliyat hujjatlari/Oʻquv dasturlar/Magistratura"

O'quv dasturlar → Magistratura bo'limiga PDF fayllarni qo'shadi.
Mavjud ma'lumotlarni o'chirmaydi (esklarini saqlab qoladi).
"""

import os

from django.core.files import File
from django.core.management.base import BaseCommand

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory

LABELS = {
    "3.Magistratura  SSMBQ fan dasturi (3).pdf":                               "SSMBQ fan dasturi (Magistratura)",
    "Adaptiv jismoniy tarbiya va parasportning tibbiy-biologik asoslari.PDF":  "Adaptiv jismoniy tarbiya va parasportning tibbiy-biologik asoslari",
    "Adaptiv jismoniy tarbiya va sportni boshqarish .PDF":                     "Adaptiv jismoniy tarbiya va sportni boshqarish",
    "Adaptiv jismoniy tarbiyada nazorat turlari va sport klassifikatsiyasi.PDF": "Adaptiv jismoniy tarbiyada nazorat turlari va sport klassifikatsiyasi",
    "Adaptiv sog'lomlashtirish jismoniy tarbiya texnologiyalari.PDF":          "Adaptiv sog'lomlashtirish jismoniy tarbiya texnologiyalari",
    "Dastur Magistratura Boks  .pdf":                                          "Boks fan dasturi (Magistratura)",
    "Dastur Sportda ilmiy tadqiqot(3).pdf":                                    "Sportda ilmiy tadqiqot fan dasturi",
    "Eshkak eshishda sportchilarni tayyorlashning ilmiy-uslubiy asoslari .pdf": "Eshkak eshishda sportchilarni tayyorlashning ilmiy-uslubiy asoslari",
    "Event-menejment.PDF":                                                     "Event-menejment",
    "FAN DASTURI DZYUDO MAGISTRATURA.pdf":                                     "Dzyudo fan dasturi (Magistratura)",
    "Ilmiy tadqiqot metodologiyasi.PDF":                                       "Ilmiy tadqiqot metodologiyasi",
    "Korporativ menejmen.PDF":                                                 "Korporativ menejment",
    "Menejmentda zamonaviy kommunikatsiyalar.PDF":                             "Menejmentda zamonaviy kommunikatsiyalar",
    "Sort iqtisodiyoti va menejmet.PDF":                                       "Sport iqtisodiyoti va menejment",
    "Sport Inshootlari Marketing.PDF":                                         "Sport inshootlari marketingi",
    "Sport faoliyatining huquqiy ta'minlanishi.PDF":                           "Sport faoliyatining huquqiy ta'minlanishi",
    "Sport inshootlarini boshqarish.PDF":                                      "Sport inshootlarini boshqarish",
    "Sport marketingi.PDF":                                                    "Sport marketingi",
    "Sport menejmenti .PDF":                                                   "Sport menejmenti",
    "Sport morfologiyasi.PDF":                                                 "Sport morfologiyasi",
    "Sport sohasida raqamli iqtisodiyot.PDF":                                  "Sport sohasida raqamli iqtisodiyot",
    "Sportda marketing kommunikasiyasi.PDF":                                   "Sportda marketing kommunikasiyasi",
    "Sportda matematik modellashtirish.PDF":                                   "Sportda matematik modellashtirish",
    "Sportda matematik-statik tahlil.PDF":                                     "Sportda matematik-statik tahlil",
    "Taekvondo Magistrarura fan dasturi (5).pdf":                              "Taekvondo fan dasturi (Magistratura)",
    "Xalqaro sport huquqi.PDF":                                                "Xalqaro sport huquqi",
}


class Command(BaseCommand):
    help = "Magistratura o'quv dasturlarini DB ga qo'shadi (mavjudlarini o'chirmaydi)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir',
            required=True,
            help="Magistratura PDF fayllar joylashgan papka yo'li",
        )

    def handle(self, *args, **options):
        pdf_dir = options['dir']

        if not os.path.isdir(pdf_dir):
            self.stdout.write(self.style.ERROR(f"Papka topilmadi: {pdf_dir}"))
            return

        # 1. Root kategoriyani topish
        try:
            root_cat = IlmiyFaoliyatCategory.objects.get(slug='oquv-dasturlar')
        except IlmiyFaoliyatCategory.DoesNotExist:
            self.stdout.write(self.style.ERROR(
                "'oquv-dasturlar' kategoriyasi topilmadi! "
                "Avval: python manage.py seed_oquv_faoliyat"
            ))
            return

        # 2. Magistratura child kategoriyasini yaratish yoki olish
        child_cat, created = IlmiyFaoliyatCategory.objects.get_or_create(
            slug='oquv-dasturlar-magistratura',
            defaults={
                'title_uz': 'Magistratura',
                'title_ru': 'Магистратура',
                'title_en': 'Master',
                'parent':   root_cat,
                'order':    2,
            },
        )
        action = 'Yaratildi' if created else 'Mavjud'
        self.stdout.write(f"[{action}] Child kategoriya: {child_cat.title_uz}")

        # Keyingi order raqamini aniqlash
        last_order = IlmiyFaoliyat.objects.filter(category=child_cat).order_by('-order').values_list('order', flat=True).first()
        next_order = (last_order or 0) + 1

        # 3. Har bir PDF ni qayta ishlash
        filenames = sorted(os.listdir(pdf_dir))
        added = 0
        skipped = 0

        for filename in filenames:
            if not filename.lower().endswith('.pdf'):
                continue

            label = LABELS.get(filename, os.path.splitext(filename)[0].strip())
            filepath = os.path.join(pdf_dir, filename)

            # Allaqachon mavjud bo'lsa o'tkazib yuborish
            if IlmiyFaoliyat.objects.filter(category=child_cat, title_uz=label).exists():
                self.stdout.write(f"  [Mavjud]  {label[:80]}")
                skipped += 1
                continue

            item = IlmiyFaoliyat(
                category=child_cat,
                title_uz=label,
                order=next_order,
                is_active=True,
            )
            with open(filepath, 'rb') as f:
                item.file.save(filename, File(f), save=False)
            item.save()

            self.stdout.write(self.style.SUCCESS(f"  [Qo'shildi] {label[:80]}"))
            added += 1
            next_order += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nTugadi: {added} ta qo'shildi, {skipped} ta mavjud edi."
        ))
