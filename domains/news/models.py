from django.db import models
from django.contrib.auth import get_user_model
from common.base_models import PublishableContent

User = get_user_model()


# SO'NGGI YANGILIKLAR
class News(PublishableContent):
    source = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Manba (Link yoki nom)"
    )

    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "So'nggi yangiliklar"
        db_table = "news_news"

    def __str__(self):
        return self.title_uz


# KUTILAYOTGAN TADBIRLAR
class Event(PublishableContent):
    location_uz = models.CharField(max_length=300, verbose_name="Manzil (Uz)")
    location_ru = models.CharField(max_length=300, blank=True, verbose_name="Manzil (Ru)")
    location_en = models.CharField(max_length=300, blank=True, verbose_name="Manzil (En)")
    start_time = models.DateTimeField(null=True, blank=True, verbose_name="Boshlanish vaqti")

    class Meta:
        verbose_name = "Tadbir"
        verbose_name_plural = "Kutilayotgan tadbirlar"
        db_table = "news_event"

    def __str__(self):
        return self.title_uz


# BLOG
class Blog(PublishableContent):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="blogs",
        verbose_name="Muallif"
    )

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Bloglar"
        db_table = "news_blog"

    def __str__(self):
        return self.title_uz
