from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from common.base_models import TimeStampedModel


class HeroVideo(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name="video nomi")
    video_url = models.URLField(
        max_length=500,
        blank=True, null=True,
        verbose_name='Video URLi',
        help_text="MP4 yoki WebM formatidagi to'g'ridan-to'g'ri havolani kiriting"
    )
    video_file = models.FileField(
        upload_to='hero_videos/files/',
        blank=True, null=True,
        verbose_name='Video fayli',
        help_text="MP4 yoki WebM formatidagi video faylni yuklang (URL bo'lmasa)"
    )
    poster_image = models.ImageField(
        upload_to="hero_videos/posters/",
        verbose_name="Poster rasmi",
        help_text="Video yuborilmaguncha joylab turiladigan rasm (poster)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
    images = GenericRelation('common.ContentImage', related_query_name='hero_video')

    class Meta:
        verbose_name = "Asosiy page video"
        verbose_name_plural = "Asosiy page videolar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


    