# View Count API — Frontend Documentation

## Umumiy Tushuncha

View count ikkita yo'l bilan ishlaydi:

1. **GET** (list/detail) — javobda `views_count` maydoni avtomatik keladi
2. **POST** `/api/.../view/` — foydalanuvchi sahifani ochganda shu endpoint chaqiriladi, cookie orqali duplicate hisoblanmaydi

---

## Cookie Mexanizmi

- Backend `view_token` cookie ni avtomatik o'rnatadi (UUID, 1 yil muddatli)
- Frontend hech narsa qilmasin — brauzer cookie ni o'zi yuboradi
- Bir xil qurilmadan ikkinchi marta POST qilsa `is_new: false` qaytadi (count ortmaydi)

---

## POST Endpoint — Umumiy Format

**Barcha POST view endpointlari bir xil ishlaydi:**

```
POST /api/{resource}/{uuid}/view/
```

**Request:**
- Body: bo'sh (empty)
- Cookie: `view_token=<UUID>` (birinchi marta yo'q bo'lsa backend o'zi yaratadi)

**Response 201** — yangi view (birinchi marta):
```json
{
  "views_count": 42,
  "is_new": true
}
```

**Response 200** — takror view (bir xil qurilma):
```json
{
  "views_count": 42,
  "is_new": false
}
```

---

## Barcha View Count Endpointlari

### NEWS DOMAIN

| POST (view yozish) | GET (views_count bilan) |
|---|---|
| `POST /api/news/{uuid}/view/` | `GET /api/news/` |
| `POST /api/events/{uuid}/view/` | `GET /api/news/{slug}/` |
| `POST /api/blogs/{uuid}/view/` | `GET /api/news/{uuid}/` |
| `POST /api/korrupsiya/{uuid}/view/` | `GET /api/events/` |
| `POST /api/elon/{uuid}/view/` | `GET /api/events/{slug}/` |
| | `GET /api/events/{uuid}/` |
| | `GET /api/blogs/` |
| | `GET /api/blogs/{slug}/` |
| | `GET /api/blogs/{uuid}/` |
| | `GET /api/korrupsiya/` |
| | `GET /api/korrupsiya/{slug}/` |
| | `GET /api/korrupsiya/{uuid}/` |
| | `GET /api/elon/` |
| | `GET /api/elon/{uuid}/` |
| | `GET /api/gallery/photo/` |
| | `GET /api/gallery/photo/{uuid}/` |
| | `GET /api/gallery/video/` |
| | `GET /api/gallery/video/{uuid}/` |

---

### ACTIVITIES DOMAIN

| POST (view yozish) | GET (views_count bilan) |
|---|---|
| `POST /api/activities/faoliyat/{uuid}/view/` | `GET /api/activities/faoliyat/` |
| `POST /api/activities/sport/tadbirlar/{uuid}/view/` | `GET /api/activities/faoliyat/{uuid}/` |
| `POST /api/activities/sport/yonalishlar/{uuid}/view/` | `GET /api/activities/sport/tadbirlar/` |

---

### PAGES DOMAIN

| POST (view yozish) | GET (views_count bilan) |
|---|---|
| `POST /api/markazlar/{slug}/view/` | `GET /api/markazlar/` |
| | `GET /api/markazlar/{slug}/` |

> **Eslatma:** Bu endpoint `{uuid}` emas, `{slug}` ishlatadi.

---

### INTERNATIONAL DOMAIN

| POST (view yozish) | GET (views_count bilan) |
|---|---|
| `POST /api/international-posts/{uuid}/view/` | `GET /api/international-posts/` |
| `POST /api/international-ratings/{uuid}/view/` | `GET /api/international-posts/{uuid}/` |
| | `GET /api/international-posts/slug/{slug}/` |
| | `GET /api/international-ratings/` |
| | `GET /api/international-ratings/{slug}/` |

---

### ACADEMIC DOMAIN

| POST (view yozish) | GET (views_count bilan) |
|---|---|
| `POST /api/academic/fakultet-kafedralar/{slug}/view/` | `GET /api/academic/fakultet-kafedralar/{slug}/` |
| | `GET /api/academic/huzuridagi-tashkilotlar/` |
| | `GET /api/academic/jamoat-tashkilotlar/` |

> **Eslatma:** Bu endpoint `{slug}` ishlatadi.

---

### INFRA DOMAIN

| POST (view yozish) | GET (views_count bilan) |
|---|---|
| `POST /api/infra/sport-majmua/{slug}/view/` | `GET /api/infra/sport-majmua/` |
| | `GET /api/infra/sport-majmua/{slug}/` |

> **Eslatma:** Bu endpoint `{slug}` ishlatadi.

---

### STUDENTS DOMAIN

| POST (view yozish) | GET (views_count bilan) |
|---|---|
| `POST /api/persons/{uuid}/view/` | `GET /api/persons/` |
| `POST /api/magistr-talabalar/{uuid}/view/` | `GET /api/persons/{uuid}/` |
| | `GET /api/olimpiya/` |
| | `GET /api/magistr-talabalar/` |
| | `GET /api/magistr-talabalar/{uuid}/` |

---

### TENDERS DOMAIN

| POST (view yozish) | GET (views_count bilan) |
|---|---|
| `POST /api/tenders/{uuid}/view/` | `GET /api/tenders/` |
| | `GET /api/tenders/{uuid}/` |
| | `GET /api/tenders/slug/{slug}/` |
| | `GET /api/tanlovlar/` |
| | `GET /api/tanlovlar/{uuid}/` |
| | `GET /api/tanlovlar/slug/{slug}/` |

---

### QABUL DOMAIN (alohida mexanizm)

Bu domain tracker ishlatmaydi — `GET` qilganda avtomatik +1 bo'ladi.

| Endpoint | Izoh |
|---|---|
| `GET /api/qabul/yangiliklar/{uuid}/` | Har GET da `views` +1 bo'ladi |

**Response ichida:**
```json
{
  "views": 15,
  ...
}
```

---

## Frontend Uchun Namuna Kod

### JavaScript / Fetch

```javascript
// Sahifa ochilganda chaqiring
async function recordView(resourceType, id) {
  await fetch(`/api/${resourceType}/${id}/view/`, {
    method: 'POST',
    credentials: 'include',  // cookie yuborish uchun muhim!
  });
}

// Misol:
recordView('news', '550e8400-e29b-41d4-a716-446655440000');
recordView('events', '550e8400-e29b-41d4-a716-446655440001');
```

### Axios

```javascript
axios.post(`/api/news/${id}/view/`, {}, {
  withCredentials: true  // cookie yuborish uchun muhim!
});
```

> **Muhim:** `credentials: 'include'` yoki `withCredentials: true` bo'lmasa cookie ketmaydi va har safar yangi view hisoblanadi.

---

## GET Response Misoli (views_count bilan)

`GET /api/news/` javobida har item ichida `views_count` keladi:

```json
{
  "count": 10,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Yangilik sarlavhasi",
      "views_count": 127,
      ...
    }
  ]
}
```

`GET /api/news/{uuid}/` (detail) javobida ham `views_count` keladi:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Yangilik sarlavhasi",
  "views_count": 127,
  ...
}
```
