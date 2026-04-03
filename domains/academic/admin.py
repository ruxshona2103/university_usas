from django.contrib import admin
from django.utils.html import format_html

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
    readonly_fields = ('created_at', 'updated_at', 'staff_guide')
    inlines       = [StaffContentInline]

    @admin.display(description='')
    def staff_guide(self, obj):
        return format_html('''
        <div style="background:#fff3f3;border-left:4px solid #e53935;padding:12px 16px;border-radius:4px;margin:4px 0;">
          <strong style="color:#e53935;font-size:13px;">📌 XODIMLAR — quyidagi sahifalar uchun ishlatiladi:</strong>
          <table style="margin-top:8px;font-size:12px;color:#c62828;border-collapse:collapse;width:100%;">
            <tr><td style="padding:3px 8px;font-weight:bold;">Akademiya → Rektorat</td>
                <td>→ Lavozim turi: <strong>Rektor</strong> yoki <strong>Prorektor</strong></td></tr>
            <tr style="background:#fff8f8;"><td style="padding:3px 8px;font-weight:bold;">Akademiya → Akademiya kengashi</td>
                <td>→ Lavozim turi: <strong>Kengash a'zosi</strong></td></tr>
            <tr><td style="padding:3px 8px;font-weight:bold;">Akademiya → Tuzilma</td>
                <td>→ Lavozim turi: <strong>Kafedra mudiri</strong> yoki <strong>Xodim</strong></td></tr>
            <tr style="background:#fff8f8;"><td style="padding:3px 8px;font-weight:bold;">Akademiya → Fakultetlar</td>
                <td>→ Lavozim turi: <strong>Dekan</strong></td></tr>
          </table>
          <div style="margin-top:8px;font-size:12px;color:#555;">
            <strong>Tablar (qo'shimcha ma'lumot):</strong> Quyidagi "Xodim kontenti" bo'limida taglarni tanlang:
            tarjimai-hol · ilmiy-faoliyat · qabul-soatlari · nashrlar · loyihalar
          </div>
        </div>
        ''')

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
        ("📌 Yo'riqnoma", {
            'fields': ('staff_guide',),
        }),
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
