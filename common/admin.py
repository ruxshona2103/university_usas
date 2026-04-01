from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display  = ('name_uz', 'name_ru', 'name_en', 'slug')
    search_fields = ('name_uz', 'name_ru', 'name_en', 'slug')
    readonly_fields = ('slug',)
    list_per_page = 30

    fieldsets = (
        ("Nomi", {
            'fields': ('name_uz', 'name_ru', 'name_en')
        }),
        ('Texnik (avtomatik)', {
            'classes': ('collapse',),
            'fields': ('slug',)
        }),
    )
