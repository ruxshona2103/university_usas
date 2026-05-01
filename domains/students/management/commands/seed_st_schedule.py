"""
python manage.py seed_st_schedule
"""
from django.core.management.base import BaseCommand
from domains.students.models import StudentInfoCategory, StudentInfo

CATEGORY = {
    'slug':     'st-schedule',
    'order':    7,
    'title_uz': 'Dars jadvali',
    'title_ru': 'Расписание занятий',
    'title_en': 'Class Schedule',
}

ITEM = {
    'order':    1,
    'title_uz': 'Dars jadvali',
    'title_ru': 'Расписание занятий',
    'title_en': 'Class Schedule',
    'content_uz': """O'zbekiston davlat sport akademiyasi bakalavriat ta'lim yo'nalishlarida dars mashg'ulotlari asosan ertalabki smenada tashkil etiladi.

Dars mashg'ulotlari quyidagi vaqt oralig'ida o'tkaziladi:

<table>
<thead>
  <tr>
    <th>Juftlik</th>
    <th>Boshlanish vaqti</th>
    <th>Tugash vaqti</th>
  </tr>
</thead>
<tbody>
  <tr><td>I-Juftlik</td><td>9:00</td><td>10:20</td></tr>
  <tr><td>II-Juftlik</td><td>10:30</td><td>11:50</td></tr>
  <tr><td>III-Juftlik</td><td>12:00</td><td>13:20</td></tr>
  <tr><td>IV-Juftlik</td><td>13:30</td><td>14:50</td></tr>
  <tr><td>V-Juftlik</td><td>15:00</td><td>16:20</td></tr>
  <tr><td>VI-Juftlik</td><td>16:30</td><td>17:50</td></tr>
</tbody>
</table>""",

    'content_ru': """Учебные занятия на бакалаврских направлениях Государственной академии спорта Узбекистана проводятся преимущественно в утреннюю смену.

Занятия проводятся в следующие временные интервалы:

<table>
<thead>
  <tr>
    <th>Пара</th>
    <th>Начало</th>
    <th>Конец</th>
  </tr>
</thead>
<tbody>
  <tr><td>I пара</td><td>9:00</td><td>10:20</td></tr>
  <tr><td>II пара</td><td>10:30</td><td>11:50</td></tr>
  <tr><td>III пара</td><td>12:00</td><td>13:20</td></tr>
  <tr><td>IV пара</td><td>13:30</td><td>14:50</td></tr>
  <tr><td>V пара</td><td>15:00</td><td>16:20</td></tr>
  <tr><td>VI пара</td><td>16:30</td><td>17:50</td></tr>
</tbody>
</table>""",

    'content_en': """Academic classes at the bachelor's degree programs of the Uzbekistan State Sports Academy are mainly organized in the morning shift.

Classes are held in the following time intervals:

<table>
<thead>
  <tr>
    <th>Period</th>
    <th>Start time</th>
    <th>End time</th>
  </tr>
</thead>
<tbody>
  <tr><td>Period I</td><td>9:00</td><td>10:20</td></tr>
  <tr><td>Period II</td><td>10:30</td><td>11:50</td></tr>
  <tr><td>Period III</td><td>12:00</td><td>13:20</td></tr>
  <tr><td>Period IV</td><td>13:30</td><td>14:50</td></tr>
  <tr><td>Period V</td><td>15:00</td><td>16:20</td></tr>
  <tr><td>Period VI</td><td>16:30</td><td>17:50</td></tr>
</tbody>
</table>""",
}


class Command(BaseCommand):
    help = "Dars jadvali ma'lumotlarini yuklaydi"

    def handle(self, *args, **options):
        cat, created = StudentInfoCategory.objects.update_or_create(
            slug=CATEGORY['slug'],
            defaults=CATEGORY,
        )
        action = 'yaratildi' if created else 'yangilandi'
        self.stdout.write(self.style.SUCCESS(f"Kategoriya: {cat.title_uz} — {action}"))

        item, created = StudentInfo.objects.update_or_create(
            category=cat,
            order=ITEM['order'],
            defaults={**ITEM, 'category': cat, 'is_active': True},
        )
        action = 'yaratildi' if created else 'yangilandi'
        self.stdout.write(self.style.SUCCESS(f"Item: {item.title_uz} — {action}"))

        self.stdout.write(self.style.SUCCESS("\nEndpoint: GET /api/student-info/st-schedule/"))
