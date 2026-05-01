from django.db import models

from common.base_models import TimeStampedModel


class FAQ(TimeStampedModel):
    """
    Savol-javob.
    """
    question_uz = models.CharField(max_length=500, verbose_name="Savol (Uz)")
    question_ru = models.CharField(max_length=500, blank=True, verbose_name="Savol (Ru)")
    question_en = models.CharField(max_length=500, blank=True, verbose_name="Savol (En)")

    answer_uz = models.TextField(blank=True, verbose_name="Javob (Uz)")
    answer_ru = models.TextField(blank=True, verbose_name="Javob (Ru)")
    answer_en = models.TextField(blank=True, verbose_name="Javob (En)")

    vote_count  = models.PositiveIntegerField(default=0, verbose_name="Ovozlar soni")
    views       = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    comments    = models.PositiveIntegerField(default=0, verbose_name="Komment soni")
    is_answered = models.BooleanField(default=False, verbose_name="Javob berilganmi?")
    is_published = models.BooleanField(default=True, verbose_name="Chiqarilsinmi?")

    class Meta:
        db_table            = 'contact_faq'
        ordering            = ['-vote_count', '-created_at']
        verbose_name        = 'Savol-javob'
        verbose_name_plural = 'Savol-javoblar'

    def __str__(self):
        return self.question_uz[:80]


class RectorAppeal(TimeStampedModel):
    """Rektorga murojaat — foydalanuvchi POST orqali yuboradi."""

    class Status(models.TextChoices):
        NEW       = 'new',       'Yangi'
        IN_REVIEW = 'in_review', "Ko'rib chiqilmoqda"
        ANSWERED  = 'answered',  'Javob berildi'

    full_name  = models.CharField(max_length=255, verbose_name="F.I.O")
    email      = models.EmailField(verbose_name="Email")
    phone      = models.CharField(max_length=25, verbose_name="Telefon")
    faculty    = models.CharField(max_length=255, blank=True, verbose_name="Fakultet / Bo'lim")
    group      = models.CharField(max_length=50, blank=True, verbose_name="Guruh raqami")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    message    = models.TextField(verbose_name="Murojaat matni")
    status     = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Holati",
    )

    class Meta:
        db_table            = 'contact_rector_appeal'
        ordering            = ['-created_at']
        verbose_name        = 'Rektorga murojaat'
        verbose_name_plural = 'Rektorga murojaatlar'

    def __str__(self):
        return f'{self.full_name} — {self.created_at.date()}'


class ContactMessage(TimeStampedModel):
    """Aloqa formasidan keladigan xabarlar."""

    class Status(models.TextChoices):
        NEW       = 'new',       'Yangi'
        IN_REVIEW = 'in_review', "Ko'rib chiqilmoqda"
        ANSWERED  = 'answered',  'Javob berildi'

    full_name = models.CharField(max_length=255, verbose_name="Ism-familiya")
    email     = models.EmailField(verbose_name="Email")
    phone     = models.CharField(max_length=25, blank=True, verbose_name="Telefon")
    subject   = models.CharField(max_length=255, verbose_name="Mavzu")
    message   = models.TextField(verbose_name="Murojaat matni")
    status    = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Holati",
    )

    class Meta:
        db_table            = 'contact_message'
        ordering            = ['-created_at']
        verbose_name        = 'Aloqa xabari'
        verbose_name_plural = 'Aloqa xabarlari'

    def __str__(self):
        return f'{self.full_name} — {self.subject[:60]}'
