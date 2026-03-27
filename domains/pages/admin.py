from django.contrib import admin
from django.utils.html import format_html

from .models import ContactConfig, PresidentQuote, SocialLink, NavbarCategory, NavbarSubItem, Partner, HeroVideo


#----------------------------------------------ALOQA SOZLAMASI--------------------------------------------  

@admin.register(ContactConfig)
class ContactConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Aloqa ma'lumotlari", {
            'fields': ('email', 'phone')
        }),
        ('Manzil', {
            'fields': ('address_uz', 'address_ru', 'address_en')
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return not ContactConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ----------------------------------------------PREZIDENT IQTIBOSI----------------------------------------------

@admin.register(PresidentQuote)
class PresidentQuoteAdmin(admin.ModelAdmin):
    list_display = ('short_quote', 'author', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('quote_uz', 'author')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Muallif', {
            'fields': ('author', 'is_active')
        }),
        ("Iqtibos matni", {
            'fields': ('quote_uz', 'quote_ru', 'quote_en')
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description="Iqtibos")
    def short_quote(self, obj):
        if len(obj.quote_uz) > 90:
            return obj.quote_uz[:90] + '...'
        return obj.quote_uz


# ----------------------------------------------IJTIMOIY TARMOQLAR----------------------------------------------

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('colored_platform', 'url', 'is_active', 'updated_at')
    list_filter = ('is_active', 'platform')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Ijtimoiy tarmoq', {
            'fields': ('platform', 'url', 'is_active')
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    PLATFORM_COLORS = {
        'telegram':  '#2CA5E0',
        'instagram': '#E1306C',
        'facebook':  '#1877F2',
        'youtube':   '#FF0000',
        'twitter':   '#1DA1F2',
    }

    @admin.display(description="Platforma")
    def colored_platform(self, obj):
        color = self.PLATFORM_COLORS.get(obj.platform, '#333333')
        return format_html(
            '<span style="color: {}; font-weight: bold;">&#9679; {}</span>',
            color,
            obj.get_platform_display()
        )


# ----------------------------------------------NAVBAR BO'LIMLARI----------------------------------------------

class NavbarSubItemInline(admin.TabularInline):
    """Bo'lim sahifasida subitemlarni to'g'ridan-to'g'ri ko'rish/tahrirlash"""
    model = NavbarSubItem
    extra = 1
    fields = ('name_uz', 'name_ru', 'name_en', 'page_type', 'order', 'is_active')
    ordering = ('order',)
    show_change_link = True


@admin.register(NavbarCategory)
class NavbarCategoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'name_uz', 'name_ru', 'name_en', 'slug', 'items_count', 'direct_url_display', 'is_active')
    list_display_links = ('name_uz',)
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name_uz', 'name_ru', 'name_en')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    inlines = [NavbarSubItemInline]

    fieldsets = (
        ("Bo'lim nomi", {
            'fields': ('name_uz', 'name_ru', 'name_en')
        }),
        ("Yo'naltirish URL (ixtiyoriy)", {
            'fields': ('direct_url',),
            'description': (
                "Faqat children bo'lmasa ishlatiladi. "
                "Tashqi sayt uchun: https://hemis.uz — "
                "Ichki sahifa uchun: /news — "
                "Bo'sh qolsa slug'dan avtomatik yasaladi."
            )
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active')
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('slug', 'created_at', 'updated_at')
        }),
    )

    @admin.display(description="Sahifalar soni")
    def items_count(self, obj):
        count = obj.items.filter(is_active=True).count()
        return format_html(
            '<span style="background:#e8f4fd; color:#1a73e8; padding:2px 10px; '
            'border-radius:12px; font-size:12px; font-weight:600;">{}</span>',
            count
        )

    @admin.display(description="URL")
    def direct_url_display(self, obj):
        if obj.direct_url:
            return format_html(
                '<span style="background:#fef7e0; color:#b06000; padding:2px 8px; '
                'border-radius:12px; font-size:12px;">&#128279; {}</span>',
                obj.direct_url[:40] + ('...' if len(obj.direct_url) > 40 else '')
            )
        return format_html(
            '<span style="color:#999; font-size:12px;">slug\'dan</span>'
        )


# NAVBAR SAHIFALARI 
@admin.register(NavbarSubItem)
class NavbarSubItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'category', 'name_uz', 'page_type_badge', 'slug', 'is_active')
    list_display_links = ('name_uz',)
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'page_type', 'category')
    search_fields = ('name_uz', 'name_ru', 'name_en')
    readonly_fields = ('slug', 'created_at', 'updated_at')

    fieldsets = (
        ("Sahifa nomi", {
            'fields': ('category', 'name_uz', 'name_ru', 'name_en')
        }),
        ("Sahifa turi", {
            'fields': ('page_type', 'redirect_url'),
            'description': (
                "Statik tanlasangiz — quyidagi matn maydonlarini to'ldiring. "
                "Yo'naltirish tanlasangiz — faqat URL kiriting."
            )
        }),
        ("Sahifa matni (Statik uchun)", {
            'classes': ('collapse',),
            'fields': ('content_uz', 'content_ru', 'content_en')
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active')
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('slug', 'created_at', 'updated_at')
        }),
    )

    @admin.display(description="Turi")
    def page_type_badge(self, obj):
        if obj.page_type == 'static':
            return format_html(
                '<span style="background:#e6f4ea; color:#137333; padding:2px 10px; '
                'border-radius:12px; font-size:12px;">Statik</span>'
            )
        return format_html(
            '<span style="background:#fef7e0; color:#b06000; padding:2px 10px; '
            'border-radius:12px; font-size:12px;">Redirect</span>'
        )


# -------------------------------------------------HAMKORLARIMIZ--------------------------------------------------
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'title_uz', 'url', 'order', 'is_active')
    list_display_links = ('title_uz',)
    list_editable = ('order', 'is_active')
    readonly_fields = ('logo_preview', 'created_at', 'updated_at')

    fieldsets = (
        ('Logo', {
            'fields': ('image', 'logo_preview')
        }),
        ('Nomi va sayt', {
            'fields': ('title_uz', 'title_ru', 'title_en', 'url')
        }),
        ('Tartib va holat', {
            'fields': ('order', 'is_active')
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.display(description="Logo")
    def logo_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:50px; max-width:120px; object-fit:contain;" />',
                obj.image.url
            )
        return "—"

# -------------------------------------------------HERO VIDEO BO'LIMI--------------------------------------------------
from django.contrib import admin
from django.utils.html import format_html
from .models import HeroVideo

@admin.register(HeroVideo)
class HeroVideoAdmin(admin.ModelAdmin):

    list_display = ('display_poster', 'title', 'display_video_link', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title',)
    readonly_fields = ('created_at', 'display_poster_preview')

    fieldsets = (
        ('Video ma\'lumotlari', {
            'fields': ('title', 'video_url', 'poster_image', 'is_active')
        }),
        ('Preview (Ko\'rinishi)', {
            'fields': ('display_poster_preview',),
        }),
        ('Texnik ma\'lumotlar', {
            'classes': ('collapse',),
            'fields': ('created_at',) 
        }),
    )

    def display_video_link(self, obj):
        """Video URLni bosiladigan havola ko'rinishida chiqaradi"""
        if obj.video_url:
            return format_html('<a href="{0}" target="_blank">Videoni ko\'rish</a>', obj.video_url)
        return "Havola yo'q"
    display_video_link.short_description = "Video Link"

    def display_poster(self, obj):
        """Ro'yxatda kichik rasmcha chiqaradi"""
        if obj.poster_image:
            return format_html('<img src="{0}" style="width: 50px; height: auto; border-radius: 5px;" />', obj.poster_image.url)
        return "Rasm yo'q"
    display_poster.short_description = "Poster"

    def display_poster_preview(self, obj):
        """Edit sahifasida kattaroq rasmcha chiqaradi"""
        if obj.poster_image:
            return format_html('<img src="{0}" style="width: 300px; height: auto; border-radius: 10px;" />', obj.poster_image.url)
        return "Rasm yuklanmagan"
    display_poster_preview.short_description = "Poster Preview"