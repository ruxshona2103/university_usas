import json
from django import forms
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django_summernote.widgets import SummernoteWidget

from .models import (
    ForeignProfessorReview, PartnerOrganization, PartnerPageConfig,
    InternationalPost, InternationalPostImage,
    InternationalRating, InternationalRatingImage,
    InternationalDeptConfig, MemorandumStat,
)


class AutoTranslateMixin:
    """UZ → RU/EN avtomatik tarjima AJAX endpoint ni admin ga qo'shadi."""

    translate_url_name = None  # har bir subclass da noyob nom

    def get_urls(self):
        urls = super().get_urls()
        return [
            path(
                'translate/',
                self.admin_site.admin_view(self.translate_view),
                name=self.translate_url_name,
            ),
        ] + urls

    def translate_view(self, request):
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)
        try:
            from deep_translator import GoogleTranslator
            body   = json.loads(request.body)
            text   = (body.get('text') or '').strip()
            if not text:
                return JsonResponse({'ru': '', 'en': ''})
            ru = GoogleTranslator(source='uz', target='ru').translate(text) or ''
            en = GoogleTranslator(source='uz', target='en').translate(text) or ''
            return JsonResponse({'ru': ru, 'en': en})
        except Exception as exc:
            return JsonResponse({'error': str(exc)}, status=500)


@admin.register(PartnerPageConfig)
class PartnerPageConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Tavsif",   {'fields': ('description_uz', 'description_ru', 'description_en')}),
    )

    def has_add_permission(self, request):
        return not PartnerPageConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class InternationalPostImageInline(admin.TabularInline):
    model   = InternationalPostImage
    extra   = 1
    fields  = ('image', 'order')
    ordering = ('order',)


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


class InternationalRatingImageInline(admin.TabularInline):
    model    = InternationalRatingImage
    extra    = 1
    fields   = ('image', 'order')
    ordering = ('order',)


class InternationalRatingForm(forms.ModelForm):
    description_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Uz)")
    description_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (Ru)")
    description_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Tavsif (En)")

    class Meta:
        model  = InternationalRating
        fields = '__all__'


@admin.register(InternationalRating)
class InternationalRatingAdmin(admin.ModelAdmin):
    form           = InternationalRatingForm
    list_display   = ('title_uz', 'date', 'order', 'is_active')
    list_editable  = ('order', 'is_active')
    list_filter    = ('is_active',)
    search_fields  = ('title_uz', 'title_ru', 'title_en')
    prepopulated_fields = {'slug': ('title_uz',)}
    readonly_fields     = ('created_at', 'updated_at')
    list_per_page  = 20
    inlines        = [InternationalRatingImageInline]

    fieldsets = (
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Matn",     {'fields': ('description_uz', 'description_ru', 'description_en')}),
        ("Rasm va sana", {'fields': ('cover', 'date')}),
        ("Slug",     {'fields': ('slug',)}),
        ("Tartib va holat", {'fields': ('order', 'is_active')}),
        ('Texnik',   {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )


@admin.register(InternationalDeptConfig)
class InternationalDeptConfigAdmin(AutoTranslateMixin, admin.ModelAdmin):
    translate_url_name   = 'intdeptconfig_translate'
    change_form_template = 'admin/international/internationaldeptconfig/change_form.html'

    fieldsets = (
        ("Bo'lim boshlig'i", {
            'fields': ('head_photo', 'head_name_uz', 'head_name_ru', 'head_name_en',
                       'head_position_uz', 'head_position_ru', 'head_position_en',
                       'head_working_hours', 'head_phone', 'head_email'),
        }),
        ("Vazifalari (Uz)", {'fields': ('tasks_uz',)}),
        ("Vazifalari (Ru / En)", {'classes': ('collapse',), 'fields': ('tasks_ru', 'tasks_en')}),
    )

    def has_add_permission(self, request):
        return not InternationalDeptConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MemorandumStat)
class MemorandumStatAdmin(AutoTranslateMixin, admin.ModelAdmin):
    translate_url_name   = 'intmemorandum_translate'
    change_form_template = 'admin/international/memorandumstat/change_form.html'

    list_display  = ('organization_uz', 'foreign_count', 'domestic_count', 'order')
    list_editable = ('foreign_count', 'domestic_count', 'order')
    search_fields = ('organization_uz',)

    fieldsets = (
        ("Tashkilot nomi (Uz)", {'fields': ('organization_uz',)}),
        ("Tashkilot nomi (Ru / En)", {'classes': ('collapse',), 'fields': ('organization_ru', 'organization_en')}),
        ("Memorandumlar", {'fields': ('foreign_count', 'domestic_count', 'order')}),
    )


class InternationalPostForm(forms.ModelForm):
    content_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Uz)")
    content_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Ru)")
    content_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (En)")

    class Meta:
        model  = InternationalPost
        fields = '__all__'


@admin.register(InternationalPost)
class InternationalPostAdmin(admin.ModelAdmin):
    form          = InternationalPostForm
    list_display  = ('title_uz', 'post_type', 'date', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active', 'post_type')
    search_fields = ('title_uz', 'title_ru', 'title_en')
    list_per_page = 20
    inlines       = [InternationalPostImageInline]

    fieldsets = (
        ("Turi va sana", {'fields': ('post_type', 'date')}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Matn", {'fields': ('content_uz', 'content_ru', 'content_en')}),
        ("Asosiy rasm", {'fields': ('image',)}),
        ("Tartib va holat", {'fields': ('order', 'is_active')}),
    )

from .models import AkademikAlmashinuv, AkademikAlmashinuvRasm


class AkademikAlmashinuvRasmInline(admin.TabularInline):
    model  = AkademikAlmashinuvRasm
    extra  = 1
    fields = ('image', 'caption_uz', 'caption_ru', 'caption_en', 'order')


class AkademikAlmashinuvForm(forms.ModelForm):
    body_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Uz)")
    body_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Ru)")
    body_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (En)")

    class Meta:
        model  = AkademikAlmashinuv
        fields = '__all__'


@admin.register(AkademikAlmashinuv)
class AkademikAlmashinuvAdmin(admin.ModelAdmin):
    form          = AkademikAlmashinuvForm
    list_display  = ('title_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title_uz',)
    inlines       = [AkademikAlmashinuvRasmInline]
    fieldsets = (
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Matn", {'fields': ('body_uz', 'body_ru', 'body_en')}),
        ("Tartib va holat", {'fields': ('order', 'is_active')}),
    )

from .models import XalqaroReytingBolim, XorijlikProfessor


class XorijlikProfessorForm(forms.ModelForm):
    bio_uz       = forms.CharField(widget=SummernoteWidget(), required=False, label="Bio (Uz)")
    bio_ru       = forms.CharField(widget=SummernoteWidget(), required=False, label="Bio (Ru)")
    bio_en       = forms.CharField(widget=SummernoteWidget(), required=False, label="Bio (En)")
    education_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Ma'lumoti (Uz)")
    education_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Ma'lumoti (Ru)")
    education_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Ma'lumoti (En)")

    class Meta:
        model  = XorijlikProfessor
        fields = '__all__'


@admin.register(XorijlikProfessor)
class XorijlikProfessorAdmin(admin.ModelAdmin):
    form          = XorijlikProfessorForm
    list_display  = ('full_name', 'country', 'from_year', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active', 'country')
    search_fields = ('full_name', 'country')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Asosiy", {'fields': ('full_name', 'photo', 'country', 'from_year', 'order', 'is_active')}),
        ("Bio / Tavsif (Uz)", {'fields': ('bio_uz',)}),
        ("Bio / Tavsif (Ru/En)", {'classes': ('collapse',), 'fields': ('bio_ru', 'bio_en')}),
        ("Ma'lumoti (Uz)", {'fields': ('education_uz',)}),
        ("Ma'lumoti (Ru/En)", {'classes': ('collapse',), 'fields': ('education_ru', 'education_en')}),
        ("Mutaxassislik", {'fields': ('specialty_uz', 'specialty_ru', 'specialty_en')}),
        ("Ilmiy daraja", {'fields': ('academic_degree_uz', 'academic_degree_ru', 'academic_degree_en')}),
        ("Ilmiy unvon", {'fields': ('academic_title_uz', 'academic_title_ru', 'academic_title_en')}),
        ('Texnik', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )


@admin.register(XalqaroReytingBolim)
class XalqaroReytingBolimAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'bolim_type', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('bolim_type', 'is_active')
    search_fields = ('title_uz', 'title_ru')
    fieldsets = (
        ("Tur va tartib", {'fields': ('bolim_type', 'order', 'is_active')}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Tavsif", {'fields': ('description_uz', 'description_ru', 'description_en')}),
        ("Rasm va havola", {'fields': ('image', 'link')}),
    )
