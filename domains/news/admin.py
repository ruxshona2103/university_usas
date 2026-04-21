from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html

from common.models import ContentImage
from .models import (
    Article, ArticleType,
    News, Event, Blog, NewsCategory,
    InformationContent, InformationImage,
    RectorActivity, Briefing, Contest, PressService, PhotoGallery, VideoGallery,
)


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('title_uz', 'title_ru')
    fieldsets = (
        ("Nomi (Uz)", {'fields': ('title_uz',)}),
        ("Nomi (Ru / En)", {'classes': ('collapse',), 'fields': ('title_ru', 'title_en')}),
        ("Meta", {'fields': ('slug', 'order')}),
    )



class ArticleImageInline(GenericTabularInline):
    """News / Event / Blog uchun ko'p rasm inline."""
    model   = ContentImage
    extra   = 1
    fields  = ('image', 'order')
    ordering = ('order',)


# Article admin (asosiy jadval — to'g'ridan-to'g'ri ro'yxatga olinmaydi)

class ArticleAdminBase(admin.ModelAdmin):
    """News, Event, Blog proxy adminlari uchun umumiy base."""
    list_filter    = ('is_published', 'date')
    search_fields  = ('title_uz', 'title_ru', 'title_en')
    readonly_fields = ('slug', 'views', 'likes', 'comments', 'created_at', 'updated_at', 'image_preview')
    list_per_page  = 20

    @admin.display(description="Rasm")
    def image_preview(self, obj):
        if obj.image:
            try:
                url = obj.image.url
            except Exception:
                return format_html('<span style="color:#e53935;">⚠ Rasm URL topilmadi</span>')
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:6px;border:1px solid #e0e0e0;" />',
                url,
            )
        return format_html('<span style="color:#999;">Rasm yo\'q</span>')

    @admin.display(description="Ko'rishlar", ordering='views')
    def views_badge(self, obj):
        return format_html(
            '<span style="background:#e8f4fd;color:#1a73e8;padding:2px 10px;'
            'border-radius:12px;font-size:12px;font-weight:600;">{}</span>',
            obj.views,
        )

    @admin.display(description="Holat", ordering='is_published')
    def status_badge(self, obj):
        if obj.is_published:
            return format_html(
                '<span style="background:#e6f4ea;color:#137333;padding:2px 10px;'
                'border-radius:12px;font-size:12px;font-weight:600;">Chiqarilgan</span>'
            )
        return format_html(
            '<span style="background:#fce8e6;color:#c5221f;padding:2px 10px;'
            'border-radius:12px;font-size:12px;font-weight:600;">Yashirin</span>'
        )



# YANGILIKLAR
@admin.register(News)
class NewsAdmin(ArticleAdminBase):
    list_display  = ('title_uz', 'date', 'source', 'is_published', 'views_badge', 'image_preview')
    list_editable = ('is_published',)
    inlines       = [ArticleImageInline]

    fieldsets = (
        ("O'zbek tili (majburiy)", {
            'fields': ('image', 'image_preview', 'title_uz', 'description_uz'),
        }),
        ("Rus tili", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru'),
        }),
        ("Ingliz tili", {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en'),
        }),
        ("Qo'shimcha", {
            'fields': ('source', 'categories', 'date', 'keywords', 'is_published'),
        }),
        ("Texnik (avtomatik)", {
            'classes': ('collapse',),
            'fields': ('slug', 'views', 'likes', 'comments', 'created_at', 'updated_at'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(article_type=ArticleType.NEWS)

    def save_model(self, request, obj, form, change):
        obj.article_type = ArticleType.NEWS
        super().save_model(request, obj, form, change)



# TADBIRLAR
@admin.register(Event)
class EventAdmin(ArticleAdminBase):
    list_display  = ('title_uz', 'date', 'start_time', 'location_uz', 'is_published', 'views_badge')
    list_editable = ('is_published',)
    inlines       = [ArticleImageInline]

    fieldsets = (
        ("O'zbek tili (majburiy)", {
            'fields': ('image', 'image_preview', 'title_uz', 'description_uz'),
        }),
        ("Rus tili", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru'),
        }),
        ("Ingliz tili", {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en'),
        }),
        ("Manzil", {
            'fields': ('location_uz', 'location_ru', 'location_en'),
        }),
        ("Vaqt va holat", {
            'fields': ('date', 'start_time', 'categories', 'keywords', 'is_published'),
        }),
        ("Texnik (avtomatik)", {
            'classes': ('collapse',),
            'fields': ('slug', 'views', 'likes', 'comments', 'created_at', 'updated_at'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(article_type=ArticleType.EVENT)

    def save_model(self, request, obj, form, change):
        obj.article_type = ArticleType.EVENT
        super().save_model(request, obj, form, change)



# BLOG
@admin.register(Blog)
class BlogAdmin(ArticleAdminBase):
    list_display  = ('title_uz', 'author_display', 'date', 'is_published', 'views_badge', 'image_preview')
    list_editable = ('is_published',)
    list_filter   = ('is_published', 'date', 'author')
    inlines       = [ArticleImageInline]

    fieldsets = (
        ("O'zbek tili (majburiy)", {
            'fields': ('image', 'image_preview', 'title_uz', 'description_uz'),
        }),
        ("Rus tili", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru'),
        }),
        ("Ingliz tili", {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en'),
        }),
        ("Muallif va holat", {
            'fields': ('author', 'date', 'categories', 'keywords', 'is_published'),
        }),
        ("Texnik (avtomatik)", {
            'classes': ('collapse',),
            'fields': ('slug', 'views', 'likes', 'comments', 'created_at', 'updated_at'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(article_type=ArticleType.BLOG)

    def save_model(self, request, obj, form, change):
        obj.article_type = ArticleType.BLOG
        super().save_model(request, obj, form, change)

    @admin.display(description="Muallif", ordering='author__username')
    def author_display(self, obj):
        if obj.author:
            full_name = obj.author.get_full_name()
            return full_name if full_name else obj.author.username
        return format_html('<span style="color:#999;">—</span>')



# AXBOROT XIZMATI 
class InformationImageInline(admin.TabularInline):
    model   = InformationImage
    extra   = 1
    fields  = ('image', 'order')
    ordering = ('order',)


class InformationContentAdminBase(admin.ModelAdmin):
    list_display   = ('title_uz', 'content_type', 'date', 'is_published', 'views', 'likes', 'comments')
    list_filter    = ('is_published',)
    search_fields  = ('title_uz', 'title_ru', 'title_en')
    list_per_page  = 20
    readonly_fields = ('views', 'likes', 'comments', 'created_at', 'updated_at')
    inlines        = [InformationImageInline]

    fieldsets = (
        ("O'zbek tili (majburiy)", {
            'fields': ('title_uz', 'description_uz'),
        }),
        ("Rus tili", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru'),
        }),
        ("Ingliz tili", {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en'),
        }),
        ("Sozlamalar", {
            'fields': ('content_type', 'date', 'video_url', 'external_url', 'is_published'),
        }),
        ("Texnik (avtomatik)", {
            'classes': ('collapse',),
            'fields': ('views', 'likes', 'comments', 'created_at', 'updated_at'),
        }),
    )


@admin.register(RectorActivity)
class RectorActivityAdmin(InformationContentAdminBase):
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Rektor tadbirlari va nutqlari' ni tanlang."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='rector')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'rector'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in super().get_fieldsets(request, obj)
        ]


@admin.register(Briefing)
class BrifingAdmin(InformationContentAdminBase):
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Brifinglar' ni tanlang."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='briefing')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'briefing'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in super().get_fieldsets(request, obj)
        ]


@admin.register(Contest)
class TanlovAdmin(InformationContentAdminBase):
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Tanlovlar' ni tanlang."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='contest')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'contest'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in super().get_fieldsets(request, obj)
        ]


@admin.register(PressService)
class MatbuotXizmatiAdmin(InformationContentAdminBase):
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Matbuot xizmati' ni tanlang."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='press')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'press'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in super().get_fieldsets(request, obj)
        ]


@admin.register(PhotoGallery)
class FotogalereyaAdmin(InformationContentAdminBase):
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Fotogalereya' ni tanlang."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='photo')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'photo'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in super().get_fieldsets(request, obj)
        ]


@admin.register(VideoGallery)
class VideogalereyaAdmin(InformationContentAdminBase):
    INFO_GUIDE_TEXT = "Navbar sahifasi → 'Axborot xizmati → Videogalereya' ni tanlang."

    def get_queryset(self, request):
        return super().get_queryset(request).filter(content_type='video')

    def save_model(self, request, obj, form, change):
        obj.content_type = 'video'
        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        return [
            (name, {**opts, 'fields': [f for f in opts['fields'] if f != 'content_type']})
            for name, opts in super().get_fieldsets(request, obj)
        ]
