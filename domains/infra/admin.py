from django.contrib import admin
from django.utils.html import format_html

from .models import (
    SportMajmua, SportMajmuaImage,
    SportMajmuaStat, SportMajmuaSportTuri, SportMajmuaTadbir,
    Sharoit,
)


class SportMajmuaImageInline(admin.TabularInline):
    model   = SportMajmuaImage
    extra   = 1
    fields  = ('image', 'order')
    ordering = ('order',)


class SportMajmuaStatInline(admin.TabularInline):
    model   = SportMajmuaStat
    extra   = 1
    fields  = ('label_uz', 'value_uz', 'order')
    ordering = ('order',)


class SportMajmuaSportTuriInline(admin.TabularInline):
    model   = SportMajmuaSportTuri
    extra   = 1
    fields  = ('name_uz', 'order')
    ordering = ('order',)


class SportMajmuaTadbirInline(admin.TabularInline):
    model   = SportMajmuaTadbir
    extra   = 1
    fields  = ('level', 'title_uz', 'order')
    ordering = ('level', 'order')


@admin.register(SportMajmua)
class SportMajmuaAdmin(admin.ModelAdmin):
    list_display  = ('name_uz', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    readonly_fields = ('slug',)
    inlines       = [
        SportMajmuaImageInline,
        SportMajmuaStatInline,
        SportMajmuaSportTuriInline,
        SportMajmuaTadbirInline,
    ]
    fieldsets = (
        ("Nomi", {
            'fields': ('name_uz', 'name_ru', 'name_en'),
        }),
        ("Joylashuvi", {
            'fields': ('location_uz', 'location_ru', 'location_en'),
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active'),
        }),
        ("Texnik (avtomatik)", {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )


@admin.register(Sharoit)
class SharoitAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('category', 'is_active')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    list_per_page = 25

    fieldsets = (
        ("Bo'lim va tartib", {
            'fields': ('category', 'order', 'is_active'),
        }),
        ("O'zbek tili (majburiy)", {
            'fields': ('title_uz', 'description_uz'),
        }),
        ("Rus tili", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'description_ru'),
        }),
        ("Ingliz tili", {
            'classes': ('collapse',),
            'fields': ('title_en', 'description_en'),
        }),
        ("Rasm va icon", {
            'fields': ('image', 'icon'),
        }),
    )
