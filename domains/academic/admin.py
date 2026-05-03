from django.contrib import admin
from django.utils.text import slugify
from django_summernote.widgets import SummernoteInplaceWidget as SummernoteWidget
from django import forms

from .models import AcademyStat, AcademyDetailPage, FakultetKafedra, KafedraPublication, KafedraXodim, KafedraRasm, HuzuridagiTashkilot, TashkiliyTuzilmaItem


@admin.register(AcademyStat)
class AcademyStatAdmin(admin.ModelAdmin):
    list_display  = ('label_uz', 'value_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active',)
    search_fields = ('label_uz', 'label_ru', 'label_en')

    fieldsets = (
        ("O'zbek tili", {'fields': ('label_uz', 'value_uz')}),
        ("Rus tili",    {'fields': ('label_ru', 'value_ru'), 'classes': ('collapse',)}),
        ("Ingliz tili", {'fields': ('label_en', 'value_en'), 'classes': ('collapse',)}),
        ("Sozlamalar",  {'fields': ('order', 'is_active')}),
    )


@admin.register(AcademyDetailPage)
class AcademyDetailPageAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Axborot-resurs markazi", {
            'fields': ('resource_center_uz', 'resource_center_ru', 'resource_center_en'),
        }),
        ("Ta'lim va tarkib ko'rsatkichlari", {
            'fields': ('edu_direction_count', 'sport_type_count', 'masters_count', 'auditorium_count'),
        }),
        ("Batafsil ma'lumotlar", {
            'fields': ('detail_uz', 'detail_ru', 'detail_en'),
        }),
    )


class KafedraRasmInline(admin.TabularInline):
    model   = KafedraRasm
    extra   = 1
    fields  = ('image', 'caption_uz', 'order', 'is_active')
    ordering = ('order',)


class KafedraXodimInline(admin.TabularInline):
    model               = KafedraXodim
    extra               = 1
    fields              = ('person', 'order')
    ordering            = ('order',)
    autocomplete_fields = ['person']

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj is not None:
            from domains.students.models import Person, PersonCategory
            # Kafedra nomiga mos PersonCategory slug qidirish
            kafedra_slug = slugify(obj.name_uz)
            qs = Person.objects.filter(is_active=True).order_by('full_name_uz')
            try:
                cat = PersonCategory.objects.filter(
                    slug__icontains=kafedra_slug[:15]
                ).first()
                if not cat:
                    # Kafedra so'zi bilan qidirish
                    cat = PersonCategory.objects.filter(
                        title_uz__icontains=obj.name_uz[:20]
                    ).first()
                if cat:
                    qs = Person.objects.filter(
                        category__in=cat.get_descendants_or_self()
                        if hasattr(cat, 'get_descendants_or_self') else
                        PersonCategory.objects.filter(pk=cat.pk)
                    ).order_by('full_name_uz')
            except Exception:
                pass
            formset.form.base_fields['person'].queryset = qs
        return formset


class KafedraPublicationInline(admin.TabularInline):
    model   = KafedraPublication
    extra   = 1
    fields  = ('title_uz', 'author', 'pub_type', 'cover', 'order')
    ordering = ('order',)


class FakultetKafedraForm(forms.ModelForm):
    description_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Uz)")
    description_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Ru)")
    description_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (En)")
    about_uz       = forms.CharField(widget=SummernoteWidget(), required=False, label="Qo'shimcha (Uz)")
    about_ru       = forms.CharField(widget=SummernoteWidget(), required=False, label="Qo'shimcha (Ru)")
    about_en       = forms.CharField(widget=SummernoteWidget(), required=False, label="Qo'shimcha (En)")

    class Meta:
        model  = FakultetKafedra
        fields = '__all__'


@admin.register(FakultetKafedra)
class FakultetKafedraAdmin(admin.ModelAdmin):
    form          = FakultetKafedraForm
    list_display  = ('name_uz', 'type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('type', 'is_active')
    search_fields = ('name_uz', 'name_ru', 'name_en')
    readonly_fields = ('slug',)
    list_per_page = 30
    inlines = [KafedraXodimInline, KafedraRasmInline, KafedraPublicationInline]

    fieldsets = (
        ("Asosiy", {
            'fields': ('type', 'slug', 'order', 'is_active', 'decree_info'),
        }),
        ("Nomi (Uz)", {'fields': ('name_uz',)}),
        ("Nomi (Ru / En)", {'classes': ('collapse',), 'fields': ('name_ru', 'name_en')}),
        ("Tavsif (Uz)", {'fields': ('description_uz',)}),
        ("Tavsif (Ru / En)", {'classes': ('collapse',), 'fields': ('description_ru', 'description_en')}),
        ("Qo'shimcha ma'lumot (ixtiyoriy)", {
            'fields': ('about_uz', 'about_ru', 'about_en'),
            'classes': ('collapse',),
        }),
        ("Sport turlari", {
            'fields': ('sport_types_uz', 'sport_types_ru', 'sport_types_en'),
            'classes': ('collapse',),
        }),
        ("Bakalavriat fanlari", {
            'fields': ('bachelor_subjects_uz', 'bachelor_subjects_ru', 'bachelor_subjects_en'),
            'classes': ('collapse',),
        }),
        ("Magistratura fanlari", {
            'fields': ('master_subjects_uz', 'master_subjects_ru', 'master_subjects_en'),
            'classes': ('collapse',),
        }),
        ("Kontakt va havola", {
            'fields': ('phone', 'email', 'link'),
            'classes': ('collapse',),
        }),
        ("Dekan (fakultet uchun)", {
            'fields': ('dean_name_uz', 'dean_name_ru', 'dean_name_en', 'dean_photo', 'dean_phone', 'dean_email'),
            'classes': ('collapse',),
        }),
        ("O'rinbosar (fakultet uchun)", {
            'fields': ('vice_dean_name_uz', 'vice_dean_name_ru', 'vice_dean_name_en', 'vice_dean_photo', 'vice_dean_phone', 'vice_dean_email'),
            'classes': ('collapse',),
        }),
        ("Mudiri (kafedra uchun)", {
            'fields': ('mudiri_name_uz', 'mudiri_name_ru', 'mudiri_name_en', 'mudiri_photo', 'mudiri_phone', 'mudiri_email', 'mudiri_degree_uz', 'mudiri_degree_ru', 'mudiri_degree_en'),
            'classes': ('collapse',),
        }),
    )


@admin.register(KafedraRasm)
class KafedraRasmAdmin(admin.ModelAdmin):
    list_display  = ('kafedra', 'caption_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('kafedra', 'is_active')
    list_per_page = 30


@admin.register(KafedraXodim)
class KafedraXodimAdmin(admin.ModelAdmin):
    list_display        = ('person', 'kafedra', 'order')
    list_editable       = ('order',)
    list_filter         = ('kafedra',)
    search_fields       = ('person__full_name_uz',)
    autocomplete_fields = ['person']
    list_per_page       = 30


@admin.register(KafedraPublication)
class KafedraPublicationAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'author', 'pub_type', 'kafedra', 'order')
    list_filter   = ('pub_type', 'kafedra')
    search_fields = ('title_uz', 'author')
    list_per_page = 30


@admin.register(HuzuridagiTashkilot)
class HuzuridagiTashkilotAdmin(admin.ModelAdmin):
    list_display  = ('name_uz', 'org_type', 'phone', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('org_type', 'is_active')
    search_fields = ('name_uz', 'name_ru')
    list_per_page = 20
    autocomplete_fields = ['person']
    fieldsets = (
        ("Tur va tartib", {'fields': ('org_type', 'slug', 'order', 'is_active')}),
        ("Rahbar (Person)", {'fields': ('person',)}),
        ("O'zbek tili (majburiy)", {'fields': ('name_uz', 'description_uz', 'about_uz', 'address_uz')}),
        ("Rus tili", {'classes': ('collapse',), 'fields': ('name_ru', 'description_ru', 'about_ru', 'address_ru')}),
        ("Ingliz tili", {'classes': ('collapse',), 'fields': ('name_en', 'description_en', 'about_en', 'address_en')}),
        ("Aloqa", {'fields': ('phone', 'email', 'website')}),
        ("Rasm", {'fields': ('image',)}),
    )


@admin.register(TashkiliyTuzilmaItem)
class TashkiliyTuzilmaItemAdmin(admin.ModelAdmin):
    list_display = ("slug", "order", "is_active", "updated_at")
    list_editable = ("order", "is_active")
    search_fields = ("slug", "text_uz", "text_ru", "text_en")
    list_per_page = 30
    readonly_fields = ("slug",)
    fieldsets = (
        ("Asosiy", {"fields": ("slug", "order", "is_active")}),
        ("Matn (Uz)", {"fields": ("text_uz",)}),
        ("Matn (Ru / En)", {"classes": ("collapse",), "fields": ("text_ru", "text_en")}),
        ("Rasm", {"fields": ("image",)}),
    )
