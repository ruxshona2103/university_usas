from django.contrib import admin
from django.utils.html import format_html

from .models import (
    News, Event, Blog,
    InformationContent, InformationImage,
    RectorActivity, Briefing, Contest, PressService, PhotoGallery, VideoGallery,
)


# UMUMIY MIXIN — News, Event, Blog uchun takrorlanuvchi logika
class PublishableAdminMixin:
    list_filter  = ('is_published', 'date')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    readonly_fields = ('slug', 'views', 'created_at', 'updated_at', 'image_preview')
    list_per_page = 20

    @admin.display(description="Rasm")
    def image_preview(self, obj):
        if obj.image:
            try:
                url = obj.image.url
            except Exception:
                return format_html('<span style="color:#e53935;">⚠ Rasm URL topilmadi</span>')
            return format_html(
                '<img src="{}" style="max-height: 120px; border-radius: 6px; '
                'border: 1px solid #e0e0e0;" />',
                url
            )
        return format_html('<span style="color:#999;">Rasm yo\'q</span>')

    @admin.display(description="Ko'rishlar", ordering='views')
    def views_badge(self, obj):
        return format_html(
            '<span style="background:#e8f4fd; color:#1a73e8; padding:2px 10px; '
            'border-radius:12px; font-size:12px; font-weight:600;">{}</span>',
            obj.views
        )

    @admin.display(description="Holat", ordering='is_published')
    def status_badge(self, obj):
        if obj.is_published:
            return format_html(
                '<span style="background:#e6f4ea; color:#137333; padding:2px 10px; '
                'border-radius:12px; font-size:12px; font-weight:600;">Chiqarilgan</span>'
            )
        return format_html(
            '<span style="background:#fce8e6; color:#c5221f; padding:2px 10px; '
            'border-radius:12px; font-size:12px; font-weight:600;">Yashirin</span>'
        )


# YANGILIKLAR
@admin.register(News)
class NewsAdmin(PublishableAdminMixin, admin.ModelAdmin):
    list_display = ('title_uz', 'date', 'source', 'is_published', 'views_badge', 'image_preview')
    list_editable = ('is_published',)
    readonly_fields = ('slug', 'views', 'created_at', 'updated_at', 'image_preview')

    fieldsets = (
        ("📌 Yo'riqnoma", {
            'fields': (),
            'description': (
                '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
                '<strong style="color:#e53935;">📌 YANGILIKLAR</strong> — Umumiy sayt yangiliklari va '
                'Talabalarga bo\'limida ham ko\'rsatiladi. Rasm, sarlavha, to\'liq matn va sana <strong>majburiy</strong>.'
                '</div>'
            ),
        }),
        ("O'zbek tili (majburiy)", {
            'fields': ('image', 'image_preview', 'title_uz', 'description_uz')
        }),
        ("Rus tili", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru')
        }),
        ("Ingliz tili", {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en')
        }),
        ("Qo'shimcha", {
            'fields': ('source', 'date', 'keywords', 'is_published')
        }),
        ('Texnik (avtomatik)', {
            'classes': ('collapse',),
            'fields': ('slug', 'views', 'created_at', 'updated_at')
        }),
    )


# TADBIRLAR
@admin.register(Event)
class EventAdmin(PublishableAdminMixin, admin.ModelAdmin):
    list_display = ('title_uz', 'date', 'start_time', 'location_uz', 'is_published', 'views_badge')
    list_editable = ('is_published',)
    readonly_fields = ('slug', 'views', 'created_at', 'updated_at', 'image_preview')

    fieldsets = (
        ("📌 Yo'riqnoma", {
            'fields': (),
            'description': (
                '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
                '<strong style="color:#e53935;">📌 KUTILAYOTGAN TADBIRLAR</strong> — Konferensiya, festival, ochiq eshiklar kuni va h.k. '
                'Manzil, boshlanish vaqti <strong>majburiy emas</strong> — bo\'lsa to\'ldiring.'
                '</div>'
            ),
        }),
        ("O'zbek tili (majburiy)", {
            'fields': ('image', 'image_preview', 'title_uz', 'description_uz')
        }),
        ("Rus tili", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru')
        }),
        ("Ingliz tili", {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en')
        }),
        ("Manzil", {
            'fields': ('location_uz', 'location_ru', 'location_en')
        }),
        ("Vaqt va holat", {
            'fields': ('date', 'start_time', 'keywords', 'is_published')
        }),
        ('Texnik (avtomatik)', {
            'classes': ('collapse',),
            'fields': ('slug', 'views', 'created_at', 'updated_at')
        }),
    )


# BLOG
@admin.register(Blog)
class BlogAdmin(PublishableAdminMixin, admin.ModelAdmin):
    list_display = ('title_uz', 'author_display', 'date', 'is_published', 'views_badge', 'image_preview')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'date', 'author')
    readonly_fields = ('slug', 'views', 'created_at', 'updated_at', 'image_preview')

    fieldsets = (
        ("📌 Yo'riqnoma", {
            'fields': (),
            'description': (
                '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
                '<strong style="color:#e53935;">📌 BLOG MAQOLALAR</strong> — O\'quv, sport, sog\'lom turmush mavzusidagi maqolalar. '
                'Muallif tanlash <strong>ixtiyoriy</strong>. Talabalarga bo\'limida ham ko\'rsatiladi.'
                '</div>'
            ),
        }),
        ("O'zbek tili (majburiy)", {
            'fields': ('image', 'image_preview', 'title_uz', 'description_uz')
        }),
        ("Rus tili", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru')
        }),
        ("Ingliz tili", {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en')
        }),
        ("Muallif va holat", {
            'fields': ('author', 'date', 'keywords', 'is_published')
        }),
        ('Texnik (avtomatik)', {
            'classes': ('collapse',),
            'fields': ('slug', 'views', 'created_at', 'updated_at')
        }),
    )

    @admin.display(description="Muallif", ordering='author__username')
    def author_display(self, obj):
        if obj.author:
            full_name = obj.author.get_full_name()
            return full_name if full_name else obj.author.username
        return format_html('<span style="color:#999;">—</span>')


# ──────────────────────────────────────────────────────────────────────────────
# AXBOROT XIZMATI
# ──────────────────────────────────────────────────────────────────────────────

class InformationImageInline(admin.TabularInline):
    model   = InformationImage
    extra   = 1
    fields  = ('image', 'order')
    ordering = ('order',)


class InformationContentAdminBase(admin.ModelAdmin):
    """Barcha InformationContent proxy adminlari uchun umumiy base."""
    list_display  = ('title_uz', 'content_type', 'navbar_item', 'date', 'is_published', 'views')
    list_filter   = ('is_published', 'navbar_item')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    list_per_page = 20
    readonly_fields = ('views', 'created_at', 'updated_at', 'info_guide')
    inlines = [InformationImageInline]

    INFO_GUIDE_TEXT = ''  # har bir subklass o'z matnini belgilaydi

    @admin.display(description='')
    def info_guide(self, obj):
        return format_html(
            '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
            '<strong style="color:#e53935;font-size:13px;">📌 {}</strong>'
            '</div>',
            self.INFO_GUIDE_TEXT
        )

    fieldsets = (
        ("📌 Yo'riqnoma", {
            'fields': ('info_guide',),
        }),
        ("O'zbek tili (majburiy)", {
            'fields': ('title_uz', 'description_uz')
        }),
        ("Rus tili", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru')
        }),
        ("Ingliz tili", {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en')
        }),
        ("Sozlamalar", {
            'fields': ('navbar_item', 'content_type', 'date', 'video_url', 'external_url', 'is_published')
        }),
        ('Texnik (avtomatik)', {
            'classes': ('collapse',),
            'fields': ('views', 'created_at', 'updated_at')
        }),
    )


@admin.register(RectorActivity)
class RectorActivityAdmin(InformationContentAdminBase):
    """Rektor tadbirlari va nutqlari."""
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Rektor tadbirlari va nutqlari' ni tanlang. Rasm, sarlavha, matn, sana to'ldiring."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='rector')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'rector'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        # content_type maydonini yashir — avtomatik belgilanadi
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in fieldsets
        ]


@admin.register(Briefing)
class BrifingAdmin(InformationContentAdminBase):
    """Brifinglar."""
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Brifinglar' ni tanlang. Rasm, sarlavha, matn, sana to'ldiring."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='briefing')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'briefing'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in fieldsets
        ]


@admin.register(Contest)
class TanlovAdmin(InformationContentAdminBase):
    """Tanlovlar."""
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Tanlovlar' ni tanlang. Ko'p rasm qo'shish mumkin (pastdagi Rasmlar bo'limidan)."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='contest')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'contest'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in fieldsets
        ]


@admin.register(PressService)
class MatbuotXizmatiAdmin(InformationContentAdminBase):
    """Matbuot xizmati."""
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Matbuot xizmati' ni tanlang. Maqola yoki xabar uchun sarlavha va matn kiriting."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='press')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'press'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in fieldsets
        ]


@admin.register(PhotoGallery)
class FotogalereyaAdmin(InformationContentAdminBase):
    """Fotogalereya."""
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Fotogalereya' ni tanlang. Sarlavha yozing va pastdagi Rasmlar bo'limidan ko'p rasm qo'shing."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='photo')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'photo'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in fieldsets
        ]


@admin.register(VideoGallery)
class VideogalereyaAdmin(InformationContentAdminBase):
    """Videogalereya."""
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Videogalereya' ni tanlang. Video URL (YouTube/Vimeo) yoki tashqi havola kiriting."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='video')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'video'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in fieldsets
        ]
