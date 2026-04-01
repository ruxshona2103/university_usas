from django.contrib import admin

from .models import Staff, StaffContent
from domains.pages.models import NavbarSubItem


class StaffContentInline(admin.TabularInline):
    model  = StaffContent
    extra  = 1
    fields = ('tag', 'content_uz', 'content_ru', 'content_en', 'order')
    ordering = ('order',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'navbar_item', 'role', 'is_head', 'phone', 'email', 'order', 'is_active')
    list_filter   = ('role', 'is_active', 'is_head', 'navbar_item__category')
    search_fields = ('full_name', 'title_uz', 'title_ru', 'title_en', 'email', 'phone')
    list_editable = ('order', 'is_active', 'is_head')
    ordering      = ('order', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines       = [StaffContentInline]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'navbar_item':
            kwargs['queryset'] = (
                NavbarSubItem.objects
                .filter(is_active=True)
                .select_related('category')
                .order_by('category__order', 'order', 'name_uz')
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        ("Bo'lim va rol", {
            'fields': ('navbar_item', 'role', 'is_head', 'order', 'is_active'),
        }),
        ("Lavozim va ism", {
            'fields': ('title_uz', 'title_ru', 'title_en', 'full_name'),
        }),
        ("Ilmiy unvon", {
            'fields': ('position_uz', 'position_ru', 'position_en'),
        }),
        ("Aloqa", {
            'fields': ('address', 'reception', 'phone', 'fax', 'email'),
        }),
        ("Rasm", {
            'fields': ('image',),
        }),
        ("Texnik", {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )
