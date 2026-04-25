from django.db import models


class InternationalDeptConfig(models.Model):
    """Singleton — Xalqaro hamkorlik bo'limi sahifasi konfiguratsiyasi."""

    head_name_uz       = models.CharField(max_length=300, blank=True, verbose_name="Bo'lim boshlig'i (Uz)")
    head_name_ru       = models.CharField(max_length=300, blank=True, verbose_name="Bo'lim boshlig'i (Ru)")
    head_name_en       = models.CharField(max_length=300, blank=True, verbose_name="Bo'lim boshlig'i (En)")
    head_position_uz   = models.CharField(max_length=300, blank=True, verbose_name="Lavozimi (Uz)")
    head_position_ru   = models.CharField(max_length=300, blank=True, verbose_name="Lavozimi (Ru)")
    head_position_en   = models.CharField(max_length=300, blank=True, verbose_name="Lavozimi (En)")
    head_working_hours = models.CharField(max_length=200, blank=True, verbose_name="Qabul kunlari")
    head_phone         = models.CharField(max_length=200, blank=True, verbose_name="Telefon")
    head_email         = models.CharField(max_length=300, blank=True, verbose_name="E-mail")
    head_photo         = models.FileField(
        upload_to='international/dept_head/',
        blank=True, null=True,
        verbose_name="Boshlig' rasmi",
    )
    # Har bir satr — bitta vazifa (serializer ro'yxatga o'giradi)
    tasks_uz = models.TextField(blank=True, verbose_name="Vazifalari (Uz)", help_text="Har bir vazifani yangi satrga yozing")
    tasks_ru = models.TextField(blank=True, verbose_name="Vazifalari (Ru)")
    tasks_en = models.TextField(blank=True, verbose_name="Vazifalari (En)")

    class Meta:
        db_table            = 'international_dept_config'
        verbose_name        = "Xalqaro bo'lim konfiguratsiyasi"
        verbose_name_plural = "Xalqaro bo'lim konfiguratsiyasi"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Xalqaro bo'lim konfiguratsiyasi"
