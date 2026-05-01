from django import forms
from django.contrib import admin
from django_summernote.widgets import SummernoteInplaceWidget as SummernoteWidget
from .models import (
    QabulBolim, QabulBolimItem,
    QabulKomissiyaTarkibi,
    QabulKuni,
    CallCenter,
    QabulYangilik,
    QabulNarx,
    QabulHujjat,
    QabulNavbar, QabulNavbarItem,
)


class QabulBolimItemForm(forms.ModelForm):
    body_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Uz)")
    body_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Ru)")
    body_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (En)")

    class Meta:
        model  = QabulBolimItem
        fields = '__all__'


class QabulBolimItemInline(admin.StackedInline):
    model  = QabulBolimItem
    form   = QabulBolimItemForm
    extra  = 1
    fields = ('item_type', 'title_uz', 'body_uz', 'body_ru', 'body_en', 'file', 'link', 'order', 'is_active')


@admin.register(QabulBolim)
class QabulBolimAdmin(admin.ModelAdmin):
    list_display   = ('title_uz', 'bolim_type', 'slug', 'order', 'is_active')
    list_editable  = ('order', 'is_active')
    list_filter    = ('bolim_type', 'is_active')
    search_fields  = ('title_uz', 'slug')
    prepopulated_fields = {'slug': ('title_uz',)}
    inlines        = [QabulBolimItemInline]

    fieldsets = (
        ("Asosiy", {'fields': ('slug', 'bolim_type', 'order', 'is_active')}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Tavsif",   {'fields': ('description_uz', 'description_ru', 'description_en')}),
    )


@admin.register(QabulKomissiyaTarkibi)
class QabulKomissiyaTarkibiAdmin(admin.ModelAdmin):
    list_display  = ('full_name_uz', 'position_uz', 'phone', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('full_name_uz', 'phone')

    fieldsets = (
        ("F.I.O",    {'fields': ('full_name_uz', 'full_name_ru', 'full_name_en')}),
        ("Lavozim",  {'fields': ('position_uz', 'position_ru', 'position_en')}),
        ("Kontakt",  {'fields': ('phone', 'email', 'photo')}),
        ("Holat",    {'fields': ('order', 'is_active')}),
    )


@admin.register(QabulKuni)
class QabulKuniAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'qabul_type', 'start_date', 'end_date', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('qabul_type', 'is_active')
    search_fields = ('title_uz',)

    fieldsets = (
        ("Asosiy",   {'fields': ('qabul_type', 'start_date', 'end_date', 'order', 'is_active')}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Izoh",     {'fields': ('description_uz', 'description_ru', 'description_en')}),
    )


@admin.register(CallCenter)
class CallCenterAdmin(admin.ModelAdmin):
    list_display  = ('phone', 'label_uz', 'working_hours_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('phone', 'label_uz')

    fieldsets = (
        ("Asosiy", {'fields': ('phone', 'order', 'is_active')}),
        ("Nomi",   {'fields': ('label_uz', 'label_ru', 'label_en')}),
        ("Ish vaqti", {'fields': ('working_hours_uz', 'working_hours_ru', 'working_hours_en')}),
    )


class QabulYangilikForm(forms.ModelForm):
    body_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Uz)")
    body_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Ru)")
    body_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (En)")

    class Meta:
        model  = QabulYangilik
        fields = '__all__'


@admin.register(QabulYangilik)
class QabulYangilikAdmin(admin.ModelAdmin):
    form          = QabulYangilikForm
    list_display  = ('title_uz', 'date', 'views', 'order', 'is_published')
    list_editable = ('order', 'is_published')
    list_filter   = ('is_published',)
    search_fields = ('title_uz',)
    readonly_fields = ('views',)

    fieldsets = (
        ("Asosiy",   {'fields': ('date', 'image', 'order', 'is_published', 'views')}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Matn",     {'fields': ('body_uz', 'body_ru', 'body_en')}),
    )


@admin.register(QabulNarx)
class QabulNarxAdmin(admin.ModelAdmin):
    list_display  = ('specialty_name_uz', 'edu_type', 'edu_form', 'price', 'year', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('edu_type', 'edu_form', 'year', 'is_active')
    search_fields = ('specialty_name_uz', 'specialty_code')

    fieldsets = (
        ("Asosiy",        {'fields': ('edu_type', 'edu_form', 'year', 'price', 'specialty_code', 'order', 'is_active')}),
        ("Yo'nalish nomi", {'fields': ('specialty_name_uz', 'specialty_name_ru', 'specialty_name_en')}),
    )


@admin.register(QabulHujjat)
class QabulHujjatAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'hujjat_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('hujjat_type', 'is_active')
    search_fields = ('title_uz',)

    fieldsets = (
        ("Asosiy",   {'fields': ('hujjat_type', 'file', 'order', 'is_active')}),
        ("Nomi",     {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Tavsif",   {'fields': ('description_uz', 'description_ru', 'description_en')}),
    )


class QabulNavbarItemInline(admin.TabularInline):
    model  = QabulNavbarItem
    extra  = 1
    fields = ('title_uz', 'title_ru', 'title_en', 'slug', 'order', 'is_active')


@admin.register(QabulNavbar)
class QabulNavbarAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'slug')
    inlines       = [QabulNavbarItemInline]

    fieldsets = (
        ("Asosiy", {'fields': ('slug', 'order', 'is_active')}),
        ("Nomi",   {'fields': ('title_uz', 'title_ru', 'title_en')}),
    )
