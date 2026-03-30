# Academic Structure — To'liq Qo'llanma

> Tuzilma, Rektorat, Kengash va barcha bo'lim sahifalarining ishlash mantig'i.
> Backend + Frontend uchun reference hujjat.

---

## Umumiy Arxitektura

```
OrganizationUnit (daraxt)
│
├── Universitet kengashi        [council]
├── Kuzatuv kengashi            [supervisory]
│
├── Rektor ★                    [rector]       ← is_featured: true
│   ├── Rektorat tashkiliy      [division]
│   ├── Xodimlar bo'limi        [division]
│   ├── Audit xizmati           [division]
│   ├── Yuridik xizmat          [division]
│   ├── Matbuot xizmati         [division]
│   ├── Devonxona va arxiv      [division]
│   ├── Raqamli ta'lim markazi  [center]
│   └── Institutlar va filiallar[institute]
│
├── Yoshlar masalalari prorektor [prorector]
│   └── ...
│
├── Ta'lim ishlari prorektor     [prorector]
│   └── ...
│
├── Fakultetlar                  [faculty]
│   └── Kafedralar               [department]
│
└── Markazlar                    [center]
```

---

## Ma'lumotlar Bazasi Modellari

### OrganizationUnit

```
┌────────────────────────────────────────────────┐
│              OrganizationUnit                  │
├────────────────┬───────────────────────────────┤
│ id             │ integer (PK)                  │
│ title_uz       │ varchar(255)                  │
│ title_ru       │ varchar(255)                  │
│ title_en       │ varchar(255)                  │
│ slug           │ varchar(255) UNIQUE           │ ← URL uchun
│ unit_type      │ choice (quyida)               │ ← render mantig'i
│ parent_id      │ FK → OrganizationUnit (null)  │ ← daraxt
│ content_uz     │ text                          │ ← sahifa matni
│ content_ru     │ text                          │
│ content_en     │ text                          │
│ has_own_page   │ boolean (default: false)      │ ← kliklanadimi
│ is_featured    │ boolean (default: false)      │ ← katta blokmi
│ order          │ integer (default: 0)          │ ← tartib
│ is_active      │ boolean (default: true)       │
│ created_at     │ datetime                      │
│ updated_at     │ datetime                      │
└────────────────┴───────────────────────────────┘

unit_type tanlovi:
  council      → Universitet kengashi
  supervisory  → Kuzatuv kengashi
  rector       → Rektor
  prorector    → Prorektor
  faculty      → Fakultet
  department   → Kafedra
  center       → Markaz
  institute    → Institut
  public_org   → Jamoat tashkiloti
  division     → Bo'lim
```

### Staff

```
┌────────────────────────────────────────────────┐
│                    Staff                       │
├────────────────┬───────────────────────────────┤
│ id             │ integer (PK)                  │
│ unit_id        │ FK → OrganizationUnit         │ ← qaysi bo'limda
│ role           │ choice (quyida)               │ ← lavozim turi
│ is_head        │ boolean (default: false)      │ ← bo'lim rahbari
│ title_uz       │ varchar(255)                  │ ← "Rektor", "Prorektor"
│ title_ru       │ varchar(255)                  │
│ title_en       │ varchar(255)                  │
│ full_name      │ varchar(255)                  │
│ position_uz    │ varchar(255)                  │ ← "Fan doktori, professor"
│ position_ru    │ varchar(255)                  │
│ position_en    │ varchar(255)                  │
│ image          │ imagefield                    │
│ address        │ varchar(300)                  │
│ reception_uz   │ varchar(100)                  │ ← "Seshanba 14:00-17:00"
│ phone          │ varchar(25)                   │
│ fax            │ varchar(25)                   │
│ email          │ varchar(254)                  │
│ order          │ integer (default: 0)          │
│ is_active      │ boolean (default: true)       │
│ created_at     │ datetime                      │
│ updated_at     │ datetime                      │
└────────────────┴───────────────────────────────┘

role tanlovi:
  rector         → Rektor
  prorector      → Prorektor
  dean           → Dekan
  dept_head      → Kafedra mudiri
  council_member → Kengash a'zosi
  staff          → Xodim
```

### Modellar orasidagi bog'lanish

```
OrganizationUnit (1)──────────────(∞) Staff
      │
      │ parent FK
      │
OrganizationUnit (1)──────────────(∞) OrganizationUnit
(parent)                               (children)
```

---

## API Endpointlar

### 1. Tuzilma daraxti

```
GET /api/structure/
```

**Parametrlar:**
```
?type=faculty       → faqat fakultetlar
?type=department    → faqat kafedralar
?type=center        → faqat markazlar
```

**Javob:**
```json
[
  {
    "id": 1,
    "title": "Universitet kengashi",
    "unit_type": "council",
    "slug": "universitet-kengashi",
    "has_own_page": true,
    "is_featured": false,
    "order": 1,
    "children": []
  },
  {
    "id": 2,
    "title": "Kuzatuv kengashi",
    "unit_type": "supervisory",
    "slug": "kuzatuv-kengashi",
    "has_own_page": true,
    "is_featured": false,
    "order": 2,
    "children": []
  },
  {
    "id": 3,
    "title": "Rektor",
    "unit_type": "rector",
    "slug": "rektorat",
    "has_own_page": true,
    "is_featured": true,
    "order": 3,
    "children": [
      {
        "id": 10,
        "title": "Rektorat tashkiliy xizmati",
        "unit_type": "division",
        "slug": "rektorat-tashkiliy",
        "has_own_page": true,
        "is_featured": false,
        "order": 1,
        "children": []
      },
      {
        "id": 11,
        "title": "Xodimlar bo'limi",
        "unit_type": "division",
        "slug": "xodimlar-bolimi",
        "has_own_page": true,
        "is_featured": false,
        "order": 2,
        "children": []
      },
      {
        "id": 12,
        "title": "Audit xizmati",
        "unit_type": "division",
        "slug": "audit-xizmati",
        "has_own_page": false,
        "is_featured": false,
        "order": 3,
        "children": []
      }
    ]
  },
  {
    "id": 4,
    "title": "Yoshlar masalalari bo'yicha birinchi prorektor",
    "unit_type": "prorector",
    "slug": "prorector-yoshlar",
    "has_own_page": true,
    "is_featured": false,
    "order": 4,
    "children": [
      {
        "id": 20,
        "title": "Institutlar va filiallar",
        "unit_type": "institute",
        "slug": "institutlar-filiallar",
        "has_own_page": true,
        "is_featured": false,
        "order": 1,
        "children": []
      }
    ]
  }
]
```

---

### 2. Bo'lim detail sahifasi (universal)

```
GET /api/units/<slug>/
```

**Misollar:**
```
GET /api/units/universitet-kengashi/
GET /api/units/rektorat/
GET /api/units/xodimlar-bolimi/
GET /api/units/xotin-qizlar-qomitasi/
```

**Javob:**
```json
{
  "id": 1,
  "title": "Universitet kengashi",
  "title_ru": "Университетский совет",
  "title_en": "University Council",
  "unit_type": "council",
  "slug": "universitet-kengashi",
  "content": "Kengash O'zbekiston Milliy universiteti doimiy faoliyat...",
  "staff": [
    {
      "id": 5,
      "is_head": true,
      "role": "council_member",
      "title": "Universitet kengashi kotibi",
      "full_name": "Baymirov Kayum Shayimovich",
      "position": "Fan doktori, professor",
      "image": "https://cdn.usas.uz/staff/baymirov.jpg",
      "address": "100174, Toshkent, Universitet ko'chasi 4",
      "reception": "Dushanba-Juma, 14:00-17:00",
      "phone": "+998 71 227-1540",
      "fax": "",
      "email": "kengash@usas.uz",
      "order": 1
    },
    {
      "id": 6,
      "is_head": false,
      "role": "council_member",
      "title": "Kengash a'zosi",
      "full_name": "...",
      "position": "...",
      "image": "...",
      "address": "...",
      "reception": "...",
      "phone": "...",
      "fax": "",
      "email": "...",
      "order": 2
    }
  ],
  "children": [],
  "breadcrumb": [
    {"title": "Akademiya", "slug": null},
    {"title": "Universitet kengashi", "slug": "universitet-kengashi"}
  ]
}
```

---

### 3. Rektorat xodimlari

```
GET /api/staff/
```

**Parametrlar:**
```
?unit__slug=rektorat              → rektorat xodimlari
?role=rector                      → faqat rektorlar
?role=prorector                   → faqat prorektorlar
?unit__type=faculty               → barcha fakultet dekanlar
?is_head=true                     → faqat rahbarlar
?ordering=order                   → tartib bo'yicha
```

**Javob:**
```json
[
  {
    "id": 1,
    "is_head": true,
    "role": "rector",
    "title": "Rektor",
    "full_name": "Madjidov Inom Urishevich",
    "position": "Texnika fanlari doktori, professor",
    "image": "https://cdn.usas.uz/staff/madjidov.jpg",
    "address": "100174, Toshkent, Olmazor tumani, Universitet ko'chasi 4",
    "reception": "Seshanba, soat 14:00-17:00",
    "phone": "+998 71 227-12-24",
    "fax": "+998 71 246-02-24",
    "email": "rektor@usas.uz",
    "order": 1
  },
  {
    "id": 2,
    "is_head": false,
    "role": "prorector",
    "title": "Birinchi prorektor",
    "full_name": "...",
    "position": "...",
    "image": "...",
    "address": "...",
    "reception": "...",
    "phone": "...",
    "fax": "...",
    "email": "...",
    "order": 2
  }
]
```

---

## Sahifalar va Navigatsiya

### Tuzilma sahifasidan bo'lim sahifasiga o'tish

```
1-QADAM: Tuzilma sahifasi
─────────────────────────
URL: /akademiya/tuzilma/
API: GET /api/structure/

Frontend daraxt chizadi:
  ┌─────────────────────────────────────────┐
  │  [Kengash ✅]     [Kuzatuv kengashi ✅] │
  │                                         │
  │         ┌──── [★ REKTOR ✅] ────┐      │
  │         │                       │      │
  │  [Xodimlar ✅] [Audit ❌] [Rektorat ✅]│
  └─────────────────────────────────────────┘

  ✅ = has_own_page: true  → kliklanadi
  ❌ = has_own_page: false → kliklanmaydi


2-QADAM: Foydalanuvchi "Rektor" ni bosadi
──────────────────────────────────────────
URL: /akademiya/rektorat/
API: GET /api/units/rektorat/

Sahifa ochiladi:
  ┌─────────────────────────────────────────┐
  │  [RASM] │ Rektor                        │
  │         │ MADJIDOV INOM URISHEVICH      │
  │         │ 📍 Toshkent, Universitet 4    │
  │         │ 🕐 Seshanba 14:00-17:00       │
  │         │ 📞 +998 71 227-12-24          │
  │         │ ✉️  rektor@usas.uz            │
  └─────────────────────────────────────────┘


3-QADAM: Foydalanuvchi "Xodimlar bo'limi" ni bosadi
────────────────────────────────────────────────────
URL: /akademiya/xodimlar-bolimi/
API: GET /api/units/xodimlar-bolimi/

Xuddi shu pattern: karta + matn
```

---

## Frontend Render Mantig'i

```javascript
// Tuzilma chart uchun
function renderUnitBox(unit) {
  if (unit.is_featured) {
    return <BigFeaturedBox unit={unit} />    // Rektor — katta
  }

  if (unit.has_own_page) {
    return (
      <a href={`/akademiya/${unit.slug}/`}>
        <UnitBox unit={unit} />             // kliklanadigan quti
      </a>
    )
  }

  return <UnitBox unit={unit} />            // oddiy quti, klik yo'q
}


// Bo'lim sahifasi uchun
function UnitDetailPage({ slug }) {
  const unit = fetch(`/api/units/${slug}/`)

  // unit_type ga qarab layout tanlaydi
  switch (unit.unit_type) {
    case 'council':    return <CouncilLayout unit={unit} />
    case 'rector':     return <RectorLayout unit={unit} />
    case 'prorector':  return <ProrectorLayout unit={unit} />
    default:           return <DefaultUnitLayout unit={unit} />
  }

  // Lekin barcha layout bir xil komponent ishlatadi:
  //   <StaffCard staff={unit.staff[0]} />   ← rahbar (is_head: true)
  //   <ContentBlock text={unit.content} />  ← matn
  //   <StaffList staff={unit.staff} />      ← qolgan xodimlar
  //   <ChildrenList children={unit.children} />
}
```

---

## Xodim Kartasi Komponenti

Barcha sahifalarda ishlatiladi — bir marta yoziladi:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  ┌─────────┐   Lavozim nomi (title)                 │
│  │         │   ───────────────────                  │
│  │  RASM   │   TO'LIQ ISM (full_name)               │
│  │         │                                        │
│  └─────────┘   📍  address                          │
│                🕐  reception                         │
│                📞  phone                             │
│                🖨️   fax  (bo'sh bo'lsa ko'rsatilmaydi)│
│                ✉️   email                            │
│                                                      │
└──────────────────────────────────────────────────────┘

Props:
  staff.title      → "Rektor" / "Kengash kotibi" / ...
  staff.full_name  → "Madjidov Inom Urishevich"
  staff.position   → "Texnika fanlari doktori, professor"
  staff.image      → rasm URL
  staff.address    → manzil
  staff.reception  → qabul vaqti
  staff.phone      → telefon
  staff.fax        → faks (ixtiyoriy)
  staff.email      → email
```

---

## To'liq Sahifalar Ro'yxati

```
SAHIFA                       FRONTEND URL                      API
─────────────────────────────────────────────────────────────────────────────
Tuzilma (org chart)          /akademiya/tuzilma/               GET /api/structure/
Faqat Fakultetlar            /akademiya/fakultetlar/           GET /api/structure/?type=faculty
Faqat Kafedralar             /akademiya/kafedralar/            GET /api/structure/?type=department

Rektorat                     /akademiya/rektorat/              GET /api/units/rektorat/
Universitet kengashi         /akademiya/universitet-kengashi/  GET /api/units/universitet-kengashi/
Kuzatuv kengashi             /akademiya/kuzatuv-kengashi/      GET /api/units/kuzatuv-kengashi/

Xodimlar bo'limi             /akademiya/xodimlar-bolimi/       GET /api/units/xodimlar-bolimi/
Audit xizmati                /akademiya/audit-xizmati/         GET /api/units/audit-xizmati/
Raqamli ta'lim markazi       /akademiya/raqamli-talim/         GET /api/units/raqamli-talim/
Xotin-qizlar qo'mitasi       /akademiya/xotin-qizlar-qomitasi/ GET /api/units/xotin-qizlar-qomitasi/

Har qanday yangi bo'lim      /akademiya/<slug>/                GET /api/units/<slug>/
─────────────────────────────────────────────────────────────────────────────
BARCHA BO'LIM SAHIFALARI = 1 TA ENDPOINT PATTERN
```

---

## Admin Panelda Qanday Kiritiladi

```
BO'LINMA QO'SHISH
═══════════════════════════════════════════
Nomi (uz):       [ Xodimlar bo'limi         ]
Nomi (ru):       [ Отдел кадров             ]
Nomi (en):       [ HR Department            ]

Turi:            [ ▼ Bo'lim (division)      ]  ← dropdown

Yuqori bo'linma: [ ▼ Rektorat              ]  ← parent

Kontent (uz):    [ Bo'lim haqida matn...   ]
                 [                          ]

O'z sahifasi:    [✓]  ← has_own_page
Ajratilgan blok: [ ]  ← is_featured (faqat Rektor uchun)
Tartib raqami:   [ 2 ]
Faol:            [✓]
═══════════════════════════════════════════

XODIM QO'SHISH
═══════════════════════════════════════════
Bo'limi:         [ ▼ Xodimlar bo'limi      ]
Lavozim turi:    [ ▼ Xodim (staff)         ]
Rahbar:          [✓]  ← is_head

Ismi:            [ Rahimov Sardor          ]
Lavozim (uz):    [ Bo'lim mudiri           ]
Rasm:            [ fayl tanlash            ]
Manzil:          [ Toshkent, Universitet 4 ]
Qabul vaqti:     [ Dushanba-Juma 14:00-17:00 ]
Telefon:         [ +998 71 ...             ]
Faks:            [                         ]
Email:           [ xodimlar@usas.uz        ]
Tartib:          [ 1 ]
═══════════════════════════════════════════
```

---

## Edge Caselar

| Holat | Yechim |
|-------|--------|
| Bo'lim o'chirilsa | `is_active: false` — ma'lumot saqlanadi, ko'rsatilmaydi |
| Parent o'zgarsa | `parent_id` yangilanadi — `slug` o'zgarmaydi, URL saqlanadi |
| Bir kishi ikki bo'limda | Ikki `Staff` yozuvi — har biri o'z `unit`-i bilan |
| Bo'limning xodimi yo'q | `staff: []` — sahifa ochiladi, karta bo'sh |
| Tuzilmada ko'rinmasin | `is_active: false` — lekin sahifasi saqlanadi |
| Klik bo'lmasin | `has_own_page: false` — sahifa yo'q, faqat chartda |

---

## Xulosa

```
DATABASE:   2 ta model    → OrganizationUnit + Staff
ENDPOINTS:  3 ta pattern  → /structure/ + /units/<slug>/ + /staff/
FRONTEND:   1 ta komponent → StaffCard (hamma joyda)
ADMIN:      Qo'lda         → unit_type, parent, order kiritiladi
SLUG:       Avtomatik      → nomdan yasaladi, URL sifatida ishlatiladi
```
