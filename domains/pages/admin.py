from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html

from common.models import ContentImage
from .models import (
    ContactConfig, PresidentQuote, SocialLink,
    NavbarCategory, NavbarSubItem, Partner, HeroVideo,
    ContentBlock, LinkBlock,
    AboutSocial, AboutSocialSection, AboutSocialSectionItem, AboutSocialExtraTask,
    AboutAcademy, AboutAcademySection, AboutAcademySectionItem, AboutAcademyProgram, AboutAcademyImage,
    OrgNode, OrgSection, Rekvizit,
)


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
@admin.register(NavbarSubItem)
class NavbarSubItemAdmin(admin.ModelAdmin):
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
            'fields': ('title', 'video_url', 'video_file', 'poster_image', 'is_active'),
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


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
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
    fields           = ('key', 'title_uz', 'title_ru', 'title_en', 'order')
    ordering         = ('order',)
    show_change_link = True


class AboutAcademyProgramInline(admin.TabularInline):
    model   = AboutAcademyProgram
    extra   = 1
    fields  = ('program_type', 'direction_uz', 'direction_ru', 'direction_en',
               'profession_uz', 'profession_ru', 'profession_en', 'order')
    ordering = ('program_type', 'order')


class AboutAcademyImageInline(admin.TabularInline):
    model   = AboutAcademyImage
    extra   = 1
    fields  = ('image', 'caption_uz', 'order', 'is_active')
    ordering = ('order',)


@admin.register(AboutAcademy)
class AboutAcademyAdmin(admin.ModelAdmin):
    inlines         = [AboutAcademySectionInline, AboutAcademyProgramInline, AboutAcademyImageInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ("Media", {
            'fields': ('logo', 'image'),
        }),
        ("Akademiya tavsifi", {
            'fields': ('description_uz', 'description_ru', 'description_en'),
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
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Nomi", {
            'fields': ('title_uz', 'title_ru', 'title_en'),
        }),
        ("Joylashuv va tur", {
            'fields': ('parent', 'node_type', 'order'),
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
