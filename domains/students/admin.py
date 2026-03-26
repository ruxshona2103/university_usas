from django.contrib import admin
from django.utils.html import format_html

from .models import Person, PersonCategory


@admin.register(PersonCategory)
class PersonCategoryAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'title_ru', 'title_en', 'slug')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    prepopulated_fields = {'slug': ('title_uz',)}
    list_per_page = 20

    fieldsets = (
        ("Kategoriya nomi", {
            'fields': ('title_uz', 'title_ru', 'title_en', 'slug')
        }),
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display       = ('image_preview', 'full_name_uz', 'categories_list', 'order', 'is_active')
    list_display_links = ('full_name_uz',)
    list_editable      = ('order', 'is_active')
    list_filter        = ('is_active', 'categories')
    search_fields      = ('full_name_uz', 'full_name_ru', 'full_name_en')
    filter_horizontal  = ('categories',)
    readonly_fields    = ('image_preview',)
    list_per_page      = 20

    fieldsets = (
        ("Rasm", {
            'fields': ('image', 'image_preview')
        }),
        ("To'liq ismi", {
            'fields': ('full_name_uz', 'full_name_ru', 'full_name_en')
        }),
        ("Tavsif", {
            'classes': ('collapse',),
            'fields': ('description_uz', 'description_ru', 'description_en')
        }),
        ("Kategoriyalar", {
            'fields': ('categories',)
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active')
        }),
    )

    @admin.display(description="Rasm")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:60px; max-width:60px; '
                'object-fit:cover; border-radius:50%;" />',
                obj.image.url
            )
        return "—"

    @admin.display(description="Kategoriyalar")
    def categories_list(self, obj):
        cats = obj.categories.all()
        if not cats:
            return "—"
        return ", ".join(c.title_uz for c in cats)
