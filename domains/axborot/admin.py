from django.contrib import admin

from .models import AxborotSection, AxborotVazifa


class AxborotVazifaInline(admin.TabularInline):
    model  = AxborotVazifa
    extra  = 1
    fields = ('body_uz', 'body_ru', 'body_en', 'order', 'is_active')


@admin.register(AxborotSection)
class AxborotSectionAdmin(admin.ModelAdmin):
    list_display  = ('number', 'title_uz', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering      = ('order', 'number')
    inlines       = [AxborotVazifaInline]


@admin.register(AxborotVazifa)
class AxborotVazifaAdmin(admin.ModelAdmin):
    list_display  = ('section', 'body_uz_short', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('section',)
    ordering      = ('section__order', 'order')

    @admin.display(description="Matn")
    def body_uz_short(self, obj):
        return obj.body_uz[:100]
