import os
import uuid
from django.db import models
from common.base_models import TimeStampedModel
from .post import InternationalPost


def post_image_upload(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'international/posts/images/{uuid.uuid4().hex}{ext}'


class InternationalPostImage(TimeStampedModel):
    post  = models.ForeignKey(
        InternationalPost,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="E'lon",
    )
    image = models.FileField(upload_to=post_image_upload, verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        app_label           = 'international'
        db_table            = 'international_post_image'
        ordering            = ['order']
        verbose_name        = "E'lon rasmi"
        verbose_name_plural = "E'lon rasmlari"

    def __str__(self):
        return f"{self.post} — rasm #{self.order}"
