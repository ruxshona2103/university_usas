from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html
from django_summernote.widgets import SummernoteInplaceWidget as SummernoteWidget

from common.models import ContentImage
from .models import (
    ContactConfig, ContactLocation, PresidentQuote, SocialLink,
    NavbarCategory, NavbarSubItem, Partner, HeroVideo,
    ContentBlock, LinkBlock, MeyoriyHujjat,
    AboutSocial, AboutSocialSection, AboutSocialSectionItem, AboutSocialExtraTask,
    AboutAcademy, AboutAcademySection, AboutAcademySectionItem, AboutAcademyProgram, AboutAcademyImage,
    OrgNode, OrgSection, Rekvizit, InteraktivXizmat,
    Markaz, MarkazXodim, MarkazSubBolim,
    AkademiyaMissiya, AkademiyaMissiyaYonalish,
    IlmiyBolim, IlmiyBolimYonalish,
    SavolJavob, SavolJavobCategory,
    HomepageHaqida, HomepageHaqidaRasm,
    KampusXizmati,
    IqtidorliTalabalar, IqtidorliVazifa,
)
import json
from django.http import JsonResponse
from django.urls import path as _path


class AutoTranslateMixin:
    translate_url_name = None

    def get_urls(self):
        return [
            _path(
                'translate/',
                self.admin_site.admin_view(self.translate_view),
                name=self.translate_url_name,
            ),
        ] + super().get_urls()

    def translate_view(self, request):
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)
        try:
            from deep_translator import GoogleTranslator
            body = json.loads(request.body)
            text = (body.get('text') or '').strip()
            if not text:
                return JsonResponse({'ru': '', 'en': ''})
            ru = GoogleTranslator(source='uz', target='ru').translate(text) or ''
            en = GoogleTranslator(source='uz', target='en').translate(text) or ''
            return JsonResponse({'ru': ru, 'en': en})
        except Exception as exc:
            return JsonResponse({'error': str(exc)}, status=500)


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


@admin.register(ContactLocation)
class ContactLocationAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'phone', 'email', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'phone', 'email')
    ordering      = ('order',)

    fieldsets = (
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Manzil",   {'fields': ('address_uz', 'address_ru', 'address_en')}),
        ("Aloqa",    {'fields': ('phone', 'email')}),
        ("Holat",    {'fields': ('order', 'is_active')}),
    )


@admin.register(Rekvizit)
class RekvizitAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Tashkilot nomi", {
            'fields': ('org_name_uz', 'org_name_ru', 'org_name_en', 'org_short_name'),
        }),
        ("Aloqa", {
            'fields': ('email_1', 'email_2', 'phone_1', 'phone_2'),
        }),
        ("Manzil", {
            'fields': ('postal_code', 'address_uz', 'address_ru', 'address_en'),
        }),
        ("Texnik", {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return not Rekvizit.objects.exists()

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
    fields = ('name_uz', 'name_ru', 'name_en', 'page_type', 'direct_url', 'redirect_url', 'order', 'is_active')
    ordering = ('order',)
    show_change_link = True


@admin.register(NavbarCategory)
class NavbarCategoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'name_uz', 'name_ru', 'name_en', 'slug', 'items_count', 'direct_url_display', 'is_active')
    list_display_links = ('name_uz',)
    list_editable = ('order', 'is_active','slug',)
    list_filter = ('is_active',)
    search_fields = ('name_uz', 'name_ru', 'name_en')
    readonly_fields = ( 'created_at', 'updated_at')
    inlines = [NavbarSubItemInline]

    fieldsets = (
        ("Bo'lim nomi", {
            'fields': ('name_uz', 'name_ru', 'name_en')
        }),
        ("Yo'naltirish URL (ixtiyoriy)", {
            'fields': ('direct_url',),
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active','slug',)
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
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
class NavbarSubItemForm(forms.ModelForm):
    content_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Kontent (Uz)")
    content_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Kontent (Ru)")
    content_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Kontent (En)")

    class Meta:
        model  = NavbarSubItem
        fields = '__all__'


@admin.register(NavbarSubItem)
class NavbarSubItemAdmin(admin.ModelAdmin):
    form        = NavbarSubItemForm
    list_display = ('order', 'category', 'name_uz', 'page_type_badge', 'slug', 'is_active')
    list_display_links = ('name_uz',)
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'page_type', 'category')
    search_fields = ('name_uz', 'name_ru', 'name_en')
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Tur', ordering='page_type')
    def page_type_badge(self, obj):
        if obj.page_type == 'static':
            return format_html('<span style="background:#e6f4ea;color:#137333;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600;">Statik</span>')
        return format_html('<span style="background:#fce8e6;color:#c5221f;padding:2px 10px;border-radius:12px;font-size:12px;font-weight:600;">Yo\'naltirish</span>')

    fieldsets = (
        ("Sahifa nomi", {
            'fields': ('category', 'name_uz', 'name_ru', 'name_en')
        }),
        ("Qisqa tavsif (hero subtitl)", {
            'fields': ('subtitle_uz', 'subtitle_ru', 'subtitle_en'),
            'description': "Sahifa banner ostidagi qisqa izoh matni (ixtiyoriy).",
        }),
        ("Sahifa turi", {
            'fields': ('page_type', 'redirect_url'),
            'description': (
                "Statik tanlasangiz — quyidagi matn maydonlarini to'ldiring. "
                "Yo'naltirish tanlasangiz — faqat URL kiriting."
            )
        }),
        ("Maxsus URL (ixtiyoriy)", {
            'fields': ('direct_url',),
            'description': "Bo'sh qolsa /page/{slug} ishlatiladi. Frontendga aynan shu URL yuboriladi.",
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
            try:
                url = obj.image.url
            except Exception:
                return format_html('<span style="color:#e53935;">⚠ URL topilmadi</span>')
            return format_html(
                '<img src="{}" style="max-height:50px; max-width:120px; object-fit:contain;" />',
                url
            )
        return "—"


# -------------------------------------------------HERO VIDEO BO'LIMI--------------------------------------------------
@admin.register(HeroVideo)
class HeroVideoAdmin(admin.ModelAdmin):

    list_display = ('display_poster', 'title', 'display_video_link', 'is_active', 'created_at')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title',)
    readonly_fields = ('created_at', 'display_poster_preview')

    fieldsets = (
        ('Video ma\'lumotlari', {
            'fields': ('title', 'video_url', 'video_file', 'poster_image', 'poster_image_ru', 'poster_image_en', 'is_active'),
            'description': "Video URL yoki Video fayli — bittasini to'ldiring.",
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
        if obj.video_url:
            return format_html('<a href="{0}" target="_blank">Videoni ko\'rish</a>', obj.video_url)
        return "Havola yo'q"
    display_video_link.short_description = "Video Link"

    def display_poster(self, obj):
        if obj.poster_image:
            try:
                url = obj.poster_image.url
            except Exception:
                return format_html('<span style="color:#e53935;">⚠ URL topilmadi</span>')
            return format_html('<img src="{0}" style="width: 50px; height: auto; border-radius: 5px;" />', url)
        return "Rasm yo'q"
    display_poster.short_description = "Poster"

    def display_poster_preview(self, obj):
        if obj.poster_image:
            try:
                url = obj.poster_image.url
            except Exception:
                return format_html('<span style="color:#e53935;">⚠ URL topilmadi</span>')
            return format_html('<img src="{0}" style="width: 300px; height: auto; border-radius: 10px;" />', url)
        return "Rasm yuklanmagan"
    display_poster_preview.short_description = "Poster Preview"


# ──────────────────────────────────────────────────────────────────────────────
# CONTENT BLOCK
# ──────────────────────────────────────────────────────────────────────────────

class ContentImageInline(GenericTabularInline):
    model  = ContentImage
    extra  = 1
    fields = ('image', 'order')


class ContentBlockForm(forms.ModelForm):
    description_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Uz)")
    description_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Ru)")
    description_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (En)")

    class Meta:
        model  = ContentBlock
        fields = '__all__'


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    form          = ContentBlockForm
    list_display  = ('block_type', 'title_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('block_type', 'is_active', 'navbar_items__category')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    readonly_fields = ('views', 'created_at', 'updated_at', 'content_block_guide')
    inlines       = [ContentImageInline]

    @admin.display(description='')
    def content_block_guide(self, obj):
        return format_html(
            '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
            '<strong style="color:#e53935;">📌 KONTENT BLOKI:</strong> Navbar sahifalarini tanlang → '
            'Blok turini tanlang (hero/rich-text/stats/gallery/quote/table/timeline) → Kontent to\'ldiring.'
            '</div>'
        )

    fieldsets = (
        ("📌 Yo'riqnoma", {
            'fields': ('content_block_guide',),
        }),
        ("Navbar sahifalari va blok turi", {
            'fields': ('navbar_items', 'block_type'),
        }),
        ("Kontent (hero / rich-text / gallery / quote uchun)", {
            'fields': ('title_uz', 'title_ru', 'title_en',
                       'description_uz', 'description_ru', 'description_en', 'link'),
        }),
        ("JSON ma'lumot (stats / table / timeline uchun)", {
            'classes': ('collapse',),
            'fields': ('json_data',),
            'description': (
                "Stats misoli: {\"stats\": [{\"value\": 5247, \"label\": \"Talabalar\", \"suffix\": \"\"}]}<br>"
                "Table misoli: {\"headers\": [\"Kod\", \"Nomi\"], \"rows\": [[\"001\", \"...\"]]} <br>"
                "Timeline misoli: {\"events\": [{\"date\": \"1991\", \"title\": \"...\", \"description\": \"...\"}]}"
            ),
        }),
        ("Taglar", {
            'fields': ('tags',),
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active'),
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('views', 'created_at', 'updated_at'),
        }),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'navbar_items':
            kwargs['queryset'] = (
                NavbarSubItem.objects.filter(is_active=True)
                .select_related('category')
                .order_by('category__order', 'order', 'name_uz')
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# LINK BLOCK

@admin.register(LinkBlock)
class LinkBlockAdmin(admin.ModelAdmin):
    list_display  = ('block_type', 'title_uz', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('block_type', 'is_active', 'navbar_items__category')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    readonly_fields = ('created_at', 'updated_at', 'link_block_guide')

    @admin.display(description='')
    def link_block_guide(self, obj):
        return format_html(
            '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
            '<strong style="color:#e53935;">📌 HAVOLA BLOKI:</strong> '
            'file-list → PDF yuklab olish uchun. useful-links → foydali havolalar uchun. '
            'Har bir hujjat/havola uchun alohida yozuv qo\'shing.'
            '</div>'
        )

    fieldsets = (
        ("📌 Yo'riqnoma", {
            'fields': ('link_block_guide',),
        }),
        ("Navbar sahifalari va blok turi", {
            'fields': ('navbar_items', 'block_type'),
        }),
        ("Kontent", {
            'fields': ('title_uz', 'title_ru', 'title_en', 'link', 'document_file'),
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active'),
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'navbar_items':
            kwargs['queryset'] = (
                NavbarSubItem.objects.filter(is_active=True)
                .select_related('category')
                .order_by('category__order', 'order', 'name_uz')
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# ME'YORIY HUJJATLAR
# ──────────────────────────────────────────────────────────────────────────────

@admin.register(MeyoriyHujjat)
class MeyoriyHujjatAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'file_preview', 'navbar_pages', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Sarlavha", {
            'fields': ('title_uz', 'title_ru', 'title_en'),
        }),
        ("Fayl", {
            'fields': ('document_file',),
        }),
        ("Sahifa", {
            'fields': ('navbar_items',),
            'description': "Qaysi sahifaga tegishli ekanini tanlang (masalan: Me'yoriy hujjatlar)",
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active'),
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).filter(block_type='file-list')

    def save_model(self, request, obj, form, change):
        obj.block_type = 'file-list'
        super().save_model(request, obj, form, change)

    @admin.display(description='Fayl')
    def file_preview(self, obj):
        if obj.document_file:
            try:
                return format_html(
                    '<a href="{}" target="_blank" style="color:#1976d2;">📄 Yuklab olish</a>',
                    obj.document_file.url,
                )
            except Exception:
                return '—'
        return '—'

    @admin.display(description='Sahifalar')
    def navbar_pages(self, obj):
        pages = obj.navbar_items.all()
        return ', '.join(p.name_uz for p in pages) if pages else '—'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'navbar_items':
            kwargs['queryset'] = (
                NavbarSubItem.objects.filter(is_active=True)
                .select_related('category')
                .order_by('category__order', 'order', 'name_uz')
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# ──────────────────────────────────────────────────────────────────────────────
# AXBOROT XIZMATI HAQIDA (AboutSocial)
# ──────────────────────────────────────────────────────────────────────────────

class AboutSocialSectionItemInline(admin.TabularInline):
    model   = AboutSocialSectionItem
    extra   = 1
    fields  = ('text_uz', 'text_ru', 'text_en', 'order')
    ordering = ('order',)


class AboutSocialSectionInline(admin.StackedInline):
    model            = AboutSocialSection
    extra            = 0
    fields           = ('key', 'title_uz', 'title_ru', 'title_en', 'order')
    ordering         = ('order',)
    show_change_link = True


class AboutSocialExtraTaskInline(admin.TabularInline):
    model   = AboutSocialExtraTask
    extra   = 1
    fields  = ('text_uz', 'text_ru', 'text_en', 'order')
    ordering = ('order',)


@admin.register(AboutSocial)
class AboutSocialAdmin(admin.ModelAdmin):
    inlines         = [AboutSocialSectionInline, AboutSocialExtraTaskInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Sahifa sarlavhasi", {
            'fields': ('title_uz', 'title_ru', 'title_en'),
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def has_add_permission(self, request):
        return not AboutSocial.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutSocialSection)
class AboutSocialSectionAdmin(admin.ModelAdmin):
    list_display    = ('key', 'title_uz', 'order', 'about_social')
    list_editable   = ('order',)
    search_fields   = ('title_uz', 'key')
    inlines         = [AboutSocialSectionItemInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Bo'lim", {
            'fields': ('about_social', 'key', 'order'),
        }),
        ("Sarlavha", {
            'fields': ('title_uz', 'title_ru', 'title_en'),
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )


# ──────────────────────────────────────────────────────────────────────────────
# AKADEMIYA HAQIDA (AboutAcademy)
# ──────────────────────────────────────────────────────────────────────────────

class AboutAcademySectionItemInline(admin.TabularInline):
    model   = AboutAcademySectionItem
    extra   = 1
    fields  = ('text_uz', 'text_ru', 'text_en', 'order')
    ordering = ('order',)


class AboutAcademySectionInline(admin.StackedInline):
    model            = AboutAcademySection
    extra            = 0
    fields           = ('key', 'title_uz', 'title_ru', 'title_en', 'order', 'items_preview')
    readonly_fields  = ('items_preview',)
    ordering         = ('order',)
    show_change_link = True

    def items_preview(self, obj):
        from django.urls import reverse
        edit_url = reverse('admin:pages_aboutacademysection_change', args=[obj.pk])
        btn = format_html(
            '<a href="{}" style="display:inline-block;margin-bottom:8px;padding:4px 14px;'
            'background:#1877be;color:#fff;border-radius:4px;font-size:12px;'
            'text-decoration:none;font-weight:600">✏ Elementlarni tahrirlash</a>',
            edit_url,
        )
        items = list(obj.items.order_by('order'))
        if not items:
            return format_html('{}<br><span style="color:#999;font-size:12px">— hali element yo\'q</span>', btn)
        lines = [format_html('<li style="margin:3px 0">{}</li>', item.text_uz[:150]) for item in items]
        lst = format_html('<ul style="margin:6px 0 0;padding-left:18px">{}</ul>',
                          format_html(''.join(str(l) for l in lines)))
        return format_html('{}{}', btn, lst)
    items_preview.short_description = "Elementlar"


class AboutAcademyProgramInline(admin.TabularInline):
    model   = AboutAcademyProgram
    extra   = 1
    fields  = ('program_type', 'direction_uz', 'direction_ru', 'direction_en',
               'profession_uz', 'profession_ru', 'profession_en', 'order')
    ordering = ('program_type', 'order')


class AboutAcademyImageInline(admin.TabularInline):
    model   = AboutAcademyImage
    extra   = 1
    fields  = ('image', 'caption_uz', 'caption_ru', 'caption_en', 'order', 'is_active')
    ordering = ('order',)


class AboutAcademyForm(forms.ModelForm):
    description_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Uz)")
    description_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Ru)")
    description_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (En)")

    class Meta:
        model  = AboutAcademy
        fields = '__all__'


@admin.register(AboutAcademy)
class AboutAcademyAdmin(admin.ModelAdmin):
    form            = AboutAcademyForm
    inlines         = [AboutAcademySectionInline, AboutAcademyProgramInline, AboutAcademyImageInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Akademiya tavsifi", {
            'fields': ('description_uz', 'description_ru', 'description_en'),
        }),
        ("Media", {
            'fields': ('logo', 'image', 'image_ru', 'image_en'),
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def has_add_permission(self, request):
        return not AboutAcademy.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutAcademySection)
class AboutAcademySectionAdmin(admin.ModelAdmin):
    list_display    = ('key', 'title_uz', 'order')
    list_editable   = ('order',)
    search_fields   = ('title_uz', 'key')
    inlines         = [AboutAcademySectionItemInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Bo'lim", {
            'fields': ('about', 'key', 'order'),
        }),
        ("Sarlavha", {
            'fields': ('title_uz', 'title_ru', 'title_en'),
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(AboutAcademyProgram)
class AboutAcademyProgramAdmin(admin.ModelAdmin):
    list_display  = ('program_type', 'direction_uz', 'profession_uz', 'order')
    list_editable = ('order',)
    list_filter   = ('program_type',)
    search_fields = ('direction_uz', 'profession_uz')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Dastur turi", {
            'fields': ('about', 'program_type', 'order'),
        }),
        ("Yo'nalish", {
            'fields': ('direction_uz', 'direction_ru', 'direction_en'),
        }),
        ("Mutaxassislik", {
            'fields': ('profession_uz', 'profession_ru', 'profession_en'),
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )


# ──────────────────────────────────────────────────────────────────────────────
# TASHKILIY TUZILMA (OrgNode)
# ──────────────────────────────────────────────────────────────────────────────

class OrgNodeChildInline(admin.TabularInline):
    model          = OrgNode
    fk_name        = 'parent'
    extra          = 0
    fields         = ('title_uz', 'node_type', 'order', 'is_starred', 'is_double_starred', 'is_highlighted', 'is_active')
    ordering       = ('order',)
    show_change_link = True


@admin.register(OrgNode)
class OrgNodeAdmin(admin.ModelAdmin):
    list_display  = ('indented_name', 'node_type', 'parent', 'order', 'is_highlighted', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('node_type', 'is_active', 'is_highlighted')
    search_fields = ('title_uz', 'title_ru')
    list_select_related = ('parent',)
    inlines       = [OrgNodeChildInline]
    readonly_fields = ('created_at', 'updated_at', 'image_preview_uz', 'image_preview_ru', 'image_preview_en')

    fieldsets = (
        ("Nomi", {
            'fields': ('title_uz', 'title_ru', 'title_en'),
        }),
        ("Rasm", {
            'fields': (
                'image', 'image_preview_uz',
                'image_ru', 'image_preview_ru',
                'image_en', 'image_preview_en',
            ),
        }),
        ("Joylashuv va tur", {
            'fields': ('parent', 'node_type', 'section', 'section_order', 'order'),
        }),
        ("Belgilar", {
            'fields': ('is_starred', 'is_double_starred', 'is_highlighted', 'is_active'),
            'description': (
                "* — yulduz belgisi (instituti*)  "
                "** — ikki yulduz (sport klubi**)  "
                "Ajratilgan — qizil ramkali tugun"
            ),
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description='Rasm (Uz) preview')
    def image_preview_uz(self, obj):
        if obj.image:
            try:
                return format_html('<img src="{}" style="max-height:80px;border-radius:4px;"/>', obj.image.url)
            except Exception:
                return '—'
        return '—'

    @admin.display(description='Rasm (Ru) preview')
    def image_preview_ru(self, obj):
        if obj.image_ru:
            try:
                return format_html('<img src="{}" style="max-height:80px;border-radius:4px;"/>', obj.image_ru.url)
            except Exception:
                return '—'
        return '—'

    @admin.display(description='Rasm (En) preview')
    def image_preview_en(self, obj):
        if obj.image_en:
            try:
                return format_html('<img src="{}" style="max-height:80px;border-radius:4px;"/>', obj.image_en.url)
            except Exception:
                return '—'
        return '—'

    @admin.display(description='Nomi', ordering='title_uz')
    def indented_name(self, obj):
        depth = 0
        p = obj.parent
        while p:
            depth += 1
            p = p.parent
        indent = '&nbsp;&nbsp;&nbsp;&nbsp;' * depth + ('└─ ' if depth else '')
        mark = ''
        if obj.is_highlighted:
            mark = ' <span style="color:#e53935;font-weight:bold;">[★]</span>'
        elif obj.is_starred:
            mark = ' <sup style="color:#888;">*</sup>'
        elif obj.is_double_starred:
            mark = ' <sup style="color:#888;">**</sup>'
        return format_html('{}{}{}', indent, obj.title_uz, mark)


@admin.register(OrgSection)
class OrgSectionAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz',)
    fieldsets = (
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Tavsif",   {'fields': ('description_uz', 'description_ru', 'description_en')}),
        ("Meta",     {'fields': ('slug', 'order', 'is_active')}),
    )


@admin.register(InteraktivXizmat)
class InteraktivXizmatAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'icon_class', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'title_ru')
    list_per_page = 20
    fieldsets = (
        ("O'zbek tili (majburiy)", {'fields': ('title_uz', 'description_uz')}),
        ("Rus tili",   {'classes': ('collapse',), 'fields': ('title_ru', 'description_ru')}),
        ("Ingliz tili", {'classes': ('collapse',), 'fields': ('title_en', 'description_en')}),
        ("Sozlamalar", {'fields': ('icon_class', 'link', 'order', 'is_active')}),
    )


# ── Markazlar ─────────────────────────────────────────────────────────────────

class MarkazSubBolimInline(admin.TabularInline):
    model   = MarkazSubBolim
    extra   = 1
    fields  = ('name_uz', 'name_ru', 'name_en', 'description_uz', 'order')
    ordering = ('order',)


class MarkazXodimInline(admin.TabularInline):
    model               = MarkazXodim
    extra               = 1
    fields              = ('person', 'order')
    autocomplete_fields = ('person',)
    ordering            = ('order',)


@admin.register(Markaz)
class MarkazAdmin(admin.ModelAdmin):
    list_display  = ('name_uz', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name_uz', 'name_ru', 'name_en')
    readonly_fields = ('slug',)
    list_per_page = 20
    inlines = [MarkazXodimInline, MarkazSubBolimInline]
    fieldsets = (
        ("Rasm (Uz)", {'fields': ('image',)}),
        ("O'zbek tili (majburiy)", {'fields': ('name_uz', 'description_uz', 'goals_uz', 'functions_uz')}),
        ("Rus tili",   {'classes': ('collapse',), 'fields': ('image_ru', 'name_ru', 'description_ru', 'goals_ru', 'functions_ru')}),
        ("Ingliz tili", {'classes': ('collapse',), 'fields': ('image_en', 'name_en', 'description_en', 'goals_en', 'functions_en')}),
        ("Sozlamalar", {'fields': ('order', 'is_active', 'slug')}),
    )


# ── Akademiya missiyasi ───────────────────────────────────────────────────────

class AkademiyaMissiyaYonalishInline(admin.TabularInline):
    model   = AkademiyaMissiyaYonalish
    extra   = 1
    fields  = ('text_uz', 'text_ru', 'text_en', 'order')
    ordering = ('order',)


@admin.register(AkademiyaMissiya)
class AkademiyaMissiyaAdmin(admin.ModelAdmin):
    inlines = [AkademiyaMissiyaYonalishInline]
    fieldsets = (
        ("Missiya matni (O'zbek tili)", {'fields': ('description_uz',)}),
        ("Missiya matni (Rus tili)",    {'classes': ('collapse',), 'fields': ('description_ru',)}),
        ("Missiya matni (Ingliz tili)", {'classes': ('collapse',), 'fields': ('description_en',)}),
    )


class IlmiyBolimYonalishInline(admin.TabularInline):
    model = IlmiyBolimYonalish
    extra = 1
    fields = ("text_uz", "text_ru", "text_en", "order")
    ordering = ("order",)


@admin.register(IlmiyBolim)
class IlmiyBolimAdmin(admin.ModelAdmin):
    inlines = [IlmiyBolimYonalishInline]
    fieldsets = (
        ("Bo'lim matni (O'zbek tili)", {"fields": ("description_uz",)}),
        ("Bo'lim matni (Rus tili)", {"classes": ("collapse",), "fields": ("description_ru",)}),
        ("Bo'lim matni (Ingliz tili)", {"classes": ("collapse",), "fields": ("description_en",)}),
    )


# ----------------------------------------------SAVOL-JAVOB (FAQ)----------------------------------------------

@admin.register(SavolJavobCategory)
class SavolJavobCategoryAdmin(AutoTranslateMixin, admin.ModelAdmin):
    translate_url_name   = 'savoljavobcategory_translate'
    change_form_template = 'admin/pages/savoljavobcategory/change_form.html'
    list_display    = ('name_uz', 'slug', 'order', 'is_active')
    list_editable   = ('order', 'is_active')
    search_fields   = ('name_uz', 'name_ru', 'name_en')
    readonly_fields = ('slug',)

    fieldsets = (
        ("Asosiy", {'fields': ('order', 'is_active', 'icon')}),
        ("Nomi (Uz)", {'fields': ('name_uz',)}),
        ("Nomi (Ru / En)", {'classes': ('collapse',), 'fields': ('name_ru', 'name_en')}),
        ("Texnik (avtomatik)", {'classes': ('collapse',), 'fields': ('slug',)}),
    )


class SavolJavobAdminForm(forms.ModelForm):
    answer_uz = forms.CharField(widget=SummernoteWidget(), required=True, label="Javob (Uz)")
    answer_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Javob (Ru)")
    answer_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Javob (En)")

    class Meta:
        model  = SavolJavob
        fields = '__all__'


@admin.register(SavolJavob)
class SavolJavobAdmin(AutoTranslateMixin, admin.ModelAdmin):
    translate_url_name   = 'savoljavob_translate'
    change_form_template = 'admin/pages/savoljavob/change_form.html'
    form            = SavolJavobAdminForm
    list_display    = ('short_question', 'category', 'order', 'is_featured', 'is_active', 'views_count')
    list_filter     = ('category', 'is_active', 'is_featured')
    list_editable   = ('order', 'is_featured', 'is_active')
    search_fields   = ('question_uz', 'question_ru', 'question_en')
    readonly_fields = ('slug', 'views_count')

    fieldsets = (
        ("Asosiy", {'fields': ('category', 'order', 'is_featured', 'is_active')}),
        ("Rasm (ixtiyoriy)", {'fields': ('image',)}),
        ("Savol (Uz)", {'fields': ('question_uz',)}),
        ("Savol (Ru / En)", {'classes': ('collapse',), 'fields': ('question_ru', 'question_en')}),
        ("Javob (Uz)", {'fields': ('answer_uz',)}),
        ("Javob (Ru / En)", {'classes': ('collapse',), 'fields': ('answer_ru', 'answer_en')}),
        ("Texnik (avtomatik)", {'classes': ('collapse',), 'fields': ('slug', 'views_count')}),
    )

    @admin.display(description="Savol")
    def short_question(self, obj):
        if len(obj.question_uz) > 90:
            return obj.question_uz[:90] + '...'
        return obj.question_uz


# ── Homepage Haqida ──────────────────────────────────────────────────────────

class HomepageHaqidaRasmInline(admin.TabularInline):
    model   = HomepageHaqidaRasm
    extra   = 1
    fields  = ('image', 'order', 'is_active')
    ordering = ('order',)


@admin.register(HomepageHaqida)
class HomepageHaqidaAdmin(admin.ModelAdmin):
    inlines         = [HomepageHaqidaRasmInline]
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Tavsif (Uz)", {
            'fields': ('description_uz',),
        }),
        ("Tavsif (Ru / En)", {
            'classes': ('collapse',),
            'fields': ('description_ru', 'description_en'),
        }),
        ("1-xususiyat (Uz)", {
            'fields': ('feature_1_title_uz', 'feature_1_desc_uz'),
        }),
        ("1-xususiyat (Ru / En)", {
            'classes': ('collapse',),
            'fields': ('feature_1_title_ru', 'feature_1_title_en', 'feature_1_desc_ru', 'feature_1_desc_en'),
        }),
        ("2-xususiyat (Uz)", {
            'fields': ('feature_2_title_uz', 'feature_2_desc_uz'),
        }),
        ("2-xususiyat (Ru / En)", {
            'classes': ('collapse',),
            'fields': ('feature_2_title_ru', 'feature_2_title_en', 'feature_2_desc_ru', 'feature_2_desc_en'),
        }),
        ("Texnik", {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def has_add_permission(self, request):
        return not HomepageHaqida.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ── Kampus xizmatlari ─────────────────────────────────────────────────────────

@admin.register(KampusXizmati)
class KampusXizmatiAdmin(AutoTranslateMixin, admin.ModelAdmin):
    translate_url_name = 'kampus-xizmati-translate'
    list_display  = ('title_uz', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'title_ru')
    list_per_page = 20
    fieldsets = (
        ("O'zbek tili (majburiy)", {'fields': ('title_uz',)}),
        ("Rus tili",   {'classes': ('collapse',), 'fields': ('title_ru',)}),
        ("Ingliz tili", {'classes': ('collapse',), 'fields': ('title_en',)}),
        ("Rasm va sozlamalar", {'fields': ('image', 'icon_class', 'link', 'order', 'is_active')}),
    )
    change_form_template = 'admin/pages/kampusxizmati/change_form.html'


# ── Iqtidorli talabalar bo'limi ───────────────────────────────────────────────

class IqtidorliVazifaInline(admin.TabularInline):
    model  = IqtidorliVazifa
    extra  = 1
    fields = ('text_uz', 'text_ru', 'text_en', 'order')


@admin.register(IqtidorliTalabalar)
class IqtidorliTalabalarAdmin(admin.ModelAdmin):
    inlines = [IqtidorliVazifaInline]
    fieldsets = (
        ("Sektor boshlig'i", {
            'fields': ('image', 'image_ru', 'image_en', 'telefon', 'email'),
        }),
        ("Lavozim (Uz)", {'fields': ('boshliq_lavozim_uz', 'boshliq_fio_uz', 'qabul_kunlari_uz')}),
        ("Lavozim (Ru)", {'classes': ('collapse',), 'fields': ('boshliq_lavozim_ru', 'boshliq_fio_ru', 'qabul_kunlari_ru')}),
        ("Lavozim (En)", {'classes': ('collapse',), 'fields': ('boshliq_lavozim_en', 'boshliq_fio_en', 'qabul_kunlari_en')}),
        ("Bo'lim sarlavhasi", {
            'fields': ('bolim_title_uz', 'bolim_title_ru', 'bolim_title_en'),
        }),
    )

    def has_add_permission(self, request):
        return not IqtidorliTalabalar.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
