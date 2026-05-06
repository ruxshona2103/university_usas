from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django_summernote.widgets import SummernoteInplaceWidget as SummernoteWidget

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


class IlmiyTadqiqotForm(forms.ModelForm):
    description_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Uz)")
    description_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Ru)")
    description_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (En)")

    class Meta:
        model  = IlmiyTadqiqot
        fields = '__all__'


@admin.register(IlmiyTadqiqot)
class IlmiyTadqiqotAdmin(admin.ModelAdmin):
    form          = IlmiyTadqiqotForm
    list_display  = ('title_uz', 'category', 'author_uz', 'date', 'is_published', 'views')
    list_editable = ('is_published',)
    list_filter   = ('is_published', 'category')
    search_fields = ('title_uz', 'title_ru', 'title_en', 'author_uz')
    readonly_fields = ('views', 'likes', 'comments', 'created_at', 'updated_at', 'slug')
    inlines       = [IlmiyTadqiqotFileInline]

    fieldsets = (
        ("Asosiy", {'fields': ('category', 'is_published', 'date', 'image', 'slug')}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Muallif", {'fields': ('author_uz', 'author_ru', 'author_en')}),
        ("Kontent", {'fields': ('description_uz', 'description_ru', 'description_en')}),
        ('Statistika', {'classes': ('collapse',), 'fields': ('views', 'likes', 'comments', 'created_at', 'updated_at')}),
    )
