from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from domains.academic.models import Staff
from .serializers import StaffSerializer


def _lang_from_request(request):
	lang = request.query_params.get('lang', 'uz')
	return lang if lang in ('uz', 'ru', 'en') else 'uz'


@extend_schema(tags=['academic'])
class StaffListAPIView(generics.ListAPIView):
	permission_classes = [AllowAny]
	serializer_class = StaffSerializer
	pagination_class = None

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['lang'] = _lang_from_request(self.request)
		return context

	def get_queryset(self):
		queryset = Staff.objects.filter(is_active=True).select_related('navbar_item', 'navbar_item__category')

		roles = self.request.query_params.getlist('role')
		if roles:
			queryset = queryset.filter(role__in=roles)

		navbar_slug = self.request.query_params.get('slug')
		if navbar_slug:
			queryset = queryset.filter(navbar_item__slug=navbar_slug)

		is_head = self.request.query_params.get('is_head')
		if is_head is not None:
			head_value = str(is_head).lower() in ('1', 'true', 'yes')
			queryset = queryset.filter(is_head=head_value)

		ordering = self.request.query_params.get('ordering')
		allowed_ordering = {'order', '-order', 'created_at', '-created_at'}
		if ordering in allowed_ordering:
			return queryset.order_by(ordering)

		return queryset.order_by('-is_head', 'order', 'created_at')
