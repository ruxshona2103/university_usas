from django.contrib import admin

from .models import AcademyStat


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
