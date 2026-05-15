import uuid
from django.db import models
from common.base_models import TimeStampedModel


class SportNatijaBosqich(models.TextChoices):
    BIRINCHI = '1', "1-bosqich"
    IKKINCHI = '2', "2-bosqich"
    MAGISTRATURA = 'magistr', "Magistratura"
    PARASPORT = 'para', "Para sport"


class SportNatija(TimeStampedModel):
    """
    Sport natijalari jadvali — har bir sport turi bo'yicha medallar soni.
    """
    bosqich = models.CharField(
        max_length=10,
        choices=SportNatijaBosqich.choices,
        default=SportNatijaBosqich.BIRINCHI,
        verbose_name="Bosqich",
    )
    sport_turi_uz = models.CharField(max_length=200, verbose_name="Sport turi (Uz)")
    sport_turi_ru = models.CharField(max_length=200, blank=True, verbose_name="Sport turi (Ru)")
    sport_turi_en = models.CharField(max_length=200, blank=True, verbose_name="Sport turi (En)")
    talabalar_soni = models.PositiveIntegerField(default=0, verbose_name="Talabalar soni")

    # Jahon chempionati
    jahon_chempionati_1 = models.PositiveIntegerField(default=0, verbose_name="Jahon chempionati — 1-o'rin")
    jahon_chempionati_2 = models.PositiveIntegerField(default=0, verbose_name="Jahon chempionati — 2-o'rin")
    jahon_chempionati_3 = models.PositiveIntegerField(default=0, verbose_name="Jahon chempionati — 3-o'rin")

    # Para osiyo o'yinlari
    para_osiyo_1 = models.PositiveIntegerField(default=0, verbose_name="Para osiyo — 1-o'rin")
    para_osiyo_2 = models.PositiveIntegerField(default=0, verbose_name="Para osiyo — 2-o'rin")
    para_osiyo_3 = models.PositiveIntegerField(default=0, verbose_name="Para osiyo — 3-o'rin")

    # Osiyo chempionati
    osiyo_chempionati_1 = models.PositiveIntegerField(default=0, verbose_name="Osiyo chempionati — 1-o'rin")
    osiyo_chempionati_2 = models.PositiveIntegerField(default=0, verbose_name="Osiyo chempionati — 2-o'rin")
    osiyo_chempionati_3 = models.PositiveIntegerField(default=0, verbose_name="Osiyo chempionati — 3-o'rin")

    # Osiyo kubogi
    osiyo_kubogi_1 = models.PositiveIntegerField(default=0, verbose_name="Osiyo kubogi — 1-o'rin")
    osiyo_kubogi_2 = models.PositiveIntegerField(default=0, verbose_name="Osiyo kubogi — 2-o'rin")
    osiyo_kubogi_3 = models.PositiveIntegerField(default=0, verbose_name="Osiyo kubogi — 3-o'rin")

    # Xalqaro turnir
    xalqaro_turnir_1 = models.PositiveIntegerField(default=0, verbose_name="Xalqaro turnir — 1-o'rin")
    xalqaro_turnir_2 = models.PositiveIntegerField(default=0, verbose_name="Xalqaro turnir — 2-o'rin")
    xalqaro_turnir_3 = models.PositiveIntegerField(default=0, verbose_name="Xalqaro turnir — 3-o'rin")

    # MDH o'yinlari
    mdh_1 = models.PositiveIntegerField(default=0, verbose_name="MDH o'yinlari — 1-o'rin")
    mdh_2 = models.PositiveIntegerField(default=0, verbose_name="MDH o'yinlari — 2-o'rin")
    mdh_3 = models.PositiveIntegerField(default=0, verbose_name="MDH o'yinlari — 3-o'rin")

    # III-Osiyo yoshlar
    osiyo_yoshlar_1 = models.PositiveIntegerField(default=0, verbose_name="Osiyo yoshlar — 1-o'rin")
    osiyo_yoshlar_2 = models.PositiveIntegerField(default=0, verbose_name="Osiyo yoshlar — 2-o'rin")
    osiyo_yoshlar_3 = models.PositiveIntegerField(default=0, verbose_name="Osiyo yoshlar — 3-o'rin")

    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'activities_sport_natija'
        ordering = ['bosqich', 'order']
        verbose_name = "Sport natija qatori"
        verbose_name_plural = "Sport natijalari"

    @property
    def jami(self):
        return sum([
            self.jahon_chempionati_1, self.jahon_chempionati_2, self.jahon_chempionati_3,
            self.para_osiyo_1, self.para_osiyo_2, self.para_osiyo_3,
            self.osiyo_chempionati_1, self.osiyo_chempionati_2, self.osiyo_chempionati_3,
            self.osiyo_kubogi_1, self.osiyo_kubogi_2, self.osiyo_kubogi_3,
            self.xalqaro_turnir_1, self.xalqaro_turnir_2, self.xalqaro_turnir_3,
            self.mdh_1, self.mdh_2, self.mdh_3,
            self.osiyo_yoshlar_1, self.osiyo_yoshlar_2, self.osiyo_yoshlar_3,
        ])

    def __str__(self):
        return f"{self.get_bosqich_display()} — {self.sport_turi_uz}"


class SportKalendar(TimeStampedModel):
    """
    Sport kalendari — rejalashtirilgan sport tadbirlari (yil bo'yicha).
    """
    yil = models.PositiveIntegerField(default=2026, verbose_name="Yil")
    sport_turi_uz = models.CharField(max_length=200, verbose_name="Sport turi (Uz)")
    sport_turi_ru = models.CharField(max_length=200, blank=True, verbose_name="Sport turi (Ru)")
    sport_turi_en = models.CharField(max_length=200, blank=True, verbose_name="Sport turi (En)")

    jahon_chempionati = models.PositiveIntegerField(default=0, verbose_name="Jahon chempionati")
    jahon_seriyasi = models.PositiveIntegerField(default=0, verbose_name="Jahon seriyasi")
    jahon_kubogi = models.PositiveIntegerField(default=0, verbose_name="Jahon kubogi")
    yoshlar_olimpiya = models.PositiveIntegerField(default=0, verbose_name="Yoshlar olimpiya o'yinlari")
    osiyo_oyinlari = models.PositiveIntegerField(default=0, verbose_name="Osiyo o'yinlari")
    osiyo_chempionati = models.PositiveIntegerField(default=0, verbose_name="Osiyo chempionati")
    osiyo_kubogi = models.PositiveIntegerField(default=0, verbose_name="Osiyo kubogi")
    xalqaro_turnir = models.PositiveIntegerField(default=0, verbose_name="Xalqaro turnir")
    ozb_chempionati = models.PositiveIntegerField(default=0, verbose_name="O'zbekiston chempionati")
    ozb_kubogi = models.PositiveIntegerField(default=0, verbose_name="O'zbekiston kubogi")
    prezident_olimpiyada = models.PositiveIntegerField(default=0, verbose_name="Prezident olimpiyadasi")

    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        db_table = 'activities_sport_kalendar'
        ordering = ['-yil', 'order']
        verbose_name = "Sport kalendari qatori"
        verbose_name_plural = "Sport kalendari"

    @property
    def jami(self):
        return (
            self.jahon_chempionati + self.jahon_seriyasi + self.jahon_kubogi
            + self.yoshlar_olimpiya + self.osiyo_oyinlari + self.osiyo_chempionati
            + self.osiyo_kubogi + self.xalqaro_turnir + self.ozb_chempionati
            + self.ozb_kubogi + self.prezident_olimpiyada
        )

    def __str__(self):
        return f"{self.yil} — {self.sport_turi_uz}"
