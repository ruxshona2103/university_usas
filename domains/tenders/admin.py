from django.contrib import admin
from django.utils.html import format_html
from .models import TenderAnnouncement, TenderImage


class TenderImageInline(admin.TabularInline):
    model  = TenderImage
    extra  = 1
    fields = ('image', 'order')


@admin.register(TenderAnnouncement)
class TenderAnnouncementAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'date', 'address', 'phone', 'is_published', 'views')
    list_editable = ('is_published',)
    list_filter   = ('is_published',)
    search_fields = ('title_uz', 'title_ru', 'title_en', 'address')
    readonly_fields = ('views', 'created_at', 'updated_at')
    inlines       = [TenderImageInline]

    fieldsets = (
        ('Kontent', {'fields': ('title_uz', 'title_ru', 'title_en', 'description_uz', 'description_ru', 'description_en')}),
        ("Aloqa va manzil", {'fields': ('date', 'address', 'email', 'phone')}),
        ("Holat", {'fields': ('is_published',)}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('views', 'created_at', 'updated_at')}),
    )
