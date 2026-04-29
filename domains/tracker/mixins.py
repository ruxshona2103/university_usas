"""
ViewsCountMixin — har qanday DRF List/Detail view ga qo'shiladi.

Ishlatish:
    class MyListAPIView(ViewsCountMixin, generics.ListAPIView):
        views_count_model = MyModel   # ixtiyoriy, queryset.model dan olinadi

    class MyDetailAPIView(ViewsCountMixin, generics.RetrieveAPIView):
        pass

Serializer da views_count field bo'lishi shart emas —
mixin get_serializer_context() orqali count ni inject qiladi.
Lekin serializer da fields=[..., 'views_count'] bo'lsa,
SerializerMethodField sifatida get_views_count() methodini yozish kerak.

Muqobil yondashuv: mixin to_representation() ni monkey-patch qiladi.
"""
import uuid

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import get_view_count, record_view, ContentView
from django.contrib.contenttypes.models import ContentType


_COOKIE_NAME = 'view_token'
_COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 yil


def _get_or_create_token(request, response=None):
    token_str = request.COOKIES.get(_COOKIE_NAME)
    new_token = False
    if token_str:
        try:
            token = uuid.UUID(token_str)
        except (ValueError, AttributeError):
            token = uuid.uuid4()
            new_token = True
    else:
        token = uuid.uuid4()
        new_token = True

    if new_token and response is not None:
        response.set_cookie(
            _COOKIE_NAME,
            str(token),
            max_age=_COOKIE_MAX_AGE,
            httponly=True,
            samesite='Lax',
        )
    return token


class ViewsCountMixin:
    """
    List va Detail viewlarga qo'shish uchun mixin.
    Har bir object serializer data siga `views_count` qo'shadi.
    """

    def _inject_views_count(self, data, instance):
        """Bir object data dict ga views_count qo'shadi."""
        if isinstance(data, dict):
            data['views_count'] = get_view_count(instance)
        return data

    def _inject_list_views_count(self, data, queryset):
        """List data (list of dicts) ga views_count qo'shadi."""
        instances = list(queryset)
        if not instances:
            return data

        # Bulk hisoblash — N+1 dan qochish uchun
        ct = ContentType.objects.get_for_model(instances[0].__class__)
        ids = [str(obj.pk) for obj in instances]
        counts = (
            ContentView.objects
            .filter(content_type=ct, object_id__in=ids)
            .values('object_id')
            .annotate(cnt=__import__('django.db.models', fromlist=['Count']).Count('id'))
        )
        count_map = {row['object_id']: row['cnt'] for row in counts}

        result = list(data)
        for i, item in enumerate(result):
            if isinstance(item, dict):
                item['views_count'] = count_map.get(str(instances[i].pk), 0)
        return result

    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response as DRFResponse
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self._inject_list_views_count(serializer.data, page)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        data = self._inject_list_views_count(serializer.data, queryset)
        return DRFResponse(data)

    def retrieve(self, request, *args, **kwargs):
        from rest_framework.response import Response as DRFResponse
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = dict(serializer.data)
        data['views_count'] = get_view_count(instance)
        return DRFResponse(data)
