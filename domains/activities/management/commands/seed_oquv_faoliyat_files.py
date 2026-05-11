"""
JSON fayldagi metadata asosida o'quv hujjatlarini IlmiyFaoliyat ga seed qiladi.
JSON: /home/university_usas/oquv_faoliyat_seed.json
Fayllar: /home/university_usas/media/misc/<uuid>.<ext>

Eski IlmiyFaoliyat yozuvlarni o'chiradi (faqat shu kategoriyalarda).
"""
import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from domains.activities.models import IlmiyFaoliyat, IlmiyFaoliyatCategory


JSON_PATH = "/home/university_usas/oquv_faoliyat_seed.json"

# Kategoriya nomlarini slug + 3 til'ga moslab
CATEGORY_MAP = {
    "Malaka talablari": {
        "slug": "malaka-talablari",
        "title_uz": "Malaka talablari",
        "title_ru": "Квалификационные требования",
        "title_en": "Qualification Requirements",
        "icon": "graduation-cap",
        "order": 1,
    },
    "Oʻquv dasturlar": {
        "slug": "oquv-dasturlar",
        "title_uz": "O'quv dasturlar",
        "title_ru": "Учебные программы",
        "title_en": "Curricula",
        "icon": "book-open",
        "order": 2,
    },
    "Oʻquv grafigi": {
        "slug": "oquv-grafigi",
        "title_uz": "O'quv grafigi",
        "title_ru": "Учебный график",
        "title_en": "Academic Schedule",
        "icon": "calendar",
        "order": 3,
    },
    "Oʻquv rejalar": {
        "slug": "oquv-rejalar",
        "title_uz": "O'quv rejalar",
        "title_ru": "Учебные планы",
        "title_en": "Study Plans",
        "icon": "file-text",
        "order": 4,
    },
}

SUB_MAP = {
    "Bakalavr":     {"title_uz": "Bakalavr", "title_ru": "Бакалавр",  "title_en": "Bachelor"},
    "Bakalavriat":  {"title_uz": "Bakalavr", "title_ru": "Бакалавр",  "title_en": "Bachelor"},
    "Magistratura": {"title_uz": "Magistratura", "title_ru": "Магистратура", "title_en": "Master"},
}


class Command(BaseCommand):
    help = "O'quv hujjatlarini JSON va misc/ media'dan IlmiyFaoliyat'ga seed qiladi"

    def handle(self, *args, **options):
        if not os.path.exists(JSON_PATH):
            self.stdout.write(self.style.ERROR(f"JSON topilmadi: {JSON_PATH}"))
            return

        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 1) Eski yozuvlarni o'chirish (faqat shu 4 kategoriyada)
        old_count = 0
        for cat_name, info in CATEGORY_MAP.items():
            slug = info["slug"]
            old = IlmiyFaoliyat.objects.filter(category__slug=slug)
            old |= IlmiyFaoliyat.objects.filter(category__parent__slug=slug)
            old_count += old.count()
            old.delete()
        self.stdout.write(self.style.WARNING(f"Eski yozuvlar o'chirildi: {old_count} ta"))

        # 2) Parent kategoriyalarni yaratish
        parents = {}
        for cat_name, info in CATEGORY_MAP.items():
            parent, _ = IlmiyFaoliyatCategory.objects.update_or_create(
                slug=info["slug"],
                defaults={
                    "title_uz": info["title_uz"],
                    "title_ru": info["title_ru"],
                    "title_en": info["title_en"],
                    "icon": info["icon"],
                    "order": info["order"],
                    "parent": None,
                },
            )
            parents[cat_name] = parent
            self.stdout.write(f"  Kategoriya: {parent.title_uz}")

        # 3) Sub-kategoriyalar (Bakalavr/Magistratura)
        subs = {}
        seen = set()
        for item in data:
            parent_name = item["category"]
            sub_name = item.get("sub")
            if not sub_name:
                continue
            key = (parent_name, sub_name)
            if key in seen:
                continue
            seen.add(key)
            sub_info = SUB_MAP.get(sub_name, {"title_uz": sub_name, "title_ru": sub_name, "title_en": sub_name})
            parent = parents[parent_name]
            sub_slug = f"{parent.slug}-{slugify(sub_info['title_uz'])}"
            sub, _ = IlmiyFaoliyatCategory.objects.update_or_create(
                slug=sub_slug,
                defaults={
                    "title_uz": sub_info["title_uz"],
                    "title_ru": sub_info["title_ru"],
                    "title_en": sub_info["title_en"],
                    "parent": parent,
                    "order": 1,
                },
            )
            subs[key] = sub
            self.stdout.write(f"    Sub: {parent.title_uz} > {sub.title_uz}")

        # 4) Yozuvlarni yaratish
        created = 0
        for item in data:
            parent_name = item["category"]
            sub_name = item.get("sub")
            target = subs.get((parent_name, sub_name)) if sub_name else parents[parent_name]
            IlmiyFaoliyat.objects.create(
                category=target,
                title_uz=item["title"],
                file=item["filename"],
                is_active=True,
                order=created + 1,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"\n{created} ta yozuv yaratildi"))
        self.stdout.write(f"Kategoriyalar: {len(parents)} parent + {len(subs)} sub")
