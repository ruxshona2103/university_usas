from django import forms
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.utils.html import format_html

from .models import (
    ContractPrice,
    ServiceVehicle,
    IlmiyFaoliyatCategory,
    IlmiyFaoliyat,
    SportStat,
    SportYonalish,
    SportTadbir,
)


class OquvFaoliyatAdminForm(forms.ModelForm):
    parent_category = forms.ModelChoiceField(
        queryset=IlmiyFaoliyatCategory.objects.filter(parent__isnull=True),
        required=False,
        label="Kategoriya",
        empty_label="---------",
    )

    class Meta:
        model  = IlmiyFaoliyat
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label    = "Sub-kategoriya"
        self.fields['category'].required = False

        if self.instance.pk and self.instance.category_id:
            cat = self.instance.category
            if cat.parent_id:
                self.fields['parent_category'].initial = cat.parent_id
                self.fields['category'].queryset = IlmiyFaoliyatCategory.objects.filter(parent_id=cat.parent_id)
            else:
                self.fields['parent_category'].initial = cat.pk
                self.fields['category'].queryset = IlmiyFaoliyatCategory.objects.filter(parent_id=cat.pk)
        else:
            self.fields['category'].queryset = IlmiyFaoliyatCategory.objects.none()

    def save(self, commit=True):
        instance = super().save(commit=False)
        # If no subcategory chosen but parent category is selected, link to parent directly
        if not instance.category_id:
            parent_cat = self.cleaned_data.get('parent_category')
            if parent_cat:
                instance.category = parent_cat
        if commit:
            instance.save()
            self.save_m2m()
        return instance


@admin.register(IlmiyFaoliyatCategory)
class OquvFaoliyatCategoryAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'parent', 'slug', 'order')
    list_editable = ('order',)
    list_filter   = ('parent',)
    search_fields = ('title_uz', 'title_ru')
    prepopulated_fields = {}  # slug auto-generated on save

    fieldsets = (
        ("Nomi (Uz)", {'fields': ('title_uz',)}),
        ("Nomi (Ru / En)", {'classes': ('collapse',), 'fields': ('title_ru', 'title_en')}),
        ("Meta", {'fields': ('parent', 'slug', 'order')}),
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
    form                = OquvFaoliyatAdminForm
    change_form_template = 'admin/activities/ilmiyfaoliyat/change_form.html'

    list_display  = ('title_uz', 'category', 'file_link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('category', 'is_active')
    search_fields = ('title_uz', 'title_ru')

    fieldsets = (
        ("Asosiy ma'lumot", {
            'fields': ('parent_category', 'category', 'title_uz'),
        }),
        ("Sarlavha (Ru / En)", {
            'classes': ('collapse',),
            'fields': ('title_ru', 'title_en'),
        }),
        ("Tavsif (Uz)", {
            'fields': ('description_uz',),
        }),
        ("Tavsif (Ru / En)", {
            'classes': ('collapse',),
            'fields': ('description_ru', 'description_en'),
        }),
        ("Media va holat", {
            'fields': ('image', 'file', 'order', 'is_active'),
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'get-subcategories/',
                self.admin_site.admin_view(self.get_subcategories_view),
                name='oquvfaoliyat_get_subcategories',
            ),
            path(
                'translate/',
                self.admin_site.admin_view(self.translate_view),
                name='oquvfaoliyat_translate',
            ),
        ]
        return custom_urls + urls

    def get_subcategories_view(self, request):
        parent_id = request.GET.get('parent_id')
        if parent_id:
            subs = list(
                IlmiyFaoliyatCategory.objects.filter(parent_id=parent_id)
                .order_by('order', 'title_uz')
                .values('id', 'title_uz')
            )
        else:
            subs = []
        return JsonResponse({'subcategories': subs})

    def translate_view(self, request):
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)
        import json
        from deep_translator import GoogleTranslator
        try:
            body = json.loads(request.body)
            text_uz = (body.get('text') or '').strip()
            if not text_uz:
                return JsonResponse({'ru': '', 'en': ''})
            ru = GoogleTranslator(source='uz', target='ru').translate(text_uz) or ''
            en = GoogleTranslator(source='uz', target='en').translate(text_uz) or ''
            return JsonResponse({'ru': ru, 'en': en})
        except Exception as exc:
            return JsonResponse({'error': str(exc)}, status=500)

    @admin.display(description="Fayl")
    def file_link(self, obj):
        if obj.file:
            try:
                return format_html('<a href="{}" target="_blank">Ko\'rish</a>', obj.file.url)
            except Exception:
                return obj.file.name or "—"
        return "—"
 
 

@admin.register(SportStat)
class SportStatAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'value', 'suffix', 'color', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'title_ru')

    fieldsets = (
        ("Qiymat", {'fields': ('value', 'suffix', 'color')}),
        ("Tavsif (Uz)", {'fields': ('title_uz',)}),
        ("Tavsif (Ru / En)", {'classes': ('collapse',), 'fields': ('title_ru', 'title_en')}),
        ("Meta", {'fields': ('order', 'is_active')}),
    )


@admin.register(SportYonalish)
class SportYonalishAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'icon', 'description_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'title_ru')

    fieldsets = (
        ("Asosiy", {'fields': ('icon', 'title_uz', 'description_uz')}),
        ("Ru / En", {'classes': ('collapse',), 'fields': ('title_ru', 'title_en', 'description_ru', 'description_en')}),
        ("Meta", {'fields': ('order', 'is_active')}),
    )


@admin.register(SportTadbir)
class SportTadbirAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'event_date', 'location_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz', 'title_ru')

    fieldsets = (
        ("Sarlavha (Uz)", {'fields': ('title_uz', 'description_uz', 'location_uz')}),
        ("Ru / En", {'classes': ('collapse',), 'fields': ('title_ru', 'title_en', 'description_ru', 'description_en', 'location_ru', 'location_en')}),
        ("Meta", {'fields': ('event_date', 'order', 'is_active')}),
    )
