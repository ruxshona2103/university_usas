from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema

from domains.academic.models import Staff
from .serializers import StaffSerializer, StaffDetailSerializer


def _lang(request):
    lang = request.query_params.get('lang', 'uz')
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


@extend_schema(tags=['academic'], summary="Xodimlar ro'yxati")
class StaffListAPIView(generics.ListAPIView):
    serializer_class   = StaffSerializer
    permission_classes = [AllowAny]
    pagination_class   = None

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_queryset(self):
        qs = Staff.objects.filter(is_active=True).select_related('navbar_item', 'navbar_item__category')

        roles = self.request.query_params.getlist('role')
        if roles:
            qs = qs.filter(role__in=roles)

        slug = self.request.query_params.get('slug')
        if slug:
            qs = qs.filter(navbar_item__slug=slug)

        is_head = self.request.query_params.get('is_head')
        if is_head is not None:
            qs = qs.filter(is_head=str(is_head).lower() in ('1', 'true', 'yes'))

        ordering = self.request.query_params.get('ordering')
        if ordering in {'order', '-order', 'created_at', '-created_at'}:
            return qs.order_by(ordering)

        return qs.order_by('-is_head', 'order', 'created_at')


@extend_schema(tags=['academic'], summary="Xodim profili (tablar bilan)")
class StaffDetailAPIView(generics.RetrieveAPIView):
    """
    Bitta xodim profili + dinamik tablar (Biografiya, Vazifa va funksiyalari...).
    """
    serializer_class   = StaffDetailSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = _lang(self.request)
        return ctx

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            return (
                Staff.objects
                .select_related('navbar_item')
                .prefetch_related('tabs__tag')
                .get(pk=pk, is_active=True)
            )
        except Staff.DoesNotExist:
            raise NotFound(detail="Xodim topilmadi.")
