from django.db import models


class HeroVideo(models.Model):
    title = models.CharField(max_length=255, verbose_name="video nomi")
    video_url = models.URLField(
        max_length=500,
        verbose_name='Video URLi',
        help_text="MP4 yoki WebM formatidagi to'g'ridan-to'g'ri havolani kiriting"
    )
    poster_image = models.ImageField(
        upload_to="hero_videos/posters/",
        verbose_name="Poster rasmi",
        help_text="Video yuborilmaguncha joylab turiladigan rasm (poster)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Asosiy page video"
        verbose_name_plural = "Asosiy page videolar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


    