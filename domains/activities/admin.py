from django.contrib import admin
from django.utils.html import format_html

from .models import ContractPrice, ServiceVehicle, IlmiyFaoliyatCategory, IlmiyFaoliyat


@admin.register(IlmiyFaoliyatCategory)
class OquvFaoliyatCategoryAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('title_uz', 'title_ru')
    prepopulated_fields = {}  # slug auto-generated on save

    fieldsets = (
        ("Nomi (Uz)", {'fields': ('title_uz',)}),
        ("Nomi (Ru / En)", {'classes': ('collapse',), 'fields': ('title_ru', 'title_en')}),
        ("Meta", {'fields': ('slug', 'order')}),
    )


@admin.register(ContractPrice)
class ContractPriceAdmin(admin.ModelAdmin):
    list_display  = ('specialty_code', 'specialty_name_uz', 'education_type', 'education_form', 'price_display', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('education_type', 'education_form', 'is_active')
    search_fields = ('specialty_code', 'specialty_name_uz', 'specialty_name_ru')

    fieldsets = (
        ("Mutaxassislik", {
            'fields': ('specialty_code', 'education_type', 'education_form'),
        }),
        ("Nomi (Uz)", {
            'fields': ('specialty_name_uz',),
        }),
        ("Nomi (Ru / En)", {
            'classes': ('collapse',),
            'fields': ('specialty_name_ru', 'specialty_name_en'),
        }),
        ("To'lov va holat", {
            'fields': ('price', 'order', 'is_active'),
        }),
    )

    @admin.display(description="To'lov (so'm)", ordering='price')
    def price_display(self, obj):
        return f"{obj.price:,} so'm".replace(',', ' ')


@admin.register(ServiceVehicle)
class ServiceVehicleAdmin(admin.ModelAdmin):
    list_display  = ('name', 'vehicle_type_uz', 'manufactured_year', 'fuel_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('fuel_type', 'is_active')
    search_fields = ('name', 'vehicle_type_uz')

    fieldsets = (
        ("Transport vositasi", {
            'fields': ('name', 'fuel_type', 'manufactured_year'),
        }),
        ("Turi (Uz)", {
            'fields': ('vehicle_type_uz',),
        }),
        ("Turi (Ru / En)", {
            'classes': ('collapse',),
            'fields': ('vehicle_type_ru', 'vehicle_type_en'),
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active'),
        }),
    )


@admin.register(IlmiyFaoliyat)
class OquvFaoliyatAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'category', 'file_link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('category', 'is_active')
    search_fields = ('title_uz', 'title_ru')

    fieldsets = (
        ("Asosiy ma'lumot", {
            'fields': ('category', 'title_uz'),
        }),
        ("Sarlavha (Ru / En)", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'title_en'),
        }),
        ("Media va holat", {
            'fields': ('image', 'file', 'order', 'is_active'),
        }),
    )

    @admin.display(description="Fayl")
    def file_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">📄 Ko\'rish</a>', obj.file.url)
        return "—"
