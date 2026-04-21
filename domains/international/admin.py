from django.contrib import admin

from .models import ForeignProfessorReview, PartnerOrganization, InternationalPost


@admin.register(ForeignProfessorReview)
class ForeignProfessorReviewAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'country', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active', 'country')
    search_fields = ('full_name', 'country', 'review_uz')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Shaxs", {'fields': ('full_name', 'position_uz', 'position_ru', 'position_en', 'country', 'photo')}),
        ("Fikr", {'fields': ('review_uz', 'review_ru', 'review_en')}),
        ("Tartib va holat", {'fields': ('order', 'is_active')}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )


@admin.register(PartnerOrganization)
class PartnerOrganizationAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'partner_type', 'country_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active', 'partner_type')
    search_fields = ('title_uz', 'title_ru', 'title_en', 'country_uz')
    list_per_page = 20

    fieldsets = (
        ("Turi", {'fields': ('partner_type',)}),
        ("Nomi", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Mamlakat", {'fields': ('country_uz', 'country_ru', 'country_en')}),
        ("Rasm va havola", {'fields': ('logo', 'image', 'website')}),
        ("Tartib va holat", {'fields': ('order', 'is_active')}),
    )


@admin.register(InternationalPost)
class InternationalPostAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'post_type', 'date', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active', 'post_type')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    list_per_page = 20

    fieldsets = (
        ("Turi va sana", {'fields': ('post_type', 'date')}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Matn", {'fields': ('content_uz', 'content_ru', 'content_en')}),
        ("Rasm", {'fields': ('image',)}),
        ("Tartib va holat", {'fields': ('order', 'is_active')}),
    )
