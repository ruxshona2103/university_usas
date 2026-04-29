import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ContentView(models.Model):
    """
    Har qanday model instance uchun view hisobi.
    view_token — cookieda saqlanadigan UUID (device/user identifikatori).
    """
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')

    view_token  = models.UUIDField(db_index=True)
    viewed_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tracker_content_view'
        unique_together = ('content_type', 'object_id', 'view_token')
        verbose_name        = "Ko'rish"
        verbose_name_plural = "Ko'rishlar"

    def __str__(self):
        return f"{self.content_type} | {self.object_id} | {self.view_token}"


def get_view_count(obj) -> int:
    ct = ContentType.objects.get_for_model(obj.__class__)
    return ContentView.objects.filter(
        content_type=ct,
        object_id=str(obj.pk),
    ).count()


def record_view(obj, view_token: uuid.UUID) -> bool:
    """True — yangi ko'rish, False — allaqachon ko'rilgan."""
    ct = ContentType.objects.get_for_model(obj.__class__)
    _, created = ContentView.objects.get_or_create(
        content_type=ct,
        object_id=str(obj.pk),
        view_token=view_token,
    )
    return created
