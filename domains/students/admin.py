from django.contrib import admin
from django.utils.html import format_html

from .models import Person, PersonCategory, PersonContent, PersonImage, StudentInfoCategory, StudentInfo


# ── PersonImage inline ────────────────────────────────────────────────────────

class PersonImageInline(admin.TabularInline):
    model   = PersonImage
    extra   = 1
    fields  = ('image', 'order')
    ordering = ('order',)


# ── PersonContent inline ──────────────────────────────────────────────────────

class PersonContentInline(admin.TabularInline):
    model   = PersonContent
    extra   = 1
    fields  = ('tags', 'content_uz', 'content_ru', 'content_en', 'order')
    ordering = ('order',)


# ── PersonCategory ────────────────────────────────────────────────────────────

@admin.register(PersonCategory)
class PersonCategoryAdmin(admin.ModelAdmin):
    list_display   = ('title_uz', 'slug', 'order')
    list_editable  = ('order',)
    search_fields  = ('title_uz', 'title_ru', 'title_en')
    readonly_fields = ('slug',)
    list_per_page  = 20

    fieldsets = (
        ("Kategoriya nomi", {
            'fields': ('title_uz', 'title_ru', 'title_en'),
        }),
        ("Tartib", {
            'fields': ('order',),
        }),
        ("Texnik (avtomatik)", {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )


# ── Person ────────────────────────────────────────────────────────────────────

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display       = ('image_preview', 'full_name_uz', 'category', 'is_head', 'order', 'is_active')
    list_display_links = ('full_name_uz',)
    list_editable      = ('order', 'is_active')
    list_filter        = ('is_active', 'is_head', 'category')
    search_fields      = ('full_name_uz', 'full_name_ru', 'full_name_en', 'email', 'phone')
    readonly_fields    = ('image_preview', 'created_at', 'updated_at')
    inlines            = [PersonImageInline, PersonContentInline]
    list_per_page      = 20

    fieldsets = (
        ("Kategoriya", {
            'fields': ('category', 'is_head'),
        }),
        ("Asosiy rasm", {
            'fields': ('image', 'image_preview'),
        }),
        ("To'liq ismi", {
            'fields': ('full_name_uz', 'full_name_ru', 'full_name_en'),
        }),
        ("Tavsif", {
            'classes': ('collapse',),
            'fields': ('description_uz', 'description_ru', 'description_en'),
        }),
        # Rektorat, dekan, kafedra mudiri kabi xodimlar uchun
        ("Lavozim va ilmiy unvon (xodimlar uchun)", {
            'classes': ('collapse',),
            'fields': (
                'title_uz', 'title_ru', 'title_en',
                'position_uz', 'position_ru', 'position_en',
            ),
        }),
        ("Kontakt (xodimlar uchun)", {
            'classes': ('collapse',),
            'fields': ('phone', 'fax', 'email', 'address', 'reception'),
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active'),
        }),
        ("Texnik", {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description="Rasm")
    def image_preview(self, obj):
        if obj.image:
            try:
                url = obj.image.url
            except Exception:
                return format_html('<span style="color:#e53935;">⚠ URL topilmadi</span>')
            return format_html(
                '<img src="{}" style="max-height:60px;max-width:60px;'
                'object-fit:cover;border-radius:50%;" />',
                url,
            )
        return "—"


class StudentInfoInline(admin.TabularInline):
    model   = StudentInfo
    extra   = 1
    fields  = ('title_uz', 'order', 'is_active')
    ordering = ('order',)


@admin.register(StudentInfoCategory)
class StudentInfoCategoryAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('title_uz',)
    readonly_fields = ('slug',)
    inlines       = [StudentInfoInline]
    list_per_page = 20

    fieldsets = (
        ("Nomi", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Tartib", {'fields': ('order',)}),
        ("Texnik", {'classes': ('collapse',), 'fields': ('slug',)}),
    )


@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('category',)
    search_fields = ('title_uz', 'title_ru', 'title_en')
    list_per_page = 20

    fieldsets = (
        ("Kategoriya", {'fields': ('category',)}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Matn", {'fields': ('content_uz', 'content_ru', 'content_en')}),
        ("Tartib va holat", {'fields': ('order', 'is_active')}),
    )
