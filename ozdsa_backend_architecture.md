# O'ZDSA Backend — Arxitektura Hujjati (TZ asosida)

> **Texnologiya steki:** Django 5.x + DRF + PostgreSQL + Redis + Celery + Docker
> **Maqsad:** usas.uz rasmiy sayti, 3 til (uz/ru/en), to'liq CMS
> **Paradigma:** Domain-Driven Design + SOLID + Clean Architecture + **DRY**

---

## Asosiy DRY Prinsipi — Takrorlanishni Oldini Olish

TZ da bir entity ko'p joyda uchraydi. Yechim: **3 universal model**:

| Muammo | Noto'g'ri yondashuv | DRY yondashuv |
|--------|---------------------|---------------|
| Rektor, Prorektor, Dekan, Kengash a'zosi | Har biri alohida model | **Staff** (role field bilan) |
| Fakultet, Kafedra, Institut, Markaz, Tuzilma | Har biri alohida model | **OrganizationUnit** (parent FK bilan) |
| Me'yoriy hujjatlar (Akademiya/Qabul/Faoliyat) | Har bir bo'limda alohida | **Document** (category FK bilan) |

---

## Loyiha Fayl Tuzilmasi

```
university_usas/
│
├── config/
│   ├── settings/base.py
│   ├── settings/dev.py
│   ├── settings/prod.py
│   ├── urls.py
│   └── celery.py
│
├── common/                         # DRY: Barcha domenlar uchun umumiy
│   ├── base_models.py              # Abstract modellar
│   ├── pagination.py
│   ├── permissions.py
│   └── utils/
│       ├── file_upload.py
│       └── slug_generator.py
│
├── infrastructure/
│   ├── translation_service/        # LibreTranslate ABC
│   ├── hemis_client/               # Hemis API client
│   ├── email_service/              # SMTP service
│   └── redis_cache.py
│
└── domains/
    ├── pages/          # Sayt konfiguratsiyasi va statik sahifalar
    ├── academic/       # Akademiya: Tuzilma + Xodimlar + Tarixi
    ├── documents/      # UNIVERSAL hujjatlar (barcha bo'limlar uchun)
    ├── news/           # Axborot xizmati
    ├── activity/       # Faoliyat (Ilmiy, Madaniy, Moliyaviy)
    ├── international/  # Xalqaro aloqalar
    ├── students/       # Talabalarga
    ├── admissions/     # Qabul
    ├── contact/        # Aloqa + Rektorga murojaat
    └── alumni/         # Faxrlarimiz
```

---

## Abstract Base Modellar (`common/base_models.py`)

```python
class TimeStampedModel(models.Model):
    """Barcha modellar uchun asos — vaqt tamg'asi"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class TranslatableModel(TimeStampedModel):
    """Ko'p tilli modellar uchun asos (uz/ru/en)"""
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255, blank=True)
    title_en = models.CharField(max_length=255, blank=True)

    def get_title(self, lang='uz'):
        return getattr(self, f'title_{lang}', '') or self.title_uz

    class Meta:
        abstract = True


class PublishableContent(TranslatableModel):
    """
    Kontent modellari uchun asos.
    News, Event, Blog, Briefing, Competition — barchasi shu modeldan meros oladi.
    """
    image           = models.ImageField(upload_to='content/%Y/%m/', blank=True)
    video_url       = models.URLField(blank=True)
    text_uz         = models.TextField()
    text_ru         = models.TextField(blank=True)
    text_en         = models.TextField(blank=True)
    description_uz  = models.TextField(blank=True)
    description_ru  = models.TextField(blank=True)
    description_en  = models.TextField(blank=True)
    keywords        = models.CharField(max_length=500, blank=True)
    slug            = models.SlugField(unique=True, blank=True, max_length=300)
    date            = models.DateField()
    is_published    = models.BooleanField(default=False)
    views           = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['-date']


class SoftDeleteModel(TimeStampedModel):
    """Yashirin o'chirish"""
    is_active  = models.BooleanField(default=True)
    class Meta:
        abstract = True
```

---

## Domain 1: `pages/` — Sayt Konfiguratsiyasi

**Maqsad:** Navbar, header, footer, statik sahifalar, hamkorlar

```
pages/
├── models/
│   ├── site_config.py     # SiteConfig (Singleton)
│   ├── stat_counter.py    # StatCounter — "Akademiya raqamlarda"
│   ├── interactive.py     # InteractiveService — Hemis, LMS, Kutubxona
│   ├── partner.py         # Partner — Hamkorlar
│   ├── navbar.py          # NavbarCategory, NavbarSubItem
│   ├── hero.py            # HeroVideo, HeroSlide
│   └── rating.py          # Rating — Milliy/Xalqaro reyting
├── api/
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── admin.py
├── services.py
└── selectors.py
```

### Modellar:

```python
# site_config.py
class SiteConfig(TimeStampedModel):
    """SINGLETON — yagona sayt sozlamasi"""
    email        = models.EmailField()
    phone        = models.CharField(max_length=25)
    address_uz   = models.CharField(max_length=300)
    address_ru   = models.CharField(max_length=300, blank=True)
    address_en   = models.CharField(max_length=300, blank=True)
    president_quote_uz = models.TextField()
    president_quote_ru = models.TextField(blank=True)
    president_quote_en = models.TextField(blank=True)
    president_name     = models.CharField(max_length=100, default="Sh. Mirziyoyev")
    promo_video_url    = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    facebook  = models.URLField(blank=True)
    youtube   = models.URLField(blank=True)
    twitter   = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


# stat_counter.py
class StatCounter(TimeStampedModel):
    """
    "Akademiya raqamlarda" sektsiyasi.
    Singleton emas — admin har bir ko'rsatkichni alohida boshqaradi.
    """
    label_uz  = models.CharField(max_length=100)   # "Fakultetlar soni"
    label_ru  = models.CharField(max_length=100, blank=True)
    label_en  = models.CharField(max_length=100, blank=True)
    value     = models.CharField(max_length=50)    # "12" yoki "1200+"
    icon      = models.CharField(max_length=50, blank=True)  # CSS icon class
    order     = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)


# interactive.py
class InteractiveService(TimeStampedModel):
    """Hemis, LMS, Kutubxona, Masofaviy ta'lim linklari"""
    title_uz  = models.CharField(max_length=100)
    title_ru  = models.CharField(max_length=100, blank=True)
    title_en  = models.CharField(max_length=100, blank=True)
    url       = models.URLField()
    icon      = models.CharField(max_length=50, blank=True)
    order     = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)


# rating.py
class RatingType(models.TextChoices):
    NATIONAL      = 'national',      'Milliy reyting'
    INTERNATIONAL = 'international', 'Xalqaro reyting'

class Rating(TranslatableModel):
    rating_type = models.CharField(max_length=20, choices=RatingType.choices)
    organization = models.CharField(max_length=200)  # "QS World Rankings"
    rank        = models.CharField(max_length=50)    # "Top 500" yoki "34"
    year        = models.PositiveSmallIntegerField()
    logo        = models.ImageField(upload_to='ratings/', blank=True)
    url         = models.URLField(blank=True)
    order       = models.PositiveSmallIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
```

### API Endpointlar:
```
GET /api/site-config/          # Sayt konfiguratsiyasi
GET /api/stats/                # Akademiya raqamlarda
GET /api/interactive-services/ # Interaktiv xizmatlar
GET /api/partners/             # Hamkorlar
GET /api/navbar/               # Navigatsiya tuzilmasi
GET /api/hero/                 # Hero video/slayd
GET /api/ratings/              # Reytinglar
GET /api/ratings/?type=national
```

---

## Domain 2: `academic/` — Akademiya (ASOSIY)

**Maqsad:** Tuzilma + Xodimlar + Tarixi + Binolar + Kengash + Rektorat

**Kalit g'oya:** `OrganizationUnit` + `Staff` — ikki universal model barcha ierarxiyani qoplaydi.

```
academic/
├── models/
│   ├── __init__.py
│   ├── unit.py         # OrganizationUnit — UNIVERSAL DARAXT MODEL
│   ├── staff.py        # Staff — UNIVERSAL XODIM MODEL
│   ├── history.py      # AcademyHistory
│   ├── building.py     # Building — O'quv binolari
│   └── requisites.py   # Requisites — Rekvizitlar (static)
├── api/
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
├── admin.py
├── services.py
└── selectors.py
```

### Modellar:

```python
# unit.py
class UnitType(models.TextChoices):
    COUNCIL      = 'council',      'Universitet kengashi'
    SUPERVISORY  = 'supervisory',  'Kuzatuv kengashi'
    RECTORATE    = 'rectorate',    'Rektorat'
    RECTOR       = 'rector',       'Rektor'
    PRORECTOR    = 'prorector',    'Prorektor'
    FACULTY      = 'faculty',      'Fakultet'
    DEPARTMENT   = 'department',   'Kafedra'
    CENTER       = 'center',       'Markaz'
    INSTITUTE    = 'institute',    'Institut'
    PUBLIC_ORG   = 'public_org',   'Jamoat tashkiloti'
    DIVISION     = 'division',     'Bo\'lim'

class OrganizationUnit(TranslatableModel):
    """
    UNIVERSAL DARAXT MODEL.
    Tuzilma sahifasi, Rektorat, Fakultetlar, Kafedralar,
    Institutlar, Markazlar — barchasi shu bir model!

    Daraxt: parent=None → top-level (Kengash, Rektor)
             parent=Rektor → Rektorat bo'limlari
             parent=Fakultet → Kafedralar
    """
    parent       = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    unit_type    = models.CharField(max_length=20, choices=UnitType.choices)
    slug         = models.SlugField(unique=True, blank=True)
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    email        = models.EmailField(blank=True)
    phone        = models.CharField(max_length=25, blank=True)
    order        = models.PositiveSmallIntegerField(default=0)
    is_featured  = models.BooleanField(default=False)  # Rektor → katta blok
    is_active    = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Tashkiliy bo'linma"


# staff.py
class StaffRole(models.TextChoices):
    RECTOR          = 'rector',       'Rektor'
    PRORECTOR       = 'prorector',    'Prorektor'
    DEAN            = 'dean',         'Dekan'
    DEPT_HEAD       = 'dept_head',    'Kafedra mudiri'
    COUNCIL_MEMBER  = 'council',      'Kengash a\'zosi'
    PROFESSOR       = 'professor',    'Professor'
    STAFF           = 'staff',        'Xodim'

class Staff(TranslatableModel):
    """
    UNIVERSAL XODIM MODEL.
    Rektor, Prorektor, Dekan, Kafedra mudiri, Kengash a'zosi,
    Professor — barchasi shu bir model!

    role + unit → kim ekanligi va qaysi bo'limda ishlashi aniq bo'ladi.
    """
    unit         = models.ForeignKey(
        OrganizationUnit, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='staff'
    )
    role         = models.CharField(max_length=20, choices=StaffRole.choices)
    image        = models.ImageField(upload_to='staff/%Y/', blank=True)
    email        = models.EmailField(blank=True)
    phone        = models.CharField(max_length=25, blank=True)
    reception_hours = models.CharField(max_length=100, blank=True)  # "Seshanba 14:00-17:00"
    position_uz  = models.CharField(max_length=200, blank=True)  # "Texnika fanlari doktori"
    position_ru  = models.CharField(max_length=200, blank=True)
    position_en  = models.CharField(max_length=200, blank=True)
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    order        = models.PositiveSmallIntegerField(default=0)
    is_active    = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Xodim"


# history.py
class AcademyHistory(TranslatableModel):
    """Akademiya tarixi — rasm + sarlavha + matn"""
    image        = models.ImageField(upload_to='history/')
    text_uz      = models.TextField()
    text_ru      = models.TextField(blank=True)
    text_en      = models.TextField(blank=True)
    year         = models.PositiveSmallIntegerField(null=True, blank=True)
    order        = models.PositiveSmallIntegerField(default=0)
    is_active    = models.BooleanField(default=True)


# building.py
class Building(TranslatableModel):
    """O'quv binolari"""
    image        = models.ImageField(upload_to='buildings/')
    description_uz = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    address      = models.CharField(max_length=300, blank=True)
    order        = models.PositiveSmallIntegerField(default=0)
    is_active    = models.BooleanField(default=True)
```

### API Endpointlar:
```
# Tuzilma sahifasi uchun
GET /api/structure/                      # To'liq daraxt (nested)
GET /api/structure/?type=faculty         # Faqat fakultetlar
GET /api/structure/?type=department      # Faqat kafedralar
GET /api/structure/<slug>/               # Bitta bo'linma

# Xodimlar uchun
GET /api/staff/                          # Barcha xodimlar
GET /api/staff/?role=rector              # Faqat rektor/prorektor (Rektorat sahifasi)
GET /api/staff/?role=council             # Kengash a'zolari
GET /api/staff/?unit=<id>               # Bo'lim xodimlari (Fakultet → Dekan)

# Akademiya haqida
GET /api/academy/history/               # Akademiya tarixi
GET /api/academy/buildings/             # O'quv binolari
GET /api/academy/requisites/            # Rekvizitlar
```

### Rektorat sahifasi qanday ishlaydi:
```
# Frontend /rektorat/ sahifasida:
GET /api/staff/?role=rector&role=prorector
# Bu bitta query bilan barcha rektorat xodimlarini beradi
# Alohida Rector modeli KERAK EMAS!
```

### Tuzilma sahifasi qanday ishlaydi:
```
GET /api/structure/
Response:
[
  {"title": "Universitet kengashi", "type": "council", "children": []},
  {
    "title": "Rektor", "type": "rector", "is_featured": true,
    "children": [
      {"title": "Rektorat tashkiliy xizmati", "type": "division"},
      {"title": "Xodimlar bo'limi", "type": "division"},
      {"title": "Audit xizmati", "type": "division"},
      ...
    ]
  },
  {"title": "Yoshlar masalalari bo'yicha prorektor", "type": "prorector", "children": [...]},
  ...
]
```

---

## Domain 3: `documents/` — Universal Hujjatlar App (YANGI)

**Maqsad:** Me'yoriy hujjatlar barcha bo'limlarda kerak → bitta app

```
documents/
├── models/
│   ├── __init__.py
│   ├── category.py    # DocumentCategory
│   └── document.py   # Document
├── api/
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
└── admin.py
```

```python
class DocumentCategory(TranslatableModel):
    """
    "Me'yoriy hujjatlar", "Qabul hujjatlari", "Faoliyat hujjatlari"
    Bir model, turli kategoriyalar.
    """
    slug      = models.SlugField(unique=True)
    order     = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)


class Document(TranslatableModel):
    """
    UNIVERSAL HUJJAT MODEL.
    Akademiya me'yoriy hujjatlari, Qabul hujjatlari,
    Faoliyat hujjatlari — barchasi shu bir model!
    """
    category   = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, related_name='documents')
    file       = models.FileField(upload_to='documents/%Y/', blank=True)
    link       = models.URLField(blank=True)       # Fayl yo'q, link bo'lsa
    date       = models.DateField(null=True, blank=True)
    order      = models.PositiveSmallIntegerField(default=0)
    is_active  = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date', 'order']
```

### API Endpointlar:
```
GET /api/documents/?category=normative       # Akademiya me'yoriy hujjatlari
GET /api/documents/?category=admission       # Qabul hujjatlari
GET /api/documents/?category=activity        # Faoliyat hujjatlari
GET /api/document-categories/               # Barcha kategoriyalar
```

---

## Domain 4: `news/` — Axborot Xizmati

```
news/
├── models/
│   ├── news.py        # News (PublishableContent + category)
│   ├── event.py       # Event (kutilayotgan tadbirlar)
│   ├── briefing.py    # Briefing (brifinglar)
│   ├── gallery.py     # PhotoGallery, VideoGallery
│   └── competition.py # Competition (tanlovlar) — yoki News category orqali
├── api/
├── admin.py
├── services.py
└── selectors.py
```

```python
class NewsCategory(models.TextChoices):
    NEWS         = 'news',        'Yangiliklar'
    ANNOUNCEMENT = 'announce',    "E'lon"
    ANTI_CORRUPT = 'anti_corrupt','Korrupsiyaga qarshi'
    GREEN        = 'green',       'Yashil Akademiya'
    WORLD        = 'world',       'Dunyo'
    COMPETITION  = 'competition', 'Tanlovlar'
    RECTOR_SPEECH = 'rector',     'Rektor tabriklari va nutqlari'

class News(PublishableContent):
    """PublishableContent → barcha fieldlar tayyor"""
    category = models.CharField(max_length=20, choices=NewsCategory.choices, default=NewsCategory.NEWS)
    source   = models.CharField(max_length=200, blank=True)

class Event(PublishableContent):
    """Kutilayotgan tadbirlar"""
    location_uz    = models.CharField(max_length=300)
    location_ru    = models.CharField(max_length=300, blank=True)
    location_en    = models.CharField(max_length=300, blank=True)
    start_datetime = models.DateTimeField()
    end_datetime   = models.DateTimeField(null=True, blank=True)
    event_link     = models.URLField(blank=True)

class Gallery(TranslatableModel):
    """Foto va Video galereya"""
    class GalleryType(models.TextChoices):
        PHOTO = 'photo', 'Fotogalereya'
        VIDEO = 'video', 'Videogalereya'
    gallery_type = models.CharField(max_length=10, choices=GalleryType.choices)
    cover_image  = models.ImageField(upload_to='gallery/')
    date         = models.DateField()
    is_published = models.BooleanField(default=False)

class GalleryItem(TimeStampedModel):
    """Galereya ichidagi rasm/video"""
    gallery   = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='items')
    image     = models.ImageField(upload_to='gallery/items/', blank=True)
    video_url = models.URLField(blank=True)
    caption   = models.CharField(max_length=300, blank=True)
    order     = models.PositiveSmallIntegerField(default=0)
```

### API Endpointlar:
```
GET /api/news/                      # Barcha yangiliklar
GET /api/news/?category=anti_corrupt # Korrupsiyaga qarshi
GET /api/news/?category=green        # Yashil akademiya
GET /api/events/                    # Kutilayotgan tadbirlar
GET /api/galleries/                 # Galereya
GET /api/galleries/?type=photo      # Fotogalereya
GET /api/galleries/<id>/            # Galereya itemlari bilan
```

---

## Domain 5: `activity/` — Faoliyat

```
activity/
├── models/
│   ├── scientific.py    # ScientificCouncil, ScientificProject, Doctorantura, Conference
│   ├── cultural.py      # StudentCouncil, GreenAcademy, Psychologist
│   ├── financial.py     # ContractPrice, Vehicle
│   └── educational.py   # Curriculum (Bakalavr/Magistr), Textbook
```

```python
class ScientificProject(PublishableContent):
    """Ilmiy loyihalar"""
    project_type = models.CharField(max_length=100, blank=True)
    grant_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

class ContractPrice(TranslatableModel):
    """To'lov-kontrakt narxlari"""
    class DegreeLevel(models.TextChoices):
        BACHELOR = 'bachelor', 'Bakalavr'
        MASTER   = 'master',   'Magistratura'
    degree_level     = models.CharField(max_length=20, choices=DegreeLevel.choices)
    direction_uz     = models.CharField(max_length=300)   # Ta'lim yo'nalishi
    direction_ru     = models.CharField(max_length=300, blank=True)
    price            = models.DecimalField(max_digits=12, decimal_places=2)
    currency         = models.CharField(max_length=10, default='UZS')
    academic_year    = models.CharField(max_length=20)    # "2024-2025"
    is_active        = models.BooleanField(default=True)
```

---

## Domain 6: `international/` — Xalqaro Aloqalar

```python
class PartnerOrganization(TranslatableModel):
    """Xalqaro hamkor tashkilotlar"""
    country      = models.CharField(max_length=100)
    logo         = models.ImageField(upload_to='international/logos/', blank=True)
    website      = models.URLField(blank=True)
    description_uz = models.TextField(blank=True)
    is_active    = models.BooleanField(default=True)

class ForeignProfessor(TranslatableModel):
    """Xorijlik professor-o'qituvchilar va ularning fikrlari"""
    country      = models.CharField(max_length=100)
    university   = models.CharField(max_length=300)
    image        = models.ImageField(upload_to='international/professors/')
    position_uz  = models.CharField(max_length=200, blank=True)
    review_uz    = models.TextField(blank=True)  # "Biz haqimizda" fikri
    review_ru    = models.TextField(blank=True)
    review_en    = models.TextField(blank=True)
    is_active    = models.BooleanField(default=True)
    order        = models.PositiveSmallIntegerField(default=0)
```

---

## Domain 7: `students/` — Talabalarga

```python
class DegreeLevel(models.TextChoices):
    BACHELOR = 'bachelor', 'Bakalavr'
    MASTER   = 'master',   'Magistratura'

class StudentGuide(TranslatableModel):
    """Yo'riqnoma (Bakalavr/Magistr)"""
    degree_level = models.CharField(max_length=20, choices=DegreeLevel.choices)
    # Document app ga yo'naltiradi
    document     = models.ForeignKey('documents.Document', on_delete=models.CASCADE)

class Schedule(TranslatableModel):
    """Dars jadvali va Yakuniy nazorat jadvali"""
    class ScheduleType(models.TextChoices):
        LESSON = 'lesson',  'Dars jadvali'
        EXAM   = 'exam',    'Yakuniy nazorat jadvali'
    schedule_type = models.CharField(max_length=10, choices=ScheduleType.choices)
    degree_level  = models.CharField(max_length=20, choices=DegreeLevel.choices)
    file          = models.FileField(upload_to='schedules/%Y/')
    semester      = models.CharField(max_length=50)
    academic_year = models.CharField(max_length=20)
    is_active     = models.BooleanField(default=True)

class AcademicMobility(PublishableContent):
    """O'ZDSAda akademik mobillik"""
    pass
```

---

## Domain 8: `admissions/` — Qabul

```python
class AdmissionQuota(TranslatableModel):
    """Qabul rejasi"""
    class DegreeLevel(models.TextChoices):
        BACHELOR = 'bachelor', 'Bakalavr'
        MASTER   = 'master',   'Magistratura'
        FOREIGN  = 'foreign',  'Xorijiy talabalar'
    degree_level    = models.CharField(max_length=20, choices=DegreeLevel.choices)
    direction_uz    = models.CharField(max_length=300)
    direction_code  = models.CharField(max_length=20, blank=True)
    quota           = models.PositiveIntegerField(default=0)
    academic_year   = models.CharField(max_length=20)
    is_active       = models.BooleanField(default=True)

class PassingScore(TranslatableModel):
    """O'tish ballari"""
    direction_uz  = models.CharField(max_length=300)
    score         = models.PositiveSmallIntegerField()
    academic_year = models.CharField(max_length=20)

class AdmissionNews(PublishableContent):
    """Qabul komissiyasi yangiliklari — PublishableContent dan"""
    pass

# Hujjatlar uchun documents.Document ishlatiladi (DRY!)
# category="admission" bilan filter qilinadi
```

---

## Domain 9: `contact/` — Aloqa + Rektorga Murojaat

```python
class RectorAppeal(TimeStampedModel):
    """Rektorga murojaat"""
    class Status(models.TextChoices):
        NEW       = 'new',       'Yangi'
        IN_REVIEW = 'in_review', "Ko'rib chiqilmoqda"
        ANSWERED  = 'answered',  'Javob berildi'
        REJECTED  = 'rejected',  'Rad etildi'
    full_name   = models.CharField(max_length=200)
    email       = models.EmailField()
    phone       = models.CharField(max_length=20)
    subject     = models.CharField(max_length=300)
    message     = models.TextField()
    attachment  = models.FileField(upload_to='appeals/', blank=True)
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    answer      = models.TextField(blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)

class FAQ(TranslatableModel):
    """Savol-Javob"""
    question_uz = models.TextField()
    question_ru = models.TextField(blank=True)
    question_en = models.TextField(blank=True)
    answer_uz   = models.TextField()
    answer_ru   = models.TextField(blank=True)
    answer_en   = models.TextField(blank=True)
    order       = models.PositiveSmallIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
```

---

## Domain 10: `alumni/` — Faxrlarimiz

```python
class AlumniType(models.TextChoices):
    GRADUATE        = 'graduate',  'Bitiruvchilar'
    HONORED_TEACHER = 'teacher',   'Faxrli ustozlar'
    LEADING_SCIENTIST = 'scientist','Ilg\'or olimlar'
    ACADEMY_STAR    = 'star',      'O\'ZDSA yulduzlari'

class Alumni(TranslatableModel):
    """
    UNIVERSAL ALUMNI MODEL.
    Bitiruvchi, Faxrli ustoz, Ilg'or olim, OZDSA yulduzi — bitta model!
    """
    alumni_type     = models.CharField(max_length=20, choices=AlumniType.choices)
    image           = models.ImageField(upload_to='alumni/')
    position_uz     = models.CharField(max_length=300, blank=True)
    position_ru     = models.CharField(max_length=300, blank=True)
    description_uz  = models.TextField(blank=True)
    description_ru  = models.TextField(blank=True)
    description_en  = models.TextField(blank=True)
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True)
    achievement     = models.CharField(max_length=500, blank=True)
    order           = models.PositiveSmallIntegerField(default=0)
    is_active       = models.BooleanField(default=True)
```

---

## To'liq API Endpoint Jadvali

```
# PAGES
GET  /api/site-config/
GET  /api/stats/
GET  /api/interactive-services/
GET  /api/partners/
GET  /api/navbar/
GET  /api/hero/
GET  /api/ratings/?type=national|international

# ACADEMIC (TUZILMA + REKTORAT + RAHBARIYAT)
GET  /api/structure/                         # To'liq daraxt
GET  /api/structure/?type=faculty|dept|...   # Filter bo'linma turiga
GET  /api/structure/<slug>/                  # Bitta bo'linma
GET  /api/staff/                             # Barcha xodimlar
GET  /api/staff/?role=rector&role=prorector  # Rektorat sahifasi
GET  /api/staff/?role=council                # Akademiya kengashi
GET  /api/staff/?unit=<id>                   # Bo'lim xodimlari
GET  /api/academy/history/
GET  /api/academy/buildings/
GET  /api/academy/requisites/

# DOCUMENTS (BARCHA BO'LIMLAR UCHUN)
GET  /api/documents/?category=normative
GET  /api/documents/?category=admission
GET  /api/document-categories/

# NEWS / AXBOROT XIZMATI
GET  /api/news/?category=news|announce|anti_corrupt|green|world|competition
GET  /api/events/
GET  /api/galleries/?type=photo|video
GET  /api/galleries/<id>/

# INTERNATIONAL
GET  /api/international/partners/
GET  /api/international/professors/

# STUDENTS
GET  /api/students/guides/?degree=bachelor|master
GET  /api/students/schedules/?type=lesson|exam
GET  /api/students/mobility/

# ADMISSIONS
GET  /api/admissions/quota/?degree=bachelor|master|foreign
GET  /api/admissions/scores/
GET  /api/admissions/news/
GET  /api/documents/?category=admission

# CONTACT
POST /api/rector-appeal/
GET  /api/faq/

# ALUMNI (FAXRLARIMIZ)
GET  /api/alumni/?type=graduate|teacher|scientist|star
```

---

## DRY Xulosasi — Qancha Model Tejaladi

| TZ talabi | Noto'g'ri (takror) | DRY yondashuv |
|-----------|---------------------|---------------|
| Rektor, Prorektor, Dekan, Kengash a'zosi | 4 ta alohida model | **1 ta Staff** (role field) |
| Tuzilma, Fakultet, Kafedra, Institut, Markaz | 5 ta alohida model | **1 ta OrganizationUnit** (parent FK) |
| Akademiya/Qabul/Faoliyat hujjatlari | 3+ ta alohida model | **1 ta Document** (category FK) |
| Bitiruvchi, Ustoz, Olim, Yulduz | 4 ta alohida model | **1 ta Alumni** (type field) |
| **Jami** | **~16 ta ortiqcha model** | **4 ta universal model** |

---

## Texnologiya Steki

```
Backend:   Django 5.x + DRF
DB:        PostgreSQL (primary) + Redis (cache/sessions)
Task Queue: Celery + django-celery-beat
Storage:   ImageKit (rasmlar) + Local/S3 (fayllar)
Docs:      drf-spectacular (Swagger + ReDoc)
Server:    Gunicorn + Nginx
Container: Docker + docker-compose
```
