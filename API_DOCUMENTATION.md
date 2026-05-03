# USAS API Documentation
> **Base URL:** `https://yourdomain.com/api/`  
> **Swagger UI:** `/swagger/`  
> **ReDoc:** `/redoc/`  
> **Lang param:** `?lang=uz` (default) | `?lang=ru` | `?lang=en`

---

## Ko'rishlar hisobi (View Count)

Barcha list va detail endpointlari javobida `views_count` maydoni qaytadi.

### Ko'rishni qaydlash
```
POST /api/<endpoint>/<id>/view/
```
- Cookie `view_token` (UUID) orqali qurilmani identifikatsiya qiladi
- Bir qurilma bir objectni faqat **1 marta** hisoblaydi
- Cookie yo'q bo'lsa — avtomatik yaratiladi va response'da qaytariladi

**Response:**
```json
{ "views_count": 42, "is_new": true }
```
- `is_new: true` — yangi ko'rish qayd etildi
- `is_new: false` — oldindan ko'rilgan (count oshmaydi)

---

## 1. Yangiliklar (News)

### Kategoriyalar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/news/categories/` | Barcha kategoriyalar (ierarxik) |
| GET | `/api/news/categories/<slug>/` | Bitta kategoriya |

### Yangiliklar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/news/` | Ro'yxat (pagination, filter) |
| GET | `/api/news/<uuid>/` | Bitta yangilik (ID) |
| GET | `/api/news/<slug>/` | Bitta yangilik (slug) |
| POST | `/api/news/<uuid>/view/` | Ko'rishni qaydlash |

**Filters:** `?category=<slug>` `?date_from=YYYY-MM-DD` `?date_to=YYYY-MM-DD` `?search=`

**Response (list item):**
```json
{
  "id": "uuid",
  "title": "Yangilik sarlavhasi",
  "description": "...",
  "image": "https://...",
  "date": "2024-01-15T10:00:00Z",
  "slug": "yangilik-sarlavhasi",
  "views_count": 120,
  "categories": [...]
}
```

---

## 2. Tadbirlar (Events)

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/events/` | Ro'yxat |
| GET | `/api/events/<uuid>/` | Bitta tadbir (ID) |
| GET | `/api/events/<slug>/` | Bitta tadbir (slug) |
| POST | `/api/events/<uuid>/view/` | Ko'rishni qaydlash |

**Filters:** `?status=upcoming` | `?status=completed` `?category=<slug>`

---

## 3. Blog

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/blogs/` | Ro'yxat |
| GET | `/api/blogs/<uuid>/` | Bitta blog (ID) |
| GET | `/api/blogs/<slug>/` | Bitta blog (slug) |
| POST | `/api/blogs/<uuid>/view/` | Ko'rishni qaydlash |

**Filters:** `?category=<slug>` `?search=`

---

## 4. Korrupsiyaga qarshi

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/korrupsiya/` | Ro'yxat |
| GET | `/api/korrupsiya/<uuid>/` | Bitta (ID) |
| GET | `/api/korrupsiya/<slug>/` | Bitta (slug) |
| POST | `/api/korrupsiya/<uuid>/view/` | Ko'rishni qaydlash |

---

## 5. E'lonlar (Elon)

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/elon/` | Ro'yxat |
| GET | `/api/elon/<uuid>/` | Bitta e'lon |
| POST | `/api/elon/<uuid>/view/` | Ko'rishni qaydlash |

**Filters:** `?date_from=` `?date_to=`

---

## 6. Tenderlar

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/tenders/` | Ro'yxat (pagination) |
| GET | `/api/tenders/<uuid>/` | Bitta tender |
| POST | `/api/tenders/<uuid>/view/` | Ko'rishni qaydlash |

**Filters:** `?search=`

---

## 7. Shaxslar (Persons / Xodimlar)

### Kategoriyalar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/categories/` | Barcha kategoriyalar |
| GET | `/api/categories/<slug>/` | Kategoriya + shaxslar |

### Shaxslar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/persons/` | Barcha shaxslar |
| GET | `/api/persons/grouped/` | Kategoriya bo'yicha guruhlangan |
| GET | `/api/persons/<uuid>/` | Bitta shaxs (to'liq: tablar, rasmlar) |
| POST | `/api/persons/<uuid>/view/` | Ko'rishni qaydlash |

**Filters:** `?category=<slug>` `?is_head=1` `?search=`

**Response:**
```json
{
  "id": "uuid",
  "full_name": "Abdullayev Jasur",
  "image": "https://...",
  "title": "Professor",
  "position": "Rektor",
  "phone": "+998901234567",
  "email": "rektor@usas.uz",
  "is_head": true,
  "category": { "id": "uuid", "title": "Rektorat", "slug": "rektorat" },
  "tabs": [...],
  "views_count": 88
}
```

---

## 8. Magistratura talabalari

### Yangi endpoint (Person FK bilan)
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/magistr-talabalar/` | Barcha magistratura talabalari |
| GET | `/api/magistr-talabalar/<uuid>/` | Bitta talaba |
| POST | `/api/magistr-talabalar/<uuid>/view/` | Ko'rishni qaydlash |

**Filters:** `?year=2024-2025` `?specialty_code=71010301` `?education_form=Kunduzgi`

**Response:**
```json
{
  "id": "uuid",
  "person": {
    "id": "uuid",
    "full_name": "Karimov Sardor",
    "image": "https://...",
    "position": "Magistrant"
  },
  "display_name": "Karimov Sardor",
  "specialty_code": "71010301",
  "specialty_name": "Jismoniy tarbiya va sport",
  "dissertation_topic": "Dissertatsiya mavzusi...",
  "supervisor_name": "Prof. Toshmatov A.",
  "supervisor_info": "f.f.d (PhD), dotsent",
  "education_form": "Kunduzgi",
  "year": "2024-2025",
  "order": 1,
  "views_count": 5
}
```

### Eski endpoint (guruh asosida)
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/magistr-students/` | Guruhlar va talabalar ro'yxati |

**Filters:** `?year=2025-2026` `?specialty_code=`

---

## 9. Talaba ma'lumotlari

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/student-info/` | Barcha kategoriyalar (ierarxik) |
| GET | `/api/student-info/<slug>/` | Bitta kategoriya + itemlar |

---

## 10. Olimpiya chempionlari

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/olimpiya/` | Barcha chempionlar |

**Filters:** `?yonalish=kurash` `?guruh=`

---

## 11. Stipendiyalar

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/stipendiya/` | Stipendiyalar miqdori jadvali |

---

## 12. Akademiya (Academic)

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/academic/stats/` | Raqamlarda statistika (15000+ talaba...) |
| GET | `/api/academic/detail/` | Batafsil sahifa kontent |
| GET | `/api/academic/fakultet-kafedralar/` | Barcha fakultet/kafedralar |
| GET | `/api/academic/fakultet-kafedralar/<slug>/` | Kafedra detail + professor tarkibi |
| POST | `/api/academic/fakultet-kafedralar/<slug>/view/` | Ko'rishni qaydlash |
| GET | `/api/academic/huzuridagi-tashkilotlar/` | Akademiya huzuridagi 5 tashkilot |
| GET | `/api/academic/kengashlar/` | Akademiya kengashi ro'yxati (`slug` + `text`) |
| GET | `/api/academic/kengashlar/<slug>/` | Akademiya kengashi detali (`slug` bo'yicha) |

**Filters (kafedralar):** `?type=tashkilot` | `?type=fakultet` | `?type=kafedra`

**Kafedra detail response:**
```json
{
  "id": "uuid",
  "name": "Jismoniy tarbiya kafedrasi",
  "description": "...",
  "dean": { "full_name": "...", "photo_url": "...", "lavozim": "Dekan" },
  "professor_tarkibi": [
    { "full_name": "...", "lavozim": "Professor", "photo_url": "..." }
  ],
  "publications": [{ "id": "uuid", "cover_url": "https://..." }],
  "views_count": 34
}
```

### Akademiya kengashi endpointlari (frontend uchun)

#### 1) List
`GET /api/academic/kengashlar/`

**Response:**
```json
[
  {
    "id": "uuid",
    "slug": "xotin-qizlar-masalalari-boyicha-maslahat-kengashi",
    "text": {
      "uz": "Xotin-qizlar masalalari bo'yicha maslahat kengashi",
      "ru": "Совет по вопросам женщин",
      "en": "Women's Advisory Council"
    },
    "order": 1
  }
]
```

#### 2) Detail
`GET /api/academic/kengashlar/<slug>/`

**Response:**
```json
{
  "id": "uuid",
  "slug": "xotin-qizlar-masalalari-boyicha-maslahat-kengashi",
  "text": {
    "uz": "Kengash haqida to'liq matn...",
    "ru": "Полный текст о совете...",
    "en": "Full council text..."
  },
  "person": {
    "id": "uuid",
    "full_name": {
      "uz": "F.I.Sh",
      "ru": "Ф.И.О",
      "en": "Full Name"
    },
    "title": {
      "uz": "Lavozim",
      "ru": "Должность",
      "en": "Position"
    },
    "photo_url": "https://yourdomain.com/media/persons/..."
  },
  "order": 1,
  "created_at": "2026-05-03T12:00:00Z",
  "updated_at": "2026-05-03T12:00:00Z"
}
```

#### TypeScript type (tavsiya)
```ts
type LocalizedText = { uz?: string; ru?: string; en?: string };

type AcademyCouncilListItem = {
  id: string;
  slug: string;
  text: LocalizedText;
  order: number;
};

type AcademyCouncilDetail = {
  id: string;
  slug: string;
  text: LocalizedText;
  person: {
    id: string;
    full_name: LocalizedText;
    title: LocalizedText;
    photo_url: string | null;
  } | null;
  order: number;
  created_at: string;
  updated_at: string;
};
```

---

## 13. Xalqaro hamkorlik (International)

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/foreign-reviews/` | Xorijlik professorlar fikrlari |
| GET | `/api/partner-organizations/` | Hamkor tashkilotlar (xalqaro + mahalliy) |
| GET | `/api/international-posts/` | Xalqaro bo'lim yangiliklari |
| GET | `/api/international-posts/<uuid>/` | Bitta post |
| POST | `/api/international-posts/<uuid>/view/` | Ko'rishni qaydlash |
| GET | `/api/international-ratings/` | Xalqaro reytinglar |
| GET | `/api/international-ratings/<slug>/` | Bitta reyting |
| POST | `/api/international-ratings/<uuid>/view/` | Ko'rishni qaydlash |
| GET | `/api/dept-config/` | Bo'lim konfiguratsiyasi |
| GET | `/api/memorandum-stats/` | Memorandumlar statistikasi |

**Filters (partner-organizations):** `?category=xalqaro` | `?category=mahalliy`  
**Filters (international-posts):** `?type=announcement` | `?type=news` | `?type=training`

---

## 14. Infratuzilma (Infra)

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/infra/sport-majmua/` | Sport majmualari ro'yxati |
| GET | `/api/infra/sport-majmua/<slug>/` | Majmua pasporti (to'liq) |
| POST | `/api/infra/sport-majmua/<slug>/view/` | Ko'rishni qaydlash |
| GET | `/api/infra/sharoitlar/` | Sharoit va imkoniyatlar |

**Filters (sharoitlar):** `?category=sport` | `?category=talim`

---

## 15. Faoliyat (Activities)

### Ilmiy faoliyat
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/activities/faoliyat/` | Barcha faoliyat itemlari |
| GET | `/api/activities/faoliyat/<uuid>/` | Bitta faoliyat |
| POST | `/api/activities/faoliyat/<uuid>/view/` | Ko'rishni qaydlash |
| GET | `/api/activities/faoliyat/categories/` | Sport sahifasi (stats+yonalishlar+tadbirlar) |
| GET | `/api/activities/faoliyat/categories/full/` | To'liq kategoriya daraxti |
| GET | `/api/activities/faoliyat/categories/<slug>/children/` | Sub-kategoriyalar |
| GET | `/api/activities/faoliyat/categories/<slug>/items/` | Kategoriya fayllari |

### Sport
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/activities/sport/stats/` | Statistika kartochalari (15+, 500+ ...) |
| GET | `/api/activities/sport/yonalishlar/` | Sport yo'nalishlari |
| POST | `/api/activities/sport/yonalishlar/<uuid>/view/` | Ko'rishni qaydlash |
| GET | `/api/activities/sport/tadbirlar/` | Yillik tadbirlar |
| POST | `/api/activities/sport/tadbirlar/<uuid>/view/` | Ko'rishni qaydlash |

### Boshqa
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/activities/contract-prices/` | Kontrakt narxlari |
| GET | `/api/activities/vehicles/` | Xizmat avtomobillari |
| GET | `/api/activities/axborot/vazifalar/` | Axborot xizmati vazifalari |
| GET | `/api/activities/axborot/xodimlar/` | Axborot xizmati xodimlari |

---

## 16. Axborot xizmati

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/axborot/sections/` | Bo'limlar va vazifalar ro'yxati |
| GET | `/api/axborot/persons/` | Axborot xizmati xodimlari |
| GET | `/api/axborot/aov-xizmat/` | To'liq sahifa (sections + persons) |

---

## 17. Sahifa kontenti (Pages)

### Sayt sozlamalari
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/contact-info/` | Aloqa ma'lumotlari (singleton) |
| GET | `/api/rekvizit/` | Tashkilot rekvizitlari |
| GET | `/api/president-quotes/` | Prezident iqtiboslari |
| GET | `/api/social-links/` | Ijtimoiy tarmoq havolalari |
| GET | `/api/partners/` | Hamkorlar (logo) |
| GET | `/api/hero-video/` | Hero videolar |
| GET | `/api/interaktiv-xizmatlar/` | Interaktiv xizmatlar (6 ta karta) |

### Navbar
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/navbar/` | To'liq navbar daraxti (`{uz:[...], ru:[...], en:[...]}`) |
| GET | `/api/pages/<slug>/` | Sahifa kontenti slug bo'yicha |

### Tashkiliy tuzilma
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/org-structure/` | To'liq tashkiliy tuzilma daraxti |
| GET | `/api/org-structure/sections/` | Sektsiyalar (frontend karta ko'rinishi) |

**Org-structure response:**
```json
[{
  "id": "uuid",
  "title": "Kuzatuv kengashi",
  "slug": "kuzatuv-kengashi",
  "position": "...",
  "photo_url": null,
  "children": [
    {
      "title": "Akademiya kengashi",
      "children": [...]
    }
  ]
}]
```

### Haqida sahifalari
| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/aboutsocial/` | Axborot xizmati vazifalari va funksiyalari |
| GET | `/api/about-academy/` | Akademiya haqida (bo'limlar, dasturlar, gallery) |

---

## 18. Aloqa (Contact)

| Method | URL | Tavsif |
|--------|-----|--------|
| GET | `/api/faq/` | FAQ ro'yxati |
| POST | `/api/faq/submit/` | FAQ yuborish |
| POST | `/api/faq/<uuid>/vote/` | FAQ ovoz berish |
| POST | `/api/rector-appeal/` | Rektora murojaat |

---

## Pagination

Barcha list viewlar quyidagi standart pagination formatini qaytaradi:
```json
{
  "count": 100,
  "next": "https://.../api/news/?page=2",
  "previous": null,
  "results": [...]
}
```
Pagination yo'q bo'lganda — to'g'ridan to'g'ri `[...]` array qaytadi.

---

## Ko'rishlar hisobi — to'liq endpoint jadvali

| POST endpoint | Model |
|---------------|-------|
| `/api/news/<uuid>/view/` | News |
| `/api/events/<uuid>/view/` | Event |
| `/api/blogs/<uuid>/view/` | Blog |
| `/api/korrupsiya/<uuid>/view/` | Korrupsiya |
| `/api/elon/<uuid>/view/` | Elon (InformationContent) |
| `/api/tenders/<uuid>/view/` | TenderAnnouncement |
| `/api/persons/<uuid>/view/` | Person |
| `/api/magistr-talabalar/<uuid>/view/` | MagistrTalaba |
| `/api/academic/fakultet-kafedralar/<slug>/view/` | FakultetKafedra |
| `/api/academic/huzuridagi-tashkilotlar/` | — (list only) |
| `/api/international-posts/<uuid>/view/` | InternationalPost |
| `/api/international-ratings/<uuid>/view/` | InternationalRating |
| `/api/infra/sport-majmua/<slug>/view/` | SportMajmua |
| `/api/activities/faoliyat/<uuid>/view/` | IlmiyFaoliyat |
| `/api/activities/sport/tadbirlar/<uuid>/view/` | SportTadbir |
| `/api/activities/sport/yonalishlar/<uuid>/view/` | SportYonalish |

---

## Xatolik kodlari

| Code | Ma'no |
|------|-------|
| 200 | Muvaffaqiyatli |
| 201 | Yaratildi (POST /view/ — yangi ko'rish) |
| 400 | Noto'g'ri so'rov |
| 404 | Topilmadi |

---

## Til parametri

Barcha multilang endpointlar `?lang=uz` (default), `?lang=ru`, `?lang=en` qabul qiladi.  
Tarjima yo'q bo'lsa — `uz` qiymati qaytariladi (fallback).
