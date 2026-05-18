"""
python manage.py seed_magistratura_category          # yaratadi / yangilaydi
python manage.py seed_magistratura_category --clear  # o'chirib qaytadan yozadi
"""
from django.core.management.base import BaseCommand
from domains.students.models import Person, PersonCategory


class Command(BaseCommand):
    help = "Magistratura talabalari PersonCategory ni yaratadi (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help="Magistratura_talabalar kategoriyasidagi barcha shaxslarni o'chiradi",
        )

    def handle(self, *args, **options):
        cat, created = PersonCategory.objects.update_or_create(
            slug='magistratura_talabalar',
            defaults={
                'title_uz': 'Magistratura talabalari',
                'title_ru': 'Студенты магистратуры',
                'title_en': "Master's Students",
                'order': 10,
            },
        )
        self.stdout.write(
            f"  [kat] {'yaratildi' if created else 'yangilandi'}: {cat.title_uz} (slug={cat.slug})"
        )

        if options['clear']:
            deleted = Person.objects.filter(category=cat).delete()[0]
            self.stdout.write(self.style.WARNING(
                f"  O'chirildi: {deleted} ta shaxs (magistratura_talabalar)"
            ))

        self.stdout.write(self.style.SUCCESS(
            "\nEndi admindan Person qo'shib, kategoriyasini "
            "'magistratura_talabalar' qilib belgilang."
        ))
