from django.contrib import admin

from .models import AcademyStat, AcademyDetailPage


@admin.register(AcademyStat)
class AcademyStatAdmin(admin.ModelAdmin):
    list_display  = ('label_uz', 'value_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('label_uz', 'label_ru', 'label_en')

    fieldsets = (
        ("O'zbek tili", {
            'fields': ('label_uz', 'value_uz'),
        }),
        ("Rus tili", {
            'fields': ('label_ru', 'value_ru'),
            'classes': ('collapse',),
        }),
        ("Ingliz tili", {
            'fields': ('label_en', 'value_en'),
            'classes': ('collapse',),
        }),
        ("Sozlamalar", {
            'fields': ('order', 'is_active'),
        }),
    )


@admin.register(AcademyDetailPage)
class AcademyDetailPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Axborot-resurs markazi", {
            'fields': ('resource_center_uz', 'resource_center_ru', 'resource_center_en'),
        }),
        ("Ta'lim va tarkib ko'rsatkichlari", {
            'fields': ('edu_direction_count', 'sport_type_count', 'masters_count', 'auditorium_count'),
        }),
        ("Batafsil ma'lumotlar", {
            'fields': ('detail_uz', 'detail_ru', 'detail_en'),
        }),
    )
