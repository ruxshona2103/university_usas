# O'ZDSA Backend — Senior Level Arxitektura Hujjati

> **Texnologiya steki:** Django 5.x + DRF + PostgreSQL + Redis + Celery + LibreTranslate (self-hosted) + Docker  
> **Maqsad:** 5000+ foydalanuvchi, 3 til (uz/ru/en), to'liq CMS, talabalar va qabul portali  
> **Arxitektura paradigmasi:** Domain-Driven Design + SOLID + Clean Architecture

---

## 📁 To'liq Loyiha Tuzilmasi

```
ozdsa_backend/
│
├── docker-compose.yml              # Barcha xizmatlar: django, postgres, redis, libretranslate
├── Dockerfile
├── requirements/
│   ├── base.txt                    # Umumiy dependencies
│   ├── dev.txt                     # Development uchun (debug-toolbar, faker)
│   └── prod.txt                    # Production (gunicorn, sentry-sdk)
├── .env.example                    # Muhit o'zgaruvchilari namunasi
├── manage.py
│
├── config/                         # Django loyiha konfiguratsiyasi
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                 # Umumiy sozlamalar
│   │   ├── dev.py                  # DEBUG=True, SQLite/PG, console email
│   │   └── prod.py                 # Gunicorn, ALLOWED_HOSTS, HTTPS
│   ├── urls.py                     # Asosiy API router
│   ├── celery.py                   # Celery konfiguratsiyasi
│   ├── asgi.py
│   └── wsgi.py
│
├── common/                         # DRY: Barcha domenlar uchun umumiy vositalar
│   ├── __init__.py
│   ├── base_models.py              # Abstract modellar (asosiy meros bazasi)
│   ├── exceptions.py               # Global xatolik handlerlari
│   ├── pagination.py               # Standart sahifalash (10, 20, 50)
│   ├── permissions.py              # IsAdminOrReadOnly, IsOwner
│   ├── mixins.py                   # TranslationMixin, SlugMixin
│   └── utils/
│       ├── __init__.py
│       ├── file_upload.py          # Fayl yuklash va validatsiya
│       ├── slug_generator.py       # Avtomatik slug yaratish
│       └── image_optimizer.py     # Rasm kompressiyasi (Pillow)
│
├── infrastructure/                 # Tashqi tizimlar — IoC & DIP
│   ├── __init__.py
│   ├── translation_service/
│   │   ├── __init__.py
│   │   ├── base.py                 # ABC: BaseTranslationService
│   │   └── libre_translate.py      # LibreTranslate implementatsiyasi
│   ├── hemis_client/
│   │   ├── __init__.py
│   │   ├── base.py                 # ABC: BaseHemisClient
│   │   └── client.py               # Hemis API HTTP client
│   ├── unilibrary_client/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── client.py
│   ├── redis_cache.py              # Cache wrapper (get/set/invalidate)
│   └── email_service/
│       ├── __init__.py
│       ├── base.py                 # ABC: BaseEmailService
│       └── smtp_service.py
│
└── domains/                        # ASOSIY BIZNES LOGIKA
    │
    ├── pages/                      # Statik sahifalar & Sayt konfiguratsiyasi
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── site_config.py      # Singleton: email, tel, prezident gapi, video URL
    │   │   ├── partner.py          # Hamkorlar logolari
    │   │   └── rating.py           # Milliy/xalqaro reyting
    │   ├── api/
    │   │   ├── views.py
    │   │   ├── serializers.py
    │   │   └── urls.py
    │   ├── admin.py
    │   ├── services.py
    │   └── selectors.py
    │
    ├── academic/                   # Akademiya bo'limi
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── about.py            # AcademyHistory, Requisites
    │   │   ├── structure.py        # Faculty, Department, Center, Institute
    │   │   ├── staff.py            # Rector, Dean, Professor, CouncilMember
    │   │   ├── document.py         # NormativeDoc, Regulation
    │   │   └── building.py         # Campus, Building (o'quv binolari)
    │   ├── api/
    │   │   ├── views.py
    │   │   ├── serializers.py
    │   │   └── urls.py
    │   ├── admin.py
    │   ├── services.py
    │   └── selectors.py
    │
    ├── activity/                   # Faoliyat bo'limi
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── scientific.py       # ScientificCouncil, ScientificProject, Doctorantura
    │   │   ├── cultural.py         # StudentCouncil, GreenAcademy, StudentDorm
    │   │   ├── financial.py        # ContractPrice, Vehicle
    │   │   └── educational.py      # Curriculum, Textbook (Bakalavr/Magistr)
    │   ├── api/
    │   │   ├── views.py
    │   │   ├── serializers.py
    │   │   └── urls.py
    │   ├── admin.py
    │   ├── services.py
    │   └── selectors.py
    │
    ├── international/              # Xalqaro aloqalar
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── partner_org.py      # InternationalPartnerOrg
    │   │   ├── foreign_staff.py    # ForeignProfessor (biz haqimizda fikri)
    │   │   └── announcement.py     # InternationalAnnouncement
    │   ├── api/
    │   │   ├── views.py
    │   │   ├── serializers.py
    │   │   └── urls.py
    │   ├── admin.py
    │   ├── services.py
    │   └── selectors.py
    │
    ├── students/                   # Talabalarga bo'limi
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── guide.py            # StudentGuide (Bakalavr/Magistr)
    │   │   ├── schedule.py         # ExamSchedule, LessonSchedule
    │   │   ├── scholarship.py      # Scholarship info
    │   │   └── course_material.py  # SubjectManual, NewBook
    │   ├── api/
    │   │   ├── views.py
    │   │   ├── serializers.py
    │   │   └── urls.py
    │   ├── admin.py
    │   ├── services.py
    │   └── selectors.py
    │
    ├── news/                       # Axborot xizmati
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── news.py             # News (PublishableContent dan meros)
    │   │   ├── event.py            # Event (PublishableContent dan meros)
    │   │   ├── announcement.py     # Announcement (PublishableContent dan meros)
    │   │   ├── gallery.py          # PhotoGallery, VideoGallery
    │   │   └── competition.py      # Competition (Tanlovlar)
    │   ├── api/
    │   │   ├── views.py
    │   │   ├── serializers.py
    │   │   └── urls.py
    │   ├── admin.py
    │   ├── tasks.py                # Celery: auto_translate_content
    │   ├── signals.py              # post_save → tarjima trigeri
    │   ├── services.py
    │   └── selectors.py
    │
    ├── admissions/                 # Qabul bo'limi
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── quota.py            # AdmissionQuota (Bakalavr/Magistr/Xorijiy)
    │   │   ├── document.py         # AdmissionDocument, Rule
    │   │   ├── contract.py         # ContractPrice, EnhancedContract
    │   │   └── faq.py              # FAQ (Savol-javob)
    │   ├── api/
    │   │   ├── views.py
    │   │   ├── serializers.py
    │   │   └── urls.py
    │   ├── admin.py
    │   ├── services.py
    │   └── selectors.py
    │
    ├── contact/                    # Aloqa + Rektorga murojaat
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── appeal.py           # RectorAppeal, ContactMessage
    │   │   └── faq.py              # PublicFAQ + javobi
    │   ├── api/
    │   │   ├── views.py
    │   │   ├── serializers.py
    │   │   └── urls.py
    │   ├── admin.py
    │   ├── services.py             # email_service orqali xat yuborish
    │   └── selectors.py
    │
    └── alumni/                     # Faxrlarimiz
        ├── models/
        │   ├── __init__.py
        │   ├── graduate.py         # Graduate (Bitiruvchilar)
        │   ├── honored_teacher.py  # HonoredTeacher (Faxrli ustozlar)
        │   └── star.py             # AcademyStar (OZDSA yulduzlari)
        ├── api/
        │   ├── views.py
        │   ├── serializers.py
        │   └── urls.py
        ├── admin.py
        ├── services.py
        └── selectors.py
```

---

## 🧱 Abstract Base Modellar (common/base_models.py)

```python
from django.db import models
from django.utils.text import slugify

# ——————————————————————————————————————————
# 1. VAQT TAMG'ASI — barcha modellar uchun asos
# ——————————————————————————————————————————
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ——————————————————————————————————————————
# 2. KO'P TIL — uz / ru / en fieldlar
# ——————————————————————————————————————————
class TranslatableModel(TimeStampedModel):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255, blank=True)
    title_en = models.CharField(max_length=255, blank=True)

    # Tarjima holati (UI uchun)
    is_translated = models.BooleanField(default=False)

    def get_title(self, lang: str = 'uz') -> str:
        value = getattr(self, f'title_{lang}', '')
        return value if value else self.title_uz

    class Meta:
        abstract = True


# ——————————————————————————————————————————
# 3. ASOSIY KONTENT — Yangilik, Tadbir, E'lon
#    barcha kontentlar shu modeldan voris oladi
# ——————————————————————————————————————————
class PublishableContent(TranslatableModel):
    # Asosiy media
    image           = models.ImageField(upload_to='content/%Y/%m/')
    video_url       = models.URLField(blank=True, help_text="YouTube/CDN URL")

    # Ko'p tilli matnlar
    text_uz         = models.TextField()
    text_ru         = models.TextField(blank=True)
    text_en         = models.TextField(blank=True)

    description_uz  = models.TextField(blank=True, help_text="Qisqa annotatsiya")
    description_ru  = models.TextField(blank=True)
    description_en  = models.TextField(blank=True)

    # SEO
    keywords        = models.CharField(max_length=500, blank=True)
    slug            = models.SlugField(unique=True, blank=True, max_length=300)

    # Holat
    date            = models.DateField()
    is_published    = models.BooleanField(default=False)
    views           = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_uz)
        super().save(*args, **kwargs)

    def get_text(self, lang: str = 'uz') -> str:
        value = getattr(self, f'text_{lang}', '')
        return value if value else self.text_uz

    def get_description(self, lang: str = 'uz') -> str:
        value = getattr(self, f'description_{lang}', '')
        return value if value else self.description_uz


# ——————————————————————————————————————————
# 4. YASHIRIN O'CHIRISH (Soft Delete)
# ——————————————————————————————————————————
class SoftDeleteModel(TimeStampedModel):
    is_active   = models.BooleanField(default=True)
    deleted_at  = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
```

---

## 📌 Domain Modellar

### `domains/pages/models/site_config.py` — Singleton
```python
class SiteConfig(TimeStampedModel):
    """
    SINGLETON PATTERN: Sayt bo'ylab yagona konfiguratsiya.
    Admin panelda faqat bitta yozuv bo'ladi.
    """
    # Header ma'lumotlari
    email           = models.EmailField()
    phone           = models.CharField(max_length=25)
    address_uz      = models.CharField(max_length=300)
    address_ru      = models.CharField(max_length=300, blank=True)
    address_en      = models.CharField(max_length=300, blank=True)

    # Prezident iqtibosi (header qismida dinamik)
    president_quote_uz  = models.TextField()
    president_quote_ru  = models.TextField(blank=True)
    president_quote_en  = models.TextField(blank=True)
    president_name      = models.CharField(max_length=100, default="Sh. Mirziyoyev")

    # Promo video (bosh sahifadagi kino)
    promo_video_url     = models.URLField(blank=True)

    # Ijtimoiy tarmoqlar
    telegram    = models.URLField(blank=True)
    instagram   = models.URLField(blank=True)
    facebook    = models.URLField(blank=True)
    youtube     = models.URLField(blank=True)
    twitter     = models.URLField(blank=True)

    # Akademiya statistikasi (bosh sahifa raqamlari)
    faculties_count     = models.PositiveSmallIntegerField(default=0)
    departments_count   = models.PositiveSmallIntegerField(default=0)
    programs_count      = models.PositiveSmallIntegerField(default=0)
    teachers_count      = models.PositiveIntegerField(default=0)
    students_count      = models.PositiveIntegerField(default=0)
    buildings_count     = models.PositiveSmallIntegerField(default=0)
    auditoriums_count   = models.PositiveSmallIntegerField(default=0)
    joint_programs_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Sayt sozlamalari"

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton: har doim bitta yozuv
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
```

### `domains/news/models/news.py` — Voris olish
```python
from common.base_models import PublishableContent

class NewsCategory(models.TextChoices):
    NEWS        = 'news',        'Yangiliklar'
    ANNOUNCEMENT = 'announcement', "E'lon"
    ANTI_CORRUPT = 'anti_corrupt', 'Korrupsiyaga qarshi'
    GREEN       = 'green',       'Yashil Akademiya'
    WORLD       = 'world',       'Dunyo'
    COMPETITION = 'competition', 'Tanlovlar'

class News(PublishableContent):
    """PublishableContent dan barcha fieldlarni meros oladi:
       image, title_uz/ru/en, text_uz/ru/en,
       description_uz/ru/en, keywords, date, slug, video_url
    """
    category    = models.CharField(max_length=20, choices=NewsCategory.choices)
    source      = models.CharField(max_length=200, blank=True)  # Manba

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        db_table = "news_news"
```

### `domains/news/models/event.py` — Kutilayotgan tadbirlar
```python
class Event(PublishableContent):
    """Kutilayotgan tadbirlar — PublishableContent dan meros"""
    location_uz     = models.CharField(max_length=300)
    location_ru     = models.CharField(max_length=300, blank=True)
    location_en     = models.CharField(max_length=300, blank=True)
    start_datetime  = models.DateTimeField()
    end_datetime    = models.DateTimeField(null=True, blank=True)
    event_link      = models.URLField(blank=True, help_text="To'liq ma'lumot linki")

    def get_location(self, lang='uz'):
        return getattr(self, f'location_{lang}', '') or self.location_uz

    class Meta:
        verbose_name = "Tadbir"
        db_table = "news_event"
```

### `domains/academic/models/structure.py`
```python
class Faculty(TranslatableModel, SoftDeleteModel):
    name_uz     = models.CharField(max_length=200)
    name_ru     = models.CharField(max_length=200, blank=True)
    name_en     = models.CharField(max_length=200, blank=True)
    slug        = models.SlugField(unique=True)
    dean        = models.ForeignKey('staff.Professor', null=True, on_delete=models.SET_NULL)
    description_uz = models.TextField(blank=True)
    order       = models.PositiveSmallIntegerField(default=0)

class Department(TranslatableModel, SoftDeleteModel):
    faculty     = models.ForeignKey(Faculty, related_name='departments', on_delete=models.CASCADE)
    name_uz     = models.CharField(max_length=200)
    name_ru     = models.CharField(max_length=200, blank=True)
    name_en     = models.CharField(max_length=200, blank=True)
    head        = models.ForeignKey('staff.Professor', null=True, on_delete=models.SET_NULL)
```

### `domains/contact/models/appeal.py`
```python
class AppealStatus(models.TextChoices):
    NEW         = 'new',         'Yangi'
    IN_REVIEW   = 'in_review',   "Ko'rib chiqilmoqda"
    ANSWERED    = 'answered',    'Javob berildi'
    REJECTED    = 'rejected',    'Rad etildi'

class RectorAppeal(TimeStampedModel):
    full_name   = models.CharField(max_length=200)
    email       = models.EmailField()
    phone       = models.CharField(max_length=20)
    subject     = models.CharField(max_length=300)
    message     = models.TextField()
    attachment  = models.FileField(upload_to='appeals/', null=True, blank=True)
    status      = models.CharField(max_length=20, choices=AppealStatus.choices, default=AppealStatus.NEW)
    answer      = models.TextField(blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Rektorga murojaat"
        db_table = "contact_rector_appeal"
```

---

## 🌐 LibreTranslate Integration

### `infrastructure/translation_service/base.py`
```python
from abc import ABC, abstractmethod

class BaseTranslationService(ABC):
    """
    DIP: Barcha tarjima xizmatlari shu interface ni implement qiladi.
    Ertaga Google/DeepL ga o'tish uchun faqat shu classni almashtirish kifoya.
    """
    SUPPORTED_LANGUAGES = ['uz', 'ru', 'en']

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Berilgan matnni tarjima qilib qaytaradi"""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Xizmat ishlab turibdimi?"""
        ...

    def translate_to_all(self, text: str, source_lang: str = 'uz') -> dict:
        """
        Bir marta chaqirib barcha tillarga tarjima qiladi.
        Qaytaradi: {'ru': '...', 'en': '...'}
        """
        result = {}
        for lang in self.SUPPORTED_LANGUAGES:
            if lang != source_lang:
                result[lang] = self.translate(text, source_lang, lang)
        return result
```

### `infrastructure/translation_service/libre_translate.py`
```python
import requests
import logging
from .base import BaseTranslationService

logger = logging.getLogger(__name__)

class LibreTranslateService(BaseTranslationService):
    """
    Self-hosted LibreTranslate integratsiyasi.
    Docker da port 5000 da ishlaydi.
    """
    def __init__(self, base_url: str = "http://libretranslate:5000", api_key: str = ""):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = 30  # sekundlar

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not text or not text.strip():
            return ''
        if source_lang == target_lang:
            return text

        # O'zbek tili LibreTranslate da "uz" kodi bilan
        lang_map = {'uz': 'uz', 'ru': 'ru', 'en': 'en'}
        src = lang_map.get(source_lang, source_lang)
        tgt = lang_map.get(target_lang, target_lang)

        try:
            payload = {
                'q': text,
                'source': src,
                'target': tgt,
                'format': 'text',
            }
            if self.api_key:
                payload['api_key'] = self.api_key

            response = requests.post(
                f"{self.base_url}/translate",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            return data.get('translatedText', text)

        except requests.exceptions.ConnectionError:
            logger.warning("LibreTranslate server bilan aloqa yo'q. Asl matn qaytarildi.")
            return text
        except requests.exceptions.Timeout:
            logger.warning("LibreTranslate so'rovi vaqt limitidan oshdi.")
            return text
        except Exception as e:
            logger.error(f"LibreTranslate xato: {e}")
            return text

    def is_available(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/languages", timeout=5)
            return r.status_code == 200
        except Exception:
            return False
```

### `domains/news/tasks.py` — Celery async tarjima
```python
from celery import shared_task
from django.apps import apps
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def auto_translate_content(self, app_label: str, model_name: str, object_id: int):
    """
    Background da ishlaydi. Admin uz yozadi → signal → shu task chaqiriladi.
    Xato bo'lsa 3 marta qayta urinadi (60 sekunddan keyin).
    """
    from infrastructure.translation_service.libre_translate import LibreTranslateService

    try:
        model = apps.get_model(app_label, model_name)
        obj = model.objects.get(id=object_id)
        service = LibreTranslateService()

        if not service.is_available():
            logger.warning("LibreTranslate mavjud emas. Task keyinga qoldirildi.")
            raise self.retry()

        # Tarjima qilinadigan field juftliklari
        translatable_fields = [
            ('title_uz', 'title_ru', 'title_en'),
            ('text_uz', 'text_ru', 'text_en'),
            ('description_uz', 'description_ru', 'description_en'),
        ]

        updated_fields = []
        for uz_field, ru_field, en_field in translatable_fields:
            uz_value = getattr(obj, uz_field, '')
            if not uz_value:
                continue

            # Faqat bo'sh bo'lsa tarjima qil (qo'lda yozilganini o'chirma)
            if not getattr(obj, ru_field, ''):
                setattr(obj, ru_field, service.translate(uz_value, 'uz', 'ru'))
                updated_fields.append(ru_field)

            if not getattr(obj, en_field, ''):
                setattr(obj, en_field, service.translate(uz_value, 'uz', 'en'))
                updated_fields.append(en_field)

        if updated_fields:
            updated_fields.append('is_translated')
            obj.is_translated = True
            obj.save(update_fields=updated_fields)
            logger.info(f"{model_name} id={object_id} tarjima qilindi: {updated_fields}")

    except model.DoesNotExist:
        logger.error(f"{model_name} id={object_id} topilmadi")
    except Exception as exc:
        logger.error(f"Tarjima xatosi {model_name} id={object_id}: {exc}")
        raise self.retry(exc=exc)
```

### `domains/news/signals.py` — Avtomatik trigger
```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models.news import News
from .models.event import Event
from .tasks import auto_translate_content

def trigger_translation(sender, instance, created, **kwargs):
    """
    Yangilik yoki tadbir saqlanganda tarjimani ishga tushiradi.
    Faqat uz matni bor, ru yoki en yo'q bo'lsa ishlaydi.
    """
    needs_translation = (
        instance.title_uz and
        (not instance.title_ru or not instance.title_en)
    )
    if needs_translation and instance.is_published:
        app_label = instance._meta.app_label
        model_name = instance.__class__.__name__
        # 5 soniyadan keyin ishga tushiradi (tranzaksiya tugashini kutadi)
        auto_translate_content.apply_async(
            args=[app_label, model_name, instance.pk],
            countdown=5
        )

# Barcha kontent modellariga signal
for model_class in [News, Event]:
    post_save.connect(trigger_translation, sender=model_class)
```

---

## 🔌 API Endpointlar Ro'yxati

```
BASE URL: /api/v1/

# ── KONFIGURATSIYA ──────────────────────────────────
GET    /config/site/              → Header ma'lumotlari (email, tel, prezident gapi, video)
GET    /config/partners/          → Hamkorlar ro'yxati
GET    /config/ratings/           → Milliy/xalqaro reytinglar

# ── AKADEMIYA ───────────────────────────────────────
GET    /academic/history/         → Akademiya tarixi
GET    /academic/faculties/       → Fakultetlar ro'yxati
GET    /academic/faculties/{slug}/→ Bitta fakultet + kafedralar
GET    /academic/departments/     → Kafedralar
GET    /academic/staff/           → Rahbariyat
GET    /academic/documents/       → Me'yoriy hujjatlar
GET    /academic/buildings/       → O'quv binolari

# ── FAOLIYAT ────────────────────────────────────────
GET    /activity/scientific/      → Ilmiy faoliyat
GET    /activity/cultural/        → Madaniy-ma'rifiy faoliyat
GET    /activity/financial/       → Moliyaviy faoliyat (kontrakt narxlari)
GET    /activity/materials/       → O'quv-uslubiy ta'minot

# ── XALQARO ALOQALAR ────────────────────────────────
GET    /international/partners/   → Xorijiy hamkor tashkilotlar
GET    /international/professors/ → Xorijlik professorlar (dinamik fikrlar)
GET    /international/announcements/ → Xalqaro e'lonlar

# ── TALABALARGA ─────────────────────────────────────
GET    /students/guides/          → Yo'riqnomalar (Bak/Mag)
GET    /students/schedules/       → Dars jadvallari
GET    /students/scholarships/    → Stipendiyalar
GET    /students/materials/       → O'quv adabiyotlari

# ── AXBOROT XIZMATI ─────────────────────────────────
GET    /news/                     → Yangiliklar ro'yxati (?category=news)
GET    /news/{slug}/              → Bitta yangilik
GET    /news/events/              → Kutilayotgan tadbirlar
GET    /news/events/{slug}/       → Bitta tadbir
GET    /news/gallery/photos/      → Foto galereya
GET    /news/gallery/videos/      → Video galereya
GET    /news/competitions/        → Tanlovlar

# ── QABUL ───────────────────────────────────────────
GET    /admissions/quotas/        → Qabul rejalari (Bak/Mag/Xorijiy)
GET    /admissions/documents/     → Hujjatlar ro'yxati
GET    /admissions/contracts/     → Kontrakt narxlari
GET    /admissions/faq/           → Ko'p so'raladigan savollar

# ── ALOQA ───────────────────────────────────────────
POST   /contact/appeal/           → Rektorga murojaat yuborish
POST   /contact/message/          → Umumiy murojaat
GET    /contact/faq/              → Savol-javoblar

# ── FAXRLARIMIZ ─────────────────────────────────────
GET    /alumni/graduates/         → Bitiruvchilar
GET    /alumni/teachers/          → Faxrli ustozlar
GET    /alumni/stars/             → OZDSA yulduzlari

# ── INFRA ───────────────────────────────────────────
GET    /health/                   → Server holati (monitoring uchun)
GET    /translation/status/       → LibreTranslate holati (admin uchun)
POST   /admin/retranslate/        → Qo'lda tarjimani qayta ishga tushirish
```

---

## 🐳 Docker Compose (docker-compose.yml)

```yaml
version: '3.9'

services:
  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ozdsa_db
      POSTGRES_USER: ozdsa_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "ozdsa_user"]
      interval: 10s

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  libretranslate:
    image: libretranslate/libretranslate:latest
    ports:
      - "5000:5000"
    environment:
      LT_LOAD_ONLY: "uz,ru,en"   # Faqat kerakli tillar (tezroq yuklaydi)
      LT_UPDATE_MODELS: "true"
    volumes:
      - lt_data:/home/libretranslate/.local/share
    restart: unless-stopped

  django:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes:
      - .:/app
      - media_data:/app/media
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
      libretranslate:
        condition: service_started
    ports:
      - "8000:8000"

  celery_worker:
    build: .
    command: celery -A config worker --loglevel=info --concurrency=4
    volumes:
      - .:/app
    env_file: .env
    depends_on:
      - redis
      - db
      - libretranslate

  celery_beat:
    build: .
    command: celery -A config beat --loglevel=info
    volumes:
      - .:/app
    env_file: .env
    depends_on:
      - redis

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - media_data:/media
      - static_data:/static
    depends_on:
      - django

volumes:
  postgres_data:
  redis_data:
  lt_data:
  media_data:
  static_data:
```

---

## 📦 Requirements (requirements/base.txt)

```
# Core
Django==5.1.4
djangorestframework==3.15.2
django-cors-headers==4.4.0
django-filter==24.3

# Database
psycopg2-binary==2.9.10

# Async & Queue
celery==5.4.0
redis==5.2.0
django-celery-results==2.5.1
django-celery-beat==2.7.0

# Media
Pillow==11.0.0
python-slugify==8.0.4

# HTTP (LibreTranslate uchun)
requests==2.32.3

# Storage (Production)
boto3==1.35.0          # AWS S3 yoki MinIO uchun
django-storages==1.14.4

# Security
django-ratelimit==4.1.0
```

---

## ⚙️ Sozlamalar (config/settings/base.py) — asosiy qismlar

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',

    # Domenlar
    'domains.pages',
    'domains.academic',
    'domains.activity',
    'domains.international',
    'domains.students',
    'domains.news',
    'domains.admissions',
    'domains.contact',
    'domains.alumni',
]

# DRF sozlamalari
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',        # Noma'lum foydalanuvchi
        'contact': '10/hour',      # Murojaat yuborish cheklovi
    },
}

# Celery
CELERY_BROKER_URL = env('REDIS_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tashkent'

# LibreTranslate
LIBRETRANSLATE_URL = env('LIBRETRANSLATE_URL', default='http://libretranslate:5000')
LIBRETRANSLATE_API_KEY = env('LIBRETRANSLATE_API_KEY', default='')

# Media fayllar
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# CORS (Frontend uchun)
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[
    'http://localhost:3000',
    'https://usas.uz',
])
```

---

## 🔒 Xavfsizlik va Ishlash Unumdorligi

### Kesh strategiyasi (Redis)
```python
# Bosh sahifa ma'lumotlari: 1 soat kesh (kam o'zgaradi)
# Yangiliklar ro'yxati: 15 daqiqa kesh
# Bitta yangilik sahifasi: 30 daqiqa kesh
# SiteConfig: 24 soat kesh (singleton)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'TIMEOUT': 60 * 15,  # 15 daqiqa default
    }
}

# View da kesh ishlatish
from django.views.decorators.cache import cache_page

@cache_page(60 * 60)  # 1 soat
def site_config_view(request): ...
```

### Rate Limiting (Murojaat spamiga qarshi)
```python
# contact/api/views.py
from django_ratelimit.decorators import ratelimit

class RectorAppealCreateView(CreateAPIView):
    throttle_scope = 'contact'   # soatiga 10 ta murojaat
```

### Select Related (N+1 muammo oldini olish)
```python
# academic/selectors.py
class FacultySelector:
    @staticmethod
    def get_all_with_departments():
        return Faculty.objects.filter(
            is_active=True
        ).select_related('dean').prefetch_related(
            'departments',
            'departments__head'
        ).order_by('order')
```

---

## 📊 Ma'lumotlar bazasi Jadvallar Xaritasi

```
pages_siteconfig          → 1 yozuv (singleton)
pages_partner             → Hamkorlar
pages_rating              → Reytinglar

academic_faculty          → Fakultetlar
academic_department       → Kafedralar (faculty FK)
academic_staff            → Xodimlar/O'qituvchilar
academic_normativedoc     → Me'yoriy hujjatlar
academic_building         → O'quv binolari

news_news                 → Yangiliklar (PublishableContent)
news_event                → Tadbirlar (PublishableContent)
news_announcement         → E'lonlar (PublishableContent)
news_gallery              → Galereya

admissions_quota          → Qabul kvotalari
admissions_document       → Hujjat talablari
admissions_contract       → Kontrakt narxlari

contact_rectorappeal      → Rektorga murojaatlar
contact_message           → Umumiy murojaatlar
contact_faq               → Savol-javoblar

alumni_graduate           → Bitiruvchilar
alumni_honoredteacher     → Faxrli ustozlar
alumni_academystar        → OZDSA yulduzlari

django_celery_results_taskresult → Celery natijalari
```

---

## 🚀 Deployment Tartib

```bash
# 1. LibreTranslate modellarini yukla (birinchi ishga tushirishda)
docker compose up libretranslate  # 10-15 daqiqa kutiladi (uz/ru/en modellari)

# 2. Boshqa xizmatlarni ishga tushir
docker compose up -d

# 3. DB migratsiyalar
docker compose exec django python manage.py migrate

# 4. Superuser yaratish
docker compose exec django python manage.py createsuperuser

# 5. Statik fayllar
docker compose exec django python manage.py collectstatic

# 6. Tarjima xizmatini tekshirish
curl http://localhost:5000/languages
```

---

## ⚡ Tarjima Oqimi Diagrammasi

```
Admin uz tilida yozadi va saqlaydi
         │
         ▼
   post_save signal chiqadi
         │
         ▼
   trigger_translation() → tekshiradi: ru yoki en bo'shmi?
         │
         ▼
   Celery task navbatga qo'shiladi (countdown=5 sek)
         │
         ▼
   Celery Worker qabul qiladi
         │
         ▼
   LibreTranslate.is_available()? ──No──► 60 sek kutib qayta urinadi
         │
        Yes
         ▼
   title_uz → translate(uz→ru) → title_ru
   title_uz → translate(uz→en) → title_en
   text_uz  → translate(uz→ru) → text_ru
   ... (barcha matn fieldlari)
         │
         ▼
   obj.save(update_fields=[...])
   is_translated = True
         │
         ▼
   Admin panelda ✅ belgisi ko'rinadi
```

---

> **Eslatma:** LibreTranslate ning O'zbek→Ingliz tarjimasi sifatini
> tahririyat komandasi tekshirib tasdiqlashi tavsiya etiladi.
> Admin panelda `is_translated` maydoni orqali tarjima holati ko'rinib turadi.
> Yomon tarjima bo'lsa — qo'lda to'g'rilash mumkin, signal uni qaytadan o'chirib yubormaydi.
