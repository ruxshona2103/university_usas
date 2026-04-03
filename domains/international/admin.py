from django.contrib import admin

from .models import ForeignProfessorReview
from domains.pages.models import NavbarSubItem


@admin.register(ForeignProfessorReview)
class ForeignProfessorReviewAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'country', 'navbar_item', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active', 'country')
    search_fields = ('full_name', 'country', 'review_uz')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("📌 Yo'riqnoma", {
            'fields': (),
            'description': (
                '<div style="background:#fff3f3;border-left:4px solid #e53935;padding:10px 14px;border-radius:4px;">'
                '<strong style="color:#e53935;">📌 XORIJIY PROFESSORLAR</strong> — '
                'Navbar sahifasi: <strong>Xalqaro aloqalar → Xorijlik professor-o\'qituvchilar</strong> ni tanlang.<br>'
                '<span style="color:#c62828;">Ism, lavozim, mamlakat, fikr matni to\'ldiring. Rasm ixtiyoriy.</span>'
                '</div>'
            ),
        }),
        ("Navbar sahifasi", {'fields': ('navbar_item',)}),
        ("Shaxs", {'fields': ('full_name', 'position_uz', 'position_ru', 'position_en', 'country', 'photo')}),
        ("Fikr", {'fields': ('review_uz', 'review_ru', 'review_en')}),
        ("Tartib va holat", {'fields': ('order', 'is_active')}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'navbar_item':
            kwargs['queryset'] = (
                NavbarSubItem.objects.filter(is_active=True)
                .select_related('category')
                .order_by('category__order', 'order')
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
