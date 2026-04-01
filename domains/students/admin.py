from django.contrib import admin
from django.utils.html import format_html

from domains.pages.models import NavbarSubItem
from .models import Person, PersonCategory, PersonContent


# ─── PersonCategory ───────────────────────────────────────────────────────────

@admin.register(PersonCategory)
class PersonCategoryAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'navbar_item', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('title_uz', 'title_ru', 'title_en')
    readonly_fields = ('slug',)
    list_per_page = 20

    fieldsets = (
        ("Navbar sahifasi", {
            'fields': ('navbar_item',),
            'description': "Bu kategoriya qaysi navbar sahifasiga tegishli?"
        }),
        ("Kategoriya nomi", {
            'fields': ('title_uz', 'title_ru', 'title_en')
        }),
        ("Tartib", {
            'fields': ('order',)
        }),
        ('Texnik (avtomatik)', {
            'classes': ('collapse',),
            'fields': ('slug',)
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'navbar_item':
            kwargs['queryset'] = (
                NavbarSubItem.objects
                .filter(is_active=True)
                .select_related('category')
                .order_by('category__order', 'order', 'name_uz')
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ─── PersonContent inline ─────────────────────────────────────────────────────

class PersonContentInline(admin.TabularInline):
    model   = PersonContent
    extra   = 1
    fields  = ('tag', 'content_uz', 'content_ru', 'content_en', 'order')
    ordering = ('order',)


# ─── Person ───────────────────────────────────────────────────────────────────

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display       = ('image_preview', 'full_name_uz', 'category', 'order', 'is_active')
    list_display_links = ('full_name_uz',)
    list_editable      = ('order', 'is_active')
    list_filter        = ('is_active', 'category')
    search_fields      = ('full_name_uz', 'full_name_ru', 'full_name_en')
    readonly_fields    = ('image_preview', 'created_at', 'updated_at')
    inlines            = [PersonContentInline]
    list_per_page      = 20

    fieldsets = (
        ("Rasm", {
            'fields': ('image', 'image_preview')
        }),
        ("To'liq ismi", {
            'fields': ('full_name_uz', 'full_name_ru', 'full_name_en')
        }),
        ("Tavsif (qisqa)", {
            'classes': ('collapse',),
            'fields': ('description_uz', 'description_ru', 'description_en')
        }),
        ("Kategoriya", {
            'fields': ('category',),
            'description': "Qaysi bo'limga tegishli (Faxrlarimiz, Bitiruvchilar...)?"
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active')
        }),
        ('Texnik', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
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
                '<img src="{}" style="max-height:60px; max-width:60px; '
                'object-fit:cover; border-radius:50%;" />',
                url
            )
        return "—"
