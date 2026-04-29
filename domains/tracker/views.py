"""
POST /api/<prefix>/<pk>/view/
Cookie: view_token=<UUID>

Javob:
  201 { "views_count": N, "is_new": true }   — yangi ko'rish
  200 { "views_count": N, "is_new": false }  — allaqachon ko'rilgan
"""
import uuid

from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .models import get_view_count, record_view

_COOKIE_NAME = 'view_token'
_COOKIE_MAX_AGE = 60 * 60 * 24 * 365


class RecordViewAPIView(APIView):
    """
    POST endpoint — object ko'rilganini qaydlaydi.
    model_class va pk_field ni subclass da set qiling,
    yoki get_target_object() ni override qiling.
    """
    permission_classes = [AllowAny]
    model_class = None    # subclassda set qilinadi
    pk_url_kwarg = 'pk'

    def get_target_object(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return self.model_class.objects.get(pk=pk)

    @extend_schema(
        responses={200: {'type': 'object', 'properties': {
            'views_count': {'type': 'integer'},
            'is_new': {'type': 'boolean'},
        }}},
        summary="Ko'rishni qaydlash (cookie-token asosida)",
    )
    def post(self, request, *args, **kwargs):
        try:
            obj = self.get_target_object()
        except self.model_class.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound()

        # token olish / yaratish
        token_str = request.COOKIES.get(_COOKIE_NAME)
        new_cookie = False
        if token_str:
            try:
                token = uuid.UUID(token_str)
            except (ValueError, AttributeError):
                token = uuid.uuid4()
                new_cookie = True
        else:
            token = uuid.uuid4()
            new_cookie = True

        is_new = record_view(obj, token)
        count = get_view_count(obj)

        status_code = 201 if is_new else 200
        response = Response({'views_count': count, 'is_new': is_new}, status=status_code)

        if new_cookie:
            response.set_cookie(
                _COOKIE_NAME, str(token),
                max_age=_COOKIE_MAX_AGE,
                httponly=True,
                samesite='Lax',
            )
        return response
