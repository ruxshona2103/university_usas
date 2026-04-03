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
        ("📌 Yo'riqnoma", {
            'fields': (),
            'description': (
                '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
                '<strong style="color:#e53935;">📌 TENDERLAR VA E\'LONLAR</strong> — '
                'Xarid, ta\'mirlash, pudrat tanlash va boshqa rasmiy e\'lonlar uchun.<br>'
                '<span style="color:#c62828;">Sarlavha va tavsif <strong>majburiy</strong>. '
                'Manzil, email, telefon to\'ldiring. '
                'Ko\'p rasm qo\'shish mumkin (pastdagi Rasmlar bo\'limidan).</span>'
                '</div>'
            ),
        }),
        ('Kontent', {'fields': ('title_uz', 'title_ru', 'title_en', 'description_uz', 'description_ru', 'description_en')}),
        ("Aloqa va manzil", {'fields': ('date', 'address', 'email', 'phone')}),
        ("Holat", {'fields': ('is_published',)}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('views', 'created_at', 'updated_at')}),
    )
