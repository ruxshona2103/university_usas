import json
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.utils.html import format_html

from .models import Person, PersonCategory, PersonContent, PersonImage, StudentInfoCategory, StudentInfo, OlimpiyaChempion, MagistrGroup, MagistrStudent


class AutoTranslateMixin:
    translate_url_name = None

    def get_urls(self):
        return [
            path(
                'translate/',
                self.admin_site.admin_view(self.translate_view),
                name=self.translate_url_name,
            ),
        ] + super().get_urls()

    def translate_view(self, request):
        if request.method != 'POST':
            return JsonResponse({'error': 'POST required'}, status=405)
        try:
            from deep_translator import GoogleTranslator
            body = json.loads(request.body)
            text = (body.get('text') or '').strip()
            if not text:
                return JsonResponse({'ru': '', 'en': ''})
            ru = GoogleTranslator(source='uz', target='ru').translate(text) or ''
            en = GoogleTranslator(source='uz', target='en').translate(text) or ''
            return JsonResponse({'ru': ru, 'en': en})
        except Exception as exc:
            return JsonResponse({'error': str(exc)}, status=500)


# ── PersonImage inline ────────────────────────────────────────────────────────

class PersonImageInline(admin.TabularInline):
    model   = PersonImage
    extra   = 1
    fields  = ('image', 'order')
    ordering = ('order',)


# ── PersonContent inline ──────────────────────────────────────────────────────

class PersonContentInline(admin.TabularInline):
    model   = PersonContent
    extra   = 1
    fields  = ('tags', 'content_uz', 'content_ru', 'content_en', 'order')
    ordering = ('order',)


# ── PersonCategory ────────────────────────────────────────────────────────────

@admin.register(PersonCategory)
class PersonCategoryAdmin(admin.ModelAdmin):
    list_display   = ('title_uz', 'slug', 'order')
    list_editable  = ('order',)
    search_fields  = ('title_uz', 'title_ru', 'title_en')
    readonly_fields = ('slug',)
    list_per_page  = 20

    fieldsets = (
        ("Kategoriya nomi", {
            'fields': ('title_uz', 'title_ru', 'title_en'),
        }),
        ("Tartib", {
            'fields': ('order',),
        }),
        ("Texnik (avtomatik)", {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    )


# ── Person ────────────────────────────────────────────────────────────────────

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display       = ('image_preview', 'full_name_uz', 'category', 'is_head', 'order', 'is_active')
    list_display_links = ('full_name_uz',)
    list_editable      = ('order', 'is_active')
    list_filter        = ('is_active', 'is_head', 'category')
    search_fields      = ('full_name_uz', 'full_name_ru', 'full_name_en', 'email', 'phone')
    readonly_fields    = ('image_preview', 'created_at', 'updated_at')
    inlines            = [PersonImageInline, PersonContentInline]
    list_per_page      = 20

    fieldsets = (
        ("Kategoriya", {
            'fields': ('category', 'is_head'),
        }),
        ("Asosiy rasm", {
            'fields': ('image', 'image_preview'),
        }),
        ("To'liq ismi", {
            'fields': ('full_name_uz', 'full_name_ru', 'full_name_en'),
        }),
        ("Tavsif", {
            'classes': ('collapse',),
            'fields': ('description_uz', 'description_ru', 'description_en'),
        }),
        # Rektorat, dekan, kafedra mudiri kabi xodimlar uchun
        ("Lavozim va ilmiy unvon (xodimlar uchun)", {
            'classes': ('collapse',),
            'fields': (
                'title_uz', 'title_ru', 'title_en',
                'position_uz', 'position_ru', 'position_en',
            ),
        }),
        ("Kontakt (xodimlar uchun)", {
            'classes': ('collapse',),
            'fields': ('phone', 'fax', 'email', 'address', 'reception'),
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active'),
        }),
        ("Texnik", {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    @admin.display(description="Rasm")
    def image_preview(self, obj):
        if obj.image:
            try:
                url = obj.image.url
            except Exception:
                return format_html('<span style="color:#e53935;">⚠ URL topilmadi</span>')
            return format_html(
                '<img src="{}" style="max-height:60px;max-width:60px;'
                'object-fit:cover;border-radius:50%;" />',
                url,
            )
        return "—"


class StudentInfoInline(admin.TabularInline):
    model   = StudentInfo
    extra   = 1
    fields  = ('title_uz', 'order', 'is_active')
    ordering = ('order',)


@admin.register(StudentInfoCategory)
class StudentInfoCategoryAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('title_uz',)
    inlines       = [StudentInfoInline]
    list_per_page = 20

    fieldsets = (
        ("Nomi", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Tartib", {'fields': ('order',)}),
        ("Texnik", {'classes': ('collapse',), 'fields': ('slug',)}),
    )


@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    list_display  = ('title_uz', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('category',)
    search_fields = ('title_uz', 'title_ru', 'title_en')
    list_per_page = 20

    fieldsets = (
        ("Kategoriya", {'fields': ('category',)}),
        ("Sarlavha", {'fields': ('title_uz', 'title_ru', 'title_en')}),
        ("Matn", {'fields': ('content_uz', 'content_ru', 'content_en')}),
        ("Tartib va holat", {'fields': ('order', 'is_active')}),
    )


class MagistrStudentInline(admin.TabularInline):
    model   = MagistrStudent
    extra   = 1
    fields  = ('order', 'student_name', 'dissertation_topic_uz', 'supervisor_name', 'supervisor_info_uz')
    ordering = ('order',)


@admin.register(MagistrGroup)
class MagistrGroupAdmin(AutoTranslateMixin, admin.ModelAdmin):
    translate_url_name   = 'magistrgroup_translate'
    change_form_template = 'admin/students/magistrgroup/change_form.html'
    list_display  = ('specialty_code', 'specialty_name_uz', 'education_lang', 'year', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('year', 'education_lang', 'is_active')
    search_fields = ('specialty_code', 'specialty_name_uz')
    inlines       = [MagistrStudentInline]

    fieldsets = (
        ("Mutaxassislik", {
            'fields': ('specialty_code', 'education_lang', 'year', 'order', 'is_active'),
        }),
        ("Nomi (Uz)", {'fields': ('specialty_name_uz',)}),
        ("Nomi (Ru / En)", {'classes': ('collapse',), 'fields': ('specialty_name_ru', 'specialty_name_en')}),
    )


@admin.register(MagistrStudent)
class MagistrStudentAdmin(AutoTranslateMixin, admin.ModelAdmin):
    translate_url_name   = 'magistrstudent_translate'
    change_form_template = 'admin/students/magistrstudent/change_form.html'
    list_display  = ('order', 'student_name', 'group', 'supervisor_name')
    list_filter   = ('group', 'group__year')
    search_fields = ('student_name', 'dissertation_topic_uz', 'supervisor_name')

    fieldsets = (
        ("Talaba", {'fields': ('group', 'order', 'student_name')}),
        ("Dissertatsiya mavzusi (Uz)", {'fields': ('dissertation_topic_uz',)}),
        ("Dissertatsiya mavzusi (Ru / En)", {'classes': ('collapse',), 'fields': ('dissertation_topic_ru', 'dissertation_topic_en')}),
        ("Ilmiy rahbar", {'fields': ('supervisor_name', 'supervisor_info_uz')}),
        ("Ilmiy daraja (Ru / En)", {'classes': ('collapse',), 'fields': ('supervisor_info_ru', 'supervisor_info_en')}),
    )


@admin.register(OlimpiyaChempion)
class OlimpiyaChempionAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'yonalish', 'guruh', 'order', 'is_active', 'image_preview')
    list_editable = ('order', 'is_active')
    list_filter   = ('is_active', 'yonalish', 'guruh')
    search_fields = ('full_name', 'yonalish', 'guruh')

    fieldsets = (
        ("Shaxs", {
            'fields': ('full_name', 'image', 'image_preview'),
        }),
        ("Sport", {
            'fields': ('yonalish', 'guruh'),
        }),
        ("Tartib va holat", {
            'fields': ('order', 'is_active'),
        }),
    )
    readonly_fields = ('image_preview',)

    @admin.display(description="Rasm")
    def image_preview(self, obj):
        if obj.image:
            try:
                url = obj.image.url
            except Exception:
                return '—'
            return format_html('<img src="{}" style="max-height:80px;border-radius:4px;"/>', url)
        return '—'
