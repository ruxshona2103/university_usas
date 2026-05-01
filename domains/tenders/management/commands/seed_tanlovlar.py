"""
python manage.py seed_tanlovlar
python manage.py seed_tanlovlar --clear
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from domains.tenders.models import TenderAnnouncement

DATA = [
    {
        "title_uz": "O'zbekiston davlat sport akademiyasi insholar tanlovini e'lon qiladi",
        "title_ru": "Узбекистанская государственная спортивная академия объявляет конкурс сочинений",
        "title_en": "Uzbekistan State Sports Academy announces an essay competition",
        "description_uz": (
            "Quyidagi mavzularda talabalar o'rtasida Insholar tanlovi o'tkaziladi:\n\n"
            "• \"Jadidlar jasorati – millatimiz faxri\" hamda\n"
            "• \"Jadidlar: milliy o'zlik, istiqlol va davlatchilik g'oyalari\"\n\n"
            "➡ Tanlov shartlari:\n\n"
            "• Insho mustaqil va ijodiy yozilgan bo'lishi kerak.\n"
            "• Ish hajmi 2–3 bet bo'lishi tavsiya etiladi.\n"
            "• Inshoda mavzuning mazmuni va g'oyasi aniq yoritilishi lozim.\n\n"
            "Tanlovning maqsadi:\n\n"
            "• Jadidlar harakati va ularning tarixiy merosini keng targ'ib qilish.\n"
            "• Yoshlar qalbida vatanparvarlik va milliy g'urur tuyg'ularini shakllantirish.\n\n"
            "📍 Manzil: O'zbekiston davlat sport akademiyasi\n\n"
            "📞 Bog'lanish uchun:\n"
            "Iqtidorli talabalarning ilmiy tadqiqot faoliyatini tashkil etish sektori hamda "
            "Yoshlar bilan ishlash, ma'naviyat va ma'rifat bo'limiga murojaat qiling."
        ),
        "description_ru": (
            "Среди студентов проводится конкурс сочинений по следующим темам:\n\n"
            "• «Мужество джадидов — гордость нашего народа»\n"
            "• «Джадиды: национальная идентичность, независимость и государственность»\n\n"
            "➡ Условия конкурса:\n\n"
            "• Сочинение должно быть написано самостоятельно и творчески.\n"
            "• Рекомендуемый объём работы — 2–3 страницы.\n"
            "• В сочинении необходимо чётко раскрыть содержание и идею темы.\n\n"
            "Цель конкурса:\n\n"
            "• Широкая пропаганда движения джадидов и их исторического наследия.\n"
            "• Воспитание патриотизма и чувства национальной гордости в сердцах молодёжи.\n\n"
            "📍 Адрес: Узбекистанская государственная спортивная академия\n\n"
            "📞 Для связи:\n"
            "Обращайтесь в сектор организации научно-исследовательской деятельности "
            "одарённых студентов, а также в отдел по работе с молодёжью, духовности и просвещению."
        ),
        "description_en": (
            "An essay competition is being held among students on the following topics:\n\n"
            "• 'The Courage of the Jadids — the Pride of Our Nation'\n"
            "• 'The Jadids: National Identity, Independence and Statehood'\n\n"
            "➡ Competition requirements:\n\n"
            "• The essay must be written independently and creatively.\n"
            "• The recommended length is 2–3 pages.\n"
            "• The essay must clearly convey the content and idea of the topic.\n\n"
            "Objectives of the competition:\n\n"
            "• To widely promote the Jadid movement and their historical legacy.\n"
            "• To cultivate patriotism and a sense of national pride in the hearts of young people.\n\n"
            "📍 Address: Uzbekistan State Sports Academy\n\n"
            "📞 Contact:\n"
            "Please apply to the Sector for Organising Research Activities of Talented Students "
            "and the Department for Youth Affairs, Spirituality and Enlightenment."
        ),
        "address": "O'zbekiston davlat sport akademiyasi",
        "date_offset_days": 30,
    },
]


class Command(BaseCommand):
    help = "Tanlovlar (e'lonlar) ma'lumotlarini seed qiladi"

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help="Eski tanlovlarni o'chirib qayta yozadi")

    def handle(self, *args, **options):
        if options['clear']:
            n = TenderAnnouncement.objects.filter(announcement_type='tanlov').delete()[0]
            self.stdout.write(self.style.WARNING(f"O'chirildi: {n} ta tanlov"))

        created = updated = 0
        for d in DATA:
            offset = d.pop('date_offset_days', 30)
            date = timezone.now() + timezone.timedelta(days=offset)
            obj, is_new = TenderAnnouncement.objects.update_or_create(
                title_uz=d['title_uz'],
                announcement_type='tanlov',
                defaults={**d, 'announcement_type': 'tanlov', 'is_published': True, 'date': date},
            )
            if is_new:
                created += 1
            else:
                updated += 1
            d['date_offset_days'] = offset
            title_safe = obj.title_uz.encode('ascii', 'replace').decode()
            self.stdout.write(f"  [{'+'if is_new else '~'}] {title_safe}")

        self.stdout.write(self.style.SUCCESS(f"\nNatija: {created} yangi, {updated} yangilandi"))
