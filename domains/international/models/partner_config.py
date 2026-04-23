from django.db import models


class PartnerPageConfig(models.Model):
    """Singleton — hamkor tashkilotlar sahifasining sarlavha va tavsifi."""

    title_uz       = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Uz)")
    title_ru       = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (Ru)")
    title_en       = models.CharField(max_length=300, blank=True, verbose_name="Sarlavha (En)")
    description_uz = models.TextField(blank=True, verbose_name="Tavsif (Uz)")
    description_ru = models.TextField(blank=True, verbose_name="Tavsif (Ru)")
    description_en = models.TextField(blank=True, verbose_name="Tavsif (En)")

    class Meta:
        db_table            = 'international_partner_page_config'
        verbose_name        = 'Hamkor sahifasi konfiguratsiyasi'
        verbose_name_plural = 'Hamkor sahifasi konfiguratsiyasi'

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
        return 'Hamkor sahifasi konfiguratsiyasi'
