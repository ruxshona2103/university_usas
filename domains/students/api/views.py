from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

from common.pagination import CustomDashboardPagination
from .serializers import PersonSerializer, PersonCategorySerializer
from ..models import Person, PersonCategory
from drf_spectacular.utils import extend_schema



@extend_schema(tags=['people'])
class PersonCategoryListAPIView(generics.ListAPIView):
    serializer_class = PersonCategorySerializer
    queryset = PersonCategory.objects.all()

@extend_schema(tags=['people'])
class PersonListAPIView(generics.ListAPIView):
    serializer_class = PersonSerializer
    pagination_class = CustomDashboardPagination
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['full_name_uz', 'full_name_ru', 'full_name_en']
    
    def get_queryset(self):
        queryset = Person.objects.filter(is_active=True).prefetch_related('categories')
        
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
            
        return queryset 