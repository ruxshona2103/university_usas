# Variant A Handoff Report (Navbar ↔ Academic)

Sana: 2026-03-30  
Loyiha: `university_usas`  
Maqsad: `academic` va `navbar` orasida slugni bitta manbadan boshqarish.

---

## 1) Vazifa va qaror

### Muammo
- Avval `slug` ikki joyda yurardi:
	- `domains/pages/models/navbar.py` ichida `NavbarSubItem.slug`
	- `domains/academic/models/unit.py` ichida `OrganizationUnit.slug`
- Natijada bir bo‘lim uchun ikki marta slug nazorati kerak bo‘lib qolgan.

### Qabul qilingan yechim (Variant A)
- `OrganizationUnit` ni `NavbarSubItem` ga bog‘lash.
- Bog‘langan holatda `OrganizationUnit.slug` avtomatik ravishda `NavbarSubItem.slug` dan olinadi.
- Demak, slugning asosiy manbasi navbar bo‘ladi.

---

## 2) Qilingan kod o‘zgarishlari

## `domains/academic/models/unit.py`

### Qo‘shilgan maydon
- `navbar_item = OneToOneField('pages.NavbarSubItem', null=True, blank=True, on_delete=SET_NULL, related_name='academic_unit')`

### Biznes qoidalari (`clean`)
- `navbar_item` tanlansa:
	- `page_type='redirect'` bo‘lgan itemga bog‘lash taqiqlanadi.
	- `is_active=False` bo‘lgan itemga bog‘lash taqiqlanadi.

### Slug sinxroni (`save`)
- Agar `navbar_item` mavjud bo‘lsa:
	- `self.slug = self.navbar_item.slug`
- Aks holda:
	- Eski fallback slug generator (`title_uz` dan) ishlashda davom etadi.

---

## `domains/academic/admin.py`

### Admin UX yaxshilanishlari
- `OrganizationUnitAdmin` ga `navbar_item` tanlash maydoni qo‘shildi.
- `search_fields` ga `navbar_item__name_uz` qo‘shildi.
- `formfield_for_foreignkey` orqali dropdown filtrlash:
	- faqat `NavbarSubItem` ichidan `is_active=True` va `page_type=STATIC`.

Natija:
- Admin foydalanuvchi xato item tanlamaydi.
- Slug qo‘lda kiritish ehtiyoji kamayadi.

---

## `domains/pages/models/navbar.py`

### Slug o‘zgarganda academic sync
- `NavbarSubItem.save()` ichida saqlangandan keyin:
	- agar bog‘langan `academic_unit` bo‘lsa va slug farq qilsa,
	- `academic_unit.save()` chaqirilib slug sinxronlanadi.

Natija:
- Navbar slug update qilinsa academic slug ham yangilanadi.

---

## `domains/academic/migrations/0004_organizationunit_navbar_item.py`

### Migration
- `OrganizationUnit` ga `navbar_item` maydoni qo‘shilgan.
- Dependency:
	- `academic.0003_...`
	- `pages.0006_herovideo`

---

## 3) Yangi management command

## `domains/academic/management/commands/map_academic_navbar.py`

### Vazifasi
- Mavjud `OrganizationUnit` yozuvlarini mos `NavbarSubItem` ga avtomatik bog‘lash.

### Matching strategiyasi
1. Avval `slug` bo‘yicha match.
2. Topilmasa `title_uz` → `slugify` bo‘yicha match.

### Candidate cheklovi
- Faqat `NavbarSubItem` ichidan:
	- `is_active=True`
	- `page_type=STATIC`

### Xavfsizlik holatlari
- `NOT FOUND`: mos item topilmadi.
- `AMBIGUOUS`: title bo‘yicha bir nechta kandidat chiqdi.
- `CONFLICT`: topilgan navbar item allaqachon boshqa unitga biriktirilgan.

### Ishlash rejimlari
- Default: `dry-run` (DB ga yozmaydi, faqat preview).
- `--apply`: real bog‘laydi.
- `--include-linked`: oldin bog‘langan unitlarni ham ko‘rib chiqadi.

---

## 4) Ishga tushirilgan buyruqlar va natijalar

Quyidagi buyruqlar bajarildi:

```bash
source venv/bin/activate
python manage.py makemigrations academic
```

Natija:
- `academic.0004_organizationunit_navbar_item` yaratildi.

```bash
source venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py migrate academic
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py check
```

Natija:
- migration muvaffaqiyatli qo‘llandi;
- `System check identified no issues (0 silenced)`.

```bash
source venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py map_academic_navbar
```

Dry-run natija namunasi:
- `units=1`, `navbar_candidates=1`
- `NOT FOUND` holati chiqdi (`Xodimlar bo‘limi` uchun mos navbar item topilmadi).
- `Summary: matched=0, applied=0, not_found=1, ambiguous=0, conflicts=0`

---

## 5) Hozirgi holat

- Variant A arxitekturasi kodda joriy qilingan.
- Slug ownership navbar tomonga o‘tkazilgan (linked yozuvlar uchun).
- Adminda noto‘g‘ri bog‘lash ehtimoli kamaytirilgan.
- Avtomatik mapping command qo‘shilgan.
- Project check holati toza.

---

## 6) Qolgan ishlar (operatsion)

1. `NOT FOUND` chiqqan unit(lar) uchun mos `NavbarSubItem` yaratish yoki slugni moslashtirish.
2. Keyin real apply:

```bash
source venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py map_academic_navbar --apply
```

3. Tekshiruv:

```bash
source venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py check
```

4. Ixtiyoriy: allaqachon linked yozuvlarni qayta hisoblash kerak bo‘lsa:

```bash
source venv/bin/activate
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py map_academic_navbar --apply --include-linked
```

---

## 7) Agentlar uchun qisqa executive summary

- Muammo: academic va navbar sluglari ikki manbada yurardi.
- Yechim (Variant A): `OrganizationUnit` ↔ `NavbarSubItem` OneToOne link.
- Qoidalar: faqat `active + static` navbar itemga bog‘lash.
- Slug sinxroni: linked holatda academic slug navbar slugdan olinadi.
- Migratsiya: `academic.0004` qo‘shildi va qo‘llandi.
- Utility: `map_academic_navbar` command bilan bulk map (dry-run/apply).
- Holat: implement tayyor, bitta mapping `NOT FOUND` case mavjud.

