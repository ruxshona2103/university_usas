from django.contrib import admin
from django.utils.html import format_html

from .models import TenderAnnouncement, TenderImage


class TenderImageInline(admin.TabularInline):
    model  = TenderImage
    extra  = 1
    fields = ('image', 'order')


@admin.register(TenderAnnouncement)
class TenderAnnouncementAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'announcement_type', 'date', 'address', 'phone', 'is_published', 'views')
    list_editable = ('is_published',)
    list_filter   = ('announcement_type', 'is_published')
    search_fields = ('title_uz', 'title_ru', 'title_en', 'address')
    readonly_fields = ('views', 'likes', 'comments', 'created_at', 'updated_at')
    inlines       = [TenderImageInline]

    fieldsets = (
        ("Tur va holat", {'fields': ('announcement_type', 'is_published', 'date')}),
        ('Kontent', {'fields': ('title_uz', 'title_ru', 'title_en', 'description_uz', 'description_ru', 'description_en')}),
        ("Aloqa va manzil", {'fields': ('address', 'email', 'phone')}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('views', 'likes', 'comments', 'created_at', 'updated_at')}),
    )
