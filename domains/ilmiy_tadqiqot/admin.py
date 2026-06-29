from django import forms
from django.contrib import admin
from django.db import models as db_models
from django.utils.html import format_html

from .models import IlmiyTadqiqot, IlmiyTadqiqotFile, IlmiyTadqiqotCategory


@admin.register(IlmiyTadqiqotCategory)
class IlmiyTadqiqotCategoryAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('title_uz', 'title_ru', 'title_en')
    prepopulated_fields = {'slug': ('title_uz',)}


class IlmiyTadqiqotFileInline(admin.TabularInline):
    model  = IlmiyTadqiqotFile
    extra  = 1
    fields = ('title_uz', 'file', 'order')


@admin.register(IlmiyTadqiqot)
class IlmiyTadqiqotAdmin(admin.ModelAdmin):
    formfield_overrides = {
        db_models.TextField: {'widget': forms.Textarea(attrs={'rows': 8, 'cols': 80})},
    }
    list_display  = ('title_uz', 'category', 'author_uz', 'date', 'is_published', 'views')
    list_editable = ('is_published',)
    list_filter   = ('is_published', 'category')
    search_fields = ('title_uz', 'title_ru', 'title_en', 'author_uz')
    readonly_fields = ('views', 'likes', 'comments', 'created_at', 'updated_at', 'slug')
    inlines       = [IlmiyTadqiqotFileInline]

    fieldsets = (
        ("Asosiy", {'fields': ('category', 'is_published', 'date', 'image', 'image_ru', 'image_en', 'slug')}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Muallif", {'fields': ('author_uz', 'author_ru', 'author_en')}),
        ("Kontent", {'fields': ('description_uz', 'description_ru', 'description_en')}),
        ('Statistika', {'classes': ('collapse',), 'fields': ('views', 'likes', 'comments', 'created_at', 'updated_at')}),
    )
