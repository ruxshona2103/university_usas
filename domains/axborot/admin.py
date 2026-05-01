from django import forms
from django.contrib import admin
from django_summernote.widgets import SummernoteWidget

from .models import AxborotSection, AxborotVazifa


class AxborotVazifaForm(forms.ModelForm):
    body_uz = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Uz)")
    body_ru = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (Ru)")
    body_en = forms.CharField(widget=SummernoteWidget(), required=False, label="Matn (En)")

    class Meta:
        model  = AxborotVazifa
        fields = '__all__'


class AxborotVazifaInline(admin.TabularInline):
    model         = AxborotVazifa
    form          = AxborotVazifaForm
    extra         = 1
    fields        = ('body_uz', 'body_ru', 'body_en', 'order', 'is_active')
    ordering      = ('order',)
    show_change_link = True


@admin.register(AxborotSection)
class AxborotSectionAdmin(admin.ModelAdmin):
    list_display   = ('number', 'title_uz', 'order', 'is_active')
    list_editable  = ('order', 'is_active')
    search_fields  = ('title_uz', 'title_ru', 'title_en')
    ordering       = ('order', 'number')
    inlines        = [AxborotVazifaInline]
    fieldsets = (
        ('Asosiy', {
            'fields': ('number', 'order', 'is_active'),
        }),
        ('Sarlavha', {
            'fields': ('title_uz', 'title_ru', 'title_en'),
        }),
    )


@admin.register(AxborotVazifa)
class AxborotVazifaAdmin(admin.ModelAdmin):
    form = AxborotVazifaForm
    list_display   = ('section', 'body_uz_short', 'order', 'is_active')
    list_editable  = ('order', 'is_active')
    list_filter    = ('section', 'is_active')
    search_fields  = ('body_uz', 'body_ru', 'body_en')
    ordering       = ('section__order', 'order')
    fieldsets = (
        ('Asosiy', {
            'fields': ('section', 'order', 'is_active'),
        }),
        ('Matn', {
            'fields': ('body_uz', 'body_ru', 'body_en'),
        }),
    )

    @admin.display(description="Matn (Uz)")
    def body_uz_short(self, obj):
        return obj.body_uz[:100]
